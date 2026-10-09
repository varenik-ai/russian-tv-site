#!/usr/bin/env python3
"""Выравнивает числа каналов на RU-страницах категорий по реальному количеству карточек."""
import sys, os, re
ROOT = sys.argv[1]
def decl(n):
    if n % 10 == 1 and n % 100 != 11: return 'канал'
    if 2 <= n % 10 <= 4 and not 12 <= n % 100 <= 14: return 'канала'
    return 'каналов'
for cat in ('novosti', 'razvlecheniya', 'kino', 'detskie', 'muzyka', 'hobbi'):
    p = os.path.join(ROOT, cat, 'index.html'); s = open(p, encoding='utf-8').read(); o = s
    n = len(re.findall(r'class="cat-ch-card">', s))
    s = re.sub(r'(<span class="badge">)\d+ канал(?:а|ов)?(</span>)', lambda m: f'{m.group(1)}{n} {decl(n)}{m.group(2)}', s)
    s = re.sub(r'"numberOfItems": \d+', f'"numberOfItems": {n}', s)
    s = re.sub(r'\b\d+ новостных каналов', f'{n} новостных каналов', s)
    s = re.sub(r'\b\d+ каналов фильмов', f'{n} каналов фильмов', s)
    if s != o: open(p, 'w', encoding='utf-8').write(s); print(cat, n)
