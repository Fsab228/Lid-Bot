# -*- coding: utf-8 -*-
"""
Minimalistic userbot: forwards ONLY inbound car rental requests from clients.

This version follows a portfolio-friendly structure with dedicated utils modules.
"""

import asyncio
import os
import sys
from pathlib import Path
from typing import Optional

from telethon import TelegramClient, events

if __name__ == "__main__" and __package__ is None:  # pragma: no cover
    CURRENT_DIR = Path(__file__).resolve().parent
    sys.path.append(str(CURRENT_DIR.parent))
    __package__ = "bot"

from .utils.channels_loader import load_target_chats  # type: ignore[import]
from .utils.filters import passes_filters  # type: ignore[import]
from .utils.notifier import notify  # type: ignore[import]
from .utils.parser import build_notification, extract_text, resolve_chat_meta  # type: ignore[import]

# ---------------- CONFIG ----------------
BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "bot" / "data"


def env_path(name: str, default: Path) -> Path:
    return Path(os.getenv(name, str(default))).expanduser().resolve()


def env_int(name: str, default: Optional[int] = None) -> Optional[int]:
    raw = os.getenv(name)
    if raw is None:
        return default
    try:
        return int(raw)
    except ValueError as exc:
        raise RuntimeError(f"Environment variable {name} must be an integer") from exc


def env_bool(name: str, default: bool) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


API_ID = env_int("API_ID")
API_HASH = os.getenv("API_HASH")
SESSION_NAME = os.getenv("SESSION_NAME", "userbot_session")

GROUPS_FILE = env_path("GROUPS_FILE", DATA_DIR / "all_channels.txt")
GROUPS_IDS_FILE = env_path("GROUPS_IDS_FILE", DATA_DIR / "channel_ids_cache.txt")

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
DEST_CHAT_ID = env_int("DEST_CHAT_ID") or 0

PROXIMITY_WINDOW = int(os.getenv("PROXIMITY_WINDOW", 3))

# Auto-saving the filtered set of valid usernames
AUTO_WRITE_CLEANED = env_bool("AUTO_WRITE_CLEANED", True)
CLEANED_USERNAMES_FILE = env_path(
    "CLEANED_USERNAMES_FILE", DATA_DIR / "active_channels_usernames.txt"
)
MAX_SKIP_LOG = int(os.getenv("MAX_SKIP_LOG", 50))
# ----------------------------------------

if API_ID is None or not API_HASH:
    raise RuntimeError("API_ID and API_HASH must be provided via environment variables.")


async def main():
    client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
    await client.start()

    print("=" * 70)
    print("🤖 LidBot: forwarding only client car-rental requests")
    print("=" * 70)

    chats, logs = await load_target_chats(
        client=client,
        groups_file=GROUPS_FILE,
        groups_ids_file=GROUPS_IDS_FILE,
        cleaned_usernames_file=CLEANED_USERNAMES_FILE,
        auto_write_cleaned=AUTO_WRITE_CLEANED,
        max_skip_log=MAX_SKIP_LOG,
    )
    for line in logs:
        print(line)
    if not chats:
        return

    async def message_handler(event):
        try:
            text = extract_text(event)
            if not text or not passes_filters(text, PROXIMITY_WINDOW):
                return

            title, link = await resolve_chat_meta(event)
            send_text = build_notification(title, text, link)
            await notify(client, send_text, BOT_TOKEN, DEST_CHAT_ID)
            print("Forwarded lead from:", title)

        except Exception as exc:
            print("Handler error:", exc)

    client.add_event_handler(message_handler, events.NewMessage(chats=chats))
    print("👂 Userbot is running...")
    await client.run_until_disconnected()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Stopped via Ctrl-C")
    except Exception as exc:
        print("Fatal error in main():", exc)

