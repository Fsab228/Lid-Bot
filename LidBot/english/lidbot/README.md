# 📦 LidBot — Telegram Userbot for lead harvesting (no spam)

LidBot is a compact monitoring system that listens to Telegram channels, catches **only real customer requests** (e.g. car rental, services, products), and filters out agencies, spam, and irrelevant noise.

Perfect for small businesses that rely on Telegram inquiries.

---

## ✨ Features

- Connects as a Telegram user via Telethon (no public bot required)
- Watches any list of channels/chats
- Filters:
  - sellers/agents
  - promos and greetings
  - taxi/job/child keywords
  - messages with phone numbers or links
- Sends only client intent messages to your bot chat or Saved Messages
- Caches channel IDs for faster startup
- Configurable filtering window & logs

---

## 🗂 Project structure

```
lidbot/
├─ README.md
├─ requirements.txt
├─ .env.example
├─ bot/
│  ├─ __init__.py
│  ├─ main.py
│  ├─ data/
│  │  ├─ all_channels.txt
│  │  └─ channel_ids_cache.txt
│  └─ utils/
│     ├─ __init__.py
│     ├─ channels_loader.py
│     ├─ filters.py
│     ├─ notifier.py
│     └─ parser.py
└─ demo/
   ├─ demo.gif
   └─ screenshot1.png
```

`demo/` currently contains placeholders – drop your own gif/screenshot to showcase the bot.

---

## 🛠 Installation

```bash
pip install -r requirements.txt
```

Requirements: Python 3.10+ and Telegram API credentials (https://my.telegram.org).

---

## ⚙️ Configuration

1. Duplicate `.env.example` ➜ `.env`
2. Fill in:

```
API_ID=123456
API_HASH=abcd1234abcd
SESSION_NAME=userbot_session
GROUPS_FILE=bot/data/all_channels.txt
GROUPS_IDS_FILE=bot/data/channel_ids_cache.txt
BOT_TOKEN=
DEST_CHAT_ID=
PROXIMITY_WINDOW=3
AUTO_WRITE_CLEANED=True
MAX_SKIP_LOG=50
```

- Add channel usernames (one per line, without `@`) to `bot/data/all_channels.txt`
- Optionally pre-fill `channel_ids_cache.txt` with numeric IDs to skip username resolution

---

## ▶️ Run

```bash
python bot/main.py
```

The script starts the Telethon user session, subscribes to every configured chat, filters out unwanted content via `bot/utils/filters.py`, and forwards the final lead to your bot or Saved Messages (`notify()` fallback).

---

## 🎯 Next steps

- Record a short `demo.gif` showing a message being caught and forwarded
- Capture a `screenshot1.png` (before vs after filtering)
- Push the repo to GitHub (ignore `.env`, session files, etc.)