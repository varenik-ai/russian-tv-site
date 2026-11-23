#!/usr/bin/env python3
"""23.11.2026: список каналов слева от плеера на экранах 901-1024 px, как на главной (там список виден до 901 px).
Раньше на страницах каналов при ширине до 1024 px список прятался (.left-sidebar{display:none}) и оставалась только кнопка «Все каналы».
Идемпотентен: блок стилей между /*sidetab*/ и /*end-sidetab*/ пересоздаётся. Ниже 901 px поведение прежнее (кнопка «Все каналы»)."""
import sys, os, re, glob
ROOT = sys.argv[1]
CSS = ('<style>/*sidetab*/@media(min-width:901px) and (max-width:1024px){.page-wrap{grid-template-columns:260px minmax(0,1fr)!important}'
       '.left-sidebar{display:flex!important}.all-channels-cta{display:none!important}.ch-name-s{font-size:15px}}/*end-sidetab*/</style>')
BLK = re.compile(r'<style>/\*sidetab\*/.*?/\*end-sidetab\*/</style>', re.S)
n = 0
for f in glob.glob(os.path.join(ROOT, '**/index.html'), recursive=True):
    if '/tools/' in f or '/.git/' in f: continue
    s = o = open(f, encoding='utf-8').read()
    if '<aside class="left-sidebar"' not in s: continue
    s = BLK.sub(CSS, s) if '/*sidetab*/' in s else s.replace('</head>', CSS + '\n</head>', 1)
    if s != o: open(f, 'w', encoding='utf-8').write(s); n += 1
print('gen_sidebar_tablet: страниц изменено', n)
