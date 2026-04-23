"""Generic webhook routing utilities."""

from __future__ import annotations

import aiohttp


class WebhookRouter:
    """Route structured alerts to external webhook endpoints."""

    async def send(self, webhook_url: str, payload: dict[str, object]) -> int:
        """POST payload to webhook and return HTTP status code."""
        async with aiohttp.ClientSession() as session:
            async with session.post(webhook_url, json=payload, timeout=20) as response:
                return response.status
