# CYMI Support-Zentrale

Eine einzelne Webseite (`index.html`), mit der du Creator-Teams bei Red Bull Can You Make It?
aus der Ferne unterstützt: Standort des Teams setzen, Ziel und Checkpoints eintragen, Route
und Wetter berechnen, Orte in der Nähe oder entlang der Route finden und alles als
Telegram-Nachricht an das Team schicken. Es gibt keinen Server und keine Installation,
alles läuft im Browser.

## Was die Seite kann

| Bereich | Funktion | Datenquelle |
|---|---|---|
| Team & Standort | mehrere Teams, Standort per Kartenklick, Suche, Koordinaten, Google-Maps-Link oder Telegram-Live-Standort | Nominatim (OSM) |
| Route | Auto/Trampen, Fahrrad, zu Fuß; Zwischenziele mit optimierter Reihenfolge; Navi- und ÖPNV-Links für Google Maps | OSRM (routing.openstreetmap.de) |
| Orte | Trinkwasser, Duschen, Toiletten, Schlafplätze, Essen, Restaurants, Gratis-WLAN, Bahnhof/Bus, Tankstellen und Raststätten (Trampen), Waschsalon, Apotheke/Arzt, Touristinfo. Suche im Umkreis von Standort oder Ziel oder entlang der Route | Overpass (OSM) |
| Wetter | jetzt, nächste 12 h, Sonnenuntergang, 3-Tage-Trend, Wetter entlang der Route zur voraussichtlichen Durchfahrtszeit, Warnhinweise | Open-Meteo |
| Telegram | Nachricht mit Vorschau und Bearbeitung, Orte optional als Karten-Pins, Chat-IDs finden, Live-Standort der Teams abholen (auf Wunsch alle 60 s) | Telegram Bot API |

## Einrichten (einmalig, ca. 5 Minuten)

1. **Bot anlegen:** Schreib in Telegram dem [@BotFather](https://t.me/BotFather) `/newbot` und kopiere das Token.
2. **Seite öffnen:** `index.html` im Browser öffnen, entweder per Doppelklick oder besser über
   GitHub Pages bzw. lokal mit `python -m http.server` im Ordner und dann `http://localhost:8000`.
3. **Token eintragen:** Abschnitt 5, Feld „Bot-Token“. Das Token bleibt nur in deinem Browser (localStorage).
4. **Team anlegen:** Abschnitt 1, Teamname eingeben, „+ Team“.
5. **Chat-ID holen:** Das Team schreibt deinem Bot einmal eine Nachricht, zum Beispiel `/start`.
   Danach klickst du auf „Chats & Chat-IDs finden“ und dann auf den Chat des Teams.

## Live-Standort der Teams

Das Team teilt im Chat mit dem Bot seinen **Live-Standort** (Büroklammer → Standort → Live-Standort teilen).
Mit „📡 Position aus Telegram“ holst du die neueste Position, mit „alle 60 s“ wird sie automatisch aktualisiert.

- Am einfachsten ist ein **Privatchat** zwischen Team und Bot.
- In einer **Gruppe** sieht der Bot Standorte nur, wenn du beim BotFather `/setprivacy` → *Disable* einstellst.
- Die Seite holt die Updates mit `getUpdates`. Ist für den Bot ein Webhook gesetzt, klappt das nicht.
  Nimm deshalb einen eigenen Bot nur für dieses Tool.

## Typischer Ablauf

1. Team wählen, Position aus Telegram holen (oder auf die Karte klicken).
2. Klick-Modus auf „Ziel“ stellen und den nächsten Checkpoint anklicken (oder suchen).
3. „Route berechnen“, danach „Wetter laden“.
4. Kategorien wählen, zum Beispiel 💧 🚿 🛏 ⛽, Suchbereich „Entlang der Route“, „Orte suchen“.
   Die drei nächsten Treffer pro Kategorie sind schon angehakt.
5. Vorschau prüfen, Notiz dazuschreiben, „📨 An Team senden“.

## Hinweise

- **Regeln prüfen:** Kläre vorher mit Red Bull bzw. in den offiziellen Regeln für Creator-Teams,
  ob Unterstützung von außen und die Nutzung von Telegram auf den Event-Handys erlaubt ist.
- Die Daten stammen aus OpenStreetMap. Öffnungszeiten und Gebühren können fehlen oder veraltet sein.
- Die Dienste sind kostenlos und für faire Nutzung gedacht. Suchen nur auf Knopfdruck, nicht in Schleifen.
- Fahrzeiten aus OSRM sind Autofahrzeiten. Beim Trampen kommt die Wartezeit dazu.
