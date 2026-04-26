from collectors.base_collector import BaseCollector


class SeedCollector(BaseCollector):
    async def collect(self, target: str, target_type: str) -> list[dict]:
        return [
            {'source': 'seed', 'content': f'{target} observed in routine chatter', 'target': target, 'target_type': target_type},
            {'source': 'seed', 'content': f'{target} linked to Example Org and Jane Doe', 'target': target, 'target_type': target_type},
        ]
