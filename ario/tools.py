"""Werkzeuge und Bestätigungsstufen. Was nicht in REGISTRY steht, ist verboten."""
import logging, shutil, webbrowser
from pathlib import Path

import config
from calendar_ario import get_events, find_free_slot, create_event

log = logging.getLogger("ario.aktionen")
if not log.handlers:
    _h = logging.FileHandler(config.LOG_DIR / "aktionen.log", encoding="utf-8")
    _h.setFormatter(logging.Formatter("%(asctime)s %(message)s"))
    log.addHandler(_h)
    log.setLevel(logging.INFO)

FREI, BESTAETIGEN = "frei", "bestaetigen"


def open_website(url):
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    webbrowser.open(url)
    return f"Geöffnet: {url}"


def system_status():
    import psutil
    d = psutil.disk_usage(Path.home().anchor or "/")
    return (f"CPU {psutil.cpu_percent(1)} %, RAM {psutil.virtual_memory().percent} %, "
            f"Laufwerk {d.percent} % belegt")


def arrange_window(title, side):
    import ctypes, pygetwindow as gw
    wins = gw.getWindowsWithTitle(title)
    if not wins:
        return "Fenster nicht gefunden."
    w = wins[0]
    sw, sh = ctypes.windll.user32.GetSystemMetrics(0), ctypes.windll.user32.GetSystemMetrics(1)
    w.restore()
    w.resizeTo(sw // 2, sh)
    w.moveTo(0 if side == "links" else sw // 2, 0)
    return f"{w.title} {side}."


def move_file(src, dst):
    if not Path(src).exists():
        return f"Datei nicht gefunden: {src}"
    shutil.move(src, dst)
    return f"Verschoben nach {dst}."


REGISTRY = {
    "open_website": (open_website, FREI),
    "system_status": (system_status, FREI),
    "arrange_window": (arrange_window, FREI),
    "get_events": (get_events, FREI),
    "find_free_slot": (find_free_slot, FREI),
    "move_file": (move_file, BESTAETIGEN),
    "create_event": (create_event, BESTAETIGEN),
}

_str = {"type": "string"}
TOOLS = [
    {"name": "open_website", "description": "Öffnet eine URL im Browser.",
     "input_schema": {"type": "object", "properties": {"url": _str}, "required": ["url"]}},
    {"name": "system_status", "description": "CPU, RAM und Speicherplatz.",
     "input_schema": {"type": "object", "properties": {}}},
    {"name": "arrange_window", "description": "Legt ein Fenster auf die linke oder rechte Bildschirmhälfte.",
     "input_schema": {"type": "object", "properties": {"title": _str,
      "side": {"type": "string", "enum": ["links", "rechts"]}}, "required": ["title", "side"]}},
    {"name": "move_file", "description": "Verschiebt eine Datei.",
     "input_schema": {"type": "object", "properties": {"src": _str, "dst": _str},
      "required": ["src", "dst"]}},
    {"name": "get_events", "description": "Termine eines Tages: heute, morgen oder JJJJ-MM-TT.",
     "input_schema": {"type": "object", "properties": {"day": _str}}},
    {"name": "find_free_slot", "description": "Erster freier Block an einem Tag (JJJJ-MM-TT).",
     "input_schema": {"type": "object", "properties": {"day": _str,
      "minutes": {"type": "integer"}}, "required": ["day"]}},
    {"name": "create_event", "description": "Legt einen Termin an. Vorher mit get_events auf Überschneidungen prüfen.",
     "input_schema": {"type": "object", "properties": {"title": _str,
      "start": {"type": "string", "description": "JJJJ-MM-TTTHH:MM"},
      "minutes": {"type": "integer"}}, "required": ["title", "start"]}},
]


QUESTIONS = {
    "move_file": "{src} nach {dst} verschieben?",
    "create_event": "Termin {title} am {start} eintragen?",
}


def question(name, args):
    try:
        return QUESTIONS[name].format(**args)
    except (KeyError, IndexError):
        return f"{name} mit {args} ausführen?"


def run_tool(name, args, confirm):
    if name not in REGISTRY:
        log.info(f"VERBOTEN {name} {args}")
        return "Diese Aktion ist nicht erlaubt."
    func, stufe = REGISTRY[name]
    if stufe == BESTAETIGEN and not confirm(question(name, args)):
        log.info(f"ABGELEHNT {name} {args}")
        return "Vom Nutzer abgelehnt."
    try:
        result = func(**args)
    except Exception as e:
        result = f"Fehler: {e}"
    log.info(f"{name} {args} -> {result}")
    return result
