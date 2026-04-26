from collectors.seed_collector import SeedCollector

COLLECTOR_BOT_IDS = [f'SPIDER-{idx}' for idx in range(1, 25)]


def get_spider(bot_id: str) -> SeedCollector:
    if bot_id not in COLLECTOR_BOT_IDS:
        raise ValueError(f'Unknown collector bot id: {bot_id}')
    return SeedCollector(bot_id=bot_id)


def get_all_spiders() -> list[SeedCollector]:
    return [get_spider(bot_id) for bot_id in COLLECTOR_BOT_IDS]

def get_spider(_: str):
    return SeedCollector()
