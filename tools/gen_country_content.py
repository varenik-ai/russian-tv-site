#!/usr/bin/env python3
"""18.11.2026: полноценный контент страниц США / Великобритании / Канады (RU+EN): время «Москва → у вас» по поясам, как смотреть, общины
(с источниками), расширенный FAQ (текст + FAQPage JSON-LD), ссылки на новогоднюю статью, гайды и страницы городов (только если они существуют).
Тексты — tools/country_data.py. Блок идёт между маркерами <!--rtv-cc--> и заменяет прежние seo-box и faq-box. Идемпотентен."""
import sys, os, re, json, html
ROOT = sys.argv[1]
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from country_data import COUNTRIES, MSK_MOMENTS_EN, MSK_MOMENTS_RU
def rd(p): return open(os.path.join(ROOT, p), encoding='utf-8').read()
def wr(p, s): open(os.path.join(ROOT, p), 'w', encoding='utf-8').write(s)
esc = html.escape
NAMES = {
  'usa': dict(en='the USA', ru='США', en_h='the USA', ru_h='США'),
  'uk': dict(en='the UK', ru='Великобритании', en_h='the UK', ru_h='Великобритании'),
  'canada': dict(en='Canada', ru='Канаде', en_h='Canada', ru_h='Канаде'),
  'germany': dict(en='Germany', ru='Германии', en_h='Germany', ru_h='Германии'),
}
CITY_NAMES = {'russian-tv-in-new-york': 'New York / Brooklyn', 'russian-tv-in-los-angeles': 'Los Angeles', 'russian-tv-in-chicago': 'Chicago',
              'russian-tv-in-london': 'London', 'russian-tv-in-toronto': 'Toronto', 'russian-tv-in-montreal': 'Montreal'}
CITY_RU = {'russian-tv-in-new-york': 'Нью-Йорк / Бруклин', 'russian-tv-in-los-angeles': 'Лос-Анджелес', 'russian-tv-in-chicago': 'Чикаго',
           'russian-tv-in-london': 'Лондон', 'russian-tv-in-toronto': 'Торонто', 'russian-tv-in-montreal': 'Монреаль'}
TH = 'style="text-align:left;padding:8px 10px;color:var(--text)"'
TD = 'style="padding:8px 10px;color:var(--muted)"'
TDB = 'style="padding:8px 10px;color:var(--text);font-weight:600"'

def table(zones, moments, lang):
    first = 'Where you are (standard time)' if lang == 'en' else 'Где вы (стандартное время)'
    head = ''.join(f'<th {TH}>{m}</th>' for m in moments)
    rows = ''
    for z, cities, vals in zones:
        rows += (f'\n        <tr style="border-bottom:1px solid var(--border)"><td {TDB}>{esc(cities)}<br><span style="font-weight:400;color:var(--muted);font-size:12px">{esc(z)}</span></td>'
                 + ''.join(f'<td {TD}>{v}</td>' for v in vals) + '</tr>')
    return (f'<div style="overflow-x:auto"><table style="width:100%;border-collapse:collapse;font-size:14px;margin-top:8px;min-width:520px">\n      <thead><tr style="border-bottom:2px solid var(--border2)"><th {TH}>{first}</th>{head}</tr></thead>\n      <tbody>{rows}\n      </tbody>\n    </table></div>')

def faq_linkify(text, lang):
    if lang == 'en':
        text = text.replace('Channel not loading — 8 fixes', '<a href="/en/blog/channel-not-loading-fix/">Channel not loading — 8 fixes</a>')
        text = text.replace("Russian TV on New Year's Eve", '<a href="/en/blog/russian-tv-new-years-eve-usa-uk-canada/">Russian TV on New Year\'s Eve</a>')
    else:
        text = text.replace('«Канал не грузится: 8 способов»', '<a href="/blog/kanal-ne-gruzitsya-chto-delat/">«Канал не грузится: 8 способов»</a>')
        text = text.replace('«Российское ТВ в новогоднюю ночь за границей»', '<a href="/blog/novogodnyaya-noch-russkoe-tv-za-granicey/">«Российское ТВ в новогоднюю ночь за границей»</a>')
    return text

