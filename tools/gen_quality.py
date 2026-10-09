#!/usr/bin/env python3
"""Подключает селектор качества на страницах каналов. Идемпотентно."""
import sys, os, glob
ROOT = sys.argv[1]
n = no = 0
for f in glob.glob(os.path.join(ROOT, '**/*-live/index.html'), recursive=True):
    s = open(f, encoding='utf-8').read(); o = s
    if 'hls.attachMedia(video);' not in s:
        no += 1; continue
    if 'rtvQuality.attach' not in s:
        s = s.replace('hls.attachMedia(video);', 'hls.attachMedia(video);\n  try { window.rtvQuality && rtvQuality.attach(hls, video); } catch (e) {}', 1)
    if 'attachNative' not in s and "    video.src = url;\n    video.play().catch(function(){});" in s:
        s = s.replace("    video.src = url;\n    video.play().catch(function(){});", "    video.src = url;\n    try { window.rtvQuality && rtvQuality.attachNative(video, url); } catch (e) {}\n    video.play().catch(function(){});", 1)
    if '/assets/quality.js' not in s:
        s = s.replace('</body>', '<script defer src="/assets/quality.js?v=6"></script>\n</body>', 1)
    if s != o: open(f, 'w', encoding='utf-8').write(s); n += 1
print('pages with quality selector:', n, '| without hls player (stubs etc):', no)
