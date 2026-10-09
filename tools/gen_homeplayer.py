#!/usr/bin/env python3
"""Главные страницы (RU/EN): тот же выбор качества и те же настройки hls.js, что на страницах каналов. Идемпотентно."""
import sys, os
ROOT = sys.argv[1]
OPTS = "{ startLevel:0, liveSyncDurationCount:3, enableWorker:true, backBufferLength:30, manifestLoadingMaxRetry:2, fragLoadingMaxRetry:3, levelLoadingMaxRetry:2 }"
def patch(path, subs):
    p = os.path.join(ROOT, path); s = open(p, encoding='utf-8').read(); o = s
    for old, new in subs:
        if new in s: continue
        if old not in s: print('MISSING in', path, ':', old[:60]); continue
        s = s.replace(old, new, 1)
    if '/assets/quality.js' not in s:
        s = s.replace('</body>', '<script defer src="/assets/quality.js?v=6"></script>\n</body>', 1)
    if s != o: open(p, 'w', encoding='utf-8').write(s); print('patched', path)
patch('index.html', [
  ("hls = new Hls({ liveSyncDurationCount:3, lowLatencyMode:true, enableWorker:true, backBufferLength:30 });", "hls = new Hls(" + OPTS + ");"),
  ("    hls.loadSource(streamUrl);\n    hls.attachMedia(video);\n", "    hls.loadSource(streamUrl);\n    hls.attachMedia(video);\n    try { window.rtvQuality && rtvQuality.attach(hls, video); } catch (e) {}\n"),
  ("    video.src = streamUrl;\n    video.addEventListener('loadedmetadata'", "    video.src = streamUrl;\n    try { window.rtvQuality && rtvQuality.attachNative(video, streamUrl); } catch (e) {}\n    video.addEventListener('loadedmetadata'"),
])
patch('en/index.html', [
  ("hls = new Hls({liveSyncDurationCount:3, lowLatencyMode:true, enableWorker:true});", "hls = new Hls(" + OPTS + ");"),
  ("    hls.loadSource(url); hls.attachMedia(video);\n", "    hls.loadSource(url); hls.attachMedia(video);\n    try { window.rtvQuality && rtvQuality.attach(hls, video); } catch (e) {}\n"),
  ("    video.src = url;\n    video.play().catch(function() { video.muted = true;", "    video.src = url;\n    try { window.rtvQuality && rtvQuality.attachNative(video, url); } catch (e) {}\n    video.play().catch(function() { video.muted = true;"),
])
