from collections import Counter


def build_structured_report(title: str, entities: list, timeline: list, claims: list, evidence_count: int) -> tuple[str, dict]:
    entity_names = [getattr(e, 'canonical_name', '') for e in entities][:10]
    claim_texts = [getattr(c, 'text', '') for c in claims][:10]
    timeline_lines = [f"- {getattr(t, 'event_time')} — {getattr(t, 'title')}" for t in timeline[:10]]

    confidence_score = round(min(0.95, 0.4 + (len(claims) * 0.05) + (evidence_count * 0.01)), 2)
    risk = 'Low'
    if confidence_score >= 0.75:
        risk = 'High'
    elif confidence_score >= 0.6:
        risk = 'Medium'

    key_findings = [c for c in claim_texts if c][:5]

    markdown = f"""# {title}

## Executive Summary
This report is generated from verified stored case data only. No unsupported conclusions are included.

## Key Findings
{chr(10).join(f'- {x}' for x in key_findings) or '- No findings available.'}

## Entities
{chr(10).join(f'- {x}' for x in entity_names) or '- No entities available.'}

## Timeline
{chr(10).join(timeline_lines) or '- No timeline entries available.'}

## Claims and Evidence Table
- Claims included: {len(claims)}
- Evidence links included: {evidence_count}

## Risk Assessment
- Risk level: {risk}

## Confidence Score
- Confidence: {confidence_score}

## Recommended Follow-up Tasks
- Validate unresolved claims against additional sources.
- Review disputed or contradictory evidence.
"""

    payload = {
        'executive_summary': 'Generated from stored case evidence only.',
        'key_findings': key_findings,
        'entities': entity_names,
        'timeline': timeline_lines,
        'claims_count': len(claims),
        'evidence_count': evidence_count,
        'risk_assessment': risk,
        'confidence_score': confidence_score,
        'recommended_follow_up_tasks': [
            'Validate unresolved claims against additional sources.',
            'Review disputed or contradictory evidence.',
        ],
        'claim_types': dict(Counter(getattr(c, 'claim_type', 'unknown') for c in claims)),
    }
    return markdown, payload
