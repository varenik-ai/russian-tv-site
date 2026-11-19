#!/usr/bin/env python3
"""19.11.2026: усиление внутренней перелинковки (в Search Console много страниц «обнаружена, не проиндексирована»).
 A) блок «Похожие каналы» на страницах индексируемых каналов (RU+EN): до 5 каналов той же рубрики со смещением по кругу, чтобы входящие ссылки распределялись ровно, + 2 гайда;
 B) в подвале всех страниц строка «Гайды» (главные статьи блога) — даёт блогу и статьям ссылки с каждой страницы сайта;
 C) в блоках «Related pages / Читайте также» статей блога — ещё до 3 гайдов того же языка.
Идемпотентен (маркеры <!--rtv-rel-->, class="rtv-fg", data-fg)."""
import sys, os, re
ROOT = sys.argv[1]
def rd(p): return open(os.path.join(ROOT, p), encoding='utf-8').read()
def wr(p, s): open(os.path.join(ROOT, p), 'w', encoding='utf-8').write(s)
RU_G = [('/blog/kak-smotret-russkoe-tv-za-granicey/', 'Как смотреть российское ТВ за границей'), ('/blog/kanal-ne-gruzitsya-chto-delat/', 'Канал не грузится: 8 способов'),
        ('/blog/vremya-po-moskve-v-chasovyh-pojasah-ssha/', 'Время по Москве в США'), ('/blog/kak-smotret-russkoe-tv-na-smart-tv/', 'Российское ТВ на Smart TV'),
        ('/blog/pervyy-kanal-rossiya-1-ntv-v-chem-raznica/', 'Первый канал, Россия 1 и НТВ: в чём разница'), ('/blog/kak-smotret-russkoe-tv-na-iphone-i-android/', 'Российское ТВ на iPhone и Android'),
        ('/blog/kak-smotret-russkoe-tv-v-kanade/', 'Как смотреть российское ТВ в Канаде'), ('/blog/kak-smotret-russkoe-tv-v-velikobritanii/', 'Как смотреть российское ТВ в Великобритании'),
        ('/blog/novogodnyaya-noch-russkoe-tv-za-granicey/', 'Российское ТВ в новогоднюю ночь за границей'), ('/blog/kakie-kanaly-smotret-po-temam/', 'Какие каналы смотреть: по темам'),
        ('/blog/gde-smotret-futbol-i-sport-na-russkih-kanalah/', 'Где смотреть футбол и спорт на русских каналах'), ('/blog/vesti-onlajn-poslednie-vypuski/', 'Вести онлайн: последние выпуски'), ('/blog/russkoe-tv-v-telegram-mini-app/', 'Российское ТВ в Telegram'), ('/blog/parad-pobedy-onlajn-za-granicey/', 'Парад Победы онлайн')]
EN_G = [('/en/blog/how-to-watch-russian-tv-in-usa/', 'How to Watch Russian TV in the USA'), ('/en/blog/channel-not-loading-fix/', 'Channel not loading: 8 fixes'),
        ('/en/blog/moscow-time-to-us-time-zones-russian-tv-schedule/', 'Moscow time in US time zones'), ('/en/blog/russian-tv-on-smart-tv-roku-chromecast-apple-tv/', 'Russian TV on Smart TV'),
        ('/en/blog/channel-one-vs-rossiya-1-vs-ntv/', 'Channel One vs Rossiya 1 vs NTV'), ('/en/blog/russian-tv-on-iphone-and-android/', 'Russian TV on iPhone and Android'),
        ('/en/blog/how-to-watch-russian-tv-in-canada/', 'How to Watch Russian TV in Canada'), ('/en/blog/how-to-watch-russian-tv-in-uk/', 'How to Watch Russian TV in the UK'),
        ('/en/blog/russian-tv-new-years-eve-usa-uk-canada/', "Russian TV on New Year's Eve"), ('/en/blog/russian-tv-channels-list-live/', 'List of Russian TV channels'), ('/en/blog/russian-tv-in-telegram-mini-app/', 'Russian TV in Telegram'), ('/en/blog/victory-day-parade-live-russian-tv-abroad/', 'Victory Day parade live')]
