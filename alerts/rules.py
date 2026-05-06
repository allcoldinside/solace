from storage.alert_store import AlertStore


async def evaluate_alert_rules(db, tenant_id: str, case_id: str, source_id: str, claim_texts: list[str], entity_names: list[str], risk_score: float = 0.0):
    store = AlertStore(db)
    rules = [r for r in await store.list_rules(tenant_id) if r.enabled]
    watchlists = await store.list_watchlists(tenant_id)
    created = []

    for rule in rules:
        if rule.rule_type == 'keyword_match':
            keywords = rule.metadata_json.get('keywords', [])
            text_blob = ' '.join(claim_texts).lower()
            for kw in keywords:
                if kw.lower() in text_blob:
                    created.append(await store.create_alert(tenant_id, case_id, rule.rule_id, f'Keyword match: {kw}', 'warning', f'Keyword {kw} found in claims', source_id, ''))
                    break
        elif rule.rule_type == 'entity_match':
            entities = {x.lower() for x in entity_names}
            expected = {x.lower() for x in rule.metadata_json.get('entity_names', [])}
            if entities & expected:
                created.append(await store.create_alert(tenant_id, case_id, rule.rule_id, 'Entity match', 'warning', 'Entity watch match detected', source_id, ''))
        elif rule.rule_type == 'risk_score_threshold':
            if risk_score >= rule.threshold:
                created.append(await store.create_alert(tenant_id, case_id, rule.rule_id, 'Risk threshold', 'critical', f'Risk score {risk_score} exceeded threshold {rule.threshold}', source_id, ''))

    # watchlist term triggers
    text_blob = ' '.join(claim_texts).lower()
    for watch in watchlists:
        for term in watch.terms:
            if term.lower() in text_blob:
                created.append(await store.create_alert(tenant_id, case_id, 'watchlist', f'Watchlist term: {term}', 'warning', f'Watchlist term matched in claims for {watch.name}', source_id, ''))
                break

    return created
