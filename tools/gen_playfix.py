#!/usr/bin/env python3
"""Исправление цикличных перезагрузок канала (11.11.2026, НТВ), идемпотентно. Правит код плеера в страницах каналов (RU и EN).
Причины (воспроизведены на /ntv-live/: createHls в 0, 5, 20, 38, 59 с, пока видео не пошло):
1) Таймер «нет кадра за 8 с» после разбора манифеста планировал переподключение, а когда кадр приходил чуть позже,
   запланированный перезапуск не отменялся и пересоздавал рабочий поток. Теперь событие playing отменяет _retryTimer.
2) У медленных источников (НТВ: сегменты по 1-4 с, иногда 10 с) первый кадр приходит на 8-12-й секунде. Пока сегменты
   реально загружаются (FRAG_LOADED не старше 6 с), таймер продлевается шагами по 3 с, но не дольше 30 с с начала подключения.
3) (также на главных) Сторож зависания считал время от последнего прогресса, которое с момента загрузки страницы до нажатия «Смотреть»
   успевало устареть (> 12 с) и сразу пересоздавал поток; теперь отсчёт обнуляется при каждом (пере)подключении."""
import sys, os, re, glob
ROOT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else '.')
MARK = '/*playfix1*/'

OLD_TIMEOUT = ("    _playTimeout = setTimeout(function() {\n"
               "      if (_hlsStopped || video.readyState >= 3) return;\n"
               "      if (_tryNudgeGap()) {")
NEW_TIMEOUT = ("    _playTimeout = setTimeout(function _chk() {\n"
               "      if (_hlsStopped || video.readyState >= 3) return;\n"
               "      if (Date.now() - _lastFragAt < 6000 && Date.now() - _sessionStart < 30000) { _playTimeout = setTimeout(_chk, 3000); return; } " + MARK + "\n"
               "      if (_tryNudgeGap()) {")
OLD_PLAYING = "video.addEventListener('playing', function() {\n  clearTimeout(_playTimeout);\n"
NEW_PLAYING = OLD_PLAYING + "  clearTimeout(_retryTimer); // frame is playing: cancel a reconnect scheduled just before it\n"
OLD_PT = "var _playTimeout = null;\n"
NEW_PT = OLD_PT + "var _lastFragAt = 0;\n"
OLD_ATTACH = "  hls.attachMedia(video);\n"
NEW_ATTACH = OLD_ATTACH + "  hls.on(Hls.Events.FRAG_LOADED, function() { _lastFragAt = Date.now(); });\n"

n = 0
for f in glob.glob(os.path.join(ROOT, '*/index.html')) + glob.glob(os.path.join(ROOT, 'en/*/index.html')):
    s = open(f, encoding='utf-8').read()
    if '_playTimeout' not in s or MARK in s: continue
    o = s
    for a, b in ((OLD_TIMEOUT, NEW_TIMEOUT), (OLD_PLAYING, NEW_PLAYING), (OLD_PT, NEW_PT), (OLD_ATTACH, NEW_ATTACH)):
        if s.count(a) != 1: print('пропуск (нет якоря):', os.path.relpath(f, ROOT), a[:40].strip()); s = o; break
        s = s.replace(a, b)
    else:
        s2 = re.sub(r'(\n  _sessionStart = _nowTs;)', r'\n  _lastProgressTime = _nowTs; ' + MARK + r'\1', s, count=1)
        if s2 == s: print('пропуск (нет _sessionStart):', os.path.relpath(f, ROOT)); continue
        open(f, 'w', encoding='utf-8').write(s2); n += 1
# главные (RU и EN): тот же устаревающий отсчёт у сторожа зависания — обнуляем при каждом loadStream
for rel in ('index.html', 'en/index.html'):
    f = os.path.join(ROOT, rel)
    s = open(f, encoding='utf-8').read()
    if MARK in s or 'function loadStream' not in s: continue
    s2 = re.sub(r'(\n  _sessionStart = _nowTs;)', r'\n  _lastProgressTime = _nowTs; ' + MARK + r'\1', s, count=1)
    if s2 != s: open(f, 'w', encoding='utf-8').write(s2); n += 1
print('gen_playfix: страниц исправлено', n)
