import asyncio
from datetime import datetime

from celery.utils.log import get_task_logger
from sqlalchemy import select

from core.database import SessionLocal
from core.models import Document
from processing.pipeline import chunk_text, clean_html, normalize_whitespace
from security.audit import write_audit
from storage.chunk_store import ChunkStore
from storage.claim_store import ClaimStore
from storage.entity_store import EntityStore, RelationshipStore
from intelligence.entity_extractor import extract_entities, extract_relationship_candidates
from intelligence.timeline_extractor import extract_timeline_candidates
from llm.service import extract_claims as llm_extract_claims, extract_entities as llm_extract_entities, summarize_document as llm_summarize_document
from storage.timeline_store import TimelineStore
from alerts.rules import evaluate_alert_rules
from tasks.celery_app import celery_app

logger = get_task_logger(__name__)


def extract_claim_candidates(chunk_text: str) -> list[str]:
    statements = []
    for part in chunk_text.split('.'):
        sentence = part.strip()
        if not sentence:
            continue
        if any(token in sentence.lower() for token in [' is ', ' are ', ' was ', ' were ', ' has ', ' have ']):
            statements.append(sentence)
    return statements[:3]


async def process_document(document_id: str) -> dict:
    async with SessionLocal() as db:
        result = await db.execute(select(Document).where(Document.document_id == document_id))
        document = result.scalar_one_or_none()
        if not document:
            raise ValueError('document not found')

        try:
            document.processing_status = 'processing'
            await db.commit()

            text = document.text_content or ''
            if document.mime_type == 'text/html' or document.title.lower().endswith('.html'):
                text = clean_html(text)
            text = normalize_whitespace(text)

            chunks = chunk_text(text)
            stored_chunks = await ChunkStore(db).replace_for_document(document.tenant_id, document.document_id, chunks)

            claim_store = ClaimStore(db)
            timeline_store = TimelineStore(db)
            auto_claims = 0
            for chunk in stored_chunks:
                llm_candidates = [c['text'] for c in llm_extract_claims(chunk['text'])] or extract_claim_candidates(chunk['text'])
                for candidate in llm_candidates:
                    normalized = normalize_whitespace(candidate.lower())
                    claim = await claim_store.create_claim(
                        tenant_id=document.tenant_id,
                        case_id=document.case_id,
                        document_id=document.document_id,
                        source_id=document.source_id,
                        text=candidate,
                        normalized_text=normalized,
                        claim_type='auto_candidate',
                        confidence_score=0.6,
                        verification_status='unverified',
                        created_by='system',
                        metadata_json={'auto_extracted': True},
                    )
                    await claim_store.add_evidence(
                        claim_id=claim.claim_id,
                        tenant_id=document.tenant_id,
                        document_id=document.document_id,
                        source_id=document.source_id,
                        chunk_id=chunk['chunk_id'],
                        start_offset=chunk['start_offset'],
                        end_offset=chunk['end_offset'],
                        excerpt_text=candidate,
                    )
                    for timeline_candidate in extract_timeline_candidates(candidate):
                        await timeline_store.create(document.tenant_id, document.case_id, timeline_candidate['event_time'], timeline_candidate['title'], timeline_candidate['description'], document.source_id, claim.claim_id, claim.confidence_score, {'generated_from_claim': True})
                    auto_claims += 1

            entity_store = EntityStore(db)
            relationship_store = RelationshipStore(db)
            entities_by_name = {}
            for chunk in stored_chunks:
                llm_entities = llm_extract_entities(chunk['text'])
                extracted_entities = llm_entities if llm_entities else extract_entities(chunk['text'])
                for ent in extracted_entities:
                    saved = await entity_store.upsert(
                        tenant_id=document.tenant_id,
                        case_id=document.case_id,
                        canonical_name=ent.get('canonical_name', ent.get('name', 'Unknown')),
                        entity_type=ent.get('entity_type', 'unknown'),
                        confidence_score=ent.get('confidence_score', ent.get('confidence', 0.5)),
                        aliases=ent.get('aliases', []),
                        metadata_json={'extracted_from_chunk': chunk['chunk_id']},
                    )
                    entities_by_name[saved.canonical_name.lower()] = saved

                for sub, pred, obj in extract_relationship_candidates(chunk['text']):
                    sub_entity = await entity_store.upsert(document.tenant_id, document.case_id, sub, 'unknown', 0.5, [], {'relationship_candidate': True})
                    obj_entity = await entity_store.upsert(document.tenant_id, document.case_id, obj, 'unknown', 0.5, [], {'relationship_candidate': True})
                    await relationship_store.create(
                        tenant_id=document.tenant_id,
                        case_id=document.case_id,
                        subject_entity_id=sub_entity.entity_id,
                        predicate=pred,
                        object_entity_id=obj_entity.entity_id,
                        source_id=document.source_id,
                        claim_id='',
                        confidence_score=0.55,
                        metadata_json={'chunk_id': chunk['chunk_id']},
                    )

            claim_texts = [c.text for c in await claim_store.list_claims(document.tenant_id, document.case_id)]
            entity_names = [e.canonical_name for e in await entity_store.list_by_case(document.tenant_id, document.case_id)]
            await evaluate_alert_rules(db, document.tenant_id, document.case_id, document.source_id, claim_texts, entity_names, risk_score=min(1.0, auto_claims * 0.1))

            summary = llm_summarize_document(text)
            document.text_content = text + "\n\n[Summary]\n" + summary
            document.processing_status = 'processed'
            document.processing_error = ''
            document.processed_at = datetime.utcnow()
            await db.commit()

            await write_audit(db, document.tenant_id, 'system', 'document.processed', 'document', document.document_id, {'chunks': len(chunks), 'auto_claims': auto_claims}, request=None)
            return {'document_id': document.document_id, 'chunks': len(chunks)}
        except Exception as exc:
            document.processing_status = 'failed'
            document.processing_error = str(exc)
            await db.commit()
            logger.exception('document processing failed', extra={'document_id': document_id})
            await write_audit(db, document.tenant_id, 'system', 'document.process_failed', 'document', document.document_id, {'error': str(exc)}, request=None)
            raise


@celery_app.task(bind=True, max_retries=3, default_retry_delay=5)
def process_document_task(self, document_id: str):
    try:
        return asyncio.run(process_document(document_id))
    except Exception as exc:
        raise self.retry(exc=exc)
