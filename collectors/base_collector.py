from abc import ABC, abstractmethod


class BaseCollector(ABC):
    bot_id: str

    def __init__(self, bot_id: str):
        self.bot_id = bot_id

    @abstractmethod
    async def collect(self, target: str, target_type: str) -> list[dict]:
        raise NotImplementedError
