from abc import ABC, abstractmethod

from llm.service import panel_response

DEFAULT_PANEL_ROLES = ['operator', 'skeptic', 'compliance', 'financial', 'strategic', 'security']


class PanelProvider(ABC):
    @abstractmethod
    def run(self, prompt: str, claims: list[dict], evidence_count: int) -> list[dict]:
        raise NotImplementedError


class MockPanelProvider(PanelProvider):
    def run(self, prompt: str, claims: list[dict], evidence_count: int) -> list[dict]:
        responses = []
        claim_refs = ', '.join(c.get('claim_id', 'unknown') for c in claims[:3]) or 'none'
        for idx, role in enumerate(DEFAULT_PANEL_ROLES):
            responses.append(
                {
                    'agent_role': role,
                    'response_text': panel_response(role, prompt, claims),
                    'confidence_score': round(0.55 + (idx * 0.05), 2),
                    'concerns_json': {'requires_human_review': role in {'skeptic', 'compliance'}},
                }
            )
        return responses
