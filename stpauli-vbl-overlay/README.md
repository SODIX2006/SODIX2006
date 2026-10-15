# St. Pauli VBL Watchparty – OBS-Overlay

Braun-weißes OBS-Paket für die **Virtual Bundesliga 2026/27**: VBL live schauen, nebenbei selbst **FC 26** zocken
und jedes Tor vom **FC St. Pauli** richtig feiern. Läuft komplett lokal, ohne Server und ohne Installation.

## In 3 Minuten startklar

1. Den Ordner `stpauli-vbl-overlay` auf deinen PC kopieren (z. B. nach `Dokumente`) und **dort liegen lassen**.
2. **OBS schließen** und **`SETUP.bat` doppelklicken**.
   Das Skript trägt deinen Ordnerpfad ein, installiert die Szenensammlung direkt in OBS und kopiert dir die Adresse vom Steuerpult in die Zwischenablage.
3. OBS öffnen → Menü **Szenensammlung → St. Pauli VBL Watchparty**.
4. **Docks → Benutzerdefinierte Browser-Docks** → Name `Kiez-Steuerpult`, URL mit **Strg+V** einfügen → *Anwenden*.
5. Quelle **Webcam** doppelklicken → Kamera auswählen.
   Quelle **VBL Stream (Browserfenster)** → das Browserfenster mit dem VBL-Twitch-Stream auswählen.

Fertig. Falls OBS die Datei nicht automatisch findet, gehst du auf *Szenensammlung → Importieren* und nimmst `obs/St-Pauli-VBL-Watchparty.json`.
Diese Datei entsteht erst durch `SETUP.bat`.

> **Konsole statt PC?** In Szene *2 LIVE* die Quelle `FC 26 - Capturekarte (Konsole)` einblenden (Auge-Symbol),
> deine Capturekarte auswählen und `FC 26 - Spielaufnahme (PC)` ausblenden.

## Die Szenen

| Szene | Was passiert |
|---|---|
| **1 START – Countdown** | „Die VBL ist zurück“, Countdown, Hamburger Hafen-Skyline mit Wellen, Zeitstrahl *Road to Hamburg* (zeigt automatisch, was heute bzw. als Nächstes ansteht) |
| **2 LIVE – Zocken + VBL** | FC 26 als Vollbild, Scoreboard deines Matches mit Bilanz, VBL-Stream im Absperrband-Rahmen oben rechts, Konferenz, Kamera, Kiez-Ticker. Beim Szenenwechsel läuft das Intro |
| **3 WATCHPARTY – VBL groß** | VBL-Stream groß, Kamera und Konferenz rechts, unten das St.-Pauli-Spiel mit Spielstand |
| **4 PAUSE** | Pausenbildschirm mit Zeitstrahl und VBL-Spielständen |
| **5 ENDE** | „Danke fürs Zuschauen – Forza St. Pauli!“ |

## Animationen

- **Intro:** Absperrband, Skyline, „DIE VBL IST ZURÜCK“ und ein *Road to Hamburg*-Stempel
- **Eigenes Tor:** braun-weiße Bänder, riesiges „TOOOR!“, Aufkleber („Der Kiez bebt!“, „Braun-weiß!“ …), Konfetti und Wackeln
- **St. Pauli trifft in der VBL:** dieselbe große Tor-Animation, auch in der Watchparty-Szene
- **Andere VBL-Tore:** Die Zeile leuchtet auf und links erscheint „Tor für …“
- **Gegentor:** dezente Einblendung (große Animation kannst du im Steuerpult einschalten)
- **Abpfiff:** „SIEG!“, „REMIS“ oder „NIEDERLAGE“, die Bilanz zählt automatisch mit

## Kiez-Steuerpult (Dock)

- **+ TOR / + Gegentor** für dein Match, **Abpfiff → Bilanz** am Ende
- **VBL Konferenz:** Paarungen und Status eintragen (`LIVE`, `67'`, `HZ`, `ENDE`, `20:00` …), Tore per **+**
  Dein Verein ist auf `FCSP` voreingestellt, solche Spiele werden braun hervorgehoben.
- Optional: **Lineup** der St.-Pauli-Spieler eintragen, es erscheint unter der Konferenz
- Intro, Test-Animationen, eigene Einblendungen, Ticker-Texte, Countdown-Zeit, Elemente ein- und ausblenden
- Alles wird automatisch gespeichert, auch über einen OBS-Neustart hinweg

Tastenkürzel im Overlay (Rechtsklick auf die Quelle → *Interagieren*): `I` Intro, `G` Tor, `H` Gegentor, `S` Sieg.

## Sounds

Eigene MP3s in `assets/` legen (`tor.mp3`, `sieg.mp3`, `intro.mp3` …, siehe `assets/LIESMICH.txt`).
Die Sounds landen im Stream und werden dir gleichzeitig auf dem Kopfhörer ausgegeben.
Nimm nur Sounds, die du im Stream verwenden darfst, sonst drohen DMCA-Sperren.

## Gut zu wissen

- **Positionen für eigene Anpassungen:** Live: VBL `1240/132` (640×360), Kamera `40/755` (400×225).
  Watchparty: VBL `32/32` (1536×864), Kamera `1600/32` (288×162).
- **VBL im eigenen Stream:** Das Weiterstreamen fremder Übertragungen kann gegen Rechte bzw. Twitch-Regeln verstoßen.
  Im Zweifel den VBL-Ton stummschalten oder nur die Konferenz und Spielstände zeigen.
- **Steuerpult wirkt nicht?** Dock und Overlays müssen aus demselben Ordner kommen. Notlösung: im Ordner
  `python -m http.server 8765` starten und überall `http://localhost:8765/...` statt `file:///...` verwenden.
- Schriften kommen von Google Fonts. Ohne Internet nimmt das Overlay automatisch Ersatzschriften.
- Vorschau im Browser: `overlay.html?demo=1` bzw. `?scene=watch&demo=1`, dazu `control.html` in einem zweiten Tab.
