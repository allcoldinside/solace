# SOLACE — Collector Reference

Full documentation for all 8 spider bots.

---

## Overview

All collectors extend `BaseCollector` and implement two methods:
- `collect(target, target_type) -> CollectionResult`
- `validate_target(target) -> bool`

Every HTTP request goes through `_fetch()` which handles rate limiting (per-collector configurable delay), 3 retries with exponential backoff, and 429 handling.

### Source Reliability Scores

The aggregator normalizes reliability scores based on source type:

| Source Type | Reliability | Rationale |
|------------|-------------|-----------|
| `cisa_advisory` | 0.98 | US government official advisories |
| `sec_edgar` | 0.97 | SEC regulatory filings |
| `opensanctions` | 0.95 | Verified sanctions database |
| `whois` | 0.95 | Authoritative domain registry |
| `dns_records` | 0.95 | Authoritative DNS |
| `opencorporates` | 0.92 | Company registry (180+ countries) |
| `shodan` | 0.90 | Internet scan data |
| `virustotal` | 0.90 | Threat correlation platform |
| `censys` | 0.88 | Certificate + device intelligence |
| `greynoise` | 0.88 | Noise vs. targeted traffic |
| `abuseipdb` | 0.88 | Community abuse reports |
| `academic_paper` | 0.85 | Peer-reviewed research |
| `otx_alienvault` | 0.85 | Community threat pulses |
| `news_rss` | 0.75 | Mainstream news (editorial standards vary) |
| `hackernews` | 0.70 | Technical community discussion |
| `reddit_post` | 0.65 | Community-generated content |
| `web_search_snippet` | 0.60 | Search result snippets (unverified) |
| `twitter_nitter` | 0.60 | Social media posts (unverified) |
| `onion_content` | 0.40 | Dark web (inherently unverifiable) |

---

## SPIDER-1: Web & News

**File:** `collectors/spider_web_news.py`
**Domain:** `web_news`
**Rate limit:** 1.5s between requests
**Reliability:** 0.75 (news_rss), 0.60 (web snippets)

### Sources

**Google News RSS:**
```
https://news.google.com/rss/search?q={target}&hl=en-US&gl=US&ceid=US:en
```
- Fetches up to 20 article links from RSS feed
- Downloads each article and extracts clean text via `trafilatura`
- Filters to articles that mention the target
- Falls back to article snippet if trafilatura returns nothing useful

**DuckDuckGo HTML:**
```
https://html.duckduckgo.com/html/?q={query}
```
- Runs 2 queries: bare target + target with date range
- Extracts result snippets via BeautifulSoup4
- Returns snippets only (not full articles) — lower reliability

### Dependencies
```
trafilatura    — Clean article text extraction
feedparser     — RSS parsing
beautifulsoup4 — HTML parsing
```

---

## SPIDER-2: Social & Forums

**File:** `collectors/spider_social.py`
**Domain:** `social_forums`
**Rate limit:** 1.0s
**Reliability:** 0.65 (reddit), 0.70 (hackernews), 0.60 (twitter)

### Sources

**Reddit (PRAW):**
- Searches `r/all` for the target
- Collects up to 20 submissions (sorted by new)
- Captures: title, post text (up to 2000 chars), score, comment count, author, subreddit

**HackerNews (Algolia API):**
```
https://hn.algolia.com/api/v1/search?query={target}&hitsPerPage=20&tags=story
```
- Story search (not comments)
- Captures: title, story text, points, comment count, author

**Nitter/Twitter (HTML scraping):**
- Tries 3 public Nitter instances in sequence, stops at first success
- Extracts tweet text from `div.tweet-content`
- No API key required — works with public content only

### Dependencies
```
praw    — Reddit API wrapper (read-only)
```

---

## SPIDER-3: Network & DNS

**File:** `collectors/spider_network.py`
**Domain:** `network_dns`
**Rate limit:** 0.5s
**Reliability:** 0.88–0.97

### Sources

