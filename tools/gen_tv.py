#!/usr/bin/env python3
"""Страница /tv/ для браузера телевизора: список каналов (пульт), плеер, проверка всех каналов. Каналы берёт из index.html. Идемпотентно."""
import sys, os, re, json
ROOT = sys.argv[1]
home = open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read()
a = home.index('const CHANNEL_GROUPS = ['); b = home.index('\n];', a)
groups = []
for m in re.finditer(r"\{ label:'([^']*)'|\{ id:'([^']+)',\s*name:'([^']+)'", home[a:b]):
    if m.group(1): groups.append({'label': m.group(1), 'channels': []})
    else: groups[-1]['channels'].append({'id': m.group(2), 'name': m.group(3)})
pm = re.search(r'var PROXIES = \[(.*?)\];', home, re.S)
proxies = re.findall(r"https://[^'\"\s]+", pm.group(1))
HTML = r'''<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<meta name="robots" content="noindex, nofollow"/>
<meta name="referrer" content="no-referrer"/>
<title>Русское ТВ на телевизоре</title>
<style>
html{font-size:1.45vw}
*{box-sizing:border-box}
html,body{margin:0;height:100%;background:#0a0a14;color:#e8e8f0;font-family:-apple-system,'Segoe UI',Roboto,Arial,sans-serif;overflow:hidden}
#side{position:absolute;left:0;top:0;bottom:0;width:27%;background:#12121f;overflow-y:auto;padding:.6rem}
#main{position:absolute;left:27%;right:0;top:0;bottom:0}
body.full #side{display:none}
body.full #main{left:0}
body.full #info{display:none}
body.full #vbox{bottom:0}
#vbox{position:absolute;left:0;right:0;top:0;bottom:30%;background:#000}
video{width:100%;height:100%;display:block}
#info{position:absolute;left:0;right:0;bottom:0;height:30%;padding:.7rem 1rem;overflow-y:auto;font-size:.9rem;line-height:1.4}
#title{font-size:1.2rem;font-weight:700}
#status{color:#9a9ab0;margin:.15rem 0 .4rem}
#sum{white-space:pre-wrap}
#dev{color:#77778f;font-size:.72rem;margin-top:.4rem;word-break:break-all}
h1{font-size:1.1rem;margin:.2rem .4rem .5rem}
h2{font-size:.8rem;color:#9a9ab0;font-weight:700;margin:.8rem .4rem .3rem}
button{display:block;width:100%;text-align:left;background:#1c1c30;color:#e8e8f0;border:.15rem solid transparent;border-radius:.45rem;padding:.4rem .6rem;margin:.18rem 0;font:inherit;font-size:.92rem;cursor:pointer;outline:0}
button:focus{border-color:#fff;background:#2a5fd0}
button.cmd{background:#2a2a48;font-weight:700}
button.on{color:#7db4ff}
button .m{float:right}
.ok{color:#6fdc8c}.au{color:#ffc857}.bad{color:#ff6b6b}
</style>
</head>
<body>
<div id="side"><h1>Русское ТВ</h1><div id="list"></div></div>
<div id="main">
  <div id="vbox"><video id="v" autoplay playsinline></video></div>
  <div id="info"><div id="title">Выберите канал</div><div id="status">Кнопки пульта: вверх и вниз, ОК. Вправо: на весь экран, влево: список.</div><div id="sum"></div><div id="dev"></div></div>
</div>
<script>
var GROUPS = __GROUPS__;
var PROXIES = __PROXIES__;
</script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/hls.js/1.5.15/hls.min.js"></script>
<script>
(function () {
  var video = document.getElementById('v'), list = document.getElementById('list');
  var titleEl = document.getElementById('title'), statusEl = document.getElementById('status'), sumEl = document.getElementById('sum'), devEl = document.getElementById('dev');
  var ATTEMPT_MS = 12000, NEED_S = 2;
  var channels = [], results = {}, btns = {}, hls = null, timer = null, poll = null, run = 0, current = null, testing = false, testBtn, soundBtn;
  var sound = true;

  function lsGet(k) { try { return localStorage.getItem(k); } catch (e) { return null; } }
  function lsSet(k, v) { try { localStorage.setItem(k, v); } catch (e) {} }
  function setStatus(t) { statusEl.textContent = t; }

  try { results = JSON.parse(lsGet('rtv_tv_results') || '{}') || {}; } catch (e) { results = {}; }
  try { var cfg = new XMLHttpRequest(); cfg.open('GET', '/proxy.json'); cfg.onload = function () { try { var d = JSON.parse(cfg.responseText); if (d && d.urls && d.urls.length) PROXIES = d.urls; } catch (e) {} }; cfg.send(); } catch (e) {}

  function hlsOk() { return !!(window.Hls && Hls.isSupported()); }
  function nativeOk() { return !!video.canPlayType('application/vnd.apple.mpegurl'); }
  function attempts() {
    var a = [];
    if (hlsOk()) { a.push({ mode: 'hls', proxy: PROXIES[0] }); if (PROXIES[1]) a.push({ mode: 'hls', proxy: PROXIES[1] }); }
    if (nativeOk()) a.push({ mode: 'native', proxy: PROXIES[0] });
    return a;
  }
  function stop() {
    run++;
    clearTimeout(timer); clearInterval(poll);
    if (hls) { try { hls.destroy(); } catch (e) {} hls = null; }
    try { video.removeAttribute('src'); video.load(); } catch (e) {}
  }
  function startPlay() {
    video.muted = testing || !sound;
    var p = video.play();
    if (p && p.catch) p.catch(function () { video.muted = true; var q = video.play(); if (q && q.catch) q.catch(function () {}); });
  }
  // cb(итог): 'video' — есть картинка, 'audio' — идёт только звук, 'fail' — не запустился
  function play(ch, cb) {
    stop();
    var my = run, list2 = attempts(), i = 0, done = false;
    function finish(res, how) { if (done || my !== run) return; done = true; clearTimeout(timer); clearInterval(poll); cb(res, how); }
    function next(why) {
      if (done || my !== run) return;
      clearTimeout(timer); clearInterval(poll);
      if (hls) { try { hls.destroy(); } catch (e) {} hls = null; }
      if (i >= list2.length) { finish('fail', why || 'нет способа воспроизведения'); return; }
      var a = list2[i++], url = a.proxy + '/stream?channel=' + encodeURIComponent(ch.id), from = null;
      setStatus('Подключение: ' + (a.mode === 'hls' ? 'hls.js' : 'встроенный плеер') + '...');
      if (a.mode === 'hls') {
        hls = new Hls({ startLevel: 0, liveSyncDurationCount: 3, manifestLoadingMaxRetry: 1, levelLoadingMaxRetry: 1, fragLoadingMaxRetry: 2 });
        hls.on(Hls.Events.ERROR, function (ev, d) { if (d && d.fatal && my === run) { if (done) lost(my); else next('hls.js: ' + d.details); } });
        hls.loadSource(url); hls.attachMedia(video);
        hls.on(Hls.Events.MANIFEST_PARSED, startPlay);
      } else {
        video.onerror = function () { if (my !== run) return; if (done) lost(my); else next('встроенный плеер: ошибка ' + (video.error ? video.error.code : '?')); };
        video.src = url + '&native=1'; startPlay();
      }
      timer = setTimeout(function () { next('нет видео за ' + (ATTEMPT_MS / 1000) + ' с'); }, ATTEMPT_MS);
      poll = setInterval(function () {
        if (from === null) { if (video.currentTime > 0) from = video.currentTime; return; }
        var adv = video.currentTime - from;
        if (adv >= NEED_S && video.videoWidth > 0) finish('video', a.mode + ' ' + video.videoHeight + 'p');
        else if (adv >= NEED_S * 2) finish('audio', a.mode);
      }, 400);
    }
    video.onerror = null;
    next();
  }
  // поток оборвался во время просмотра: подключаемся заново
  function lost(my) { setStatus('Переподключение...'); setTimeout(function () { if (my === run && !testing && current) open(current); }, 3000); }
  function mark(ch) {
    var r = results[ch.id], b = btns[ch.id]; if (!b) return;
    var m = b.querySelector('.m');
    m.textContent = !r ? '' : r.r === 'video' ? '✓' : r.r === 'audio' ? '♪' : '✕';
    m.className = 'm ' + (!r ? '' : r.r === 'video' ? 'ok' : r.r === 'audio' ? 'au' : 'bad');
  }
  function summary() {
    var ok = 0, bad = [], au = [], seen = 0;
    channels.forEach(function (c) { var r = results[c.id]; if (!r) return; seen++; if (r.r === 'video') ok++; else if (r.r === 'audio') au.push(c.name); else bad.push(c.name); });
    if (!seen) { sumEl.textContent = ''; return; }
    sumEl.textContent = 'Проверено ' + seen + ' из ' + channels.length + '. С картинкой: ' + ok + '.' +
      (au.length ? '\nТолько звук: ' + au.join(', ') + '.' : '') + (bad.length ? '\nНе запустились: ' + bad.join(', ') + '.' : '');
  }
  function save(ch, res, how) { results[ch.id] = { r: res, h: how }; lsSet('rtv_tv_results', JSON.stringify(results)); mark(ch); summary(); }
  function open(ch) {
    testing = false; current = ch; titleEl.textContent = ch.name; lsSet('rtv_tv_last', ch.id);
    play(ch, function (res, how) {
      save(ch, res, how);
      if (res === 'video') setStatus('Идёт трансляция (' + how + ')');
      else if (res === 'audio') setStatus('Идёт только звук, картинки нет (' + how + ')');
      else setStatus('Канал не запустился: ' + how);
    });
  }
  function test() {
    if (testing) { testing = false; stop(); testBtn.textContent = '▶ Проверить все каналы'; setStatus('Проверка остановлена'); return; }
    testing = true; results = {}; channels.forEach(mark); summary(); testBtn.textContent = '■ Остановить проверку';
    var i = 0;
    (function step() {
      if (!testing) return;
      if (i >= channels.length) { testing = false; stop(); testBtn.textContent = '▶ Проверить все каналы'; titleEl.textContent = 'Проверка завершена'; setStatus('Сфотографируйте этот экран и пришлите результат.'); return; }
      var ch = channels[i++]; titleEl.textContent = 'Проверка ' + i + ' из ' + channels.length + ': ' + ch.name;
      play(ch, function (res, how) { save(ch, res, how); step(); });
    })();
  }
  function makeBtn(text, cls, fn) {
    var b = document.createElement('button'); b.type = 'button'; if (cls) b.className = cls; b.textContent = text;
    b.addEventListener('click', fn); list.appendChild(b); return b;
  }
  testBtn = makeBtn('▶ Проверить все каналы', 'cmd', test);
  soundBtn = makeBtn('🔊 Звук включён', 'cmd', function () { sound = !sound; video.muted = testing || !sound; soundBtn.textContent = sound ? '🔊 Звук включён' : '🔇 Звук выключен'; });
  GROUPS.forEach(function (g) {
    var h = document.createElement('h2'); h.textContent = g.label; list.appendChild(h);
    g.channels.forEach(function (c) {
      channels.push(c);
      var b = makeBtn('', '', function () { if (current === c && !testing && !document.body.classList.contains('full') && video.currentTime > 0) { document.body.classList.add('full'); return; } open(c); });
      var n = document.createElement('span'); n.textContent = c.name; b.appendChild(n);
      var m = document.createElement('span'); m.className = 'm'; b.appendChild(m);
      btns[c.id] = b; mark(c);
    });
  });
  summary();
  document.addEventListener('keydown', function (e) {
    var k = e.keyCode, full = document.body.classList.contains('full');
    if (full) {
      if (k === 37 || k === 27 || k === 461 || k === 10009 || k === 13) { document.body.classList.remove('full'); var f = current && btns[current.id]; if (f) f.focus(); e.preventDefault(); }
      return;
    }
    if (k === 39) { if (current) document.body.classList.add('full'); e.preventDefault(); return; }
    if (k !== 38 && k !== 40) return;
    e.preventDefault();
    var all = list.querySelectorAll('button'), idx = -1, i;
    for (i = 0; i < all.length; i++) if (all[i] === document.activeElement) idx = i;
    idx = k === 40 ? Math.min(idx + 1, all.length - 1) : Math.max(idx - 1, 0);
    all[idx].focus(); if (all[idx].scrollIntoView) all[idx].scrollIntoView({ block: 'center' });
  });
  devEl.textContent = 'hls.js: ' + (hlsOk() ? 'да' : 'нет') + ' · встроенный HLS: ' + (nativeOk() ? 'да' : 'нет') + ' · ' + navigator.userAgent;
  var last = lsGet('rtv_tv_last'), start = null;
  channels.forEach(function (c) { if (c.id === last) start = c; });
  (start && btns[start.id] || testBtn).focus();
  window.onerror = function (msg) { setStatus('Ошибка страницы: ' + msg); };
})();
</script>
</body>
</html>
'''
out = HTML.replace('__GROUPS__', json.dumps(groups, ensure_ascii=False)).replace('__PROXIES__', json.dumps(proxies))
os.makedirs(os.path.join(ROOT, 'tv'), exist_ok=True)
open(os.path.join(ROOT, 'tv/index.html'), 'w', encoding='utf-8').write(out)
print('tv:', sum(len(g['channels']) for g in groups), 'каналов,', len(proxies), 'прокси')
