# VBL Watchparty Overlay für OBS

Animiertes Overlay, um die **Virtuelle Bundesliga** live zu verfolgen und gleichzeitig selbst **FC** zu zocken.
Läuft komplett lokal – kein Server und keine Installation nötig.

## Was drin ist

| Szene | URL | Inhalt |
|---|---|---|
| Hauptszene | `overlay.html` | Scoreboard eures Matches, Bilanz (S/U/N), VBL-Kopf mit Uhr, Rahmen für den VBL-Stream (Bild-in-Bild), Konferenz-Tabelle, Kamerarahmen, Lauf-Ticker |
| Countdown | `overlay.html?scene=countdown` | „Die VBL ist zurück“ mit Countdown, animiertem Hintergrund und den VBL-Paarungen |
| Pause | `overlay.html?scene=pause` | Pausenbildschirm mit den aktuellen VBL-Ergebnissen |
| Steuerpult | `control.html` | Hier bedient ihr alles während des Streams |

**Animationen:** Intro-Sting „DIE VBL IST ZURÜCK“ beim Start, große „TOOOR!“-Animation mit Konfetti und Kameraruckeln bei eigenen Toren,
aufleuchtende Zeile + Einblendung „Tor für …“ bei VBL-Toren, Rahmen mit umlaufendem Farbverlauf, Lichtreflexe, Einflug-Animationen.

## Einrichtung in OBS

1. Den Ordner `vbl-overlay` irgendwo auf dem PC ablegen (alle Dateien müssen zusammen bleiben).
2. **Hauptszene:** Quelle hinzufügen → *Browser* →
   - *Lokale Datei* anhaken → `overlay.html` auswählen
   - Breite `1920`, Höhe `1080`
   - Die Browserquelle **ganz oben** in der Quellenliste platzieren.
3. Darunter eure anderen Quellen:
   - **Spielaufnahme** (FC) als Vollbild
   - **VBL-Stream** (z. B. Fensteraufnahme des Browsers oder eine Browserquelle mit dem Stream) in den Rahmen oben rechts ziehen: Position `1240 / 132`, Größe `640 × 360`
   - **Webcam** in den Rahmen unten links: Position `40 / 680`, Größe `400 × 300`
4. **Countdown-** und **Pause-Szene:** jeweils eigene OBS-Szene, Browserquelle mit *Lokale Datei* deaktiviert und als URL
   `file:///C:/Pfad/zu/vbl-overlay/overlay.html?scene=countdown` (bzw. `?scene=pause`) eintragen.
5. **Steuerpult als Dock:** OBS → *Docks* → *Benutzerdefinierte Browser-Docks* → Name `VBL`, URL
   `file:///C:/Pfad/zu/vbl-overlay/control.html`. Das Dock dann z. B. neben die Szenen ziehen.

> Tipp: Bei der Browserquelle „Browser aktualisieren, wenn die Szene aktiv wird“ anhaken, dann läuft das Intro
> jedes Mal, wenn ihr in die Hauptszene wechselt. Ohne Intro: `overlay.html?intro=0`.

## Während des Streams

- **+ TOR** bei eurem Match → Score springt hoch, große Tor-Animation in der Teamfarbe.
- **Spiel beenden → Bilanz** → zählt Sieg/Remis/Niederlage, setzt 0:0 und erhöht „Spiel 1“ → „Spiel 2“.
- **VBL Konferenz:** Paarungen und Status frei eintragen (`LIVE`, `67'`, `HZ`, `ENDE`, `20:00` …). Jedes **+** löst die Torbenachrichtigung aus.
- **Intro abspielen**, **eigene Einblendung (Toast)** senden, einzelne Elemente ein-/ausblenden.
- Alle Eingaben werden automatisch gespeichert und bleiben auch nach einem OBS-Neustart erhalten.

Tastenkürzel direkt im Overlay (Rechtsklick auf die Quelle → *Interagieren*): `I` Intro, `G` Tor Heim, `H` Tor Gast.

## Vorschau im Browser

`overlay.html?demo=1` im Chrome öffnen (grüner Hintergrund statt transparent, spielt Intro, Tor und Einblendung nacheinander ab).
`control.html` im selben Browser in einem zweiten Tab öffnen, dann wirken die Buttons live.

## Falls das Dock das Overlay nicht steuert

Dock und Overlay müssen dieselbe Adresse nutzen (beide `file:///…` aus demselben Ordner). Klappt es trotzdem nicht,
beide über einen Mini-Webserver laden: im Ordner `python -m http.server 8765` starten und in OBS
`http://localhost:8765/overlay.html` bzw. `http://localhost:8765/control.html` verwenden.

Schriften (Bebas Neue, Rajdhani) kommen von Google Fonts; ohne Internet wird automatisch auf Impact/Arial ausgewichen.
