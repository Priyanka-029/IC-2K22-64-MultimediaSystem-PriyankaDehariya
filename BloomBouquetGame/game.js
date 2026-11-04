'use strict';
/* BLOOM BOUQUET - HTML5 canvas version.
   Customization: WIND GUST event (edit CFG below to personalise). */
const CFG = { title: 'BLOOM BOUQUET', name: 'Your Name Here', lives: 3,
  windEvery: 15, windDur: 5, windStr: 150, tBase: 18, tPer: 6 };

const cv = document.getElementById('c'), ctx = cv.getContext('2d'), W = 800, H = 600, G = 535;
const FL = { rose: ['Rose'], tulip: ['Tulip'], sunflower: ['Sunflower'], daisy: ['Daisy'], lavender: ['Lavender'] };
const COL = { rose: '#e1284b', tulip: '#ff82be', sunflower: '#ffc81e', daisy: '#ffffff', lavender: '#a573e1' };
const KS = { bee: 1.4, wilted: .95, dew: .9 };
const NOTES = [392, 440, 523, 587, 523, 440, 392, 330];

// ---------- audio (Web Audio, no files) ----------
let AC, mute = false, ni = 0;
function snd(f, d = .15, s = 0, v = .15) {
  if (mute) return;
  try {
    AC = AC || new AudioContext();
    const o = AC.createOscillator(), g = AC.createGain(), n = AC.currentTime;
    o.frequency.setValueAtTime(f, n); o.frequency.linearRampToValueAtTime(Math.max(40, f + s * d), n + d);
    g.gain.setValueAtTime(v, n); g.gain.linearRampToValueAtTime(0, n + d);
    o.connect(g); g.connect(AC.destination); o.start(); o.stop(n + d);
  } catch (e) {}
}
setInterval(() => { if (state === 'play') snd(NOTES[ni++ % 8], .28, 0, .04); }, 300);

// ---------- drawing helpers ----------
const C = (x, y, r, f, s) => { ctx.beginPath(); ctx.arc(x, y, r, 0, 7); if (f) { ctx.fillStyle = f; ctx.fill(); } if (s) { ctx.strokeStyle = s; ctx.lineWidth = 1; ctx.stroke(); } };
const E = (x, y, rx, ry, f) => { ctx.beginPath(); ctx.ellipse(x, y, rx, ry, 0, 0, 7); ctx.fillStyle = f; ctx.fill(); };
const L = (x1, y1, x2, y2, c, w) => { ctx.strokeStyle = c; ctx.lineWidth = w; ctx.beginPath(); ctx.moveTo(x1, y1); ctx.lineTo(x2, y2); ctx.stroke(); };
function T(s, x, y, size, col = '#fff', al = 'center') {
  ctx.font = `bold ${size}px Arial`; ctx.textAlign = al; ctx.textBaseline = 'middle';
  ctx.fillStyle = 'rgba(0,0,0,.4)'; ctx.fillText(s, x + 2, y + 2); ctx.fillStyle = col; ctx.fillText(s, x, y);
}

function head(k, x, y, r) {
  if (k === 'daisy') { for (let i = 0; i < 10; i++) C(x + Math.cos(i * .628) * r * .65, y + Math.sin(i * .628) * r * .65, r * .38, '#fcfcfc', '#cdd'); C(x, y, r * .42, '#ffc828'); }
  else if (k === 'sunflower') { for (let i = 0; i < 14; i++) C(x + Math.cos(i * .449) * r * .74, y + Math.sin(i * .449) * r * .74, r * .3, '#ffc81e', '#d79600'); C(x, y, r * .52, '#784619'); }
  else if (k === 'rose') { C(x, y, r, '#a51230'); C(x, y, r * .82, '#e1284b'); C(x, y, r * .6, '#be1937'); C(x, y, r * .42, '#f04b69'); C(x, y, r * .2, '#a51230'); }
  else if (k === 'tulip') {
    ctx.beginPath(); ctx.moveTo(x - .9 * r, y - .2 * r); ctx.lineTo(x - .55 * r, y - r); ctx.lineTo(x, y - .3 * r);
    ctx.lineTo(x + .55 * r, y - r); ctx.lineTo(x + .9 * r, y - .2 * r); ctx.lineTo(x + .6 * r, y + .85 * r); ctx.lineTo(x - .6 * r, y + .85 * r);
    ctx.closePath(); ctx.fillStyle = '#f064a5'; ctx.fill(); E(x, y, .42 * r, .8 * r, '#ffa0cd');
  } else for (let j = 0; j < 7; j++) C(x + (j % 2 ? .22 : -.22) * r, y - r + j * .34 * r, .27 * r, j % 2 ? '#b98cf0' : '#9664d7');
}

