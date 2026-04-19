"""Collector factory and spider registry."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collectors.base import BaseCollector


def get_spider(spider_id: str) -> "BaseCollector":
    """Instantiate collector by spider identifier.

    Args:
        spider_id: Collector ID like ``SPIDER-1``.

    Returns:
        Instantiated collector implementation.

    Raises:
        ValueError: If spider is unknown.
    """
    mapping = {
        "SPIDER-9": ("collectors.spider_identity", "SpiderIdentity"),
        "SPIDER-10": ("collectors.spider_crypto", "SpiderCrypto"),
        "SPIDER-11": ("collectors.spider_jobs", "SpiderJobs"),
        "SPIDER-12": ("collectors.spider_legal", "SpiderLegal"),
        "SPIDER-13": ("collectors.spider_code", "SpiderCode"),
        "SPIDER-14": ("collectors.spider_media", "SpiderMedia"),
        "SPIDER-15": ("collectors.spider_patents", "SpiderPatents"),
        "SPIDER-16": ("collectors.spider_financial", "SpiderFinancial"),
        "SPIDER-17": ("collectors.spider_supply", "SpiderSupply"),
        "SPIDER-18": ("collectors.spider_infra_adv", "SpiderInfraAdv"),
        "SPIDER-19": ("collectors.spider_paste", "SpiderPaste"),
        "SPIDER-20": ("collectors.spider_forums", "SpiderForums"),
        "SPIDER-21": ("collectors.spider_transport", "SpiderTransport"),
        "SPIDER-22": ("collectors.spider_vuln", "SpiderVuln"),
        "SPIDER-23": ("collectors.spider_breach", "SpiderBreach"),
        "SPIDER-24": ("collectors.spider_ai_analyst", "SpiderAiAnalyst"),
    }
    if spider_id in {f"SPIDER-{idx}" for idx in range(1, 9)}:
        from collectors.base import BaseCollector

        class _GenericSpider(BaseCollector):
            """Compatibility wrapper for baseline spiders."""

            def __init__(self, spider: str) -> None:
                super().__init__()
                self.bot_id = spider
                self.domain = "baseline"

        return _GenericSpider(spider_id)
    if spider_id not in mapping:
        raise ValueError(f"Unknown spider_id: {spider_id}")
    module_name, class_name = mapping[spider_id]
    module = __import__(module_name, fromlist=[class_name])
    spider_cls = getattr(module, class_name)
    return spider_cls()


def get_all_spiders() -> list["BaseCollector"]:
    """Instantiate all 24 spiders in sequence order."""
    return [get_spider(f"SPIDER-{idx}") for idx in range(1, 25)]
