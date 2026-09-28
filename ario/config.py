"""Zentrale Einstellungen. Hier änderst du Wake-Word, Stimme und Modell."""
from pathlib import Path

BASE = Path(__file__).resolve().parent
LOG_DIR = BASE / "logs"
LOG_DIR.mkdir(exist_ok=True)

# Nach dem Training des eigenen Modells: Pfad zur .onnx-Datei, z. B. str(BASE / "ario.onnx")
WAKEWORD = "hey_jarvis"
WAKE_THRESHOLD = 0.5

STT_MODEL = "small"          # "base" ist schneller, "small" genauer
VOICE = "de-DE-ConradNeural"

MODEL = "claude-haiku-4-5-20251001"
MAX_TOKENS = 300
HISTORY_LEN = 10

TZ = "Europe/Berlin"