function obj(k, x, y, a, t, s = 1) {
  ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s);
  if (FL[k]) { L(0, 5, 0, 34, '#328c3c', 4); E(8, 20, 8, 4, '#46aa4b'); head(k, 0, -13, k === 'lavender' ? 17 : 19); }
  else if (k === 'weed') { for (let i = 0; i < 12; i++) L(0, 0, Math.cos(i * .52) * 24, Math.sin(i * .52) * 24, '#286e28', 4); C(0, 0, 15, '#378c32', '#1e501e'); C(-4, -4, 6, '#55af46'); }
  else if (k === 'bee') { const w = (t * 14 | 0) % 2 ? -4 : 4; E(-8, -10 + w, 7, 9, 'rgba(200,230,255,.8)'); E(8, -10 + w, 7, 9, 'rgba(200,230,255,.8)'); E(0, 3, 17, 10, '#ffcd28'); ctx.fillStyle = '#1e1914'; [-7, 1, 9].forEach(q => ctx.fillRect(q, -6, 4, 18)); C(17, 3, 3, '#1e1914'); }
  else if (k === 'wilted') { ctx.strokeStyle = '#6e783c'; ctx.lineWidth = 4; ctx.beginPath(); ctx.moveTo(0, 34); ctx.lineTo(1, 16); ctx.lineTo(10, 6); ctx.stroke(); for (let i = 0; i < 8; i++) C(12 + Math.cos(i * .785) * 9, 12 + Math.sin(i * .785) * 9, 6, '#785537'); C(12, 12, 6, '#4b321e'); }
  else { ctx.fillStyle = '#5aaafa'; ctx.beginPath(); ctx.moveTo(0, -20); ctx.lineTo(13, 6); ctx.lineTo(-13, 6); ctx.fill(); C(0, 6, 13, '#5aaafa', '#96d2ff'); C(-5, 3, 3, '#fff'); }
  ctx.restore();
}

function basket(x, t) {
  if (inv > 0 && (t * 14 | 0) % 2) return;
  const y = H - 78;
  col.slice(-6).forEach((k, i) => { const fx = x - 30 + i * 11, fy = y + 8 - (i % 3) * 7; L(fx, fy + 4, fx, y + 24, '#328c3c', 3); head(k, fx, fy, 11); });
  ctx.fillStyle = '#aa733c'; ctx.beginPath(); ctx.moveTo(x - 44, y + 26); ctx.lineTo(x + 44, y + 26); ctx.lineTo(x + 32, y + 64); ctx.lineTo(x - 32, y + 64); ctx.fill();
  for (let i = 32; i < 64; i += 8) L(x - 40 + (i - 26) / 3, y + i, x + 40 - (i - 26) / 3, y + i, '#825528', 2);
  ctx.fillStyle = '#8c5c2d'; ctx.fillRect(x - 48, y + 22, 96, 9);
}

function bouquet(ks, cx, by, s) {
  const n = ks.length, h = [];
  ks.forEach((k, i) => {
    const a = (n > 1 ? (i / (n - 1) - .5) * 2 : 0) * .96, d = (95 + (i % 2) * 22) * s;
    const hx = cx + Math.sin(a) * d, hy = by - Math.cos(a) * d;
    L(cx, by, hx, hy, '#328c3c', 4 * s); h.push([hy, k, hx]);
  });
  h.sort((a, b) => a[0] - b[0]).forEach(([y, k, x]) => head(k, x, y, 21 * s));
  ctx.fillStyle = '#faebd7'; ctx.beginPath(); ctx.moveTo(cx - 40 * s, by - 28 * s); ctx.lineTo(cx + 40 * s, by - 28 * s); ctx.lineTo(cx + 9 * s, by + 72 * s); ctx.lineTo(cx - 9 * s, by + 72 * s); ctx.fill();
  ctx.fillStyle = '#eb4682';
  [-1, 1].forEach(d => { ctx.beginPath(); ctx.moveTo(cx, by - 6 * s); ctx.lineTo(cx + d * 26 * s, by - 20 * s); ctx.lineTo(cx + d * 26 * s, by + 8 * s); ctx.fill(); });
  C(cx, by - 6 * s, 6 * s, '#c01e5a');
}

