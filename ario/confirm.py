"""Erkennt, ob eine gesprochene Antwort eine Zustimmung ist."""
import re

YES = {"ja", "jo", "jep", "klar", "okay", "ok", "bestätigt", "mach", "genau"}
NO = {"nein", "nee", "nicht", "stopp", "stop", "abbrechen", "lass"}


def is_yes(text):
    words = set(re.findall(r"\w+", text.lower()))
    return bool(words & YES) and not words & NO
