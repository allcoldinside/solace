"""Invariant checks for generated artifacts."""

from __future__ import annotations

from core.errors import InvariantError
from reports.schema import ReportData


def validate_report(report: ReportData) -> None:
    if not report.report_id.startswith("REPORT-"):
        raise InvariantError("report_id must start with REPORT-")
    if not report.subject or not report.subject_type or not report.executive_summary or not report.full_markdown:
        raise InvariantError("report is missing required narrative fields")
    if not 0 <= report.confidence_score <= 1:
        raise InvariantError("confidence_score must be between 0 and 1")