// pre-rendered background
const bg = document.createElement('canvas'); bg.width = W; bg.height = H;
(function () {
  const b = bg.getContext('2d'), g = b.createLinearGradient(0, 0, 0, G);
  g.addColorStop(0, '#78c3f5'); g.addColorStop(1, '#d7f0ff'); b.fillStyle = g; b.fillRect(0, 0, W, G);
  const c = (x, y, r, f) => { b.beginPath(); b.arc(x, y, r, 0, 7); b.fillStyle = f; b.fill(); };
  c(690, 150, 62, '#fff5be'); c(690, 150, 42, '#ffe882');
  b.fillStyle = '#7fc66f'; b.beginPath(); b.ellipse(160, 550, 280, 130, 0, 0, 7); b.fill();
  b.fillStyle = '#6fba60'; b.beginPath(); b.ellipse(620, 570, 320, 130, 0, 0, 7); b.fill();
  b.fillStyle = '#5caa50'; b.fillRect(0, G, W, H - G);
  for (let i = 0; i < 140; i++) { const x = Math.random() * W, y = G + 4 + Math.random() * 60; b.strokeStyle = '#3e8a38'; b.lineWidth = 2; b.beginPath(); b.moveTo(x, y); b.lineTo(x + Math.random() * 6 - 3, y - 5 - Math.random() * 6); b.stroke(); }
  for (let i = 0; i < 26; i++) c(Math.random() * W, G + 10 + Math.random() * 50, 3, ['#fff', '#ffbed7', '#ffe16e'][i % 3]);
  for (let x = 0; x < W; x += 34) { b.fillStyle = '#faf5eb'; b.fillRect(x + 4, G - 38, 20, 44); b.beginPath(); b.moveTo(x + 4, G - 38); b.lineTo(x + 14, G - 50); b.lineTo(x + 24, G - 38); b.fill(); }
  b.fillStyle = '#ebe4d7'; b.fillRect(0, G - 24, W, 7);
})();

// ---------- game state ----------
let state = 'menu', mt = 0, score, lives, el, bq, lvl, spT, fl, pt, ft, pet, inv, shake, cel, lastB, lastBonus;
let wClock, wLeft, wDir = 1, wF, px = W / 2, tx = W / 2, useMouse = false, order, have, col, oT, oMax, newRec = false;
let best = +(localStorage.getItem('bloomBest') || 0);
const clouds = Array.from({ length: 5 }, () => ({ x: Math.random() * W, y: 110 + Math.random() * 190, v: 8 + Math.random() * 14, s: .7 + Math.random() * .7 }));
const keys = {};
const rnd = a => a[Math.random() * a.length | 0];

function reset() {
  score = 0; lives = CFG.lives; el = 0; bq = 0; lvl = 1; spT = .5; fl = []; pt = []; ft = []; pet = [];
  inv = shake = cel = 0; lastB = []; lastBonus = 0; wClock = wLeft = wF = 0; px = tx = W / 2; useMouse = false; newOrder();
}
function newOrder() {
  const n = Math.min(5, 2 + (bq / 2 | 0)), mc = bq < 3 ? 2 : 3, ks = Object.keys(FL).sort(() => Math.random() - .5).slice(0, n);
  order = {}; have = {}; col = [];
  ks.forEach(k => { order[k] = 1 + (Math.random() * mc | 0); have[k] = 0; });
  oMax = Math.min(75, CFG.tBase + Object.values(order).reduce((a, b) => a + b) * CFG.tPer); oT = oMax;
}
function start() { reset(); state = 'play'; snd(440, .3, 500); }
function endGame() {
  state = 'over'; snd(420, .9, -330, .25); newRec = score > best;
  if (newRec) { best = score; try { localStorage.setItem('bloomBest', best); } catch (e) {} }
}

// ---------- input ----------
addEventListener('keydown', e => {
  const k = e.key.toLowerCase();
  if (['arrowleft', 'arrowright', ' '].includes(k)) e.preventDefault();
  keys[k] = true;
  if (['arrowleft', 'arrowright', 'a', 'd'].includes(k)) useMouse = false;
  if (k === 'm') mute = !mute;
  if (state === 'menu' && (k === 'enter' || k === ' ')) start();
  else if (state === 'play' && (k === 'p' || k === 'escape')) state = 'pause';
  else if (state === 'pause' && (k === 'p' || k === 'escape' || k === 'enter')) state = 'play';
  else if (state === 'over') { if (k === 'r' || k === 'enter' || k === ' ') start(); else if (k === 'escape') state = 'menu'; }
});
addEventListener('keyup', e => { keys[e.key.toLowerCase()] = false; });
function pointerX(e) { const r = cv.getBoundingClientRect(); tx = (e.clientX - r.left) * W / r.width; useMouse = true; }
cv.addEventListener('pointermove', pointerX);
cv.addEventListener('pointerdown', e => {
  pointerX(e);
  if (state === 'menu' || state === 'over') start(); else if (state === 'pause') state = 'play';
});

