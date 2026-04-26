from abc import ABC, abstractmethod


class BaseCollector(ABC):
    @abstractmethod
    async def collect(self, target: str, target_type: str) -> list[dict]:
        raise NotImplementedError
