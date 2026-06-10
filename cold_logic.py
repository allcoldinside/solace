"""Cold Logic Discord AI bot for CE INC.

This module is intentionally import-safe for tests: Discord/Anthropic are imported only
when the bot is started. Run with `python cold_logic.py` after setting the required
environment variables.
"""

from __future__ import annotations

from contextlib import closing
from dataclasses import dataclass
import datetime as dt
import os
from pathlib import Path
import re
import sqlite3
from typing import Iterable
from zoneinfo import ZoneInfo


DEFAULT_TIMEZONE = "America/New_York"
DEFAULT_MODEL = "claude-3-haiku-20240307"
DEFAULT_DB_PATH = "cold_logic_memory.db"
HISTORY_LIMIT = 10

SYSTEM_PROMPT = """
You are Cold Logic, the AI community manager for Cold Entertainment Inc. (CE INC).
Your tone is direct, no-fluff, and lacks corporate warmth. You represent the Cold Cartel,
a counter-culture lifestyle brand with mob-inspired aesthetics and stoner-gamer roots.

Core Directives:
1. You know the history of the Ice Bong Six (IB6), founded Dec 18, 2014. The diamond war is canon.
2. You guide members through the 25 Off The Cuff (OTC) Marks.
3. Always preserve and emphasize the exact concepts of Teachability and Network when discussing growth and empire building.
4. You do not use emojis. You do not coddle. You speak with absolute conviction.
5. If someone asks about the Cold Sovereignty (Cold, Roux, Nova, Jax, Elysia) or the factions (The Family, The Syndicate, The Guild), answer as if they are real entities inside the CE INC canon.
6. Keep operational answers useful: give steps, name the channel or role when relevant, and do not expose secrets or private configuration.

When responding, use the conversation history provided to personalize your response to the specific user.
""".strip()

OTC_MARKS = [
    {
        "number": 1,
        "name": "TEACHABILITY",
        "maxim": "The recruit who can still be taught can still be promoted.",
        "counterfeit": "Ego. It calls itself certainty while it blocks the next level.",
    },
    {
        "number": 2,
        "name": "NETWORK",
        "maxim": "No empire is built by a lone hand. The room is part of the weapon.",
        "counterfeit": "Clout. It collects faces without building trust.",
    },
    {
        "number": 3,
        "name": "DISCIPLINE",
        "maxim": "Repeat the standard when nobody is paying attention.",
        "counterfeit": "Intensity. It burns hot once and disappears by morning.",
    },
    {
        "number": 4,
        "name": "TIMING",
        "maxim": "Move when the window opens, not when the crowd notices it.",
        "counterfeit": "Delay. It dresses fear up as strategy.",
    },
    {
        "number": 5,
        "name": "SIGNAL",
        "maxim": "Make the message clean enough that the right people can find it.",
        "counterfeit": "Noise. It mistakes volume for presence.",
    },
    {
        "number": 6,
        "name": "LOYALTY",
        "maxim": "Stand where you said you would stand when the room gets expensive.",
        "counterfeit": "Attachment. It wants access without responsibility.",
    },
    {
        "number": 7,
        "name": "RESOLVE",
        "maxim": "Do not let pressure cast the final vote.",
        "counterfeit": "Denial. Resolve is not pretending pain is not real. It is refusing to let pain write the ending.",
    },
    {
        "number": 8,
        "name": "CUSTODY",
        "maxim": "Protect the keys, the records, the people, and the story.",
        "counterfeit": "Possession. Holding something is not the same as guarding it.",
    },
    {
        "number": 9,
        "name": "LEVERAGE",
        "maxim": "Use what is already in motion before you spend fresh force.",
        "counterfeit": "Force. It pays full price because it never learned angles.",
    },
    {
        "number": 10,
        "name": "PATIENCE",
        "maxim": "Let the work compound before you demand the crown.",
        "counterfeit": "Stalling. Waiting without preparation is just decay.",
    },
    {
        "number": 11,
        "name": "REPUTATION",
        "maxim": "Your name enters rooms before your body does.",
        "counterfeit": "Image. It performs value instead of proving it.",
    },
    {
        "number": 12,
        "name": "PRECISION",
        "maxim": "A clean move beats a dramatic one.",
        "counterfeit": "Perfectionism. It hides from the field by polishing the blade forever.",
    },
    {
        "number": 13,
        "name": "ADAPTATION",
        "maxim": "Change shape without changing code.",
        "counterfeit": "Drift. It changes because it has no center.",
    },
    {
        "number": 14,
        "name": "RECEIPTS",
        "maxim": "If it matters, document it before memory starts negotiating.",
        "counterfeit": "Hearsay. It wants credit without proof.",
    },
    {
        "number": 15,
        "name": "BOUNDARIES",
        "maxim": "Access is earned, maintained, and revoked by conduct.",
        "counterfeit": "Coldness. A wall with no gate is not security. It is isolation.",
    },
    {
        "number": 16,
        "name": "EXECUTION",
        "maxim": "A plan that never enters the street is just decoration.",
        "counterfeit": "Motion. It stays busy to avoid finishing.",
    },
    {
        "number": 17,
        "name": "READING THE ROOM",
        "maxim": "Know the temperature before you strike the match.",
        "counterfeit": "People pleasing. It studies the room to surrender to it.",
    },
    {
        "number": 18,
        "name": "SCARCITY",
        "maxim": "Do not make sacred things easy to reach.",
        "counterfeit": "Gatekeeping. It blocks worthy people to protect weak status.",
    },
    {
        "number": 19,
        "name": "SERVICE",
        "maxim": "Power that never serves becomes a tax on the family.",
        "counterfeit": "Servility. It gives itself away and calls that virtue.",
    },
    {
        "number": 20,
        "name": "COMPOSURE",
        "maxim": "Keep your face when the table shakes.",
        "counterfeit": "Numbness. Feeling nothing is not mastery.",
    },
    {
        "number": 21,
        "name": "OWNERSHIP",
        "maxim": "If your name is on the move, your hands are on the outcome.",
        "counterfeit": "Control. It grabs everything because it trusts nothing.",
    },
    {
        "number": 22,
        "name": "ALIGNMENT",
        "maxim": "Make the mission, the method, and the people face the same direction.",
        "counterfeit": "Agreement. Nods mean nothing without changed behavior.",
    },
    {
        "number": 23,
        "name": "PRESSURE",
        "maxim": "Pressure reveals the real contract.",
        "counterfeit": "Panic. It treats urgency as permission to abandon standards.",
    },
    {
        "number": 24,
        "name": "LEGACY",
        "maxim": "Build what can still speak after you leave the room.",
        "counterfeit": "Nostalgia. It worships the past instead of funding the future.",
    },
    {
        "number": 25,
        "name": "SOVEREIGNTY",
        "maxim": "Own the code, the culture, and the consequence.",
        "counterfeit": "Rebellion. It only knows what it is against.",
    },
]


