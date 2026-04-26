def evaluate_alerts(report) -> list[str]:
    return ['moderate-confidence-alert'] if report.confidence_score >= 0.7 else []
