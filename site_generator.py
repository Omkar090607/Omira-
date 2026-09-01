"""
site_generator.py — "generate a website for a bakery" for Omira.

Mirrors new_omira.py's existing create_document() pattern: one AI call
produces the content/structure, this saves it to disk and opens it in the
browser. Output is a single self-contained HTML file (inline CSS/JS) so
there's nothing to configure or serve — double-click and it works.
"""

import os
import re
import webbrowser
from datetime import datetime
from pathlib import Path


def _output_folder():
    desktop = Path(os.path.expanduser("~")) / "OneDrive" / "Desktop"
    if not desktop.exists():
        desktop = Path(os.path.expanduser("~")) / "Desktop"
    folder = desktop / "Omira Websites"
    folder.mkdir(exist_ok=True)
    return folder


def generate_website(business_description, ask_ai_fn, omira_persona="You are Omira, a helpful assistant.",
                      speak_fn=None):
    """business_description e.g. 'a bakery called Sweet Crumbs' or
    'a plumbing business'. ask_ai_fn is Omira's existing ask_ai(). Returns
    the path to the saved .html file, or None on failure (and speaks why,
    if speak_fn is given)."""

    def _say(msg):
        if speak_fn:
            speak_fn(msg)

    _say(f"Building a website for {business_description}, sir. One moment.")

    system_prompt = (
        omira_persona + " You are a web designer. Produce ONE complete, "
        "self-contained HTML file for the described small business: inline "
        "<style> for CSS (clean, modern, mobile-responsive, tasteful color "
        "palette fitting the business type — no generic bootstrap look), a "
        "hero section with business name and tagline, an about/story "
        "section, a products/services section with 3-6 plausible sample "
        "items, a contact section with a simple non-functional contact "
        "form, and a footer. No external dependencies, no images (use CSS "
        "shapes/gradients/emoji instead), no placeholder lorem ipsum — "
        "write real plausible copy for this business. "
        "Output ONLY the raw HTML starting with <!DOCTYPE html>, nothing else."
    )

    html = ask_ai_fn(system_prompt, f"Business: {business_description}", 4000)
    if not html:
        _say("I could not reach an AI model to build that website, sir.")
        return None

    # Strip accidental markdown code fences if the model added them.
    html = re.sub(r"^```(?:html)?\s*\n?", "", html.strip())
    html = re.sub(r"\n?```\s*$", "", html)

    if "<html" not in html.lower():
        _say("The AI response did not look like a valid website, sir. Please try again.")
        return None

    safe_name = re.sub(r"[^a-zA-Z0-9 _-]", "", business_description).strip()[:40] or "Website"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = _output_folder() / f"{safe_name}_{timestamp}.html"
    path.write_text(html, encoding="utf-8")

    try:
        webbrowser.open(path.as_uri())
    except Exception:
        pass

    _say(f"Your website for {business_description} is ready and open in your browser, sir.")
    return path


def parse_website_command(command):
    patterns = (
        r"(?:build|generate|create|make)\s+(?:me\s+)?(?:a|the)?\s*website\s+(?:for|on|about)\s+(?P<biz>.+)",
        r"website\s+for\s+(?P<biz>.+)",
    )
    for pattern in patterns:
        match = re.search(pattern, command, flags=re.IGNORECASE)
        if match:
            return match.group("biz").strip()
    return None
