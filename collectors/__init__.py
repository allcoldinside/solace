from collectors.seed_collector import SeedCollector


def get_spider(_: str):
    return SeedCollector()
