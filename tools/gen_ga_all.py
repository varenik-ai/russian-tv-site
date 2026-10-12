#!/usr/bin/env python3
"""Подключает assets/consent.js (GA4, GTM, Метрика, Clarity) на все индексируемые страницы, где его ещё нет. Идемпотентно."""
import sys, os, glob
ROOT = sys.argv[1]
n = 0
for f in glob.glob(os.path.join(ROOT, '**/*.html'), recursive=True):
    rel = os.path.relpath(f, ROOT)
    if rel.startswith(('tools/', 'node_modules/', 'google')): continue
    s = open(f, encoding='utf-8').read()
    if 'noindex' in s or 'assets/consent.js' in s or '</head>' not in s: continue
    s = s.replace('</head>', '  <script src="/assets/consent.js?v=2"></script>\n</head>', 1)
    open(f, 'w', encoding='utf-8').write(s); n += 1; print('added:', rel)
print('pages updated:', n)
