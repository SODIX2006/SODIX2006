"""Lokaler Schnellweg: häufige Befehle ohne API-Anfrage (kostet nichts)."""
from tools import open_website, system_status
from calendar_ario import get_events

state = {"link": None}

WEBSITES = {
    "youtube": "https://youtube.com",
    "github": "https://github.com",
}


def local_answer(text):
    t = text.lower().strip(" .!?")
    if "meeting" in t and ("öffne" in t or "öffnen" in t):
        return open_website(state["link"]) if state["link"] else "Kein Meeting-Link vorhanden."
    if "was steht" in t or "welche termine" in t:
        for day in ("übermorgen", "morgen", "heute"):
            if day in t:
                return get_events(day)
    if "auslastung" in t or "systemstatus" in t:
        return system_status()
    if t.startswith("öffne "):
        site = WEBSITES.get(t.removeprefix("öffne ").strip())
        if site:
            return open_website(site)
    return None