changed = 0
# --- A) похожие каналы
chan = {}
for d in sorted(os.listdir(ROOT)):
    if not (d.endswith('-live') and os.path.isdir(os.path.join(ROOT, d))): continue
    s = rd(d + '/index.html')
    if 'noindex' in s.lower()[:6000]: continue
    cat = re.search(r'<a href="([^"]*)" class="cat-tag">', s)
    h1 = re.search(r'<h1[^>]*>([^<]*)</h1>', s)
    if not cat or not h1: continue
    ru = re.sub(r'\s+смотреть онлайн бесплатно\s*$', '', h1.group(1)).strip()
    en = ru
    if os.path.exists(os.path.join(ROOT, 'en', d, 'index.html')):
        e = re.search(r'<h1[^>]*>([^<]*)</h1>', rd('en/' + d + '/index.html'))
        if e: en = re.sub(r'^Watch\s+|\s+Live Online Free\s*$', '', e.group(1)).strip()
    chan[d] = (cat.group(1), ru, en)
bycat = {}
for d, (c, _, _) in chan.items(): bycat.setdefault(c, []).append(d)
for c in bycat: bycat[c].sort()
CATN = {'novosti': ('Новости', 'News'), 'kino': ('Кино', 'Movies'), 'hobbi': ('Хобби и познавательные', 'Hobby'), 'sport': ('Спорт', 'Sport'),
        'razvlecheniya': ('Развлечения', 'Entertainment'), 'muzyka': ('Музыка', 'Music'), 'detskie': ('Детские', 'Kids')}
CATEN = {'novosti': '/en/news/', 'kino': '/en/movies/', 'hobbi': '/en/hobby/', 'sport': '/en/sport/', 'razvlecheniya': '/en/entertainment/', 'muzyka': '/en/music/', 'detskie': '/en/kids/'}
LS = 'style="color:#7db4ff;text-decoration:underline"'
for d, (c, ru, en) in chan.items():
    key = c.rstrip('/').split('/')[-1]
    lst = bycat[c]; i = lst.index(d)
    for lang in ('ru', 'en'):
        path = (d if lang == 'ru' else 'en/' + d) + '/index.html'
        if not os.path.exists(os.path.join(ROOT, path)): continue
        s = o = rd(path)
        base = '/' if lang == 'ru' else '/en/'
        # каналы, уже стоящие в блоке «Похожие каналы» (sim-box), не дублируем
        sim = set(re.findall(r'class="sim-item"', s) and re.findall(r'<a href="(?:/en)?/([a-z0-9-]+-live)/" class="sim-item"', s))
        order = [lst[(i + k) % len(lst)] for k in range(1, len(lst))]
        pick = [x for x in order if x not in sim][:5]
        links = ' · '.join(f'<a href="{base}{p}/" {LS}>{chan[p][1] if lang == "ru" else chan[p][2]}</a>' for p in pick)
        G = RU_G if lang == 'ru' else EN_G
        _r = (list(chan).index(d) * 2) % len(G); gl = ' · '.join(f'<a href="{u}" {LS}>{t}</a>' for u, t in [G[_r], G[(_r + 1) % len(G)]])
        cat_link = (c if lang == 'ru' else CATEN.get(key, '/en/'))
        cat_name = CATN.get(key, ('', ''))[0 if lang == 'ru' else 1]
        if lang == 'ru':
            ch_line = f'      <p>Ещё каналы рубрики <a href="{cat_link}" {LS}>{cat_name}</a>: {links}.</p>\n' if links else f'      <p>Все каналы рубрики: <a href="{cat_link}" {LS}>{cat_name}</a>.</p>\n'
            blk = (f'<!--rtv-rel-->\n    <div class="desc-box" style="margin-top:16px">\n      <h2>Смотрите также</h2>\n{ch_line}'
                   f'      <p>Полезные гайды: {gl}.</p>\n    </div>\n<!--/rtv-rel-->\n')
        else:
            ch_line = f'      <p>More channels in <a href="{cat_link}" {LS}>{cat_name}</a>: {links}.</p>\n' if links else f'      <p>All channels in <a href="{cat_link}" {LS}>{cat_name}</a>.</p>\n'
            blk = (f'<!--rtv-rel-->\n    <div class="desc-box" style="margin-top:16px">\n      <h2>You may also like</h2>\n{ch_line}'
                   f'      <p>Useful guides: {gl}.</p>\n    </div>\n<!--/rtv-rel-->\n')
        if '<!--rtv-rel-->' in s:
            s = re.sub(r'<!--rtv-rel-->.*?<!--/rtv-rel-->\n', lambda m: blk, s, count=1, flags=re.S)
        else:
            j = s.find('<div class="faq-box">')
            if j < 0: continue
            k = s.rfind('\n', 0, j)
            s = s[:k + 1] + '    ' + blk + '\n' + s[k + 1:]
        if s != o: wr(path, s); changed += 1