CONV = {
  'usa': [["New York","America/New_York"],["Chicago","America/Chicago"],["Denver","America/Denver"],["Phoenix","America/Phoenix"],["Los Angeles","America/Los_Angeles"],["Anchorage","America/Anchorage"],["Honolulu","Pacific/Honolulu"]],
  'uk': [["London","Europe/London"]],
  'germany': [["Berlin","Europe/Berlin"]],
  'canada': [["St. John's","America/St_Johns"],["Halifax","America/Halifax"],["Toronto / Montreal","America/Toronto"],["Winnipeg","America/Winnipeg"],["Edmonton","America/Edmonton"],["Vancouver","America/Vancouver"]],
}
def conv(key, lang):
    z = json.dumps(CONV[key], ensure_ascii=False).replace("'", '&#39;')
    return f'<div class="rtv-conv" data-lang="{lang}" data-default="21:00" data-zones=\'{z}\'></div><script defer src="/assets/moscow-time.js?v=1"></script>'

def build(key, lang):
    c = COUNTRIES[key]; n = NAMES[key]; en = lang == 'en'
    name = n['en'] if en else n['ru']
    zones = c['en_zones'] if en else c['ru_zones']
    moments = MSK_MOMENTS_EN if en else MSK_MOMENTS_RU
    cities = [(slug, (CITY_NAMES if en else CITY_RU)[slug]) for _, slug in c['cities'] if os.path.exists(os.path.join(ROOT, 'en', slug, 'index.html'))]
    city_html = ''
    if cities:
        pre = 'City pages: ' if en else 'Страницы городов: '
        base = '/en/' if en else '/'
        city_html = f'<p>{pre}' + ', '.join(f'<a href="/en/{s}/">{nm}</a>' for s, nm in cities) + '.</p>'
    if en:
        others = {'usa': ('/en/russian-tv-in-usa/', 'the USA'), 'uk': ('/en/russian-tv-in-uk/', 'the UK'), 'canada': ('/en/russian-tv-in-canada/', 'Canada'), 'germany': ('/en/russian-tv-in-germany/', 'Germany')}
        links = ' · '.join(f'<a href="{u}">Russian TV in {t}</a>' for k, (u, t) in others.items() if k != key)
        _g = {'canada': '<a href="/en/blog/how-to-watch-russian-tv-in-canada/">How to Watch Russian TV in Canada</a> · ', 'uk': '<a href="/en/blog/how-to-watch-russian-tv-in-uk/">How to Watch Russian TV in the UK</a> · ', 'usa': '<a href="/en/blog/moscow-time-to-us-time-zones-russian-tv-schedule/">Moscow Time to US Time Zones</a> · ', 'germany': '<a href="/en/blog/how-to-watch-russian-tv-in-germany/">How to Watch Russian TV in Germany</a> · '}.get(key, '')
        _g += '<a href="/en/blog/russian-tv-on-smart-tv-roku-chromecast-apple-tv/">Russian TV on Smart TV</a> · '
        _g += '<a href="/en/blog/channel-one-vs-rossiya-1-vs-ntv/">Channel One vs Rossiya 1 vs NTV</a> · '
        reading = ('<p><strong>Read next:</strong> ' + _g + '<a href="/en/blog/russian-tv-new-years-eve-usa-uk-canada/">Russian TV on New Year\'s Eve in the USA, UK and Canada</a> · '
                   '<a href="/en/blog/how-to-watch-russian-tv-in-usa/">How to Watch Russian TV in the USA for Free</a> · <a href="/en/blog/channel-not-loading-fix/">Channel not loading: 8 fixes</a> · ' + links + '</p>')
        h = dict(a=f'Russian TV in {name} — what you can watch', b=f'Moscow time in {name}: when to watch', c='How to watch on any device', d=f'Russian speakers in {name}', f='Frequently asked questions')
    else:
        others = {'usa': ('/russkie-kanaly-v-ssha/', 'США'), 'uk': ('/russkie-kanaly-v-velikobritanii/', 'Великобритании'), 'canada': ('/russkie-kanaly-v-kanade/', 'Канаде'), 'germany': ('/russkie-kanaly-v-germanii/', 'Германии')}
        links = ' · '.join(f'<a href="{u}">Русское ТВ в {t}</a>' for k, (u, t) in others.items() if k != key)
        _g = {'canada': '<a href="/blog/kak-smotret-russkoe-tv-v-kanade/">Как смотреть российское ТВ в Канаде</a> · ', 'uk': '<a href="/blog/kak-smotret-russkoe-tv-v-velikobritanii/">Как смотреть российское ТВ в Великобритании</a> · ', 'usa': '<a href="/blog/vremya-po-moskve-v-chasovyh-pojasah-ssha/">Время по Москве в США</a> · ', 'germany': '<a href="/blog/kak-smotret-russkoe-tv-v-germanii/">Как смотреть российское ТВ в Германии</a> · '}.get(key, '')
        reading = ('<p><strong>Читайте также:</strong> ' + _g + '<a href="/blog/novogodnyaya-noch-russkoe-tv-za-granicey/">Российское ТВ в новогоднюю ночь за границей</a> · '
                   '<a href="/blog/kak-smotret-russkoe-tv-za-granicey/">Как смотреть российское ТВ за границей</a> · <a href="/blog/kanal-ne-gruzitsya-chto-delat/">Канал не грузится: 8 способов</a> · ' + links + '</p>')
        h = dict(a=f'Русское ТВ в {name} — что можно смотреть', b=f'Московское время в {name}: когда смотреть', c='Как смотреть на любом устройстве', d=f'Русскоязычные жители в {name}', f='Частые вопросы')
    P = 'en_' if en else 'ru_'
    faq = c[P + 'faq']
    faq_html = ''.join(f'\n    <details>\n      <summary>{esc(q)} <span>▾</span></summary>\n      <p>{faq_linkify(esc(a), lang)}</p>\n    </details>' for q, a in faq)
    block = f'''<!--rtv-cc-->
  <div class="seo-box">
    <h2>{h['a']}</h2>
    {c[P + 'intro']}
  </div>

  <div class="seo-box" style="margin-top:16px">
    <h2>{h['b']}</h2>
    {c[P + 'when']}
    {table(zones, moments, lang)}
    <h3 style="margin-top:18px">{'Moscow time converter (today\'s date, with daylight saving)' if en else 'Конвертер московского времени (на сегодня, с летним временем)'}</h3>
    {conv(key, lang)}
  </div>

  <div class="seo-box" style="margin-top:16px">
    <h2>{h['c']}</h2>
    {c[P + 'how']}
  </div>

  <div class="seo-box" style="margin-top:16px">
    <h2>{h['d']}</h2>
    {c[P + 'people']}
    {city_html}
    {reading}
  </div>

  <div class="faq-box">
    <h2>{h['f']}</h2>{faq_html}
  </div>
<!--/rtv-cc-->
'''
    return block, faq

