/*
 * St. Pauli VBL Discord-Watchparty – gemeinsamer Zustand zwischen Steuerpult und Overlays.
 *
 * Synchronisiert über drei Wege, damit es in OBS (Browser-Dock + Browser-Quellen)
 * und im normalen Browser zuverlässig klappt:
 *   1. BroadcastChannel  (sofort)
 *   2. storage-Event     (sofort, andere Tabs/Fenster)
 *   3. Polling           (Fallback alle 700 ms)
 */
const KIEZ = (() => {
  const KEY = 'stpauli-vbl-state-v2';
  const EVT = 'stpauli-vbl-event-v1';

  const DEFAULT = {
    rev: 0,
    me: {
      label: 'FC 26 · Weekend League · Spiel 1',
      homeName: 'SODIX',
      homeTag: 'FCSP',
      homeColor: '#6b4029',
      homeScore: 0,
      awayName: 'GEGNER',
      awayTag: 'GEG',
      awayColor: '#7c8594',
      awayScore: 0,
      goalAnim: true,      // große Animation bei eigenem Tor
      celebrateAway: false, // Gegentor nur als kleine Einblendung
      sounds: true,
      volume: 0.8,
    },
    record: { w: 0, d: 0, l: 0 },
    vbl: {
      title: 'VIRTUAL BUNDESLIGA',
      subtitle: 'Club Championship · Showdown 1',
      focus: 'FCSP',
      lineup: '',
      matches: [
        { id: 'm1', home: 'FCSP', away: 'GEGNER', hs: 0, as: 0, status: 'LIVE' },
      ],
    },
    // Road to Hamburg – Saison 2026/27 (laut Bundesliga-Ankündigung)
    season: [
      { d: '2026-10-15', t: 'Saisonstart', p: 'Online' },
      { d: '2026-10-25', t: 'Showdown 1', p: 'München' },
      { d: '2026-11-14', t: 'Showdown 2', p: 'Berlin' },
      { d: '2026-12-20', t: 'Showdown 3', p: 'Dresden' },
      { d: '2027-01-22', t: 'Showdown 4', p: 'Köln' },
      { d: '2027-02-21', t: 'Showdown 5', p: 'Dortmund' },
      { d: '2027-03-12', t: 'FINALE', p: 'Hamburg' },
    ],
    ticker: [
      'Die Virtual Bundesliga ist zurück – Road to Hamburg!',
      'Willkommen zur Kiez-Watchparty im Discord',
      'Braun-weiß im Herzen: Wir supporten den FC St. Pauli eSports',
      'Finale am 12. & 13. März 2027 in Hamburg',
      'Nebenbei zocke ich selbst FC 26 – Tipps und Sprüche gern in den Voice!',
    ],
    social: 'DISCORD · KIEZ-WATCHPARTY',
    discord: {
      channel: 'VBL-Watchparty',
    },
    countdown: {
      target: '',
      headline: 'DIE VBL IST ZURÜCK',
      sub: 'Road to Hamburg · Die Watchparty startet gleich',
      done: 'ANSTOSS!',
    },
    pause: {
      headline: 'KURZE PAUSE',
      sub: 'Bin gleich zurück – quatscht ruhig weiter',
    },
    end: {
      headline: 'DANKE FÜRS DABEISEIN',
      sub: 'Bis zum nächsten Spieltag im Discord – Forza St. Pauli!',
    },
    show: {
      scoreboard: true,
      record: true,
      vblHeader: true,
      pip: true,
      vblTable: true,
      cam: true,
      voice: true,
      ticker: true,
    },
  };

  let bc = null;
  try { bc = new BroadcastChannel('stpauli-vbl'); } catch (e) { /* nicht verfügbar */ }

  const clone = (o) => JSON.parse(JSON.stringify(o));

  function merge(base, extra) {
    if (!extra || typeof extra !== 'object') return base;
    for (const k of Object.keys(extra)) {
      const b = base[k];
      const e = extra[k];
      if (b && typeof b === 'object' && !Array.isArray(b) && e && typeof e === 'object' && !Array.isArray(e)) {
        merge(b, e);
      } else {
        base[k] = e;
      }
    }
    return base;
  }

  const stateCbs = [];
  const eventCbs = [];
  let lastRev = -1;
  const seen = new Set();

  function load() {
    try {
      const raw = localStorage.getItem(KEY);
      if (raw) return merge(clone(DEFAULT), JSON.parse(raw));
    } catch (e) { /* kaputter Speicher -> Standard */ }
    return clone(DEFAULT);
  }

  function save(state) {
    state.rev = Date.now();
    lastRev = state.rev; // eigenes Speichern nicht als Fremd-Update behandeln
    try { localStorage.setItem(KEY, JSON.stringify(state)); } catch (e) { /* egal */ }
    if (bc) bc.postMessage({ kind: 'state', state });
  }

  function reset() {
    const s = clone(DEFAULT);
    save(s);
    return s;
  }

  function emit(ev) {
    ev.id = Date.now() + '-' + Math.random().toString(36).slice(2, 8);
    seen.add(ev.id);
    try { localStorage.setItem(EVT, JSON.stringify(ev)); } catch (e) { /* egal */ }
    if (bc) bc.postMessage({ kind: 'event', ev });
  }

  function pushState(s) {
    if (!s || s.rev === lastRev) return;
    lastRev = s.rev;
    const full = merge(clone(DEFAULT), s);
    stateCbs.forEach((cb) => cb(full));
  }

  function pushEvent(ev) {
    if (!ev || !ev.id || seen.has(ev.id)) return;
    seen.add(ev.id);
    eventCbs.forEach((cb) => cb(ev));
  }

  if (bc) {
    bc.onmessage = (m) => {
      if (m.data.kind === 'state') pushState(m.data.state);
      if (m.data.kind === 'event') pushEvent(m.data.ev);
    };
  }

  window.addEventListener('storage', (e) => {
    try {
      if (e.key === KEY && e.newValue) pushState(JSON.parse(e.newValue));
      if (e.key === EVT && e.newValue) pushEvent(JSON.parse(e.newValue));
    } catch (err) { /* egal */ }
  });

  // Alte Events beim Start nicht erneut abspielen
  try {
    const old = JSON.parse(localStorage.getItem(EVT) || 'null');
    if (old && old.id) seen.add(old.id);
  } catch (e) { /* egal */ }

  setInterval(() => {
    try {
      const raw = localStorage.getItem(KEY);
      if (raw) pushState(JSON.parse(raw));
      const ev = localStorage.getItem(EVT);
      if (ev) pushEvent(JSON.parse(ev));
    } catch (e) { /* egal */ }
  }, 700);

  function onState(cb) {
    stateCbs.push(cb);
    const s = load();
    lastRev = s.rev;
    cb(s);
  }

  function onEvent(cb) { eventCbs.push(cb); }

  return { DEFAULT, load, save, reset, emit, onState, onEvent, clone };
})();
