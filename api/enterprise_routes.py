"""Enterprise API route payload helpers."""

from __future__ import annotations


def list_enterprise_features() -> dict[str, list[str]]:
    """List enterprise add-ons exposed through API routes."""
    return {
        "features": [
            "24-spider collection matrix",
            "5-analyst panel mode",
            "NotebookLM sync",
            "MISP IOC push/pull",
            "Slack command integration",
        ]
    }
