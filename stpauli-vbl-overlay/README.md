# St. Pauli VBL Discord-Watchparty – OBS-Overlay

Braun-weißes OBS-Paket für die **Virtual Bundesliga 2026/27** als **Discord-Übertragung**: VBL mit deinen Leuten im
Sprachkanal schauen, nebenbei selbst **FC 26** zocken und jedes Tor vom **FC St. Pauli** richtig feiern.
OBS baut das Bild, Discord überträgt es per *Bildschirm teilen*. Läuft komplett lokal, ohne Server und ohne Installation.

> 📖 **Ausführliche Anleitung mit Spickzettel für alle Animationen (Tor, Abpfiff, Intro …): `ANLEITUNG.html`**
> Doppelklick, dann öffnet sie sich im Browser. Das Setup öffnet sie am Ende auch automatisch.

## In 3 Minuten startklar

1. Den Ordner `stpauli-vbl-overlay` auf deinen PC kopieren (z. B. nach `Dokumente`) und **dort liegen lassen**.
2. **OBS schließen** und **`SETUP.bat` doppelklicken**.
   Das Skript trägt deinen Ordnerpfad ein, installiert die Szenensammlung direkt in OBS und kopiert dir die Adresse vom Steuerpult in die Zwischenablage.
3. OBS öffnen → Menü **Szenensammlung → St. Pauli VBL Watchparty**.
4. **Docks → Benutzerdefinierte Browser-Docks** → Name `Kiez-Steuerpult`, URL mit **Strg+V** einfügen → *Anwenden*.
5. Quelle **Webcam** doppelklicken → Kamera auswählen.
   Quelle **VBL Stream (Browserfenster)** → das Browserfenster mit dem VBL-Twitch-Stream auswählen.

6. **Discord „Im Voice“** einrichten und **in Discord teilen** – siehe nächster Abschnitt.

Falls OBS die Datei nicht automatisch findet, gehst du auf *Szenensammlung → Importieren* und nimmst `obs/St-Pauli-VBL-Watchparty.json`.
Diese Datei entsteht erst durch `SETUP.bat`.

> **Konsole statt PC?** In Szene *2 LIVE* die Quelle `FC 26 - Capturekarte (Konsole)` einblenden (Auge-Symbol),
> deine Capturekarte auswählen und `FC 26 - Spielaufnahme (PC)` ausblenden.

## Discord

### OBS-Bild in Discord übertragen
1. In OBS mit Rechtsklick ins Vorschaubild → **Fensterprojektor (Programm)**. Das Fenster offen lassen, es darf auch hinter dem Spiel liegen.
2. In Discord in den Sprachkanal gehen → **Bildschirm teilen** → Reiter *Anwendungen* → **Fensterprojektor (Programm)**.
3. Qualität: Ohne Nitro überträgt Discord mit 720p/30 FPS, mit Nitro bis 1080p/60. Das Overlay ist auf beides ausgelegt.

**Ton:** Discord überträgt den Ton der geteilten Anwendung, hier also OBS. Die Tor- und Sieg-Sounds aus dem Overlay
sind schon so eingestellt, dass sie über OBS laufen. Deine Freunde hören sie also, du ebenfalls.
Den VBL-Ton holen sich deine Leute am einfachsten direkt von der VBL auf Twitch. Alternativ teilst du statt des
Projektors direkt das Browserfenster mit dem VBL-Stream.

> Willst du die Übertragung lieber als Kamera senden: In OBS *Virtuelle Kamera starten* und in Discord als Kamera
> „OBS Virtual Camera“ wählen. Das funktioniert auch in Videoanrufen, ist aber auf 720p begrenzt.

### „Im Voice“ – wer gerade spricht
Das Overlay hat einen braun-weißen „Im Voice“-Kasten: in der Live-Szene links, in der Watchparty rechts.
Dort zeigt Discord StreamKit die Avatare aus deinem Sprachkanal. Wer spricht, leuchtet auf.

1. **streamkit.discord.com/overlay** öffnen → *Install for OBS* → mit Discord verbinden.
2. **Voice Widget** wählen → deinen Server und den Sprachkanal auswählen → die URL rechts kopieren.
3. In OBS die Quelle **Discord Voice (StreamKit)** doppelklicken → die URL einfügen → OK.
   Das braun-weiße Design (CSS) ist schon eingetragen. Ändert Discord intern etwas, sieht es notfalls wie das normale StreamKit aus.

Den Namen des Sprachkanals über dem Kasten und den Text rechts im Ticker änderst du im Steuerpult.
Der Kasten lässt sich dort unter *Einblenden* auch ausschalten.

## Die Szenen

| Szene | Was passiert |
|---|---|
| **1 START – Countdown** | „Die VBL ist zurück“, Countdown, Hamburger Hafen-Skyline mit Wellen, Zeitstrahl *Road to Hamburg* (zeigt automatisch, was heute bzw. als Nächstes ansteht) |
| **2 LIVE – Zocken + VBL** | FC 26 als Vollbild, Scoreboard deines Matches mit Bilanz, „Im Voice“ links, VBL-Stream im Absperrband-Rahmen oben rechts, Konferenz, Kamera, Kiez-Ticker. Beim Szenenwechsel läuft das Intro |
| **3 WATCHPARTY – VBL groß** | VBL-Stream groß, rechts Kamera, „Im Voice“ und Konferenz, unten das St.-Pauli-Spiel mit Spielstand |
| **4 PAUSE** | Pausenbildschirm mit Zeitstrahl und VBL-Spielständen |
| **5 ENDE** | „Danke fürs Dabeisein – bis zum nächsten Spieltag im Discord!“ |

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
Die Sounds laufen über OBS, deine Freunde im Discord hören sie also mit, du ebenfalls.

## Gut zu wissen

- **Positionen für eigene Anpassungen:** Live: VBL `1240/132` (640×360), Kamera `40/755` (400×225), Voice `52/244` (276×360).
  Watchparty: VBL `32/32` (1536×864), Kamera `1600/32` (288×162), Voice `1612/270` (264×280).
- **Nur für deine Runde:** Ein privater Discord-Kanal mit Freunden ist etwas anderes als ein öffentlicher Stream.
  Wenn du das Ganze später öffentlich auf Twitch oder YouTube streamst, gelten dort Rechte an der VBL-Übertragung und an der Musik.
- **Steuerpult wirkt nicht?** Dock und Overlays müssen aus demselben Ordner kommen. Notlösung: im Ordner
  `python -m http.server 8765` starten und überall `http://localhost:8765/...` statt `file:///...` verwenden.
- Schriften kommen von Google Fonts. Ohne Internet nimmt das Overlay automatisch Ersatzschriften.
- Vorschau im Browser: `overlay.html?demo=1` bzw. `?scene=watch&demo=1`, dazu `control.html` in einem zweiten Tab.
