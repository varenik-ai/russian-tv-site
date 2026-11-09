#!/usr/bin/env python3
"""Текст баннера «Подпишись в Telegram» над плеером (RU/EN). Идемпотентно. Запускать после страниц-генераторов."""
import sys, os, glob
ROOT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else '.')
PAIRS = [
 ('</b> — запасной способ смотреть, если сайт станет недоступен</div>', '</b> — все каналы в одном приложении, бесплатно</div>'),
 ('</b> — a backup way to watch if the site goes down</div>', '</b> — all channels in one app, free</div>'),
]
n = 0
for f in glob.glob(os.path.join(ROOT, '**/*.html'), recursive=True):
    s = open(f, encoding='utf-8').read(); o = s
    for a, b in PAIRS: s = s.replace(a, b)
    if s != o: open(f, 'w', encoding='utf-8').write(s); n += 1
print('tgtext:', n, 'страниц изменено')
