import hashlib
from datetime import datetime

from fastapi import APIRouter, Depends, File, HTTPException, Request, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from processing.text_extract import extract_text
from security.audit import write_audit
from security.deps import current_user
from storage.case_store import CaseStore
from storage.document_store import DocumentStore
from storage.object_store import ObjectStore
from storage.source_store import SourceStore
from tasks.document_processing import process_document_task

router = APIRouter(prefix='/cases', tags=['sources'])


@router.post('/{case_id}/sources/upload')
async def upload_source_document(
    case_id: str,
    request: Request,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    user=Depends(current_user),
):
    case = await CaseStore(db).get(user.tenant_id, case_id)
    if not case:
        raise HTTPException(status_code=404, detail='case not found')

    content = await file.read()
    sha256_hash = hashlib.sha256(content).hexdigest()

    duplicate = await DocumentStore(db).find_by_hash(user.tenant_id, case_id, sha256_hash)
    if duplicate:
        raise HTTPException(status_code=409, detail={'message': 'duplicate hash detected', 'document_id': duplicate.document_id})

    object_key = f"{user.tenant_id}/{case_id}/{datetime.utcnow().strftime('%Y%m%d%H%M%S')}-{file.filename}"
    await ObjectStore().put(object_key, content)

    source = await SourceStore(db).create(
        tenant_id=user.tenant_id,
        case_id=case_id,
        source_type='upload',
        name=file.filename,
        uri=file.filename,
        collection_method='user_upload',
        authorization_basis='user provided',
        collected_by=user.user_id,
        metadata_json={'size_bytes': len(content), 'mime_type': file.content_type or 'application/octet-stream'},
    )

    text_content = extract_text(content, file.filename, file.content_type)
    document = await DocumentStore(db).create(
        tenant_id=user.tenant_id,
        case_id=case_id,
        source_id=source.source_id,
        title=file.filename,
        mime_type=file.content_type or 'application/octet-stream',
        object_key=object_key,
        sha256_hash=sha256_hash,
        size_bytes=len(content),
        text_content=text_content,
    )

    try:
        task = process_document_task.delay(document.document_id)
        task_id = task.id
    except Exception:
        task_id = None

    await write_audit(
        db,
        user.tenant_id,
        user.user_id,
        'document.upload',
        'document',
        document.document_id,
        {'case_id': case_id, 'source_id': source.source_id, 'sha256_hash': sha256_hash},
        request=request,
    )

    return {'source_id': source.source_id, 'document_id': document.document_id, 'sha256_hash': sha256_hash, 'object_key': object_key, 'task_id': task_id}
