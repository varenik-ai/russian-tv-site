#!/usr/bin/env python3
"""16.11.2026: счётчики (assets/consent.js: GA4 G-XLSJE8NKJE, Яндекс.Метрика, Clarity) на страницах, куда их раньше не подключали: /404.html (видно, по каким адресам приходят
несуществующие страницы) и /tv/ (браузер телевизора). Не подключаются сознательно: /diag/ (диагностика, ничего не отправляет), google*.html (файл подтверждения),
страницы-перенаправления (meta refresh: убранные каналы, /en/about/). Идемпотентен."""
import sys, os
ROOT = sys.argv[1]
TAG = '<script src="/assets/consent.js?v=3"></script>'
n = 0
for rel in ('404.html', 'tv/index.html'):
    p = os.path.join(ROOT, rel)
    if not os.path.exists(p): continue
    s = open(p, encoding='utf-8').read()
    if 'assets/consent.js' in s: continue
    if '</head>' not in s: print('нет </head> в', rel); continue
    s = s.replace('</head>', '  ' + TAG + '\n</head>', 1)
    open(p, 'w', encoding='utf-8').write(s); n += 1
print('gen_ga_extra: файлов изменено', n)
