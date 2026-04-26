from reports.schema import ReportData


def validate_report(report: ReportData) -> None:
    assert report.report_id.startswith('REPORT-')
    assert report.subject
    assert 0 <= report.confidence_score <= 1
    assert report.full_markdown
