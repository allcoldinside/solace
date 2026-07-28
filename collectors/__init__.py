"""Collector registry – maps spider names to their classes."""
from __future__ import annotations

from collectors.seed_collector import SeedCollector
from collectors.spider_ai_analyst import SpiderAiAnalyst
from collectors.spider_breach import SpiderBreach
from collectors.spider_code import SpiderCode
from collectors.spider_crypto import SpiderCrypto
from collectors.spider_financial import SpiderFinancial
from collectors.spider_forums import SpiderForums
from collectors.spider_identity import SpiderIdentity
from collectors.spider_infra_adv import SpiderInfraAdv
from collectors.spider_jobs import SpiderJobs
from collectors.spider_legal import SpiderLegal
from collectors.spider_media import SpiderMedia
from collectors.spider_paste import SpiderPaste
from collectors.spider_patents import SpiderPatents
from collectors.spider_supply import SpiderSupply
from collectors.spider_transport import SpiderTransport
from collectors.spider_vuln import SpiderVuln

REGISTRY: dict[str, type] = {
    'seed':        SeedCollector,
    'SPIDER-9':    SpiderIdentity,
    'SPIDER-10':   SpiderCrypto,
    'SPIDER-11':   SpiderJobs,
    'SPIDER-12':   SpiderLegal,
    'SPIDER-13':   SpiderCode,
    'SPIDER-14':   SpiderMedia,
    'SPIDER-15':   SpiderPatents,
    'SPIDER-16':   SpiderFinancial,
    'SPIDER-17':   SpiderSupply,
    'SPIDER-18':   SpiderInfraAdv,
    'SPIDER-19':   SpiderPaste,
    'SPIDER-20':   SpiderForums,
    'SPIDER-21':   SpiderTransport,
    'SPIDER-22':   SpiderVuln,
    'SPIDER-23':   SpiderBreach,
    'SPIDER-24':   SpiderAiAnalyst,
}


def get_spider(name: str):
    """Return an instantiated collector for *name*, defaulting to SeedCollector."""
    cls = REGISTRY.get(name, SeedCollector)
    return cls()


__all__ = ['REGISTRY', 'get_spider', 'SeedCollector']
