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
    "holehe_email": 0.72,
    "maigret_username": 0.72,
    "wmn_username": 0.70,
    "blockchain_btc": 0.92,
    "blockchain_eth": 0.92,
    "blockchain_multichain": 0.90,
    "crypto_scam_db": 0.88,
    "job_listing_indeed": 0.70,
    "job_listing_linkedin": 0.72,
    "job_listing_glassdoor": 0.68,
    "job_listing_remote": 0.70,
    "court_pacer": 0.95,
    "court_ftc": 0.95,
    "court_cfpb": 0.95,
    "regulatory_federal_register": 0.95,
    "github_code": 0.80,
    "github_repos": 0.80,
    "github_users": 0.75,
    "gitlab_code": 0.78,
    "pastebin": 0.45,
    "image_tineye": 0.82,
    "image_exif": 0.95,
    "image_flickr": 0.65,
    "image_wikimedia": 0.65,
    "patent_uspto": 0.93,
    "patent_epo": 0.93,
    "patent_wipo": 0.93,
    "market_alpha_vantage": 0.88,
    "market_yahoo": 0.85,
    "crypto_coingecko": 0.85,
    "econ_fred": 0.88,
    "supply_usaspending": 0.90,
    "supply_worldbank": 0.90,
    "supply_officers": 0.90,
    "supply_companies_house": 0.92,
    "infra_bgp": 0.92,
    "infra_cert_transparency": 0.94,
    "infra_dns_history": 0.88,
    "infra_ipinfo": 0.88,
    "infra_robtex": 0.88,
    "paste_pastebin": 0.45,
    "paste_gist": 0.45,
    "paste_intelx": 0.45,
    "paste_psbdmp": 0.45,
    "forum_4chan": 0.40,
    "forum_telegram_public": 0.50,
    "forum_reddit_security": 0.45,
    "forum_breach_mirror": 0.40,
    "transport_ais": 0.88,
    "transport_flight": 0.88,
    "transport_opensky": 0.90,
    "vuln_nvd": 0.97,
    "vuln_exploit_db": 0.88,
    "vuln_packetstorm": 0.80,
    "breach_hibp": 0.95,
    "breach_dehashed": 0.80,
    "breach_leakcheck": 0.78,
    "ai_intermediate_analysis": 0.75,
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
