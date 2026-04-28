"""SPIDER-10 cryptocurrency and blockchain collector."""

from __future__ import annotations

import aiohttp

from collectors.base import BaseCollector
from config.settings import get_settings
settings = get_settings()
from core.schemas import CollectionResult, CollectorID, TargetType


class SpiderCrypto(BaseCollector):
    """Collect on-chain indicators from public blockchain APIs."""

    bot_id = "SPIDER-10"
    domain = "crypto"
    source_reliability = 0.92

    async def collect(self, target: str, target_type: TargetType) -> CollectionResult:
        """Collect blockchain context for an address-like target."""
        items = []
        async with aiohttp.ClientSession() as session:
            btc = await self.fetch_json(session, f"https://blockchain.info/rawaddr/{target}?limit=5")
            if isinstance(btc, dict):
                items.append(self.build_item(source_url=f"https://blockchain.info/rawaddr/{target}", source_type="blockchain_btc", content=f"Bitcoin address {target} tx count={btc.get('n_tx', 0)} balance={btc.get('final_balance', 0)}.", target=target, target_type=target_type))
            blockchair = await self.fetch_json(session, f"https://api.blockchair.com/bitcoin/dashboards/address/{target}")
            if isinstance(blockchair, dict):
                items.append(self.build_item(source_url=f"https://api.blockchair.com/bitcoin/dashboards/address/{target}", source_type="blockchain_multichain", content=f"Blockchair dashboard returned data keys: {','.join(blockchair.keys())}.", target=target, target_type=target_type, reliability=0.90))
            if settings.etherscan_api_key:
                eth = await self.fetch_json(session, "https://api.etherscan.io/api", params={"module": "account", "action": "balance", "address": target, "tag": "latest", "apikey": settings.etherscan_api_key})
                if isinstance(eth, dict):
                    items.append(self.build_item(source_url="https://api.etherscan.io/api", source_type="blockchain_eth", content=f"Etherscan response status={eth.get('status')} for address {target}.", target=target, target_type=target_type))
        return CollectionResult(collector_id=CollectorID.SPIDER_10, items=items)
