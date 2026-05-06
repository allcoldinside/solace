from abc import ABC, abstractmethod

from config.settings import get_settings


class LLMProvider(ABC):
    @abstractmethod
    def chat(self, system_prompt: str, user_prompt: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def summarize(self, text: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def extract(self, text: str, mode: str) -> list[dict]:
        raise NotImplementedError

    @abstractmethod
    def embed(self, text: str) -> list[float]:
        raise NotImplementedError


class MockLLMProvider(LLMProvider):
    def chat(self, system_prompt: str, user_prompt: str) -> str:
        return f"MOCK_CHAT: {user_prompt[:120]}"

    def summarize(self, text: str) -> str:
        return f"MOCK_SUMMARY: {text[:120]}"

    def extract(self, text: str, mode: str) -> list[dict]:
        if mode == 'claims':
            parts = [p.strip() for p in text.split('.') if p.strip()]
            return [{'text': p, 'evidence': p[:80], 'confidence': 0.6} for p in parts[:5]]
        if mode == 'entities':
            candidates = []
            for token in text.split():
                if token[:1].isupper() and len(token) > 2:
                    candidates.append({'name': token.strip('.,'), 'entity_type': 'unknown', 'confidence': 0.5})
            return candidates[:10]
        return []

    def embed(self, text: str) -> list[float]:
        n = min(8, max(1, len(text) // 20))
        return [float((i + 1) / n) for i in range(n)]


class OptionalProvider(LLMProvider):
    def __init__(self):
        self._mock = MockLLMProvider()

    def chat(self, system_prompt: str, user_prompt: str) -> str:
        return self._mock.chat(system_prompt, user_prompt)

    def summarize(self, text: str) -> str:
        return self._mock.summarize(text)

    def extract(self, text: str, mode: str) -> list[dict]:
        return self._mock.extract(text, mode)

    def embed(self, text: str) -> list[float]:
        return self._mock.embed(text)


def get_provider() -> LLMProvider:
    settings = get_settings()
    if settings.llm_provider == 'mock' or not settings.llm_provider:
        return MockLLMProvider()
    return OptionalProvider()
