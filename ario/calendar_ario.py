"""Google-Kalender: lesen, freie Zeiten finden, Termine anlegen."""
import datetime as dt, time

import config

SCOPES = ["https://www.googleapis.com/auth/calendar.events"]
TOKEN = config.BASE / "token.json"
CREDENTIALS = config.BASE / "credentials.json"
_cache = {"t": 0, "events": []}


def _service():
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build

    creds = None
    if TOKEN.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN), SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            creds = InstalledAppFlow.from_client_secrets_file(
                str(CREDENTIALS), SCOPES).run_local_server(port=0)
        TOKEN.write_text(creds.to_json())
    return build("calendar", "v3", credentials=creds)


def _events():
    # höchstens alle 5 Minuten bei Google nachfragen
    if time.time() - _cache["t"] > 300:
        now = dt.datetime.now(dt.timezone.utc)
        res = _service().events().list(
            calendarId="primary", timeMin=now.isoformat(),
            timeMax=(now + dt.timedelta(days=14)).isoformat(),
            singleEvents=True, orderBy="startTime").execute()
        _cache.update(t=time.time(), events=res.get("items", []))
    return _cache["events"]


def _start(e):
    return e["start"].get("dateTime", e["start"].get("date"))


def _day(day):
    today = dt.date.today()
    d = {"heute": today, "morgen": today + dt.timedelta(days=1),
         "übermorgen": today + dt.timedelta(days=2)}.get(day.lower().strip())
    return d.isoformat() if d else day


def get_events(day="heute"):
    d = _day(day)
    hits = [f"{_start(e)[11:16] or 'ganztägig'} {e.get('summary', '')}"
            for e in _events() if _start(e).startswith(d)]
    return "; ".join(hits) or "Keine Termine."


def find_free_slot(day, minutes=60, von=8, bis=18):
    day = _day(day)
    busy = sorted((dt.datetime.fromisoformat(_start(e)).replace(tzinfo=None),
                   dt.datetime.fromisoformat(e["end"]["dateTime"]).replace(tzinfo=None))
                  for e in _events()
                  if _start(e).startswith(day) and "dateTime" in e["start"])
    t = dt.datetime.fromisoformat(f"{day}T{von:02d}:00")
    end = dt.datetime.fromisoformat(f"{day}T{bis:02d}:00")
    for b_start, b_end in busy + [(end, end)]:
        if (min(b_start, end) - t).total_seconds() >= minutes * 60:
            return f"Frei ab {t:%H:%M}."
        t = max(t, b_end)
    return "Kein freier Block."


def create_event(title, start, minutes=60):
    s = dt.datetime.fromisoformat(start)
    body = {"summary": title,
            "start": {"dateTime": s.isoformat(), "timeZone": config.TZ},
            "end": {"dateTime": (s + dt.timedelta(minutes=minutes)).isoformat(), "timeZone": config.TZ}}
    _service().events().insert(calendarId="primary", body=body).execute()
    _cache["t"] = 0
    return f"Eingetragen: {title}, {s:%d.%m. %H:%M}."


def upcoming_meeting(within_min=5):
    now = dt.datetime.now().astimezone()
    for e in _events():
        if "dateTime" not in e["start"]:
            continue
        diff = (dt.datetime.fromisoformat(_start(e)) - now).total_seconds() / 60
        link = e.get("hangoutLink") or e.get("location", "")
        if 0 < diff <= within_min and link.startswith("http"):
            return e["id"], e.get("summary", "Meeting"), link
    return None
