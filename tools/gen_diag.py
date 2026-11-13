#!/usr/bin/env python3
"""Страница /diag/ (12.11.2026): диагностика доступности потоков из браузера зрителя (сообщение «из Болгарии не играют Первый, Россия 1, НТВ, МИР, Звезда»).
Проверки идут в браузере зрителя теми же запросами, что делает плеер: плейлист через воркер, плейлист напрямую у источника (direct.js),
первый сегмент напрямую (с CORS; при ошибке — без CORS, чтобы отличить сетевую блокировку от отсутствия заголовка CORS). Ничего не отправляется на сервер:
отчёт показывается на экране, его можно скопировать. Страница noindex, без рекламы и счётчиков. Идемпотентно (файл перезаписывается целиком)."""
import sys, os
ROOT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else '.')
HTML = r'''<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<meta name="robots" content="noindex, nofollow"/>
<title>Проверка потоков</title>
<style>
*{box-sizing:border-box}
body{margin:0;padding:16px;background:#0a0a14;color:#e8e8f0;font:15px/1.45 -apple-system,'Segoe UI',Roboto,Arial,sans-serif}
h1{font-size:20px;margin:0 0 6px}
p{margin:6px 0;color:#b8b8c8}
button{font:inherit;padding:12px 18px;margin:8px 8px 8px 0;border:0;border-radius:8px;background:#2a5fd0;color:#fff;cursor:pointer}
button[disabled]{opacity:.5}
pre{white-space:pre-wrap;word-break:break-word;background:#14141f;border-radius:8px;padding:12px;font:13px/1.5 ui-monospace,Menlo,Consolas,monospace;color:#e8e8f0}
.ok{color:#5fd38a}.bad{color:#ff7a7a}.warn{color:#ffc857}
</style>
</head>
<body>
<h1>Проверка потоков</h1>
<p>Страница проверяет из вашего браузера, достижимы ли источники каналов. Данные никуда не отправляются: результат показан ниже. Нажмите «Проверить», подождите около минуты и пришлите скриншот или скопированный отчёт.</p>
<button id="go">Проверить</button><button id="go2">Проверить запасные источники</button><button id="cp" disabled>Скопировать отчёт</button>
<pre id="out">Нажмите «Проверить».</pre>
<script>
(function () {
  var W = 'https://stream.russian-tv.com';
  var CH = [['perviy', 'Первый канал'], ['rossiya1', 'Россия 1'], ['ntv', 'НТВ'], ['zvezda', 'Звезда'], ['mir', 'МИР'],
            ['moskva24', 'Москва 24'], ['soyuz', 'Союз'], ['pyatyy', 'Пятый канал']];
  var out = document.getElementById('out'), go = document.getElementById('go'), cp = document.getElementById('cp'), text = [];
  function log(s, cls) { text.push(s); var d = document.createElement('div'); if (cls) d.className = cls; d.textContent = s; if (!out.firstChild || out.firstChild.nodeType === 3) out.textContent = ''; out.appendChild(d); }
  function t() { return performance.now(); }
  function tmo(ms) { var c = new AbortController(); setTimeout(function () { c.abort(); }, ms); return c.signal; }
  function fmt(r) { return (r.ok ? 'OK' : 'ОШИБКА') + ' ' + r.info + ' · ' + r.ms + ' мс'; }
  async function get(url, opt, readAll) {
    var t0 = t(), res = {ok: false, info: '', ms: 0, body: ''};
    try {
      var r = await fetch(url, Object.assign({signal: tmo(12000), cache: 'no-store'}, opt || {}));
      if (r.type === 'opaque') { res.ok = true; res.info = 'ответ получен (без CORS)'; }
      else {
        res.info = 'HTTP ' + r.status;
        if (readAll) res.body = await r.text();
        else { var rd = r.body.getReader(), c = await rd.read(); res.info += ', ' + (c.value ? c.value.length : 0) + ' байт'; try { rd.cancel(); } catch (e) {} }
        res.ok = r.ok;
      }
    } catch (e) { res.info = (e && e.name === 'AbortError') ? 'нет ответа за 12 с' : 'сетевая ошибка (' + (e && e.message) + ')'; }
    res.ms = Math.round(t() - t0); return res;
  }
  function firstUri(txt) { var l = txt.split('\n'); for (var i = 0; i < l.length; i++) { var s = l[i].trim(); if (s && s[0] !== '#') return s; } return ''; }
  async function one(id, name) {
    log('— ' + name + ' (' + id + ')');
    var m = await get(W + '/stream?channel=' + id, {}, true);
    log('  воркер, главный плейлист: ' + fmt(m), m.ok ? 'ok' : 'bad');
    if (!m.ok) return;
    var v = firstUri(m.body), body = m.body;
    if (/#EXT-X-STREAM-INF/.test(m.body) && v) {
      var vurl = /^https?:/.test(v) ? v : W + v;
      var w = await get(vurl, {}, true);
      log('  воркер, плейлист потока: ' + fmt(w), w.ok ? 'ok' : 'bad');
      if (!w.ok) return;
      body = w.body;
      var mm = /[?&]url=([^&]+)/.exec(vurl);
      if (mm) {
        var src = decodeURIComponent(mm[1]), host = (/^https?:\/\/([^\/]+)/.exec(src) || [])[1];
        var d = await get(src, {}, true);
        log('  напрямую у источника (' + host + '): ' + fmt(d), d.ok ? 'ok' : 'bad');
        if (!d.ok) { var d2 = await get(src, {mode: 'no-cors'}); log('    без CORS: ' + fmt(d2), d2.ok ? 'warn' : 'bad'); }
      }
    }
    var seg = firstUri(body);
    if (!/^https?:/.test(seg)) { log('  сегмент: не удалось определить адрес (' + (seg || 'пусто') + ')', 'warn'); return; }
    var sh = (/^https?:\/\/([^\/]+)/.exec(seg) || [])[1];
    var s = await get(seg);
    log('  сегмент (' + sh + '): ' + fmt(s), s.ok ? 'ok' : 'bad');
    if (!s.ok) { var s2 = await get(seg, {mode: 'no-cors'}); log('    без CORS: ' + fmt(s2), s2.ok ? 'warn' : 'bad'); }
  }
  var ALT = [['НТВ · cinerama 1023', 'https://stream8.cinerama.uz/1023/tracks-v1a1/mono.m3u8'],
             ['Россия 1 · cinerama 1020', 'https://stream8.cinerama.uz/1020/tracks-v1a1/mono.m3u8'],
             ['Россия 24 · cinerama 1021', 'https://stream8.cinerama.uz/1021/tracks-v1a1/mono.m3u8'],
             ['ТВЦ · cinerama 1025', 'https://stream8.cinerama.uz/1025/tracks-v1a1/mono.m3u8'],
             ['ТВЦ · ngenix', 'https://zabava-htlive.cdn.ngenix.net/hls/CH_TVC/variant.m3u8'],
             ['Россия Культура · cinerama 1048', 'https://stream8.cinerama.uz/1048/tracks-v1a1/mono.m3u8'],
             ['контроль: кино · cinerama 1055', 'https://stream8.cinerama.uz/1055/tracks-v1a1/mono.m3u8'],
             ['контроль: Россия 1 · smotrim', 'https://stream.smotrim.ru/hls2/russia_hd/playlist_1.m3u8']];
  async function alt(name, url) {
    log('— ' + name);
    var m = await get(url, {}, true), host = (/^https?:\/\/([^\/]+)/.exec(url) || [])[1];
    log('  плейлист (' + host + '): ' + fmt(m), m.ok ? 'ok' : 'bad');
    if (!m.ok) return;
    var body = m.body, cur = url;
    if (/#EXT-X-STREAM-INF/.test(body)) {
      cur = new URL(firstUri(body), url).href; var v = await get(cur, {}, true);
      log('  плейлист потока: ' + fmt(v), v.ok ? 'ok' : 'bad'); if (!v.ok) return; body = v.body;
    }
    var seg = new URL(firstUri(body), cur).href, sh = (/^https?:\/\/([^\/]+)/.exec(seg) || [])[1];
    var s = await get(seg);
    log('  сегмент (' + sh + '): ' + fmt(s), s.ok ? 'ok' : 'bad');
    if (!s.ok) { var s2 = await get(seg, {mode: 'no-cors'}); log('    без CORS: ' + fmt(s2), s2.ok ? 'warn' : 'bad'); return; }
    var t0 = t(), n = 0;
    try { var r = await fetch(seg, {signal: tmo(25000), cache: 'no-store'}), rd = r.body.getReader(), c;
      while (!(c = await rd.read()).done) n += c.value.length;
      var sec = (t() - t0) / 1000, kb = Math.round(n / 1024 / sec);
      log('  скорость полного сегмента: ' + Math.round(n / 1024) + ' КБ за ' + sec.toFixed(1) + ' с = ' + kb + ' КБ/с' + (kb < 300 ? ' (МЕДЛЕННО для HD)' : ''), kb < 300 ? 'warn' : 'ok');
    } catch (e) { log('  скорость полного сегмента: не удалось загрузить за 25 с (получено ' + Math.round(n / 1024) + ' КБ)', 'bad'); }
  }
  document.getElementById('go2').onclick = async function () {
    go.disabled = true; cp.disabled = true; text = []; out.textContent = '';
    log('Запасные источники. Время: ' + new Date().toISOString() + ' · пояс: ' + (Intl.DateTimeFormat().resolvedOptions().timeZone || '?'));
    log('Браузер: ' + navigator.userAgent);
    for (var i = 0; i < ALT.length; i++) { try { await alt(ALT[i][0], ALT[i][1]); } catch (e) { log('  сбой проверки: ' + e.message, 'bad'); } }
    log('Готово.'); go.disabled = false; cp.disabled = false;
  };
  go.onclick = async function () {
    go.disabled = true; cp.disabled = true; text = []; out.textContent = '';
    log('Время: ' + new Date().toISOString() + ' · пояс: ' + (Intl.DateTimeFormat().resolvedOptions().timeZone || '?'));
    log('Браузер: ' + navigator.userAgent);
    log('Язык: ' + navigator.language + ' · сеть: ' + ((navigator.connection && (navigator.connection.effectiveType + ', ' + navigator.connection.type)) || 'н/д'));
    for (var i = 0; i < CH.length; i++) { try { await one(CH[i][0], CH[i][1]); } catch (e) { log('  сбой проверки: ' + e.message, 'bad'); } }
    log('Готово.'); go.disabled = false; cp.disabled = false;
  };
  cp.onclick = function () { var s = text.join('\n'); try { navigator.clipboard.writeText(s).then(function () { cp.textContent = 'Скопировано'; }, function () { window.prompt('Скопируйте отчёт', s); }); } catch (e) { window.prompt('Скопируйте отчёт', s); } };
})();
</script>
</body>
</html>
'''
os.makedirs(os.path.join(ROOT, 'diag'), exist_ok=True)
open(os.path.join(ROOT, 'diag/index.html'), 'w', encoding='utf-8').write(HTML)
print('gen_diag: diag/index.html записан')
