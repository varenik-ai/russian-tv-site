#!/usr/bin/env python3
"""Страница не должна «уезжать» вниз после выбора канала и прятать баннер над плеером. Идемпотентно.
1) Страницы каналов: активный канал в списке центрировался через scrollIntoView, а он прокручивает и окно (на ширине ~1440x800
   страница опускалась на 400+ px). Теперь прокручивается только сам список (.ch-list-scroll).
2) Главная: при выборе канала страница прокручивалась до верха плеера, баннер Telegram над плеером уходил за экран, теперь
   прокрутка идёт до верха баннера; активный пункт списка слева центрируется внутри списка, окно не двигается."""
import sys, os, glob, re
ROOT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else '.')
CH_OLD = re.compile(r"var active = document\.querySelector\('\.ch-item-s\.active'\);\s*if \(active\) active\.scrollIntoView\(\{block:'center', behavior:'auto'\}\);")
CH_NEW = ("var active = document.querySelector('.ch-item-s.active'), box = document.querySelector('.ch-list-scroll');\n"
          "  if (active && box) box.scrollTop = Math.max(0, active.getBoundingClientRect().top - box.getBoundingClientRect().top + box.scrollTop - box.clientHeight / 2 + active.offsetHeight / 2);")
H_PLAYER = "var el = document.getElementById('player-wrap');\n    var headerH"
H_PLAYER_NEW = "var el = document.querySelector('.tg-banner-desk') || document.getElementById('player-wrap');   // до баннера над плеером, а не до плеера\n    var headerH"
H_ITEM = "if (activeItem) activeItem.scrollIntoView({ behavior:'smooth', block:'nearest' });"
H_ITEM_NEW = "if (activeItem) sidebar.scrollTo({ top: Math.max(0, activeItem.getBoundingClientRect().top - sidebar.getBoundingClientRect().top + sidebar.scrollTop - sidebar.clientHeight / 2 + activeItem.offsetHeight / 2), behavior: 'smooth' });"
n = 0
for f in glob.glob(os.path.join(ROOT, '**/*.html'), recursive=True):
    s = o = open(f, encoding='utf-8').read()
    s = CH_OLD.sub(lambda m: CH_NEW, s)
    s = s.replace(H_PLAYER, H_PLAYER_NEW).replace(H_ITEM, H_ITEM_NEW)
    if s != o: open(f, 'w', encoding='utf-8').write(s); n += 1
print('noscroll:', n, 'страниц изменено')
