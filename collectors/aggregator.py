"""Collector aggregation and normalization logic."""

from core.schemas import CollectionResult, RawIntelItemSchema

SOURCE_RELIABILITY: dict[str, float] = {
    "sec_edgar": 0.97,
    "cisa_advisory": 0.98,
    "opensanctions": 0.95,
    "opencorporates": 0.92,
    "whois": 0.95,
    "dns_records": 0.95,
    "shodan": 0.90,
    "censys": 0.88,
    "otx_alienvault": 0.85,
    "virustotal": 0.90,
    "greynoise": 0.88,
    "abuseipdb": 0.88,
    "news_rss": 0.75,
    "hackernews": 0.70,
    "reddit_post": 0.65,
    "twitter_nitter": 0.60,
    "web_search_snippet": 0.60,
    "academic_paper": 0.85,
    "onion_content": 0.40,
}


class AggregatorBot:
    """Aggregates and normalizes data from all spider collectors."""

    def process(self, results: list[CollectionResult]) -> list[RawIntelItemSchema]:
        """Deduplicate, filter, normalize reliability, and rank items.

        Args:
            results: Collector batch results.

        Returns:
            Processed and sorted intelligence items.
        """
        unique: dict[str, RawIntelItemSchema] = {}
        for result in results:
            for item in result.items:
                if len(item.content.strip()) < 80:
                    continue
                normalized_score = SOURCE_RELIABILITY.get(item.source_type, item.reliability_score)
                normalized_score = max(0.0, min(1.0, normalized_score))
                enriched_item = item.model_copy(update={"reliability_score": normalized_score})
                unique[item.content_hash] = enriched_item
        sorted_items = sorted(unique.values(), key=lambda current: current.reliability_score, reverse=True)
        return sorted_items
