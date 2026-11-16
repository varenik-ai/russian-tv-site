#!/usr/bin/env python3
"""16.11.2026: «Мой мир» — телемагазин, а не познавательный канал (сайт moymir.ru: «интернет-магазин товаров из рекламы», meta keywords «телемагазин»;
iptv-org: категория shop). Правит описания на страницах канала, в карточках категории и в данных главных (RU+EN). Идемпотентен."""
import sys, os, re
ROOT = sys.argv[1]
def rd(p): return open(os.path.join(ROOT, p), encoding='utf-8').read()
def wr(p, s): open(os.path.join(ROOT, p), 'w', encoding='utf-8').write(s)
n = 0
def put(p, s, o):
    global n
    if s != o: wr(p, s); n += 1
p = 'moy-mir-live/index.html'; s = rd(p); o = s
s = s.replace('познавательное ТВ', 'телемагазин').replace('«Мой мир» — познавательный телеканал: передачи о мире, науке и жизни.',
    '«Мой мир» — телеканал-магазин: в эфире показывают и продают товары для дома, красоты и здоровья (на сайте moymir.ru — интернет-магазин товаров из рекламы).')
put(p, s, o)
p = 'en/moy-mir-live/index.html'; s = rd(p); o = s
s = s.replace('Educational TV', 'TV Shopping').replace('educational TV', 'TV shopping').replace('Moy Mir is an educational channel with programmes about the world, science and life.',
    'Moy Mir is a TV shopping channel that presents and sells products for home, beauty and health (moymir.ru is an online store of advertised products).')
put(p, s, o)
for p, ru in (('hobbi/index.html', True), ('en/hobby/index.html', False)):
    s = rd(p); o = s
    nm, new = ('Мой мир', 'Телемагазин') if ru else ('Moy Mir', 'TV shopping')
    s = re.sub(r'(<div class="cat-ch-name">%s</div>\s*<div class="cat-ch-desc">)[^<]*' % re.escape(nm), lambda m: m.group(1) + new, s)
    put(p, s, o)
for p, ru in (('index.html', True), ('en/index.html', False)):
    s = rd(p); o = s
    new = 'Телемагазин' if ru else 'TV shopping'
    s = re.sub(r'(\{ id:[\'"]moymir[\'"].*?desc:\s*[\'"])[^\'"]*', lambda m: m.group(1) + new, s)
    put(p, s, o)
p = 'tools/gen_site.py'; s = open(os.path.join(ROOT, p), encoding='utf-8').read(); o = s
s = s.replace("'Мой мир','Moy Mir','Познавательное телевидение','Educational television'", "'Мой мир','Moy Mir','Телемагазин','TV shopping'")
s = s.replace("'познавательное ТВ','educational TV')", "'телемагазин','TV shopping')") if "'МИР','#00897b','#081412','познавательное ТВ'" in s else s
s = s.replace("'moymir': ('Познавательный телеканал: передачи о мире, науке и жизни.','An educational channel: programmes about the world, science and life.')",
              "'moymir': ('Телеканал-магазин: в эфире показывают и продают товары для дома, красоты и здоровья.','A TV shopping channel presenting and selling products for home, beauty and health.')")
if s != o: open(os.path.join(ROOT, p), 'w', encoding='utf-8').write(s)
print('gen_fix_moymir: файлов изменено', n)
