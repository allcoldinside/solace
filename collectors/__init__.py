"""Collectors package with lazy imports."""

from typing import Type

from collectors.base_collector import BaseCollector


def get_spider(spider_id: str) -> Type[BaseCollector]:
    """Resolve a spider class lazily.

    Args:
        spider_id: Collector identifier like SPIDER-1.

    Returns:
        Collector class.

    Raises:
        KeyError: If spider id is unknown.
    """
    mapping: dict[str, str] = {
        "SPIDER-AGGREGATOR": "collectors.aggregator.AggregatorBot",
    }
    target = mapping.get(spider_id)
    if target is None:
        raise KeyError(f"Unknown spider id: {spider_id}")
    module_name, class_name = target.rsplit(".", 1)
    module = __import__(module_name, fromlist=[class_name])
    return getattr(module, class_name)


__all__ = ["BaseCollector", "get_spider"]
