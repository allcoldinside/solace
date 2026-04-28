"""Slack integration for SOLACE alerts and slash command formatting."""

from __future__ import annotations

from config.settings import get_settings
settings = get_settings()


class SolaceSlackBot:
    """Send alerts and format slash command responses for Slack."""

    def __init__(self) -> None:
        """Lazy import Slack SDK client to respect optional dependency usage."""
        from slack_sdk import WebClient

        self.client = WebClient(token=settings.slack_bot_token)

    async def post_alert(self, title: str, body: str) -> dict[str, object]:
        """Post alert message into configured Slack channel."""
        return self.client.chat_postMessage(channel=settings.slack_alerts_channel_id, text=f"*{title}*\n{body}")

    def parse_command(self, command_text: str) -> dict[str, str]:
        """Parse `/solace` command text into action and argument."""
        tokens = command_text.strip().split(maxsplit=1)
        action = tokens[0] if tokens else "help"
        argument = tokens[1] if len(tokens) > 1 else ""
        return {"action": action, "argument": argument}