// ---------- logic ----------
const burst = (x, y, c, n = 14) => { for (let i = 0; i < n; i++) { const a = Math.random() * 6.28, v = 60 + Math.random() * 180, l = .4 + Math.random() * .5; pt.push({ x, y, vx: Math.cos(a) * v, vy: Math.sin(a) * v - 60, l, m: l, c }); } };
const pop = (s, x, y, c) => ft.push({ s, x, y, c, l: 1 });

function spawn() {
  const w = [60, 10 + Math.min(lvl * 2, 14), 4 + Math.min(lvl * 2, 12), 9, 4], c = ['f', 'weed', 'bee', 'wilted', 'dew'];
  let r = Math.random() * w.reduce((a, b) => a + b), i = 0; while ((r -= w[i]) > 0) i++;
  let k = c[i];
  if (k === 'f') { const nd = Object.keys(order).filter(q => have[q] < order[q]); k = nd.length && Math.random() < .6 ? rnd(nd) : rnd(Object.keys(FL)); }
  fl.push({ k, x: 30 + Math.random() * (W - 60), y: -40, sp: (135 + lvl * 14) * (KS[k] || 1) * (.85 + Math.random() * .35), ph: Math.random() * 6.28, a: 0 });
}

function catchIt(f) {
  const k = f.k, x = f.x, y = f.y;
  if (FL[k]) {
    if (have[k] < order[k]) {
      have[k]++; col.push(k); score += 10; burst(x, y, COL[k]); pop('+10', x, y, '#ffd73c'); snd(700, .14, 700);
      if (Object.keys(order).every(q => have[q] >= order[q])) {
        lastBonus = 50 + Math.round(oT) * 2; score += lastBonus; bq++; lvl = 1 + bq; lastB = col.slice(); cel = 2.8; fl = [];
        [523, 659, 784, 1047].forEach((f2, i) => setTimeout(() => snd(f2, .15), i * 120));
      }
    } else { score = Math.max(0, score - 5); burst(x, y, '#999', 8); pop('Not in order -5', x, y, '#e05a5a'); snd(240, .22, -60); }
  } else if (k === 'wilted') {
    score = Math.max(0, score - 10); burst(x, y, '#785537', 12);
    if (col.length) { have[col.pop()]--; pop('Wilted! -1 flower', x, y, '#be7846'); } else pop('Wilted -10', x, y, '#be7846');
    snd(240, .22, -60);
  } else if (k === 'dew') { oT = Math.min(oMax, oT + 8); burst(x, y, '#78beff'); pop('+8 sec', x, y, '#82c8ff'); snd(900, .25, -400); }
  else if (inv <= 0) { lives--; score = Math.max(0, score - 10); inv = 1.2; shake = .35; burst(x, y, k === 'bee' ? '#ffc83c' : '#46963c', 22); pop('OUCH! -10', x, y, '#e63c3c'); snd(170, .35, -100, .3); }
}

