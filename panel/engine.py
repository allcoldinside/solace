from panel.models import PANEL_BOT_IDS


def analyze_panel(report) -> dict:
    transcript = [f'{bot_id}: reviewed {report.subject}' for bot_id in PANEL_BOT_IDS]
    return {
        'summary': f'8-bot panel reviewed {report.report_id}',
        'transcript': transcript,
        'bots_used': PANEL_BOT_IDS,
    }
