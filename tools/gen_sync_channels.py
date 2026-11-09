#!/usr/bin/env python3
"""Синхронизация каталога каналов сайта с мини-аппом. Идемпотентно. Запускать после gen_site.py и остальных страничных шагов.
1) «НТВ Хит» убран из боковых списков и каталога EN-главной: у воркера нет канала ntv_hit (/stream → 404), в мини-аппе его нет.
   Сама страница ntv-hit-live остаётся (noindex), ссылок на неё из каталога больше нет.
Россия-К есть только в мини-аппе намеренно (подтверждено владельцем 9.11.2026), на сайт не добавлять."""
import sys, os, glob, re
ROOT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else '.')
SIDE = re.compile(r'<a href="/(?:en/)?ntv-hit-live/" class="ch-item-s[^"]*"[^>]*>.*?</a>\n?', re.S)
EN_HOME = re.compile(r'[ \t]*\{ id:"ntv_hit"[^\n]*\},?\n')
CARD = re.compile(r'[ \t]*<a href="/en/ntv-hit-live/" class="cat-ch-card">.*?</a>\n\s*\n?', re.S)
LISTITEM = re.compile(r'[ \t]*\{\s*"@type": "ListItem",\s*"position": \d+,\s*"name": "NTV Hit",\s*"url": "[^"]*"\s*\},?\n', re.S)
# точечные правки текстов: (файл, что, на что)
TEXT = [
 ('blog/pervyy-kanal-rossiya-1-ntv-v-chem-raznica/index.html',
  ' Помимо основного канала, в подборке на сайте есть и его тематическое ответвление — <a href="/ntv-hit-live/">НТВ Хит</a>, ориентированное на развлекательный контент и повторы популярных проектов.', ''),
 ('en/blog/how-to-watch-russian-tv-in-usa/index.html', 'NTV, NTV Hit, TNT', 'NTV, TNT'),
 ('muzyka/index.html', 'Музыка Первого, НТВ-Хит.', 'Музыка Первого.'),
]
n = 0
for rel, a, b in TEXT:
    f = os.path.join(ROOT, rel)
    if os.path.exists(f):
        t = open(f, encoding='utf-8').read()
        if a in t: open(f, 'w', encoding='utf-8').write(t.replace(a, b)); n += 1
f = os.path.join(ROOT, 'en/news/index.html')
if os.path.exists(f):
    t = o = open(f, encoding='utf-8').read()
    if 'ntv-hit-live' in t:
        t = CARD.sub('', t); t = LISTITEM.sub('', t)
        def renum(m):
            c = iter(range(1, 100)); return re.sub(r'"position": \d+', lambda x: '"position": %d' % next(c), m.group(0))
        t = re.sub(r'"@type": "ItemList".*?\]\s*\}', renum, t, flags=re.S)
        t = t.replace('"numberOfItems": 15', '"numberOfItems": 14').replace('15 channels', '14 channels').replace('15 russian news channels', '14 russian news channels')
        t = t.replace('NTV, NTV Hit, Rossiya 24', 'NTV, Rossiya 24')
        open(f, 'w', encoding='utf-8').write(t); n += 1
for f in glob.glob(os.path.join(ROOT, '**/*.html'), recursive=True):
    s = open(f, encoding='utf-8').read(); o = s
    s = SIDE.sub('', s)
    if os.path.relpath(f, ROOT) == 'en/index.html': s = EN_HOME.sub('', s)
    if s != o: open(f, 'w', encoding='utf-8').write(s); n += 1
print('sync_channels:', n, 'страниц изменено')
