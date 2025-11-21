# 🔍 Telegram Lead Bot

<div align="center">

**Smart userbot for automatic search and filtering of car rental leads in Telegram channels**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Telethon](https://img.shields.io/badge/Telethon-1.28+-green.svg)](https://github.com/LonamiWebs/Telethon)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Configuration](#-configuration)

</div>

---

## 📖 Description

Telegram Lead Bot is a minimalistic userbot that automatically monitors multiple Telegram channels and forwards **ONLY** client requests for car rentals. The bot uses intelligent filtering with morphological analysis for accurate lead detection.

We built this bot to automate the search for potential clients in Telegram. The bot has the following capabilities:

- **Monitor multiple channels** simultaneously
- **Smart filtering** using morphological analysis (pymorphy3)
- **Filter only client requests** - blocks seller advertisements
- **Automatic caching** of channel IDs for fast startup
- **Spam protection** - filters banned topics

The bot is built as efficiently as possible. No complex settings - just add channels and run.

## ✨ Features

### Main Functions
- 🔍 **Automatic lead search** - real-time monitoring of multiple channels
- 🧠 **Smart filtering** - morphological analysis for accurate request detection
- 🎯 **Only client requests** - automatic blocking of seller advertisements
- 🚫 **Spam protection** - filters banned topics (drugs, scams, 18+)
- 📊 **Channel caching** - fast username to ID resolution
- 🔗 **Message links** - automatic link generation for found leads
- ⚡ **Asynchronous** - high performance thanks to async/await

### Filtering
- ✅ **Allows:** client requests for car rental ("need a car", "looking for car rental")
- ❌ **Blocks:** seller advertisements, job postings, taxis, real estate, spam

## 🚀 Installation

Telegram Lead Bot supports Python 3.8 and above.

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

This project depends on the following packages:

- `telethon` - library for working with Telegram API
- `pymorphy3` - morphological analyzer for Russian language
- `requests` - for sending messages via Bot API

### Step 2: Get API Credentials

#### Telegram API ID and API Hash:
1. Go to [my.telegram.org](https://my.telegram.org/)
2. Log in using your phone number
3. Go to "API development tools" section
4. Create a new application
5. Copy `api_id` and `api_hash`

#### Telegram Bot Token (optional):
1. Open [@BotFather](https://t.me/BotFather) in Telegram
2. Send command `/newbot`
3. Follow the instructions to create a bot
4. Copy the received token

#### User ID (for receiving leads):
1. Open [@userinfobot](https://t.me/userinfobot) in Telegram
2. Send command `/start`
3. Copy your User ID

### Step 3: Configuration

Open file `d.py` and configure the following parameters:

```python
API_ID = 12345678              # Your API ID
API_HASH = "your_api_hash"    # Your API Hash
BOT_TOKEN = "your_bot_token"  # Bot token (or "" if not using)
DEST_CHAT_ID = 123456789      # Your Telegram ID for receiving leads
```

### Step 4: Add Channels

Create file `all_channels.txt` and add channels (one per line):

```
@dubai_chat
@uae_rental
https://t.me/dubai_cars
```

Or use `channel_ids_cache.json` file for cached channel IDs (faster).

### Step 5: Run

```bash
python d.py
```

On first run, you will be asked to authorize via Telegram (enter phone number and confirmation code).

## 📝 Usage

### Main File (d.py)

The bot automatically:
1. Loads channel list from `all_channels.txt` or `channel_ids_cache.json`
2. Resolves usernames to IDs (if using username file)
3. Starts monitoring all specified channels
4. Filters messages by keywords
5. Forwards found leads to specified chat

### Example

**Input message in channel:**
```
Need a car for rent for a week. Who can help?
```

**Bot forwards:**
```
🔎 Found message in Dubai Chat:

Need a car for rent for a week. Who can help?

👉 Open message
```

### What Gets Filtered

**Allowed (client requests):**
- "Need a car for rent"
- "Looking for car rental"
- "Want to rent a car"
- "Where can I get a car?"

**Blocked (seller advertisements):**
- "Renting out a car"
- "We offer car rental"
- "We have cars in stock"
- Messages with phones/URLs

**Blocked (irrelevant):**
- Job postings ("Driver needed")
- Taxi/rideshare ("Going from Dubai")
- Real estate ("Studio for rent")
- Banned topics (drugs, scams, 18+)

## 📋 API Reference

### Configuration

All settings are at the beginning of `d.py` file:

```python
API_ID = 12345678                    # Telegram API ID
API_HASH = "your_api_hash"          # Telegram API Hash
SESSION_NAME = "userbot_session"    # Session file name
GROUPS_FILE = "all_channels.txt"    # File with channel list
BOT_TOKEN = "your_bot_token"        # Bot token (optional)
DEST_CHAT_ID = 123456789            # Chat ID for receiving leads
PROXIMITY_WINDOW = 3                # Distance between keywords
```

### Main Functions

#### `safe_lemma(word)`
Lemmatizes word for Russian language. Uses pymorphy3 for Cyrillic, otherwise returns lowercase.

**Example:**
```python
safe_lemma("машины")  # -> "машина"
safe_lemma("car")     # -> "car"
```

#### `extract_username(line)`
Extracts username from string (supports t.me links and regular usernames).

**Example:**
```python
extract_username("https://t.me/dubai_chat")  # -> "dubai_chat"
extract_username("@dubai_chat")              # -> "dubai_chat"
```

#### `has_proximity(lemmas, left_set, right_set, window)`
Checks if lemmas from two sets occur within distance <= window words.

**Example:**
```python
lemmas = ["нужна", "машина", "аренду"]
has_proximity(lemmas, CAR_LEMMAS, INTENT_LEMMAS, 3)  # -> True
```

### Keyword Dictionaries

The bot uses several dictionaries for filtering:

- `CAR_LEMMAS` - words related to cars
- `INTENT_LEMMAS` - client intent words ("need", "looking", "want")
- `OFFER_LEMMAS` - seller words ("renting", "offering", "price")
- `JOB_LEMMAS` - words related to job postings
- `TAXI_LEMMAS` - words related to taxi/rideshare
- `RENTAL_KEYWORDS` - rental keywords

## ⚙️ Configuration

### Changing Proximity Window

In `d.py` file:

```python
PROXIMITY_WINDOW = 3  # Distance (in words) between keywords
```

### Adding New Keywords

Edit corresponding dictionaries in `d.py`:

```python
RAW_CAR_LEMMAS = {
    "машина", "авто", "car",  # Add your words
    # ...
}
```

### Auto-saving Valid Channels

```python
AUTO_WRITE_CLEANED = True  # Automatically save valid usernames
CLEANED_USERNAMES_FILE = "active_channels_usernames.txt"
```

## 📁 Project Structure

```
telegram-lead-bot/
├── d.py                          # Main bot file
├── requirements.txt              # Python dependencies
├── README.md                     # Documentation
├── all_channels.txt              # List of channels to monitor
├── channel_ids_cache.json        # Channel ID cache (created automatically)
├── active_channels_usernames.txt # Valid usernames (created automatically)
└── userbot_session.session       # Session file (created on authorization)
```

## 🛠️ Technologies

- **Python 3.8+** - programming language
- **Telethon 1.28+** - library for Telegram API
- **pymorphy3 2.0+** - morphological analyzer for Russian language
- **requests** - for sending messages via Bot API

## 🔒 Security

- ✅ Session files (`.session`) are not committed to Git (added to `.gitignore`)
- ✅ API credentials are stored in code (can be moved to `.env`)
- ✅ It's recommended to keep session files secure
- ✅ Don't publish session files in public repositories

## 🐛 Troubleshooting

### Bot Won't Start
- Check API_ID and API_HASH correctness
- Make sure all dependencies are installed
- Check if `all_channels.txt` file exists

### Bot Not Finding Leads
- Check that channels are added to `all_channels.txt`
- Make sure bot has access to channels
- Check logs for errors

### Authorization Errors
- Delete `userbot_session.session` file and authorize again
- Check API_ID and API_HASH correctness

### Too Many/Few Messages
- Configure keyword dictionaries in `d.py`
- Change `PROXIMITY_WINDOW` for stricter/looser filtering

## 📊 Performance

- Bot can monitor hundreds of channels simultaneously
- Uses caching for fast username resolution
- Asynchronous message processing for high performance
- Morphological analysis with caching for fast operation

## 🤝 Contributing

Telegram Lead Bot is an open source project!

This project is constantly evolving, and we welcome any contribution or feedback.

**Open Tasks:**
- Adding support for other languages
- Improving filtering
- Adding web interface for management
- Performance optimization

If you want to contribute:

1. Fork the repository
2. Create a branch for new feature (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is created for educational purposes. Use at your own risk.

## ⭐ Acknowledgments

- [Telethon](https://github.com/LonamiWebs/Telethon) - excellent library for Telegram
- [pymorphy3](https://github.com/kmike/pymorphy3) - morphological analyzer for Russian language

---

<div align="center">

**Made with ❤️ using Python and Telethon**

⭐ If you liked the project, give it a star!

</div>
