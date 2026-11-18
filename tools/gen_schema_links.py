#!/usr/bin/env python3
"""18.11.2026: (1) BroadcastService JSON-LD на страницах основных каналов (RU+EN), (2) перелинковка: ссылки «Russian TV in USA/UK/Canada»
(«Русское ТВ в США/Великобритании/Канаде») в подвале всех страниц и в блоках «Related pages / Читайте также» статей блога. Идемпотентен."""
import sys, os, re, json
ROOT = sys.argv[1]
CH = {'perviy-kanal-live': ('Channel One Russia', 'Первый канал'), 'rossiya-1-live': ('Rossiya 1', 'Россия 1'), 'ntv-live': ('NTV', 'НТВ'),
      'rossiya-24-live': ('Rossiya 24', 'Россия 24'), 'tv-centr-live': ('TV Centre', 'ТВ Центр'),
      'rossiya-rtr-evropa-live': ('Rossiya RTR Europe', 'Россия РТР — Европа'), 'rossiya-rtr-usa-live': ('Rossiya RTR USA', 'Россия РТР — США')}
ORG = {'@type': 'Organization', 'name': 'Russian TV Online', 'url': 'https://russian-tv.com/'}
def rd(p): return open(os.path.join(ROOT, p), encoding='utf-8').read()
def wr(p, s): open(os.path.join(ROOT, p), 'w', encoding='utf-8').write(s)
changed = 0
# 1) BroadcastService
for slug, (en, ru) in CH.items():
    for lang, path in (('en', f'en/{slug}/index.html'), ('ru', f'{slug}/index.html')):
        if not os.path.exists(os.path.join(ROOT, path)): continue
        s = o = rd(path)
        url = f'https://russian-tv.com/{"en/" if lang == "en" else ""}{slug}/'
        svc = {'@type': 'BroadcastService', '@id': url + '#broadcast', 'name': en if lang == 'en' else ru, 'broadcastDisplayName': en if lang == 'en' else ru,
               'url': url, 'inLanguage': 'ru', 'broadcastTimezone': 'Europe/Moscow', 'provider': ORG}
        if lang == 'en': svc['areaServed'] = [{'@type': 'Country', 'name': n} for n in ('United States', 'United Kingdom', 'Canada')]
        def fix(m):
            try: d = json.loads(m.group(1))
            except Exception: return m.group(0)
            g = d.get('@graph')
            if not isinstance(g, list) or not any(x.get('@type') == 'WebPage' for x in g if isinstance(x, dict)): return m.group(0)
            g[:] = [x for x in g if not (isinstance(x, dict) and x.get('@type') == 'BroadcastService')] + [svc]
            return '<script type="application/ld+json">' + json.dumps(d, ensure_ascii=False, indent=2) + '</script>'
        s = re.sub(r'<script type="application/ld\+json">(.*?)</script>', fix, s, count=1, flags=re.S)
        if s != o: wr(path, s); changed += 1
# 2) перелинковка
EN = [('/en/russian-tv-in-usa/', 'Russian TV in the USA'), ('/en/russian-tv-in-uk/', 'Russian TV in the UK'), ('/en/russian-tv-in-canada/', 'Russian TV in Canada')]
RU = [('/russkie-kanaly-v-ssha/', 'Русское ТВ в США'), ('/russkie-kanaly-v-velikobritanii/', 'Русское ТВ в Великобритании'), ('/russkie-kanaly-v-kanade/', 'Русское ТВ в Канаде')]
for dp, dn, fs in os.walk(ROOT):
    dn[:] = [d for d in dn if d not in ('.git', 'tv', 'node_modules', 'assets')]
    if 'index.html' not in fs and '404.html' not in fs: continue
    for f in ('index.html', '404.html'):
        if f not in fs: continue
        path = os.path.relpath(os.path.join(dp, f), ROOT)
        s = o = rd(path)
        if '</footer>' not in s: continue
        en = path.startswith('en/')
        L = EN if en else RU
        fx = ('<div class="rtv-fx" style="text-align:center;margin-top:10px;font-size:12px;line-height:1.8">' + ' · '.join(f'<a href="{u}" style="color:#8b8ba0;text-decoration:underline">{t}</a>' for u, t in L) + '</div>\n')
        if 'class="rtv-fx"' in s: s = re.sub(r'<div class="rtv-fx".*?</div>\n', lambda m: fx, s, count=1, flags=re.S)
        else: s = s.replace('</footer>', fx + '</footer>', 1)
        if '/blog/' in path and 'class="related-links"' in s and 'data-fx' not in s:
            li = ''.join(f'<li data-fx><a href="{u}">{t}</a></li>' for u, t in L)
            if not any(u in s.split('class="related-links"')[1].split('</ul>')[0] for u, _ in L):
                s = re.sub(r'(<div class="related-links">.*?)(</ul>)', lambda m: m.group(1) + li + m.group(2), s, count=1, flags=re.S)
        if s != o: wr(path, s); changed += 1
print('gen_schema_links: страниц изменено', changed)
