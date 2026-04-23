"""OpenCTI integration helpers."""

from __future__ import annotations


class OpenCTIClient:
    """Simple OpenCTI query helper placeholder with concrete behavior."""

    async def upsert_indicator(self, value: str, pattern_type: str = "stix") -> dict[str, str]:
        """Return normalized indicator payload for upstream API submission."""
        return {"value": value, "pattern_type": pattern_type}
