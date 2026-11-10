#!/usr/bin/env python3
"""Логотипы остальных каналов (скачаны с Wikimedia Commons 10.11.2026, лицензии указаны в assets/logos/SOURCES.md).
1) Копии для списков в assets/logos/trim/ (Viju: чёрные буквы заменены на белые, чтобы читались на тёмной плитке).
2) Значки в боковых списках всех страниц каналов (RU/EN) и в данных каналов на главных заменяются буквенных плиток на логотипы.
Идемпотентно. Запускать после gen_logos_trim.py и gen_layout.py."""
import sys, os, re, glob, shutil
ROOT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else '.')
# Кинокомедия и Родное кино (логотипы 8:1, в плитке 80x10 px нечитаемы) пока оставлены с буквенными плитками.
# slug канала -> файл в assets/logos/ (без trim/)
MAP = {
 'sankt-peterburg-live': 'logo-spb.png', 'moskva-24-live': 'logo-moskva24.png',
 'viju-tv-live': 'logo-viju-tv1000.svg', 'kino-detektiv-live': 'logo-viju-russian.svg',
 'kanal-360-live': 'logo-360.png', '360-novosti-live': 'logo-360.png', 'rt-documentary-live': 'logo-rt-doc.png',
 'viju-sport-live': 'logo-viju-sport.svg', 'vesti-fm-live': 'logo-vesti-fm.svg', 'fon-music-live': 'logo-fon-music.png',
 'flosports-hockey-live': 'logo-flosports.png', 'flosports-racing-live': 'logo-flosports.png',
 'trace-sport-stars-live': 'logo-trace-sport-stars.png',
}
src = os.path.join(ROOT, 'assets/logos'); out = os.path.join(src, 'trim'); os.makedirs(out, exist_ok=True)
for f in sorted(set(MAP.values())):
    s = os.path.join(src, f); d = os.path.join(out, f)
    if f.endswith('.svg'):
        t = open(s, encoding='utf-8').read().replace('fill="black"', 'fill="white"')   # чёрные буквы -> белые (Viju)
        if 'fill=' not in t.split('>', 2)[1] and 'vesti' in f:                       # Вести FM: чёрное по умолчанию -> белое
            t = t.replace('<svg ', '<svg fill="#fff" ', 1)
        open(d, 'w', encoding='utf-8').write(t)
    else:
        shutil.copyfile(s, d)
ITEM = {}
for slug, f in MAP.items():
    ITEM[slug] = re.compile(r'(<a href="/(?:en/)?' + re.escape(slug) + r'/" class="ch-item-s[^"]*" data-name="([^"]*)"[^>]*>)<div class="ch-icon-s" style="[^"]*">[^<]*</div>')
n = 0
for p in glob.glob(os.path.join(ROOT, '**/*.html'), recursive=True):
    s = o = open(p, encoding='utf-8').read()
    for slug, f in MAP.items():
        s = ITEM[slug].sub(lambda m: m.group(1) + '<div class="ch-icon-s ch-logo-s"><img src="/assets/logos/trim/' + f + '" alt="' + m.group(2) + '" loading="lazy"></div>', s)
    if os.path.relpath(p, ROOT) in ('index.html', 'en/index.html'):
        for slug, f in MAP.items():
            s = re.sub(r'(slug\s*:\s*([\'"])' + re.escape(slug) + r'\2)(?![^}\n]*logo\s*:)([^}\n]*?)(\s*\})', lambda m: m.group(1) + m.group(3) + ", logo:'/assets/logos/trim/" + f + "'" + m.group(4), s)
    if s != o: open(p, 'w', encoding='utf-8').write(s); n += 1
print('logos more:', n, 'страниц изменено,', len(MAP), 'каналов')
