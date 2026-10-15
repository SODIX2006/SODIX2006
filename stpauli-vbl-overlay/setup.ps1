# St. Pauli VBL Watchparty - richtet die OBS-Szenensammlung automatisch ein.
# Start per Doppelklick auf SETUP.bat (OBS vorher schliessen).

$ErrorActionPreference = 'Stop'
$dir = $PSScriptRoot
$base = ([System.Uri]$dir).AbsoluteUri.TrimEnd('/')   # z. B. file:///C:/Users/Name/stpauli-vbl-overlay
$utf8 = New-Object System.Text.UTF8Encoding $false

Write-Host ''
Write-Host '  ===  ST. PAULI VBL DISCORD-WATCHPARTY - OBS SETUP  ===' -ForegroundColor Yellow
Write-Host ''

if (Get-Process -Name obs64, obs32, obs -ErrorAction SilentlyContinue) {
    Write-Host '  OBS laeuft gerade. Bitte OBS komplett schliessen und SETUP.bat erneut starten.' -ForegroundColor Red
    exit 1
}

# 1) Szenensammlung mit dem richtigen Ordnerpfad erzeugen
$template = [System.IO.File]::ReadAllText((Join-Path $dir 'obs\szenensammlung.vorlage.json'), $utf8)
$json = $template.Replace('@@BASE@@', $base)
$out = Join-Path $dir 'obs\St-Pauli-VBL-Watchparty.json'
[System.IO.File]::WriteAllText($out, $json, $utf8)
Write-Host "  [OK] Szenensammlung erstellt: $out" -ForegroundColor Green

# 2) Direkt in OBS installieren (erscheint unter Szenensammlung)
$scenes = Join-Path $env:APPDATA 'obs-studio\basic\scenes'
if (Test-Path $scenes) {
    $target = Join-Path $scenes 'St_Pauli_VBL_Watchparty.json'
    if (Test-Path $target) {
        Copy-Item $target ($target + '.backup') -Force
        Write-Host '  [OK] Alte Version gesichert (.backup)' -ForegroundColor Green
    }
    Copy-Item $out $target -Force
    Write-Host '  [OK] In OBS installiert -> Menue "Szenensammlung" -> "St. Pauli VBL Watchparty"' -ForegroundColor Green
} else {
    Write-Host '  [!] OBS-Ordner nicht gefunden. In OBS manuell importieren:' -ForegroundColor Yellow
    Write-Host '      Szenensammlung -> Importieren -> obs\St-Pauli-VBL-Watchparty.json'
}

# 3) Steuerpult-Adresse fuer das Browser-Dock in die Zwischenablage
$dock = "$base/control.html"
try { Set-Clipboard -Value $dock; $clip = ' (liegt in der Zwischenablage)' } catch { $clip = '' }

Write-Host ''
Write-Host '  NOCH 4 KLEINIGKEITEN IN OBS:' -ForegroundColor Yellow
Write-Host '   1. Docks -> Benutzerdefinierte Browser-Docks -> Name: Kiez-Steuerpult'
Write-Host "      URL: $dock$clip"
Write-Host '   2. Quelle "Webcam" doppelklicken -> deine Kamera auswaehlen'
Write-Host '   3. Quelle "VBL Stream (Browserfenster)" -> Browserfenster mit dem VBL-Twitch-Stream auswaehlen'
Write-Host '      (Konsole statt PC? In Szene 2 die Capturekarte einblenden und die PC-Spielaufnahme ausblenden.)'
Write-Host '   4. Discord "Im Voice": streamkit.discord.com/overlay -> Voice Widget -> Server + Sprachkanal waehlen'
Write-Host '      -> URL kopieren -> in OBS bei "Discord Voice (StreamKit)" als URL eintragen'
Write-Host ''
Write-Host '  IN DISCORD TEILEN:' -ForegroundColor Yellow
Write-Host '   OBS: Rechtsklick ins Vorschaubild -> Fensterprojektor (Programm)'
Write-Host '   Discord: Sprachkanal -> Bildschirm teilen -> Fenster "Fensterprojektor (Programm)" waehlen'
Write-Host ''
Write-Host '  Die komplette Anleitung (inkl. Animationen) oeffnet sich jetzt im Browser.'
Write-Host '  Forza St. Pauli!' -ForegroundColor Yellow
try { Start-Process (Join-Path $dir 'ANLEITUNG.html') } catch { }
Write-Host ''