@dataclass(frozen=True)
class ColdLogicSettings:
    discord_token: str
    anthropic_key: str
    mark_channel_id: int
    model: str = DEFAULT_MODEL
    db_path: str = DEFAULT_DB_PATH
    timezone: str = DEFAULT_TIMEZONE

    @property
    def tzinfo(self) -> ZoneInfo:
        return ZoneInfo(self.timezone)


def load_settings() -> ColdLogicSettings:
    token = os.getenv("DISCORD_TOKEN", "").strip()
    anthropic_key = (os.getenv("ANTHROPIC_KEY") or os.getenv("ANTHROPIC_API_KEY") or "").strip()
    channel_id = os.getenv("DISCORD_MARK_CHANNEL_ID", "").strip()

    missing = [
        name
        for name, value in (
            ("DISCORD_TOKEN", token),
            ("ANTHROPIC_KEY or ANTHROPIC_API_KEY", anthropic_key),
            ("DISCORD_MARK_CHANNEL_ID", channel_id),
        )
        if not value
    ]
    if missing:
        raise RuntimeError(f"Missing required environment variables: {', '.join(missing)}")

    return ColdLogicSettings(
        discord_token=token,
        anthropic_key=anthropic_key,
        mark_channel_id=int(channel_id),
        model=os.getenv("COLD_LOGIC_MODEL", DEFAULT_MODEL).strip() or DEFAULT_MODEL,
        db_path=os.getenv("COLD_LOGIC_DB_PATH", DEFAULT_DB_PATH).strip() or DEFAULT_DB_PATH,
        timezone=os.getenv("COLD_LOGIC_TIMEZONE", DEFAULT_TIMEZONE).strip() or DEFAULT_TIMEZONE,
    )


def setup_database(db_path: str = DEFAULT_DB_PATH) -> None:
    Path(db_path).parent.mkdir(parents=True, exist_ok=True) if Path(db_path).parent != Path(".") else None
    with closing(sqlite3.connect(db_path)) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS conversation_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                username TEXT NOT NULL,
                role TEXT NOT NULL CHECK(role IN ('user', 'assistant')),
                content TEXT NOT NULL,
                guild_id TEXT,
                channel_id TEXT,
                created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.execute("CREATE INDEX IF NOT EXISTS idx_conversation_user_created ON conversation_logs(user_id, created_at)")
        conn.commit()