def apply(path, key, lang):
    s = rd(path + '/index.html'); o = s
    block, faq = build(key, lang)
    if '<!--rtv-cc-->' in s:
        s = re.sub(r'<!--rtv-cc-->.*?<!--/rtv-cc-->\n', lambda m: block, s, count=1, flags=re.S)
    else:
        boxes = list(re.finditer(r'  <div class="seo-box"[^>]*>.*?\n  </div>\n\n?', s, re.S))
        if not boxes: print('нет seo-box:', path); return False
        first = boxes[0].start()
        s = re.sub(r'  <div class="seo-box"[^>]*>.*?\n  </div>\n\n?', '', s, flags=re.S)
        s = re.sub(r'  <div class="faq-box">.*?\n  </div>\n\n?', '', s, count=1, flags=re.S)
        s = s[:first] + block + '\n' + s[first:]
    # FAQPage JSON-LD
    def fix_ld(m):
        try: d = json.loads(m.group(1))
        except Exception: return m.group(0)
        def patch(node):
            if isinstance(node, dict):
                if node.get('@type') == 'FAQPage':
                    node['mainEntity'] = [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in faq]
                for v in node.values(): patch(v)
            elif isinstance(node, list):
                for v in node: patch(v)
        patch(d)
        return '<script type="application/ld+json">' + json.dumps(d, ensure_ascii=False, indent=2) + '</script>'
    s = re.sub(r'<script type="application/ld\+json">(.*?)</script>', fix_ld, s, flags=re.S)
    if s != o: wr(path + '/index.html', s); return True
    return False

n = 0
for key, c in COUNTRIES.items():
    for path, lang in ((c['en_path'], 'en'), (c['ru_path'], 'ru')):
        if apply(path, key, lang): n += 1
print('gen_country_content: страниц изменено', n)
