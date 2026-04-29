"""Collector factory and spider registry."""

from __future__ import annotations

from typing import TYPE_CHECKING, Type

from collectors.base_collector import BaseCollector

if TYPE_CHECKING:
    pass


def get_spider(spider_id: str) -> Type[BaseCollector]:
    mapping: dict[str, tuple[str, str]] = {
        "SPIDER-AGGREGATOR": ("collectors.aggregator", "AggregatorBot"),
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
    if spider_id not in mapping:
        raise ValueError(f"Unknown spider_id: {spider_id}")
    module_name, class_name = mapping[spider_id]
    module = __import__(module_name, fromlist=[class_name])
    return getattr(module, class_name)


__all__ = ["BaseCollector", "get_spider"]