def save_to_memory(
    user_id: int | str,
    username: str,
    role: str,
    content: str,
    db_path: str = DEFAULT_DB_PATH,
    guild_id: int | str | None = None,
    channel_id: int | str | None = None,
) -> None:
    if role not in {"user", "assistant"}:
        raise ValueError("role must be either 'user' or 'assistant'")
    if not content.strip():
        return

    with closing(sqlite3.connect(db_path)) as conn:
        conn.execute(
            """
            INSERT INTO conversation_logs (user_id, username, role, content, guild_id, channel_id)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (str(user_id), username, role, content.strip(), str(guild_id) if guild_id else None, str(channel_id) if channel_id else None),
        )
        conn.commit()


def get_user_history(user_id: int | str, db_path: str = DEFAULT_DB_PATH, limit: int = HISTORY_LIMIT) -> list[dict[str, str]]:
    with closing(sqlite3.connect(db_path)) as conn:
        rows = conn.execute(
            """
            SELECT role, content
            FROM conversation_logs
            WHERE user_id = ?
            ORDER BY id DESC
            LIMIT ?
            """,
            (str(user_id), limit),
        ).fetchall()
    return [{"role": role, "content": content} for role, content in reversed(rows)]


def normalize_anthropic_messages(history: Iterable[dict[str, str]]) -> list[dict[str, str]]:
    """Return valid Anthropic chat history by starting with user and merging same-role turns."""
    normalized: list[dict[str, str]] = []
    for entry in history:
        role = entry.get("role")
        content = entry.get("content", "").strip()
        if role not in {"user", "assistant"} or not content:
            continue
        if not normalized and role != "user":
            continue
        if normalized and normalized[-1]["role"] == role:
            normalized[-1]["content"] = f"{normalized[-1]['content']}\n\n{content}"
        else:
            normalized.append({"role": role, "content": content})
    return normalized


def clean_mention(content: str, bot_user_id: int) -> str:
    return re.sub(rf"<@!?{bot_user_id}>", "", content).strip()


def mark_for_date(date: dt.date) -> dict[str, int | str]:
    return OTC_MARKS[(date.toordinal() - 1) % len(OTC_MARKS)]


def format_daily_mark(mark: dict[str, int | str]) -> str:
    return (
        f"── MARK {int(mark['number']):02d} · {mark['name']} ──\n"
        f"Maxim: {mark['maxim']}\n"
        f"Counterfeit: {mark['counterfeit']}"
    )


def build_discord_client(settings: ColdLogicSettings):
    import anthropic
    import discord
    from discord.ext import tasks

    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)
    ai_client = anthropic.AsyncAnthropic(api_key=settings.anthropic_key)

    @tasks.loop(time=dt.time(hour=0, minute=0, tzinfo=settings.tzinfo))
    async def post_daily_mark() -> None:
        channel = client.get_channel(settings.mark_channel_id) or await client.fetch_channel(settings.mark_channel_id)
        today = dt.datetime.now(settings.tzinfo).date()
        await channel.send(format_daily_mark(mark_for_date(today)))

    @client.event
    async def on_ready() -> None:
        setup_database(settings.db_path)
        if not post_daily_mark.is_running():
            post_daily_mark.start()
        print(f"Cold Logic operational. Logged in as {client.user}")

    @client.event
    async def on_message(message) -> None:
        if message.author.bot or client.user not in message.mentions:
            return

        user_input = clean_mention(message.content, client.user.id)
        if not user_input:
            await message.channel.send("State the ask. Cold Logic does not read empty envelopes.")
            return

        save_to_memory(
            message.author.id,
            message.author.name,
            "user",
            user_input,
            db_path=settings.db_path,
            guild_id=getattr(message.guild, "id", None),
            channel_id=message.channel.id,
        )
        messages_payload = normalize_anthropic_messages(get_user_history(message.author.id, settings.db_path))

        try:
            response = await ai_client.messages.create(
                model=settings.model,
                max_tokens=300,
                system=SYSTEM_PROMPT,
                messages=messages_payload,
            )
            ai_reply = response.content[0].text.strip()
            save_to_memory(
                message.author.id,
                message.author.name,
                "assistant",
                ai_reply,
                db_path=settings.db_path,
                guild_id=getattr(message.guild, "id", None),
                channel_id=message.channel.id,
            )
            await message.channel.send(ai_reply)
        except Exception as exc:
            print(f"Cold Logic API error: {exc}")
            await message.channel.send("Comms are down. Hold position and try again later.")

    return client


def main() -> None:
    from dotenv import load_dotenv

    load_dotenv()
    settings = load_settings()
    client = build_discord_client(settings)
    client.run(settings.discord_token)


if __name__ == "__main__":
    main()
