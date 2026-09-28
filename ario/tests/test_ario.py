import datetime as dt
from types import SimpleNamespace

import pytest

import brain, calendar_ario, shortcuts, tools
from confirm import is_yes


@pytest.mark.parametrize("text,expected", [
    ("Ja.", True), ("Ja, mach das", True), ("okay", True),
    ("Nein", False), ("Ja, nein, lieber nicht", False),
    ("Im Januar", False), ("", False),
])
def test_is_yes(text, expected):
    assert is_yes(text) is expected


def test_unknown_tool_is_forbidden():
    assert tools.run_tool("format_c", {}, lambda q: True) == "Diese Aktion ist nicht erlaubt."


def test_confirm_level_asks_and_respects_no(tmp_path):
    src = tmp_path / "a.txt"
    src.write_text("x")
    asked = []
    result = tools.run_tool("move_file", {"src": str(src), "dst": str(tmp_path / "b.txt")},
                            lambda q: asked.append(q) or False)
    assert result == "Vom Nutzer abgelehnt."
    assert src.exists()
    assert "verschieben?" in asked[0]


def test_confirm_level_runs_on_yes(tmp_path):
    src = tmp_path / "a.txt"
    src.write_text("x")
    tools.run_tool("move_file", {"src": str(src), "dst": str(tmp_path / "b.txt")}, lambda q: True)
    assert (tmp_path / "b.txt").exists()


def test_every_tool_has_schema_and_registry_entry():
    assert {t["name"] for t in tools.TOOLS} == set(tools.REGISTRY)


def test_trim_starts_with_real_user_message():
    h = [{"role": "user", "content": "a"},
         {"role": "assistant", "content": [1]},
         {"role": "user", "content": [{"type": "tool_result"}]},
         {"role": "assistant", "content": [2]},
         {"role": "user", "content": "b"},
         {"role": "assistant", "content": [3]}]
    brain.trim(h, limit=4)
    assert h[0] == {"role": "user", "content": "b"}


def _fake_events(monkeypatch, day, busy):
    events = [{"id": str(i), "start": {"dateTime": f"{day}T{s}:00+02:00"},
               "end": {"dateTime": f"{day}T{e}:00+02:00"}, "summary": f"T{i}"}
              for i, (s, e) in enumerate(busy)]
    monkeypatch.setattr(calendar_ario, "_events", lambda: events)


def test_find_free_slot(monkeypatch):
    _fake_events(monkeypatch, "2026-10-01", [("08:00", "09:30"), ("10:00", "12:00")])
    assert calendar_ario.find_free_slot("2026-10-01", 60) == "Frei ab 12:00."
    assert calendar_ario.find_free_slot("2026-10-01", 30) == "Frei ab 09:30."


def test_find_free_slot_ignores_time_after_workday(monkeypatch):
    _fake_events(monkeypatch, "2026-10-01", [("08:00", "17:30"), ("20:00", "22:00")])
    assert calendar_ario.find_free_slot("2026-10-01", 60) == "Kein freier Block."


def test_get_events_morgen(monkeypatch):
    morgen = (dt.date.today() + dt.timedelta(days=1)).isoformat()
    _fake_events(monkeypatch, morgen, [("09:00", "10:00")])
    assert calendar_ario.get_events("morgen") == "09:00 T0"


def test_local_answer(monkeypatch):
    monkeypatch.setattr(shortcuts, "get_events", lambda d: f"events {d}")
    monkeypatch.setattr(shortcuts, "open_website", lambda u: f"open {u}")
    assert shortcuts.local_answer("Was steht morgen an?") == "events morgen"
    assert shortcuts.local_answer("Öffne YouTube.") == "open https://youtube.com"
    assert shortcuts.local_answer("Meeting öffnen") == "Kein Meeting-Link vorhanden."
    assert shortcuts.local_answer("Trag morgen einen Termin ein") is None


def test_think_rolls_back_history_on_error(monkeypatch):
    def boom(**kw):
        raise RuntimeError("API down")
    monkeypatch.setattr(brain, "client", lambda: SimpleNamespace(messages=SimpleNamespace(create=boom)))
    brain.history.clear()
    with pytest.raises(RuntimeError):
        brain.think("Hallo", lambda q: True)
    assert brain.history == []
