"""Sperrbildschirm erkennen und per Telegram schreiben."""
import logging, urllib.parse, urllib.request

from voice import speak


def is_locked():
    import psutil
    # LogonUI.exe läuft nur, solange der Sperrbildschirm aktiv ist
    return any(p.info["name"] == "LogonUI.exe" for p in psutil.process_iter(["name"]))


def telegram(text):
    import keyring
    token = keyring.get_password("ario", "telegram")
    chat = keyring.get_password("ario", "telegram_chat")
    data = urllib.parse.urlencode({"chat_id": chat, "text": text}).encode()
    urllib.request.urlopen(f"https://api.telegram.org/bot{token}/sendMessage", data, timeout=10)


def notify(spoken, written=None):
    if is_locked():
        try:
            telegram(written or spoken)
            return
        except Exception as e:
            logging.error(f"Telegram: {e}")
    speak(spoken)
