#!/usr/bin/env python3
"""Страницы каналов и главные (RU/EN).
1) Страницы каналов: колонка с плеером и баннерами прижата к списку каналов (место справа под рекламный блок), колонка списка
   300 px, названия каналов 17,25 px (+15 процентов).
2) Значки каналов во всех списках: общий стиль assets/ch-icons.css (широкая тёмная плитка 92x52), логотипы без пустых полей
   (assets/logos/trim/, tools/gen_logos_trim.py). Подключается ссылкой на CSS и подменой адресов картинок.
Идемпотентно. Метка блока: /*rtvlayout3*/ (старые /*rtvlayout*/ и /*rtvlayout2*/ удаляются)."""
import sys, os, glob, re
ROOT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else '.')
OLD = ['/*rtvlayout*/@media(min-width:1025px){.main-col{margin:0!important}}.ch-name-s{font-size:17.25px}.ch-icon-s{width:52px;height:52px;border-radius:10px;font-size:13px}.ch-icon-s.ch-logo-s{background:#f1f4f9!important;padding:6px}.ch-icon-s:not(.ch-logo-s){background:#eef1f6!important}.ch-item-s.active .ch-icon-s{box-shadow:0 0 0 2px rgba(26,95,217,.55)}.ch-icon-s.ch-logo-s:has(img[src$="/ntv.svg"],img[src$="logo-zvezda.svg"],img[src$="logo-muz-tv.svg"]){background:#1b2a4a!important}', '/*rtvlayout2*/@media(min-width:1025px){.main-col{margin:0!important}}.ch-name-s{font-size:17.25px}.ch-icon-s{width:52px;height:52px;border-radius:10px;font-size:13px}.ch-icon-s.ch-logo-s{background:#f1f4f9!important;padding:6px}.ch-icon-s:not(.ch-logo-s){background:#eef1f6!important}.ch-item-s.active .ch-icon-s{box-shadow:0 0 0 2px rgba(26,95,217,.55)}']
CSS = (
 '/*rtvlayout3*/'
 '@media(min-width:1025px){.main-col{margin:0!important}.page-wrap{grid-template-columns:300px minmax(0,1fr)}}'
 '.ch-name-s{font-size:17.25px}'
)
LINK = '<link rel="stylesheet" href="/assets/ch-icons.css?v=6">'
TRIM = set(os.listdir(os.path.join(ROOT, 'assets/logos/trim'))) if os.path.isdir(os.path.join(ROOT, 'assets/logos/trim')) else set()
IMG = re.compile(r'(<img src=")/assets/logos/(?:light/|trim/)?([^/"]+\.svg)"')
JSLOGO = re.compile(r'(logo:\s*[\'"])/assets/logos/(?:light/|trim/)?([^/\'"]+\.svg)([\'"])')   # данные каналов в скриптах главных
n = 0
for f in glob.glob(os.path.join(ROOT, '**/*.html'), recursive=True):
    s = o = open(f, encoding='utf-8').read()
    has_icons = 'ch-icon-s' in s
    if not has_icons: continue
    s = IMG.sub(lambda m: m.group(1) + ('/assets/logos/trim/' if m.group(2) in TRIM else '/assets/logos/') + m.group(2) + '"', s)
    s = JSLOGO.sub(lambda m: m.group(1) + ('/assets/logos/trim/' if m.group(2) in TRIM else '/assets/logos/') + m.group(2) + m.group(3), s)
    if 'class="left-sidebar"' in s and '/*rtvlayout3*/' not in s:
        for v in OLD: s = s.replace(v, '')
        i = s.find('.ch-icon-s{'); k = s.find('</style>', i)
        if i < 0 or k < 0: print('нет <style>:', os.path.relpath(f, ROOT))
        else: s = s[:k] + CSS + s[k:]
    if 'assets/ch-icons.css' not in s and '</head>' in s:
        s = s.replace('</head>', LINK + '</head>', 1)
    if s != o: open(f, 'w', encoding='utf-8').write(s); n += 1
print('layout:', n, 'страниц изменено')
