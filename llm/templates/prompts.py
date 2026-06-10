SYSTEM_GUARDRAILS = (
    'Use only lawfully authorized data. '
    'Cite available evidence references. '
    'Do not make unsupported claims or conclusions.'
)

PROMPTS = {
    'summarize_document': f"{SYSTEM_GUARDRAILS}\nSummarize the document faithfully.",
    'extract_claims': f"{SYSTEM_GUARDRAILS}\nExtract factual claims with evidence snippets.",
    'extract_entities': f"{SYSTEM_GUARDRAILS}\nExtract entities and classify type.",
    'panel_response': f"{SYSTEM_GUARDRAILS}\nProvide role-specific panel response citing case claims.",
}
