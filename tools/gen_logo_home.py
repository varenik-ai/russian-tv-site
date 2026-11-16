#!/usr/bin/env python3
"""16.11.2026: логотип в шапке («🇷🇺 Русское ТВ») на всех страницах ведёт на главную своего языка: RU — «/», EN — «/en/».
Главная RU раньше имела <div class="logo"> (не ссылка), на двух EN-страницах (/en/advertising/, /en/privacy/) логотип вёл на русскую главную. Идемпотентен."""
import sys, os, re, glob
ROOT = sys.argv[1]
n = 0
for f in glob.glob(os.path.join(ROOT, '**/*.html'), recursive=True):
    rel = os.path.relpath(f, ROOT)
    if rel.startswith(('node_modules', 'tools')): continue
    s = open(f, encoding='utf-8').read(); o = s
    home = '/en/' if rel.startswith('en/') else '/'
    # <div class="logo">…</div> -> ссылка на главную (внутри только span)
    s = re.sub(r'<div class="logo">(.*?)</div>', lambda m: f'<a href="{home}" class="logo" style="text-decoration:none">{m.group(1)}</a>', s, count=1, flags=re.S)
    # неверный адрес логотипа
    s = re.sub(r'<a href="[^"]*"( class="logo"[^>]*>)', lambda m: f'<a href="{home}"{m.group(1)}', s, count=1)
    if s != o: open(f, 'w', encoding='utf-8').write(s); n += 1
print('gen_logo_home: файлов изменено', n)
