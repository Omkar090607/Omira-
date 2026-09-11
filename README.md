# OMIRA — Personal AI Assistant for Windows

OMIRA is a Windows-based AI personal assistant built with Python that enables users to control their computer and perform everyday tasks using natural voice commands.

It combines voice interaction, AI models, Windows automation, API integrations, document processing, and system controls into a single desktop assistant.

## Features

### Voice Interaction

* Natural voice-based interaction
* Supports English, Hindi, and Marathi
* Hands-free computer interaction through voice commands

### AI and Intelligent Assistance

* General question answering using the Gemini API
* OpenAI API and Ollama support as alternative AI providers
* AI-powered document summarization
* AI-assisted task execution

### Windows System Control

OMIRA can perform various Windows system operations through voice commands, including:

* Volume control
* Brightness control
* Screenshot capture
* Battery status
* System information
* Lock system
* Sleep
* Restart
* Shutdown

### Applications and Websites

* Launch supported Windows applications
* Close supported applications
* Open websites through voice commands
* Automate frequently used computer tasks

### Email Assistant

Gmail integration allows OMIRA to:

* Check emails
* Read emails
* Send emails
* Reply to emails

### WhatsApp Messaging

* Send WhatsApp messages using saved contacts or phone numbers
* Confirmation-based messaging to reduce accidental sends

### Document Summarization

* Search for documents in Desktop, Documents, and Downloads
* Process supported documents
* Generate AI-powered summaries

### Website Generator

* Generate complete HTML websites using voice commands
* Automatically create and open generated websites

### Music Assistant

* Play songs from the local music library
* Search for music on YouTube

### Desktop System Tray Mode

OMIRA can run in the Windows system tray with controls for:

* Start
* Stop
* Quit

### Status Bridge

* Optional local WebSocket-based status interface
* Provides real-time status information from OMIRA

## Technology Stack

| Category             | Technologies                   |
| -------------------- | ------------------------------ |
| Programming Language | Python 3.11+                   |
| Backend / API        | FastAPI                        |
| AI                   | Gemini API, OpenAI API, Ollama |
| Web Technologies     | HTML, CSS, JavaScript          |
| Communication        | WebSockets                     |
| Platform             | Windows 10/11                  |

## Architecture

OMIRA processes voice commands and routes them to the appropriate service or system operation.

```text
Voice Input
     |
     v
Command Processing
     |
     v
Intent / Task Detection
     |
     +-------------------+-------------------+
     |                   |                   |
     v                   v                   v
AI Assistance      Windows Control     External APIs
     |                   |                   |
     +-------------------+-------------------+
                         |
                         v
                    Task Execution
                         |
                         v
                  Application Response
```

## Installation

### 1. Clone the Repository

```bash
git clone YOUR_REPOSITORY_URL
cd OMIRA
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file based on `.env.example` and add the required API credentials.

Example:

```env
GEMINI_API_KEY=your_api_key
OPENAI_API_KEY=your_api_key
```

Do not commit `.env` or expose API credentials publicly.

### 4. Run OMIRA

Run the main application:

```bash
python new_omira.py
```

To run the desktop system-tray version:

```bash
python omira_app.py
```

## Security

OMIRA may require API keys and credentials for external services.

Follow these practices:

* Store credentials in `.env`
* Never hard-code API keys in source code
* Never commit `.env` to GitHub
* Use `.env.example` to document required environment variables
* Review permissions before enabling external integrations

Add the following to `.gitignore`:

```gitignore
.env
__pycache__/
*.pyc
```

## Project Structure

A typical project structure can be organized as:

```text
OMIRA/
│
├── new_omira.py
├── omira_app.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
│
├── assets/
├── modules/
└── ...
```

Update this structure to match the actual repository.

## Core Technical Concepts

OMIRA demonstrates practical implementation of:

* Python application development
* Artificial Intelligence and Generative AI integration
* Voice-based interaction
* REST API integration
* Windows automation
* Gmail integration
* WhatsApp messaging automation
* AI-powered document processing
* Website generation
* WebSocket communication
* Desktop application development
* Environment-based configuration
* External API integration

## Future Improvements

Potential areas for future development include:

* Improved natural-language command understanding
* Additional Windows application integrations
* Additional AI model providers
* Enhanced conversation memory
* Improved error handling and recovery
* Advanced security controls
* Cross-platform support
* Containerized deployment for supported components

## Project Status

**Active Development**

OMIRA is an evolving personal AI assistant focused on exploring the integration of AI, voice interaction, automation, APIs, and desktop application development.

## Author

**Omkar Awaze**

Computer Technology Student | Full-Stack Developer

Email: [omkarawaze1915@gmail.com](mailto:omkarawaze1915@gmail.com)

## License

Add an appropriate license to the repository if you intend to make the project open source.

---

Built with Python for Windows 10/11.
