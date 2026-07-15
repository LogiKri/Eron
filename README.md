# Eron

A personal Telegram bot template built with [aiogram 3](https://docs.aiogram.dev/). Eron is meant to run on your
own machine and act as a private assistant: chat with an LLM, fetch files from your PC, launch applications, or
shut the machine down-all restricted to a single Telegram user (you).

## Features

-Language selection (English / Russian) on first start
-AI chat backed by [Groq](https://groq.com/) (swap in any provider you like in `app/modules/llm.py`)
-PC control: grab a file by full path, or search by (partial) name and pick the right one from a
  list of matches; launch applications; schedule/cancel shutdown
-Settings: custom AI role/persona, nickname, chat history view & reset
-Access restricted to a single Telegram user ID via middleware
-Built-in API key checker for OpenAI, Groq, Anthropic, Google, Cohere, Mistral, Perplexity, and DeepSeek
  (`app/modules/key_checker.py`)

## Getting started

```bash
git clone https://github.com/LogiKri/Eron.git
cd Eron
python -m venv .venv
source .venv/bin/activate   # .venv\Scripts\activate on Windows
pip install -r requirements.txt
cp .env.example .env
```

Fill in `.env`:

```
BOT_TOKEN=     # from @BotFather
USER_ID=       # your numeric Telegram user id, e.g. from @userinfobot
GROQ_TOKEN=    # optional, needed for the chat feature
SEARCH_ROOTS=  # optional, comma-separated folders to search for files, e.g. "C:\Users\you,D:\"
               # defaults to your home directory
```

Run it:

```bash
python -m app.main
```

## Project structure

```
app/
  main.py            entrypoint
  config.py           env var loading
  middleware/          owner-only access control
  handlers/            common, chat, pc_control, settings
  modules/              texts, keyboards, storage, llm, key_checker, files, device
  data/                 profiles.json (created at runtime, gitignored)
```

## Notes

-Storage is a single JSON file (`app/data/profiles.json`) — enough for a personal, single-user bot. Swap in
  SQLite/Postgres if you extend this into a multi-user project.
-The "PC control" features run real commands on the host (shutdown, launching binaries). Only enable/deploy this
  on a machine you own and trust, and keep `USER_ID` correct — the middleware is your only guard.
-The `key_checker` module is a standalone utility; wire it into a handler if you want to verify keys from Telegram.

