#!/usr/bin/env python3
"""Красная полоса прокрутки у списка каналов слева от плеера (страницы каналов и главные RU/EN): широкая (10 px), с видимой дорожкой,
чтобы было видно, сколько прокручено. Chrome/Edge/Safari — ::-webkit-scrollbar, Firefox — scrollbar-color. Идемпотентно. Метка: /*rtvscroll*/."""
import sys, os, glob
ROOT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else '.')
S = '.ch-list-scroll,.channel-sidebar'
CSS = (
 '/*rtvscroll*/'
 + S + '{scrollbar-width:auto;scrollbar-color:auto}'
 '.ch-list-scroll::-webkit-scrollbar,.channel-sidebar::-webkit-scrollbar{display:block;width:10px}'
 '.ch-list-scroll::-webkit-scrollbar-track,.channel-sidebar::-webkit-scrollbar-track{background:rgba(255,255,255,.1);border-radius:5px}'
 '.ch-list-scroll::-webkit-scrollbar-thumb,.channel-sidebar::-webkit-scrollbar-thumb{background:#e53935;border-radius:5px;min-height:36px}'
 '.ch-list-scroll::-webkit-scrollbar-thumb:hover,.channel-sidebar::-webkit-scrollbar-thumb:hover{background:#ff5252}'
 '@supports not selector(::-webkit-scrollbar){' + S + '{scrollbar-width:auto;scrollbar-color:#e53935 rgba(255,255,255,.14)}}'
)
n = 0
for f in glob.glob(os.path.join(ROOT, '**/*.html'), recursive=True):
    s = open(f, encoding='utf-8').read()
    if '/*rtvscroll*/' in s: continue
    i = s.find('.ch-list-scroll{')
    if i < 0: i = s.find('.channel-sidebar {')
    if i < 0: i = s.find('.channel-sidebar{')
    if i < 0: continue
    k = s.find('</style>', i)
    if k < 0: print('нет <style>:', os.path.relpath(f, ROOT)); continue
    open(f, 'w', encoding='utf-8').write(s[:k] + CSS + s[k:]); n += 1
print('scrollbar:', n, 'страниц изменено')
