#!/usr/bin/env python3
"""15.11.2026: число каналов 54 -> 56 (добавлены «Россия РТР — Европа» и «Россия РТР — США»).
Предыдущие шаги (gen_seo -> 60, gen_remove_broken -> 54, gen_polish) приводят текст к 54; этот шаг идёт последним и меняет 54 на 56
со склонением («54 канала» -> «56 каналов»). Идемпотентен: после замены в тексте остаётся 56.
Не трогает CSS-проценты (54%) и числа вне контекста «каналы»."""
import sys, os, re, glob
ROOT = sys.argv[1]
OLD, NEW = 54, 60   # 19.11.2026: +СТС, РЕН ТВ, Матч ТВ, Пятница! (было 56)
NOUN = r'(?:канал(?:а|ов)?|телеканал(?:а|ов|ам)?|русск\w+|российск\w+|channels?|Channels?|Russian|live|TV|ТВ)'
rep = [
    (re.compile(r'\b(?:54|56) (русских|российских) (канала|телеканала)\b'), r'56 \1 \2'.replace('канала', 'каналов')),
]
def fix(s):
    o = s
    s = re.sub(r'\b(?:54|56) (русских|российских) канала\b', r'60 \1 каналов', s)
    s = re.sub(r'\b(?:54|56) (русских|российских) телеканала\b', r'60 \1 телеканалов', s)
    s = re.sub(r'\b(?:54|56) канала\b', '60 каналов', s)
    s = re.sub(r'\b(?:54|56) телеканала\b', '60 телеканалов', s)
    s = re.sub(r'(?<![\d%.#:\-])\b(?:54|56) (?=(?:русск|российск|телеканал|каналов|channels|Channels|Russian|Live|live|TV|ТВ))', '60 ', s)
    s = re.sub(r'(?<![\d%.#:\-])\b(?:54|56) (?=Channels)', '60 ', s)
    s = s.replace('"numberOfItems": 54', '"numberOfItems": 60').replace('"numberOfItems":54', '"numberOfItems":60').replace('"numberOfItems": 56', '"numberOfItems": 60').replace('"numberOfItems":56', '"numberOfItems":60')
    return s
n = 0
for f in glob.glob(os.path.join(ROOT, '**/*'), recursive=True):
    if not f.endswith(('.html', '.md', '.xml', '.json', '.txt')) or '/node_modules/' in f or '/tools/' in f: continue
    try: s = open(f, encoding='utf-8').read()
    except Exception: continue
    t = fix(s)
    if t != s: open(f, 'w', encoding='utf-8').write(t); n += 1
print(f'gen_recount: файлов изменено {n}')
