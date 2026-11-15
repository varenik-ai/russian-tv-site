#!/usr/bin/env python3
"""15.11.2026: число каналов 54 -> 56 (добавлены «Россия РТР — Европа» и «Россия РТР — США»).
Предыдущие шаги (gen_seo -> 60, gen_remove_broken -> 54, gen_polish) приводят текст к 54; этот шаг идёт последним и меняет 54 на 56
со склонением («54 канала» -> «56 каналов»). Идемпотентен: после замены в тексте остаётся 56.
Не трогает CSS-проценты (54%) и числа вне контекста «каналы»."""
import sys, os, re, glob
ROOT = sys.argv[1]
OLD, NEW = 54, 56
NOUN = r'(?:канал(?:а|ов)?|телеканал(?:а|ов|ам)?|русск\w+|российск\w+|channels?|Channels?|Russian|live|TV|ТВ)'
rep = [
    (re.compile(r'\b54 (русских|российских) (канала|телеканала)\b'), r'56 \1 \2'.replace('канала', 'каналов')),
]
def fix(s):
    o = s
    s = re.sub(r'\b54 (русских|российских) канала\b', r'56 \1 каналов', s)
    s = re.sub(r'\b54 (русских|российских) телеканала\b', r'56 \1 телеканалов', s)
    s = re.sub(r'\b54 канала\b', '56 каналов', s)
    s = re.sub(r'\b54 телеканала\b', '56 телеканалов', s)
    s = re.sub(r'(?<![\d%.#:\-])\b54 (?=(?:русск|российск|телеканал|каналов|channels|Channels|Russian|Live|live|TV|ТВ))', '56 ', s)
    s = re.sub(r'(?<![\d%.#:\-])\b54 (?=Channels)', '56 ', s)
    s = s.replace('"numberOfItems": 54', '"numberOfItems": 56').replace('"numberOfItems":54', '"numberOfItems":56')
    return s
n = 0
for f in glob.glob(os.path.join(ROOT, '**/*'), recursive=True):
    if not f.endswith(('.html', '.md', '.xml', '.json', '.txt')) or '/node_modules/' in f or '/tools/' in f: continue
    try: s = open(f, encoding='utf-8').read()
    except Exception: continue
    t = fix(s)
    if t != s: open(f, 'w', encoding='utf-8').write(t); n += 1
print(f'gen_recount: файлов изменено {n}')
