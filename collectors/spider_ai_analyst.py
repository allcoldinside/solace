"""SPIDER-24 AI intermediate analyst collector."""

from __future__ import annotations

import aiohttp

from collectors.base import BaseCollector
from config.settings import settings
from core.schemas import CollectionResult, CollectorID, TargetType


class SpiderAiAnalyst(BaseCollector):
    """Run local Ollama pre-analysis against aggregated collection snippets."""

    bot_id = "SPIDER-24"
    domain = "ai_analyst"
    rate_limit = 0.1
    source_reliability = 0.75

    async def collect(self, target: str, target_type: TargetType) -> CollectionResult:
        """Generate intermediate analysis guidance for the panel pipeline."""
        prompt = self._build_analysis_prompt([], target)
        response = await self._run_ollama_analysis(prompt)
        content = response or f"No Ollama response for {target}; panel should use primary sources directly."
        item = self.build_item(source_url=f"{settings.ollama_host}/api/generate", source_type="ai_intermediate_analysis", content=content, target=target, target_type=target_type)
        return CollectionResult(collector_id=CollectorID.SPIDER_24, items=[item])

    async def _run_ollama_analysis(self, prompt: str) -> str:
        """Execute a non-streaming generation request against local Ollama."""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{settings.ollama_host}/api/generate",
                    json={"model": getattr(settings, "ollama_default_model", "llama3.1"), "prompt": prompt, "stream": False},
                    timeout=30,
                ) as response:
                    if response.status >= 400:
                        self.logger.warning("ollama_error", status=response.status)
                        return ""
                    data = await response.json(content_type=None)
                    return str(data.get("response", ""))
        except aiohttp.ClientError as error:
            self.logger.warning("ollama_network_error", error=str(error))
            return ""

    def _build_analysis_prompt(self, items: list[dict[str, str]], target: str) -> str:
        """Build concise pre-screening instructions for the local analyst model."""
        digest = "\n\n".join(
            f"[{item.get('source_type', 'unknown')}] {item.get('content', '')[:300]}" for item in items[:15]
        )
        return (
            f"You are an intelligence analyst reviewing collection data on {target}.\n\n"
            f"{digest}\n\n"
            "Provide: major finding, deception indicators, cross-source correlation, and threat level rationale."
        )
