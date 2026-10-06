# CYMI Support-Zentrale

Eine einzelne Webseite (`index.html`), mit der du Creator-Teams bei Red Bull Can You Make It?
aus der Ferne unterstützt. Du gibst **einmal** dein Telegram-Bot-Token ein, danach läuft alles automatisch:
Teams melden sich selbst an, ihr Live-Standort erscheint auf der Karte, Fotos und Nachrichten landen
im Posteingang, und der Bot beantwortet Fragen wie „Wo gibt's Wasser?“ selbstständig.
Es gibt keinen Server und keine Installation, alles läuft im Browser.

## Einrichten (einmalig, ca. 3 Minuten)

1. **Bot anlegen:** Schreib in Telegram dem [@BotFather](https://t.me/BotFather) `/newbot` und kopiere das Token.
2. **Seite öffnen:** `index.html` im Browser öffnen (Chrome oder Firefox).
3. **Token eintragen:** Abschnitt 0, „Verbinden“. Ab jetzt verbindet sich die Seite bei jedem Öffnen automatisch.
4. **Link an die Teams schicken:** Die Seite zeigt dir `https://t.me/<dein_bot>`. Sobald ein Team dort auf
   „Start“ tippt, ist es automatisch als Team angelegt und bekommt die Bedienknöpfe.

Mit „🔔 Benachrichtigungen“ meldet dein Browser neue Nachrichten, auch wenn der Tab im Hintergrund ist.

## Was die Teams im Bot-Chat machen können

Die Teams teilen einmal ihren **Live-Standort** (📎 → Standort → Live-Standort teilen, 8 Stunden) und
tippen dann einfach auf die Knöpfe:

| Knopf / Befehl | Antwort des Bots |
|---|---|
| 💧 Wasser · 🚿 Dusche · 🚻 WC · 🛏 Schlafen · 🍞 Essen · ⛽ Trampen · 📶 WLAN · 🚉 Bahnhof · 💊 Apotheke | die 5 nächsten Orte mit Entfernung, Öffnungszeiten und Google-Maps-Link, dazu der nächste als Karten-Pin. Der Suchradius wird automatisch größer, wenn in der Nähe nichts ist |
| 🌦 Wetter | Wetter jetzt, nächste 12 h, Sonnenuntergang, 3 Tage, Warnungen, Wetter am Ziel |
| 🧭 Route | Entfernung und Fahrzeit zum Ziel, Navi- und Bus-&-Bahn-Link, Wetter bei Ankunft |
| `/ziel Berlin` | setzt das Ziel des Teams und schickt gleich die Route |
| alles andere (Text, Fotos, Videos, Sprachnachrichten, Dateien) | landet bei dir im Posteingang |

**Wichtig:** Der Bot antwortet nur, solange die Seite bei dir offen ist (am besten auf einem
Laptop, der an bleibt). Ist sie zu, bleiben die Nachrichten bis zu 24 Stunden bei Telegram liegen und
kommen beim nächsten Öffnen an.

## Was du auf der Seite machst

| Bereich | Funktion |
|---|---|
| 1 · Team & Standort | Teams wechseln, Standort per Karte, Suche, Koordinaten oder Maps-Link korrigieren |
| 2 · Nachrichten | Chatverlauf mit dem Team inkl. Fotos, Videos, Sprachnachrichten, Dateien und Bot-Antworten; schnelle Antwort |
| 3 · Ziel & Route | Ziel und Zwischenziele je Team, optimale Reihenfolge, „Ziel für alle Teams übernehmen“ |
| 4 · Orte finden | 12 Kategorien im Umkreis von Standort oder Ziel oder entlang der Route |
| 5 · Wetter | Standort, Ziel und Punkte entlang der Route zur voraussichtlichen Durchfahrtszeit |
| 6 · Update senden | fertige Nachricht mit Route, Wetter und Orten, plus **Bilder, Videos, Audio und Dateien** als Anhang, optional an alle Teams |

## Gut zu wissen

- **Backup:** „⬇ Backup“ speichert Teams, Verlauf und Token als Datei. Damit kannst du alles auf einem
  anderen Rechner wiederherstellen. Die Datei enthält dein Token, also nicht weitergeben.
- **Nur ein Tab:** Telegram erlaubt pro Bot nur einen Empfänger. Ist die Seite zweimal offen, gibt es eine Warnung.
- **Eigener Bot:** Nimm einen Bot nur für dieses Tool. Ist für ihn ein Webhook gesetzt, fragt die Seite, ob sie ihn entfernen soll.
- **Gruppen:** In Gruppen sieht der Bot normale Nachrichten und Standorte nur, wenn du beim BotFather
  `/setprivacy` → *Disable* einstellst. Der Knopf „📍 Standort senden“ funktioniert nur im Privatchat.
- **Dateigrößen:** Bots können Dateien bis 20 MB empfangen und bis 50 MB senden (Fotos bis 10 MB).
- **Daten:** OpenStreetMap (Overpass, Nominatim, OSRM), Karten von CARTO/Esri, Wetter von Open-Meteo.
  Öffnungszeiten und Gebühren können fehlen oder veraltet sein. Fahrzeiten sind Autofahrzeiten,
  beim Trampen kommt die Wartezeit dazu.
- **Regeln prüfen:** Kläre vorher mit Red Bull, ob Unterstützung von außen für Creator-Teams erlaubt ist
  und ob Telegram auf den Event-Handys genutzt werden darf.