**WHOIS:**
- Uses `python-whois` (run in executor thread — synchronous library)
- Captures: registrar, registration/expiry dates, nameservers, registrant info (if public)

**DNS Records:**
- Queries all record types: A, AAAA, MX, NS, TXT, CNAME
- Uses `dnspython` async resolution
- Single combined item with all record types

**Shodan:**
```
https://api.shodan.io/shodan/host/search?key={SHODAN_API_KEY}&query={target}&limit=10
```
- Only runs if `SHODAN_API_KEY` is set
- Captures: IP, port, banner, OS, org per match

**Censys:**
```
https://search.censys.io/api/v2/hosts/search?q={target}&per_page=5
```
- Only runs if `CENSYS_API_ID` and `CENSYS_API_SECRET` are set
- Basic auth with API credentials
- Captures: IP, services per match

### Dependencies
```
python-whois    — WHOIS queries
dnspython       — DNS resolution
```

---

## SPIDER-4: Dark Web

**File:** `collectors/spider_darkweb.py`
**Domain:** `dark_web`
**Rate limit:** 3.0s (Tor is slow)
**Reliability:** 0.40 (inherently unverifiable)

### Network Isolation

SPIDER-4 runs in the `tor_net` Docker network which is defined as `internal: true` — it has no internet gateway. Traffic only flows through the Tor daemon. This network is completely separate from `solace_net`.

### Sources

**Connectivity check first:**
```
https://check.torproject.org/api/ip
```
If Tor is unreachable, spider returns empty result with an error — it does not fall back to clearnet.

**Ahmia (dark web search index):**
```
https://ahmia.fi/search/?q={target}
```
Ahmia is a clearnet-accessible search engine that indexes .onion sites. Returns: title, onion URL, description.

**DarkSearch API:**
```
https://darksearch.io/api/search?query={target}&page=1
```
Another dark web search index with public API. Returns: title, onion URL, description.

### Important Notes

- All items tagged with `"warning": "Unverified dark web source"` in metadata
- Reliability deliberately set to 0.40
- Panel engine should treat dark web items with extra skepticism
- This spider is in STANDBY by default — activate by ensuring Tor is running

---

## SPIDER-5: Corporate & Financial

**File:** `collectors/spider_corporate.py`
**Domain:** `corporate_financial`
**Rate limit:** 1.0s
**Reliability:** 0.92–0.97

### Sources

**OpenCorporates:**
```
https://api.opencorporates.com/v0.4/companies/search?q={target}
```
- 180+ country company registries
- Captures: company name, jurisdiction, company number, status, incorporation date, registered address
- Optional API token via `OPENCORPORATES_API_KEY` (higher rate limits)

**SEC EDGAR:**
```
https://efts.sec.gov/LATEST/search-index?q="{target}"&forms=10-K,8-K,20-F
```
- Full-text search of SEC filings
- Captures: form type, company name, filed date, period of report
- No API key required (public government data)

**OpenSanctions:**
```
https://api.opensanctions.org/search/default?q={target}&limit=5
```
- Sanctions database covering 100+ lists worldwide
- Includes: UN, US OFAC, EU, UK, and many national lists
- Also covers PEP (Politically Exposed Persons) data
- Captures: entity name, schema, datasets matched, confidence score, properties
- Items with score < 0.5 are filtered out

---

## SPIDER-6: Geospatial

**File:** `collectors/spider_geo.py`
**Domain:** `geo_satellite`
**Rate limit:** 1.5s (Nominatim requires 1s between requests per their policy)
**Reliability:** 0.78–0.90

### Sources

**Nominatim (OpenStreetMap geocoding):**
```
https://nominatim.openstreetmap.org/search?q={target}&format=json&addressdetails=1&limit=5
```
- Converts target name to geographic coordinates
- Returns: lat/lon, full address, country, state, city, OSM ID

