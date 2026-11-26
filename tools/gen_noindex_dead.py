#!/usr/bin/env python3
"""26.11.2026: страницы каналов без рабочего источника закрыты от индексации (noindex, follow) и убраны из sitemap.xml.
Каналы остаются в каталоге и списках (на случай, если источник оживёт), но поисковики не видят страниц с неработающим плеером.
РЕН ТВ, Матч ТВ, Пятница!: fs.uplink.kz отвечает 403 с 23.11.2026, другого источника нет.
Вернуть в индекс: убрать слаг из DEAD и пересобрать (gen_site/gen_audit_fixes заново добавят страницу в sitemap). Идёт последним. Идемпотентен."""
import sys, os, re
ROOT = sys.argv[1] if len(sys.argv) > 1 else '.'
DEAD = ['ren-tv-live', 'match-tv-live', 'pyatnica-live']
ROBOTS = '<meta name="robots" content="noindex, follow"/>'
n = 0
for slug in DEAD:
    for pre in ('', 'en/'):
        p = os.path.join(ROOT, pre + slug, 'index.html')
        if not os.path.exists(p): continue
        s = o = open(p, encoding='utf-8').read()
        s = re.sub(r'<meta name="robots"[^>]*>', ROBOTS, s, count=1)
        if ROBOTS not in s: s = s.replace('</title>', '</title>\n' + ROBOTS, 1)
        if s != o: open(p, 'w', encoding='utf-8').write(s); n += 1
p = os.path.join(ROOT, 'sitemap.xml'); s = o = open(p, encoding='utf-8').read()
SL = '|'.join(map(re.escape, DEAD))
s = re.sub(r'[ \t]*<url>(?:(?!</url>).)*?<loc>https://russian-tv\.com/(?:en/)?(?:%s)/</loc>.*?</url>\n?' % SL, '', s, flags=re.S)
if s != o: open(p, 'w', encoding='utf-8').write(s); n += 1
print('gen_noindex_dead: файлов изменено', n)
