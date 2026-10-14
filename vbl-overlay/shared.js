/*
 * VBL Watchparty Overlay – gemeinsamer Zustand zwischen Steuerpult und Overlay.
 *
 * Synchronisiert über drei Wege, damit es in OBS (Browser-Dock + Browser-Quelle)
 * und im normalen Browser zuverlässig klappt:
 *   1. BroadcastChannel  (sofort)
 *   2. storage-Event     (sofort, andere Tabs/Fenster)
 *   3. Polling           (Fallback alle 700 ms)
 */
const VBL = (() => {
  const KEY = 'vbl-overlay-state-v1';
  const EVT = 'vbl-overlay-event-v1';

  const DEFAULT = {
    rev: 0,
    me: {
      label: 'FC 26 · Weekend League · Spiel 1',
      homeName: 'SODIX',
      homeTag: 'SDX',
      homeColor: '#ff1f45',
      homeScore: 0,
      awayName: 'GEGNER',
      awayTag: 'GEG',
      awayColor: '#2f7bff',
      awayScore: 0,
      goalAnim: true,
    },
    record: { w: 0, d: 0, l: 0 },
    vbl: {
      title: 'VIRTUELLE BUNDESLIGA',
      subtitle: 'Club Championship · Spieltag 1',
      matches: [
        { id: 'm1', home: 'FCB', away: 'BVB', hs: 0, as: 0, status: 'LIVE' },
        { id: 'm2', home: 'B04', away: 'RBL', hs: 0, as: 0, status: 'LIVE' },
        { id: 'm3', home: 'SGE', away: 'VFB', hs: 0, as: 0, status: 'LIVE' },
        { id: 'm4', home: 'SCF', away: 'BMG', hs: 0, as: 0, status: '20:00' },
        { id: 'm5', home: 'S04', away: 'HSV', hs: 0, as: 0, status: '20:00' },
      ],
    },
    ticker: [
      'Die Virtuelle Bundesliga ist zurück!',
      'Heute: VBL live schauen & parallel selbst FC zocken',
      'Folgt dem Kanal, damit ihr kein Tor verpasst',
    ],
    social: '@sodix2006',
    countdown: {
      target: '',
      headline: 'DIE VBL IST ZURÜCK',
      sub: 'Der Stream startet gleich',
      done: 'GLEICH GEHT’S LOS',
    },
    pause: {
      headline: 'KURZE PAUSE',
      sub: 'Bin gleich wieder da – VBL läuft weiter',
    },
    show: {
      scoreboard: true,
      record: true,
      vblHeader: true,
      pip: true,
      vblTable: true,
      cam: true,
      ticker: true,
    },
  };

  let bc = null;
  try { bc = new BroadcastChannel('vbl-overlay'); } catch (e) { /* nicht verfügbar */ }

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
    try { localStorage.setItem(EVT, JSON.stringify(ev)); } catch (e) { /* egal */ }
    if (bc) bc.postMessage({ kind: 'event', ev });
  }

  const stateCbs = [];
  const eventCbs = [];
  let lastRev = -1;
  const seen = new Set();

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
