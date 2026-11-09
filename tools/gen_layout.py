#!/usr/bin/env python3
"""Страницы каналов (RU/EN): колонка с плеером и баннерами сдвинута к списку каналов (освобождает место справа под рекламный блок),
названия каналов в списке +15 процентов (15 → 17,25 px), логотипы крупнее (40 → 52 px) на светлой плитке (в списке используются светлые
варианты логотипов из assets/logos/light/, см. gen_logos_light.py). Идемпотентно. Метка: /*rtvlayout2*/ (старая /*rtvlayout*/ заменяется)."""
import sys, os, glob, re
ROOT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else '.')
V1 = '/*rtvlayout*/@media(min-width:1025px){.main-col{margin:0!important}}.ch-name-s{font-size:17.25px}.ch-icon-s{width:52px;height:52px;border-radius:10px;font-size:13px}.ch-icon-s.ch-logo-s{background:#f1f4f9!important;padding:6px}.ch-icon-s:not(.ch-logo-s){background:#eef1f6!important}.ch-item-s.active .ch-icon-s{box-shadow:0 0 0 2px rgba(26,95,217,.55)}.ch-icon-s.ch-logo-s:has(img[src$="/ntv.svg"],img[src$="logo-zvezda.svg"],img[src$="logo-muz-tv.svg"]){background:#1b2a4a!important}'
CSS = (
 '/*rtvlayout2*/'
 '@media(min-width:1025px){.main-col{margin:0!important}}'
 '.ch-name-s{font-size:17.25px}'
 '.ch-icon-s{width:52px;height:52px;border-radius:10px;font-size:13px}'
 '.ch-icon-s.ch-logo-s{background:#f1f4f9!important;padding:6px}'
 '.ch-icon-s:not(.ch-logo-s){background:#eef1f6!important}'
 '.ch-item-s.active .ch-icon-s{box-shadow:0 0 0 2px rgba(26,95,217,.55)}'
)
LIGHT = set(os.listdir(os.path.join(ROOT, 'assets/logos/light'))) if os.path.isdir(os.path.join(ROOT, 'assets/logos/light')) else set()
ITEM = re.compile(r'(<a href="[^"]*" class="ch-item-s[^"]*"[^>]*>\s*<div class="ch-icon-s ch-logo-s"><img src=")/assets/logos/([^/"]+\.svg)"')
n = 0
for f in glob.glob(os.path.join(ROOT, '**/*.html'), recursive=True):
    s = o = open(f, encoding='utf-8').read()
    if 'class="left-sidebar"' not in s: continue
    s = ITEM.sub(lambda m: m.group(1) + ('/assets/logos/light/' if m.group(2) in LIGHT else '/assets/logos/') + m.group(2) + '"', s)
    if '/*rtvlayout2*/' not in s:
        s = s.replace(V1, '')
        i = s.find('.ch-icon-s{'); k = s.find('</style>', i)
        if i < 0 or k < 0: print('нет <style>:', os.path.relpath(f, ROOT))
        else: s = s[:k] + CSS + s[k:]
    if s != o: open(f, 'w', encoding='utf-8').write(s); n += 1
print('layout:', n, 'страниц изменено')
