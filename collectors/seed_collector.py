from collectors.base_collector import BaseCollector


class SeedCollector(BaseCollector):
    async def collect(self, target: str, target_type: str) -> list[dict]:
        return [
            {
                'source': f'seed:{self.bot_id}',
                'content': f'{target} observed by {self.bot_id} in routine chatter',
                'target': target,
                'target_type': target_type,
                'collector_id': self.bot_id,
            },
            {
                'source': f'seed:{self.bot_id}',
                'content': f'{target} linked to Example Org and Jane Doe by {self.bot_id}',
                'target': target,
                'target_type': target_type,
                'collector_id': self.bot_id,
            },
        ]