# --- B) подвал: строка «Гайды»  и  C) блоки related в статьях
_pages = []
for dp, dn, fs in os.walk(ROOT):
    dn[:] = [x for x in dn if x not in ('.git', 'tv', 'node_modules', 'assets')]
    for f in ('index.html', '404.html'):
        if f in fs: _pages.append(os.path.relpath(os.path.join(dp, f), ROOT))
_pages.sort()
_cnt = {'ru': 0, 'en': 0}
for path in _pages:
    if True:
        s = o = rd(path)
        if '</footer>' not in s: continue
        en = path.startswith('en/')
        G = EN_G if en else RU_G
        _l = 'en' if en else 'ru'; _o = _cnt[_l]; _cnt[_l] += 1
        _su = '/' + path.replace('index.html', '')
        FG = [x for x in (G[(_o * 4 + k) % len(G)] for k in range(len(G))) if x[0] != _su][:4]
        allg = ('/en/blog/', 'All guides') if en else ('/blog/', 'Все гайды')
        row = ('<div class="rtv-fg" style="text-align:center;margin-top:6px;font-size:12px;line-height:1.8">' + ('Guides: ' if en else 'Гайды: ') +
               ' · '.join(f'<a href="{u}" style="color:#8b8ba0;text-decoration:underline">{t}</a>' for u, t in [allg] + FG) + '</div>\n')
        CT = ([('/en/news/', 'News'), ('/en/movies/', 'Movies'), ('/en/entertainment/', 'Entertainment'), ('/en/music/', 'Music'), ('/en/sport/', 'Sport'), ('/en/kids/', 'Kids'), ('/en/hobby/', 'Hobby')] if en else
              [('/novosti/', 'Новости'), ('/kino/', 'Кино'), ('/razvlecheniya/', 'Развлечения'), ('/muzyka/', 'Музыка'), ('/sport/', 'Спорт'), ('/detskie/', 'Детские'), ('/hobbi/', 'Хобби')])
        crow = ('<div class="rtv-fc" style="text-align:center;margin-top:6px;font-size:12px;line-height:1.8">' + ('Categories: ' if en else 'Рубрики: ') +
                ' · '.join(f'<a href="{u}" style="color:#8b8ba0;text-decoration:underline">{t}</a>' for u, t in CT) + '</div>\n')
        row = crow + row
        s = re.sub(r'<div class="rtv-fc".*?</div>\n', '', s, count=1, flags=re.S)
        if 'class="rtv-fg"' in s: s = re.sub(r'<div class="rtv-fg".*?</div>\n', lambda m: row, s, count=1, flags=re.S)
        elif 'class="rtv-fx"' in s: s = re.sub(r'(<div class="rtv-fx".*?</div>\n)', lambda m: m.group(1) + row, s, count=1, flags=re.S)
        else: s = s.replace('</footer>', row + '</footer>', 1)
        if '/blog/' in path and path not in ('blog/index.html', 'en/blog/index.html') and 'class="related-links"' in s:
            self_url = '/' + path.replace('index.html', '')
            s = re.sub(r'<li data-fg>.*?</li>', '', s)
            seg = s.split('class="related-links"', 1)
            ul = seg[1].split('</ul>', 1)[0]
            extra = [(u, t) for u, t in G if u != self_url and u not in ul][:3]
            if extra:
                li = ''.join(f'<li data-fg><a href="{u}">{t}</a></li>' for u, t in extra)
                s = re.sub(r'(<div class="related-links">.*?)(</ul>)', lambda m: m.group(1) + li + m.group(2), s, count=1, flags=re.S)
        if s != o: wr(path, s); changed += 1
print('gen_internal_links: страниц изменено', changed)
