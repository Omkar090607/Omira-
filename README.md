# Omira

**Instagram messaging and Amazon shopping are intentionally removed from
this build.** They relied on browser/screen automation I could not get
fully verified working end-to-end before the submission deadline, and
this build only includes what's actually solid. See "What was removed"
below for full honesty on that.

WhatsApp messaging **is** included, but only by contact name (not
search-and-send) — see "What's included" below.

## Setup
1. Put all these files in one folder.
2. `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and fill in your own keys —
   `GEMINI_API_KEY` and/or `OPENAI_API_KEY`. Fill in `OMIRA_EMAIL_ADDRESS`
   / `OMIRA_EMAIL_PASSWORD` (a Gmail **App Password**, not your real
   password) if you want email features. Never share or commit your real
   `.env`.
4. `python new_omira.py`

## What's included
- **Voice control, hands-free, no wake word** — just speak, Omira acts.
- **General Q&A** via Gemini (or OpenAI/Ollama as fallback) — "what is
  artificial intelligence", open-ended questions.
- **Apps & websites** — "open Chrome", "open Google", "open YouTube",
  "close Notepad".
- **System controls** — volume, brightness, screenshot, lock, sleep,
  shutdown/restart (asks to confirm first), battery status, system info.
- **Email** — check, read, reply, send (needs Gmail App Password in
  `.env`).
- **WhatsApp — send by contact name** — "send hello to Aditya on
  whatsapp". Looks the name up in `contacts.json` (case-insensitive,
  exact match), or you can just say a phone number directly. Omira asks
  you to say "confirm" before actually sending, so a misheard command
  can't fire a message off by accident. Uses `pywhatkit`, which opens
  `web.whatsapp.com` in your default browser (must already be logged
  in) and sends from there — no pixel-coordinate clicking involved.
  Add contacts by editing `contacts.json`:
  `{"Name": "+countrycodenumber"}`.
- **Document summarizing** — "summarize the budget report" finds the
  file in Desktop/Documents/Downloads and reads back a summary.
- **Website generation** — "build a website for a bakery called Sweet
  Crumbs" generates and opens a real HTML site.
- **Music** — "play shape of you" — local library first, YouTube search
  fallback.
- **Multilingual voice** — English, Hindi, Marathi in one neural voice.
- **Optional orb status UI** — a local-only WebSocket feed
  (`status_bridge.py`) other Omira frontends can connect to, if you have
  one; entirely optional, everything above works without it.

## What was removed, and why
- **Instagram messaging** — used the older screen-pixel-coordinate
  clicking approach, which is exactly the kind of fragile, unverified
  automation this cleanup was meant to remove.
- **Amazon shopping (search/cart/checkout)** — logic was written and
  reasoned through, never confirmed by a completed real run.
- **WhatsApp search-and-send by typed name (no contacts.json)** — the
  old pixel-coordinate-clicking version of this (searching WhatsApp Web's
  UI directly) is gone for the same reason as Instagram. Sending to a
  name already saved in `contacts.json` is a much simpler, more reliable
  path — no clicking, just opening a chat directly by phone number — so
  that one stayed and is now wired up (see "What's included" above).

If you say a command like "message Mummy on instagram" or "buy
headphones", Omira now replies "isn't included in this build, sir"
instead of attempting it — so a demo can't hang or silently do nothing.
Saying "send hello to Mummy on whatsapp" works, as long as "Mummy" is a
name in `contacts.json`.

## Quiet terminal
The console prints nothing by default — only "Hello sir." is spoken at
startup, then Omira listens silently. Set `OMIRA_VERBOSE=1` in `.env`
any time you want diagnostic output back.

## About the Gemini 429 errors
Two things combine to exhaust Gemini's free daily quota fast:
1. **Model aliases.** `gemini-flash-latest` can silently point at a newer
   preview model with a much smaller quota than the stable release. This
   is pinned to `gemini-2.5-flash` by default (`OMIRA_GEMINI_MODEL` in
   `.env`).
2. **Hands-free mode has no wake word**, so background noise or a
   half-heard word can cost a Gemini request. Omira ignores short,
   ambiguous input instead of spending a request on it, and pauses
   Gemini calls for 90 seconds after a 429 instead of retrying
   immediately (`OMIRA_GEMINI_COOLDOWN_SECONDS`).

For guaranteed accessibility even after Gemini's quota is used up, set
`OPENAI_API_KEY` **or** run [Ollama](https://ollama.com) locally
(`ollama pull llama3.1` then `ollama serve`) — Omira automatically falls
over to whichever is configured.

## Orb UI integration (optional)
Omira can optionally broadcast its live state (idle / listening /
processing / responding / error) over a **one-way, read-only** local
WebSocket (`status_bridge.py`, bound to `127.0.0.1` only — not reachable
from your network). If `websockets` isn't installed or no frontend is
running, Omira works completely normally regardless.

## Running as a desktop app instead of a terminal script
`omira_app.py` wraps Omira in a system-tray icon (Start/Stop/Quit)
instead of a console window. Run `python omira_app.py` instead of
`python new_omira.py`.

## Files
- `new_omira.py` — the assistant core (`main()` — run directly, or via
  `omira_app.py`)
- `omira_app.py` — system-tray desktop wrapper around `new_omira.py`
- `doc_summarizer.py` — finds and summarizes a file by spoken name
- `site_generator.py` — generates a self-contained HTML business website
- `musiclibrary.py` — song name -> YouTube link lookup
- `contacts.json` — kept for future contact-lookup use; not required for
  anything in this build
- `status_bridge.py` — optional local WebSocket status feed for an orb
  UI, if you have one
- `requirements.txt` — `pip install -r requirements.txt`
- `.env.example` — copy to `.env` and fill in your own keys (never share
  or commit `.env`)
- `.gitignore` — keeps `.env` out of git if you push this to GitHub
