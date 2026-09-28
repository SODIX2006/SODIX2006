# A.R.I.O.

Sprachgesteuerter Arbeits-Copilot für Windows. Wake-Word und Spracherkennung laufen lokal,
nur der erkannte Text geht an die Claude API. Die ausführliche Bauanleitung steht in der Doc
„A.R.I.O. – Bauanleitung“.

## Einrichten

```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -c "import keyring; keyring.set_password('ario','anthropic', input('Anthropic-Key: '))"
python -c "import keyring; keyring.set_password('ario','telegram', input('Telegram-Token: '))"
python -c "import keyring; keyring.set_password('ario','telegram_chat', input('Chat-ID: '))"
```

`credentials.json` aus der Google Cloud Console in diesen Ordner legen. Starten mit `python main.py`.

## Dateien

| Datei | Aufgabe |
|---|---|
| `config.py` | Wake-Word, Stimme, Modell, Limits |
| `main.py` | Hauptschleife und Meeting-Wächter |
| `voice.py` | Wake-Word, Spracherkennung, Sprachausgabe |
| `brain.py` | Claude-Anbindung und Persönlichkeit |
| `tools.py` | Werkzeuge und Bestätigungsstufen |
| `shortcuts.py` | lokaler Schnellweg ohne API-Kosten |
| `confirm.py` | erkennt „ja“ und „nein“ in der Antwort |
| `calendar_ario.py` | Google-Kalender |
| `presence.py` | Sperrbildschirm und Telegram |

## Tests

```
pip install pytest
pytest tests
```