function update(dt, t) {
  clouds.forEach(c => { c.x += c.v * dt * (wLeft > 0 ? 3 : 1) * wDir; if (c.x > W + 100) c.x = -100; if (c.x < -100) c.x = W + 100; });
  if (state === 'menu') { mt += dt; return; }
  if (state !== 'play') return;
  el += dt;
  if (keys.arrowleft || keys.a) tx = px -= 540 * dt;
  if (keys.arrowright || keys.d) tx = px += 540 * dt;
  if (useMouse) px += (tx - px) * Math.min(1, 14 * dt);
  px = tx = Math.max(52, Math.min(W - 52, px));

  pt.forEach(p => { p.x += p.vx * dt; p.y += p.vy * dt; p.vy += 220 * dt; p.l -= dt; }); pt = pt.filter(p => p.l > 0);
  ft.forEach(f => { f.y -= 50 * dt; f.l -= dt; }); ft = ft.filter(f => f.l > 0);
  pet.forEach(p => { p.x += p.vx * dt; p.y += Math.sin(t * 6 + p.ph) * 60 * dt; }); pet = pet.filter(p => p.x > -40 && p.x < W + 40);
  shake = Math.max(0, shake - dt); inv = Math.max(0, inv - dt);

  if (cel > 0) {
    cel -= dt;
    if (Math.random() < .6) burst(250 + Math.random() * 300, 200 + Math.random() * 220, rnd(['#ffd73c', '#ff96c8', '#fff']), 2);
    if (cel <= 0) newOrder();
    return;
  }

  // wind gust event (customization)
  if (wLeft > 0) {
    wLeft -= dt; wF = wLeft > 0 ? wDir * CFG.windStr * Math.sin(Math.PI * (1 - wLeft / CFG.windDur)) : 0;
    if (Math.random() < .55) pet.push({ x: wDir > 0 ? -20 : W + 20, y: 110 + Math.random() * 400, vx: wDir * (320 + Math.random() * 200), ph: Math.random() * 6, c: rnd(['#ffaac8', '#fff', '#82c86e', '#ffdc78']) });
  } else if ((wClock += dt) >= CFG.windEvery) { wClock = 0; wLeft = CFG.windDur; wDir = rnd([-1, 1]); snd(260, .9, 120, .12); }

  if ((oT -= dt) <= 0) { lives--; shake = .35; pop("TIME'S UP!", W / 2, 190, '#e63c3c'); snd(170, .35, -100, .3); newOrder(); }
  if ((spT -= dt) <= 0) { spawn(); spT = Math.max(.28, .85 - (lvl - 1) * .05); }

  const mult = 1 + (lvl - 1) * .06, bt = H - 78;
  fl.forEach(f => {
    if (cel > 0) return;
    f.y += f.sp * mult * dt;
    f.x = Math.max(26, Math.min(W - 26, f.x + wF * .9 * dt + (f.k === 'bee' ? Math.sin(t * 5 + f.ph) * 140 * dt : 0)));
    f.a = f.k === 'weed' ? f.a + dt * 2 : (FL[f.k] || f.k === 'wilted') ? Math.sin(t * 3 + f.ph) * .31 : 0;
    if (Math.abs(f.x - px) < 48 && f.y + 14 > bt + 10 && f.y - 14 < bt + 32) { f.dead = 1; catchIt(f); }
  });
  fl = fl.filter(f => !f.dead && f.y < H + 40);
  if (lives <= 0) endGame();
}

// ---------- screens ----------
function hud(t) {
  T('SCORE ' + score, 14, 22, 26, '#fff', 'left'); T('BEST ' + best, 16, 48, 16, '#fff', 'left'); T('Bouquets: ' + bq, 16, 70, 19, '#ffebf5', 'left');
  for (let i = 0; i < lives; i++) { ctx.fillStyle = '#ff466e'; ctx.font = '28px Arial'; ctx.textAlign = 'right'; ctx.fillText('♥', W - 14 - i * 28, 24); }
  T('LEVEL ' + lvl, W - 14, 52, 19, '#ffd73c', 'right'); T(`TIME ${String(el / 60 | 0).padStart(2, '0')}:${String(el % 60 | 0).padStart(2, '0')}`, W - 14, 76, 16, '#fff', 'right');
  ctx.fillStyle = 'rgba(35,55,40,.75)'; ctx.beginPath(); ctx.roundRect(205, 4, 390, 98, 12); ctx.fill(); ctx.strokeStyle = '#fff0c8'; ctx.lineWidth = 2; ctx.stroke();
  T('BOUQUET ORDER #' + (bq + 1), 400, 17, 16, '#ffd73c');
  const ks = Object.keys(order), x0 = 400 - ks.length * 38;
  ks.forEach((k, i) => {
    const sx = x0 + i * 76, ok = have[k] >= order[k];
    obj(k, sx + 18, 52, 0, t, .55); T(have[k] + '/' + order[k], sx + 54, 50, 19, ok ? '#8cffa0' : '#fff'); if (ok) T('OK', sx + 54, 68, 15, '#8cffa0');
  });
  const f = Math.max(0, oT / oMax);
  ctx.fillStyle = '#1e281e'; ctx.fillRect(217, 88, 366, 8); ctx.fillStyle = f > .5 ? '#5ad264' : f > .25 ? '#f0c83c' : '#eb5046'; ctx.fillRect(217, 88, 366 * f, 8);
  if (wLeft > 0) { const a = wDir > 0 ? '>>>' : '<<<'; T(`${a} WIND GUST ${a}`, W / 2, 124, 19); }
}

