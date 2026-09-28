"""Startpunkt: Hauptschleife und Hintergrund-Wächter."""
import logging, threading, time

import config

logging.basicConfig(filename=config.LOG_DIR / "ario.log", level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(message)s", encoding="utf-8")

from voice import wait_for_wakeword, record_until_silence, transcribe, speak
from brain import think
from presence import notify
from calendar_ario import upcoming_meeting
from confirm import is_yes
from shortcuts import local_answer, state

notified = set()


def confirm(question):
    speak(question)
    return is_yes(transcribe(record_until_silence(max_s=5)))


def watcher():
    while True:
        try:
            m = upcoming_meeting()
            if m and m[0] not in notified:
                event_id, title, link = m
                notified.add(event_id)
                state["link"] = link
                notify(f"{title} in fünf Minuten. Sag: Meeting öffnen.",
                       f"{title} startet in 5 Minuten: {link}")
        except Exception as e:
            logging.error(f"Wächter: {e}")
        time.sleep(60)


def main():
    threading.Thread(target=watcher, daemon=True).start()
    speak("A.R.I.O. online.")
    while True:
        try:
            wait_for_wakeword()
            text = transcribe(record_until_silence())
            if not text:
                continue
            logging.info(f"Gehört: {text}")
            speak(local_answer(text) or think(text, confirm))
        except Exception as e:
            logging.exception(f"Hauptschleife: {e}")
            speak("Fehler. Details im Log.")


if __name__ == "__main__":
    main()
