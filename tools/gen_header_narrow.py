#!/usr/bin/env python3
"""Узкие телефоны (до 430 px): в шапке страниц стран/блога кнопка «Подписаться» остаётся значком Telegram без текста, ссылка EN
влезает в экран (раньше шапка выходила за правый край на 17 px, и страница прокручивалась по горизонтали). Идемпотентно."""
import sys, os, glob
ROOT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else '.')
STYLE = '<style id="hdr-narrow">@media(max-width:430px){header .tg-btn{font-size:0;gap:0;padding:8px 10px}header .lang-alt{margin-left:4px;padding:5px 10px}}</style>'
n = 0
for f in glob.glob(os.path.join(ROOT, '**/*.html'), recursive=True):
    s = open(f, encoding='utf-8').read()
    if 'lang-alt' not in s or 'id="hdr-narrow"' in s or '</head>' not in s: continue
    open(f, 'w', encoding='utf-8').write(s.replace('</head>', STYLE + '</head>', 1)); n += 1
print('header_narrow:', n, 'страниц изменено')
