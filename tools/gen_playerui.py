#!/usr/bin/env python3
"""Подключает единый UI плеера (player-ui.js) на страницы каналов и главные (RU/EN). Идемпотентно."""
import sys, os, glob, re
ROOT = sys.argv[1]
n = 0
files = glob.glob(os.path.join(ROOT, '**/*-live/index.html'), recursive=True) + [os.path.join(ROOT, 'index.html'), os.path.join(ROOT, 'en/index.html')]
for f in files:
    s = open(f, encoding='utf-8').read(); o = s
    if '/assets/quality.js' not in s: continue
    s = re.sub(r'/assets/quality\.js\?v=\d+', '/assets/quality.js?v=6', s)
    if '/assets/player-ui.js' not in s:
        s = s.replace('<script defer src="/assets/quality.js?v=6"></script>', '<script defer src="/assets/player-ui.js?v=2"></script>\n<script defer src="/assets/quality.js?v=6"></script>', 1)
    if s != o: open(f, 'w', encoding='utf-8').write(s); n += 1
print('pages with unified player UI:', n)