function overlay(title, sub, c) { ctx.fillStyle = c; ctx.fillRect(0, 0, W, H); T(title, W / 2, H / 2 - 20, 60); T(sub, W / 2, H / 2 + 40, 24, '#dcf0dc'); }

function menu() {
  T(CFG.title, W / 2, 70 + Math.sin(mt * 2) * 7, 60, '#fffaf5'); T('Catch flowers. Fill the order. Make the bouquet!', W / 2, 125, 24, '#fff5fa');
  ctx.fillStyle = 'rgba(30,55,40,.6)'; ctx.beginPath(); ctx.roundRect(30, 150, W - 60, 250, 14); ctx.fill();
  Object.keys(FL).forEach((k, i) => { obj(k, 100 + i * 150, 205, 0, mt); T(FL[k][0], 100 + i * 150, 252, 16); });
  T('Collect the flowers on the ORDER card:  +10 each', W / 2, 278, 19, '#ffd73c');
  [['weed', 'Weed  -1 life'], ['bee', 'Bee  -1 life'], ['wilted', 'Wilted  -1 flower'], ['dew', 'Dew drop  +8 sec']].forEach(([k, s], i) => { obj(k, 80 + i * 190, 345, 0, mt, .75); T(s, 112 + i * 190, 345, 16, '#fff', 'left'); });
  T('Move: LEFT / RIGHT or A / D or the MOUSE / touch', W / 2, 428, 19); T('Pause: P     Mute: M', W / 2, 456, 19);
  T('WIND GUSTS blow everything sideways - plan ahead!', W / 2, 484, 19, '#fffabe');
  if ((mt * 2 | 0) % 2 === 0) T('Press ENTER or tap to START', W / 2, 530, 36);
  T('Best: ' + best, 14, H - 18, 16, '#fff', 'left'); T('By ' + CFG.name, W - 14, H - 18, 16, '#fff', 'right');
}

function over() {
  ctx.fillStyle = 'rgba(25,10,20,.78)'; ctx.fillRect(0, 0, W, H);
  T('SHOP CLOSED', W / 2, 130, 60, '#ff8296'); T('Score: ' + score, W / 2, 215, 38);
  T(newRec ? 'NEW HIGH SCORE!' : 'Best: ' + best, W / 2, 262, 26, newRec ? '#ffd73c' : '#e6e6f5');
  T(`Bouquets made: ${bq}   |   Time played: ${el | 0}s`, W / 2, 310, 19, '#e6e6f5');
  if (lastB.length) bouquet(lastB, W / 2, 395, .8);
  T('Press R / ENTER / tap to PLAY AGAIN', W / 2, 520, 26); T('ESC - main menu', W / 2, 556, 19, '#c8c8e1');
}

function draw(t) {
  ctx.save();
  if (shake > 0) ctx.translate((Math.random() - .5) * 12, (Math.random() - .5) * 12);
  ctx.drawImage(bg, 0, 0);
  clouds.forEach(c => [[0, 0, 26], [26, -8, 32], [58, 0, 26], [28, 8, 24]].forEach(([dx, dy, r]) => C(c.x + dx * c.s, c.y + dy * c.s, r * c.s, '#fff')));
  if (state === 'menu') menu();
  else {
    fl.forEach(f => obj(f.k, f.x, f.y, f.a, t)); basket(px, t);
    pet.forEach(p => E(p.x, p.y, 6, 3.5, p.c)); pt.forEach(p => C(p.x, p.y, Math.max(1, 5 * p.l / p.m), p.c));
    ft.forEach(f => { ctx.globalAlpha = Math.max(0, f.l); T(f.s, f.x, f.y, 19, f.c); ctx.globalAlpha = 1; });
    hud(t);
    if (cel > 0) {
      ctx.fillStyle = 'rgba(20,30,20,.47)'; ctx.fillRect(0, 0, W, H);
      bouquet(lastB, W / 2, 400, 1.5 * (1 + .04 * Math.sin(t * 8)));
      T(`BOUQUET #${bq} READY!`, W / 2, 170, 38, '#ffd73c'); T('Bonus +' + lastBonus, W / 2, 214, 26);
    }
    if (state === 'pause') overlay('PAUSED', 'Press P / ESC or tap to resume', 'rgba(10,25,15,.65)');
    if (state === 'over') over();
  }
  ctx.restore();
}

// ---------- main loop ----------
reset(); state = 'menu';
let last = performance.now();
(function loop(now) {
  const dt = Math.min((now - last) / 1000, .05); last = now;
  update(dt, now / 1000); draw(now / 1000);
  requestAnimationFrame(loop);
})(last);
