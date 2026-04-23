"""NotebookLM-oriented Google Drive synchronization helpers."""

from __future__ import annotations

from datetime import datetime

from reports.schema import ReportData


class NotebookLMSync:
    """Manage NotebookLM-friendly report files and index metadata."""

    def __init__(self) -> None:
        """Initialize in-memory report index."""
        self._synced_reports: dict[str, ReportData] = {}
        self._entity_counts: dict[str, int] = {}

    async def sync_report_to_notebooklm_folder(self, report: ReportData) -> str:
        """Record a report as synced and return deterministic document id."""
        self._synced_reports[report.report_id] = report
        self._entity_counts[report.subject] = self._entity_counts.get(report.subject, 0) + 1
        return f"NLM-{report.report_id}"

    async def update_master_index(self) -> str:
        """Generate markdown index table for all synced reports."""
        header = "| report_id | subject | date | confidence | key_finding_1 |"
        rows = [header, "|---|---|---|---|---|"]
        for report in self._synced_reports.values():
            date_str = datetime.utcnow().strftime("%Y-%m-%d")
            first_finding = report.key_findings[0] if report.key_findings else ""
            rows.append(f"| {report.report_id} | {report.subject} | {date_str} | MEDIUM | {first_finding} |")
        return "\n".join(rows)

    async def create_entity_summary_doc(self, entity_name: str) -> str:
        """Build summary text for reports linked to a specific entity."""
        related = [r for r in self._synced_reports.values() if r.subject == entity_name]
        summary_lines = [f"# Entity Summary: {entity_name}", f"Reports: {len(related)}"]
        for report in related:
            summary_lines.append(f"- {report.report_id}: {report.executive_summary[:120]}")
        return "\n".join(summary_lines)
