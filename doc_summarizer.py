"""
doc_summarizer.py — "summarize <document>" for Omira.

Resolves a spoken filename to an actual file on disk (fuzzy match across
common folders), extracts its text (.txt, .docx, .pdf), and summarizes it
using Omira's existing AI backend (pass in your ask_ai function — no new
API wiring needed).

Setup:
    pip install pypdf   # docx already in requirements.txt via python-docx
"""

import difflib
import os
from pathlib import Path

try:
    from docx import Document as DocxDocument
except ImportError:
    DocxDocument = None

try:
    from pypdf import PdfReader
except ImportError:
    PdfReader = None


def _search_folders():
    home = Path(os.path.expanduser("~"))
    candidates = [
        home / "OneDrive" / "Desktop", home / "Desktop",
        home / "OneDrive" / "Documents", home / "Documents",
        home / "Downloads",
    ]
    return [p for p in candidates if p.exists()]


SUPPORTED_EXT = {".txt", ".docx", ".pdf", ".md"}


def find_document(spoken_name, max_depth=2):
    """Fuzzy-match a spoken filename against files in common folders.
    Returns a Path or None. Searches shallowly (max_depth) to stay fast."""
    spoken_name = spoken_name.lower().strip()
    candidates = []

    for folder in _search_folders():
        for root, dirs, files in os.walk(folder):
            depth = len(Path(root).relative_to(folder).parts)
            if depth >= max_depth:
                dirs[:] = []
            for fname in files:
                ext = Path(fname).suffix.lower()
                if ext in SUPPORTED_EXT:
                    candidates.append(Path(root) / fname)

    if not candidates:
        return None

    names = [c.stem.lower() for c in candidates]
    matches = difflib.get_close_matches(spoken_name, names, n=1, cutoff=0.4)
    if matches:
        idx = names.index(matches[0])
        return candidates[idx]

    # fallback: substring match
    for c in candidates:
        if spoken_name in c.stem.lower():
            return c
    return None


def extract_text(path, max_chars=6000):
    path = Path(path)
    ext = path.suffix.lower()

    if ext in {".txt", ".md"}:
        return path.read_text(encoding="utf-8", errors="ignore")[:max_chars]

    if ext == ".docx":
        if DocxDocument is None:
            raise RuntimeError("python-docx not installed")
        doc = DocxDocument(str(path))
        text = "\n".join(p.text for p in doc.paragraphs if p.text.strip())
        return text[:max_chars]

    if ext == ".pdf":
        if PdfReader is None:
            raise RuntimeError("pypdf not installed — pip install pypdf")
        reader = PdfReader(str(path))
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
            if len(text) >= max_chars:
                break
        return text[:max_chars]

    raise RuntimeError(f"Unsupported file type: {ext}")


def summarize_document(spoken_name, ask_ai_fn, omira_persona="You are Omira, a helpful assistant."):
    """High-level entry point. ask_ai_fn should be Omira's existing
    ask_ai(system_prompt, user_prompt, max_tokens) function.

    Returns a spoken-ready summary string, or an explanation of what went
    wrong (never silently fails).
    """
    path = find_document(spoken_name)
    if path is None:
        return f"I could not find a document matching '{spoken_name}' in your Desktop, Documents, or Downloads."

    try:
        text = extract_text(path)
    except Exception as exc:
        return f"I found {path.name} but could not read it: {exc}"

    if not text.strip():
        return f"I found {path.name} but it appears to be empty or unreadable."

    system_prompt = (
        omira_persona + " Summarize the given document in 3-4 clear sentences, "
        "covering its main points. Plain prose, no markdown, no preamble."
    )
    summary = ask_ai_fn(system_prompt, text, 300)
    if not summary:
        return f"I found {path.name} but could not reach an AI model to summarize it."

    return f"Here's a summary of {path.name}: {summary.strip()}"