**Overpass API (OSM entity search):**
```
https://overpass-api.de/api/interpreter
```
- OverpassQL query to find named entities (nodes, ways, relations)
- Finds businesses, buildings, landmarks matching the target name
- Returns: coordinates, address, website, phone, OSM type/ID

**IP Geolocation:**
```
https://ipapi.co/{ip}/json/
```
- Only runs if target is a valid IPv4 address
- Returns: country, region, city, coordinates, ISP, ASN, timezone

**Copernicus Satellite (metadata only):**
- Queries Copernicus Open Access Hub for Sentinel-2 coverage metadata
- Returns coverage info only (not actual imagery)
- Requires Copernicus credentials (gracefully skips if unavailable)

---

## SPIDER-7: Documents

**File:** `collectors/spider_documents.py`
**Domain:** `documents_leaks`
**Rate limit:** 1.5s
**Reliability:** 0.80–0.98

### Sources

**CISA Cybersecurity Advisories:**
```
https://www.cisa.gov/cybersecurity-advisories/all.xml
```
- RSS feed of all CISA advisories
- Filters to advisories mentioning the target
- Extremely high reliability (0.98) — US government official source

**Semantic Scholar:**
```
https://api.semanticscholar.org/graph/v1/paper/search?query={target}&limit=5
```
- Academic paper search
- Captures: title, abstract, year, venue, authors
- Useful for technical targets, researchers, organizations

---

## SPIDER-8: Threat Intelligence

**File:** `collectors/spider_threat.py`
**Domain:** `threat_feeds`
**Rate limit:** 0.5s
**Reliability:** 0.85–0.90

### Sources

**OTX AlienVault:**
```
https://otx.alienvault.com/api/v1/search/pulses?q={target}&limit=5
```
- Requires `ALIENVAULT_OTX_API_KEY`
- Searches threat pulse database
- Captures: pulse name, description, TLP, tags, indicator count

**VirusTotal:**
```
https://www.virustotal.com/api/v3/search?query={target}&limit=5
```
- Requires `VIRUSTOTAL_API_KEY`
- Searches across files, URLs, IPs, domains
- Captures: entity type, analysis stats, reputation score

**AbuseIPDB:**
```
https://api.abuseipdb.com/api/v2/check?ipAddress={target}&maxAgeInDays=90
```
- Only runs if target is a valid IP address
- Uses public key (limited — set own key for higher limits)
- Captures: abuse confidence score, country, ISP, total reports, last reported

**GreyNoise:**
```
https://api.greynoise.io/v3/community/{target}
```
- Requires `GREYNOISE_API_KEY`
- Only runs if target is a valid IP address
- Classifies IP as: benign/malicious internet noise vs. targeted attack traffic
- Captures: noise classification, riot (known business), name, message

---

## Adding Custom Collectors

To add a new collector:

1. Create `collectors/spider_custom.py` extending `BaseCollector`
2. Set `bot_id = "SPIDER-9"`, `domain = "custom"`, `rate_limit`, `source_reliability`
3. Implement `collect()` and `validate_target()`
4. Add to `SOURCE_RELIABILITY` dict in `collectors/aggregator.py`
5. Register in `collectors/__init__.py`'s `get_spider()` factory
6. Add to `get_all_spiders()` list

Example minimal collector:
```python
class SpiderCustom(BaseCollector):
    bot_id = "SPIDER-9"
    domain = "custom"
    rate_limit = 1.0
    source_reliability = 0.75

    async def validate_target(self, target: str) -> bool:
        return bool(target)

    async def collect(self, target: str, target_type: TargetType) -> CollectionResult:
        start = time.monotonic()
        items, errors = [], []
        async with self:
            data = await self._fetch(f"https://api.example.com/search?q={target}")
            if data and isinstance(data, dict):
                for result in data.get("results", []):
                    items.append(self._build_item(
                        content=result["text"],
                        source_url=result["url"],
                        source_type="custom_api",
                        target=target,
                        target_type=target_type.value,
                    ))
        return self._build_result(target, target_type.value, items,
                                  time.monotonic() - start, errors)
```
