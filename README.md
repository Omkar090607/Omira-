# OMIRA — Personal AI Assistant for Windows 🤖

OMIRA is a Windows-based AI personal assistant that lets you control your computer and perform everyday tasks using natural voice commands.

## ✨ Features

* 🎙️ **Voice Assistant** — Hands-free voice interaction with English, Hindi, and Marathi support.
* 🤖 **AI Q&A** — Answers general questions using Gemini, with OpenAI/Ollama fallback support.
* 🖥️ **Windows Control** — Control volume, brightness, screenshots, battery status, system information, lock, sleep, restart, and shutdown.
* 🌐 **Apps & Websites** — Open and close supported applications and websites using voice commands.
* 📧 **Email Assistant** — Check, read, send, and reply to emails using Gmail.
* 💬 **WhatsApp Messaging** — Send messages using saved contacts or phone numbers with confirmation.
* 📄 **Document Summarizer** — Find and summarize documents from Desktop, Documents, and Downloads.
* 🌐 **Website Generator** — Generate and open complete HTML websites using voice commands.
* 🎵 **Music Assistant** — Play songs from the local library or search YouTube.
* 🖥️ **Desktop Mode** — Run OMIRA from the Windows system tray with Start, Stop, and Quit controls.
* 🔌 **Status Bridge** — Optional local WebSocket interface for OMIRA's live status.

## 🛠️ Tech Stack

**Python 3.11+ • FastAPI • Gemini API • OpenAI API • Ollama • HTML/CSS/JavaScript • WebSockets**

## 🚀 Installation

```bash
git clone YOUR_REPOSITORY_URL
cd OMIRA
pip install -r requirements.txt
```

Create `.env` from `.env.example` and add your API credentials.

Run:

```bash
python new_omira.py
```

Or run the desktop system-tray version:

```bash
python omira_app.py
```

## 🔐 Security

Keep API keys and email credentials inside `.env`. **Never commit `.env` to GitHub.**

## 🎯 Project

OMIRA combines **voice recognition + AI + Windows automation** to create a practical personal computer assistant.

**Built with Python for Windows 10/11.**
