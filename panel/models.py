from dataclasses import dataclass


PANEL_BOT_IDS = [
    'ANALYST-ALPHA',
    'ANALYST-BRAVO',
    'ANALYST-CHARLIE',
    'ANALYST-DELTA',
    'ANALYST-ECHO',
    'ANALYST-FOXTROT',
    'ANALYST-GOLF',
    'ANALYST-HOTEL',
]


@dataclass
class PanelBotResult:
    bot_id: str
    finding: str
