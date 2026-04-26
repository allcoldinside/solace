from reports.schema import ReportData, new_report_id


def generate_report(target: str, target_type: str, enriched_items: list[dict], entities: list[dict]) -> ReportData:
    findings = [x['content'] for x in enriched_items[:5]]
    md = '# SOLACE Report\n\n' + '\n'.join(f'- {f}' for f in findings)
    return ReportData(
        report_id=new_report_id(),
        subject=target,
        subject_type=target_type,
        classification='TLP:WHITE',
        confidence='MEDIUM',
        confidence_score=0.72,
        executive_summary=f'Assessment for {target}',
        key_findings=findings,
        entity_map=entities,
        timeline=['T0 collection complete', 'T1 analysis complete'],
        behavioral_indicators=['association patterns'],
        threat_assessment='Moderate risk from open-source indicators.',
        source_log=[x.get('source', 'unknown') for x in enriched_items],
        gaps=['Need corroborating private telemetry'],
        analyst_notes='Seed pipeline run.',
        full_markdown=md,
    )
