#!/usr/bin/env python3
"""Исправления по аудиту 18.10.2026 (идемпотентно, запускается последним в run_all.sh).

1. consent.js: убран пустой Google Tag Manager (контейнер без тегов грузил 333 КБ), версия скрипта ?v=3.
2. Логотипы с чужого домена smotret.tv заменены на локальные (assets/logos/).
3. Шрифт Inter: самохостинг (assets/fonts/, @font-face в <head>) вместо Google Fonts.
4. JSON-LD каналов: убран VideoObject с фиктивными датами; description WebPage = meta description.
5. Старый домен russian-tv.online в текстах → russian-tv.com.
6. Тексты: укороченные title/description, исправленные битые EN-описания, счётчики на странице «за рубежом».
7. hreflang: /blog/ ↔ /en/blog/, /sport/ ↔ /en/sport/; лишний hreflang en убран у /russkie-kanaly-za-rubezhom/.
8. Внутренние ссылки: карточка статьи «Вести» в блоге, ссылка на EN-блог в подвале EN-главной.
9. «Похожие каналы»: кольцо по категории (каждый канал получает ровно 4 ссылки), добор из смежных категорий.
10. sitemap.xml: lastmod из git, без changefreq/priority, hreflang для блога и спорта.
"""
import sys, os, re, glob, json, subprocess
from collections import OrderedDict

ROOT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else '.')


def rd(p):
    return open(os.path.join(ROOT, p), encoding='utf-8').read()


def wr(p, s):
    open(os.path.join(ROOT, p), 'w', encoding='utf-8').write(s)


def pages():
    out = []
    for f in glob.glob(os.path.join(ROOT, '**/*.html'), recursive=True):
        rel = os.path.relpath(f, ROOT)
        if rel.startswith(('tools/', 'node_modules/')) or os.path.basename(rel).startswith('google'):
            continue
        out.append(rel)
    return sorted(out)


PAGES = pages()
changed = {}


def save(rel, s, orig, tag):
    if s != orig:
        wr(rel, s)
        changed.setdefault(tag, set()).add(rel)


# ---------------------------------------------------------------- 1. GTM
p = 'assets/consent.js'
s = rd(p); o = s
s = re.sub(r"[ \t]*\(function \(w, d, s, l, i\) \{ w\[l\] = w\[l\] \|\| \[\]; w\[l\]\.push\(\{ 'gtm\.start'.*?GTM-TWVC9XDN'\);\n", '', s, flags=re.S)
s = s.replace('GA4, Google Tag Manager, Yandex.Metrika', 'GA4, Yandex.Metrika')
save(p, s, o, 'consent.js')
for rel in PAGES:
    t = rd(rel); o = t
    t = t.replace('/assets/consent.js?v=2', '/assets/consent.js?v=3')
    save(rel, t, o, 'consent v3')

for rel in ('privacy/index.html', 'en/privacy/index.html'):
    t = rd(rel); o = t
    t = re.sub(r'[ \t]*<li><strong>Google Tag Manager</strong>[^\n]*</li>\n', '', t)
    save(rel, t, o, 'privacy')
for rel in PAGES:
    t = rd(rel); o = t
    t = re.sub(r'[ \t]*<!-- (?:End )?Google Tag Manager(?: \(noscript\))? -->\n?', '', t)
    save(rel, t, o, 'privacy')

# ---------------------------------------------------------------- 2. логотипы
for rel in PAGES:
    t = rd(rel); o = t
    t = t.replace('https://smotret.tv/images/', '/assets/logos/')
    save(rel, t, o, 'logos')

# ---------------------------------------------------------------- 3. шрифты
FONT_FACES = ''.join(
    '@font-face{font-family:"Inter";font-style:normal;font-weight:100 900;font-display:swap;'
    'src:url(/assets/fonts/inter-%s.woff2) format("woff2");unicode-range:%s}' % (sub, rng)
    for sub, rng in (
        ('cyrillic', 'U+0301,U+0400-045F,U+0490-0491,U+04B0-04B1,U+2116'),
        ('cyrillic-ext', 'U+0460-052F,U+1C80-1C8A,U+20B4,U+2DE0-2DFF,U+A640-A69F,U+FE2E-FE2F'),
        ('latin', 'U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD'),
        ('latin-ext', 'U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+0304,U+0308,U+0329,U+1D00-1DBF,U+1E00-1E9F,U+1EF2-1EFF,U+2020,U+20A0-20AB,U+20AD-20C4,U+2113,U+2C60-2C7F,U+A720-A7FF'),
    ))
FONT_BLOCK = ('<link rel="preload" href="/assets/fonts/inter-cyrillic.woff2" as="font" type="font/woff2" crossorigin/>\n'
              '<link rel="preload" href="/assets/fonts/inter-latin.woff2" as="font" type="font/woff2" crossorigin/>\n'
              '<style id="inter-font">' + FONT_FACES + '</style>')
GF_PRECONNECT = re.compile(r'<link rel="preconnect" href="https://fonts\.(?:googleapis|gstatic)\.com"[^>]*/?>\s*')
GF_NOSCRIPT = re.compile(r'<noscript><link rel="stylesheet" href="https://fonts\.googleapis\.com/css2\?family=Inter[^>]*/?></noscript>\s*')
GF_ANY = re.compile(r'<link [^>]*href="https://fonts\.googleapis\.com/css2\?family=Inter[^>]*>\s*')
for rel in PAGES:
    t = rd(rel); o = t
    if 'fonts.googleapis.com' in t:
        t = GF_NOSCRIPT.sub('', t)
        t = GF_ANY.sub('', t)
        t = GF_PRECONNECT.sub('', t)
        if 'id="inter-font"' not in t:
            t = t.replace('</head>', FONT_BLOCK + '\n</head>', 1)
    save(rel, t, o, 'fonts')

# ---------------------------------------------------------------- 4. JSON-LD
LD = re.compile(r'(<script type="application/ld\+json">)(.*?)(</script>)', re.S)


def meta_desc(t):
    m = re.search(r'<meta name="description" content="([^"]*)"', t)
    return re.sub(r'^▶\s*', '', m.group(1)).strip() if m else None


def fix_ld(rel):
    t = rd(rel); o = t
    if not rel.endswith('-live/index.html') and rel not in ('en/russian-tv-in-germany/index.html', 'en/russian-tv-in-usa/index.html'):
        return
    d = meta_desc(t)

    def sub(m):
        try:
            j = json.loads(m.group(2))
        except Exception:
            return m.group(0)
        if '@graph' not in j:
            return m.group(0)
        g = [n for n in j['@graph'] if n.get('@type') != 'VideoObject']
        for n in g:
            if n.get('@type') == 'WebPage' and d:
                n['description'] = d
        j['@graph'] = g
        return m.group(1) + json.dumps(j, ensure_ascii=False, indent=2) + m.group(3)
    t = LD.sub(sub, t)
    save(rel, t, o, 'json-ld')


for rel in PAGES:
    fix_ld(rel)

# ---------------------------------------------------------------- 5. старый домен
for rel in PAGES:
    t = rd(rel); o = t
    t = t.replace('russian-tv.online', 'russian-tv.com')
    save(rel, t, o, 'old domain')

# ---------------------------------------------------------------- 6. тексты
TITLES = {
    'kino/index.html': ('▶ Российские кино-каналы онлайн — 15 каналов фильмов бесплатно без VPN', '▶ Российские кино-каналы онлайн — 15 каналов бесплатно, без VPN'),
    'rossiya-1-live/index.html': ('▶ Россия 1 прямой эфир — смотреть онлайн бесплатно без VPN | Вести', '▶ Россия 1 прямой эфир — смотреть онлайн бесплатно | Вести'),
    'istoriya-live/index.html': ('▶ Телеканал История прямой эфир онлайн — документальные фильмы без VPN', '▶ Телеканал История прямой эфир — документальные фильмы онлайн'),
    'kino-detektiv-live/index.html': ('▶ Viju TV1000 Русское кино прямой эфир — русское кино онлайн без VPN', '▶ Viju TV1000 Русское кино — прямой эфир, фильмы онлайн'),
    'kinopremiera-live/index.html': ('▶ Кинопремьера прямой эфир — новинки кино онлайн бесплатно без VPN', '▶ Кинопремьера прямой эфир — новинки кино онлайн бесплатно'),
    'russkie-kanaly-v-velikobritanii/index.html': ('▶ Русское ТВ в Великобритании — 58 каналов онлайн без VPN, бесплатно', '▶ Русское ТВ в Великобритании — 58 каналов онлайн бесплатно'),
    'en/russian-tv-in-netherlands/index.html': ('▶ Watch Russian TV in the Netherlands Free Online — 58 Channels, No VPN', '▶ Watch Russian TV in the Netherlands Free — 58 Channels, No VPN'),
    'en/russian-tv-in-switzerland/index.html': ('▶ Watch Russian TV in Switzerland Free Online — 58 Channels, No VPN', '▶ Watch Russian TV in Switzerland Free — 58 Channels, No VPN'),
    'en/russian-tv-in-czech-republic/index.html': ('▶ Watch Russian TV in the Czech Republic Free Online — 58 Channels, No VPN', '▶ Russian TV in the Czech Republic Free — 58 Channels, No VPN'),
    'en/flosports-racing-live/index.html': ('▶ FloSports Racing Live Stream Free | Motor Racing Online — No VPN', '▶ FloSports Racing Live Stream Free | Motor Racing — No VPN'),
    'en/kinokomediya-live/index.html': ('▶ Kinokomediya Live Stream Free | Russian Comedies Online — No VPN', '▶ Kinokomediya Live Stream Free | Russian Comedies — No VPN'),
    'blog/index.html': ('Блог — статьи о русском ТВ, каналах и вещании за границей | Русское ТВ', 'Блог о русском ТВ — каналы и просмотр за границей | Русское ТВ'),
    'blog/gde-smotret-futbol-i-sport-na-russkih-kanalah/index.html': ('Где смотреть футбол и спорт на русских каналах онлайн | Русское ТВ', 'Где смотреть футбол и спорт на русских каналах | Русское ТВ'),
    'en/blog/how-to-watch-russian-tv-in-usa/index.html': ('How to Watch Russian TV in the USA for Free in 2026 — Complete Guide', 'How to Watch Russian TV in the USA for Free in 2026 — Guide'),
    'chestnyy-detektiv-live/index.html': ('▶ Честный детектив прямой эфир — детективы и криминал онлайн без VPN', '▶ Честный детектив прямой эфир — детективы и криминал онлайн'),
    'rt-documentary-live/index.html': ('▶ RT Documentary прямой эфир — документальные фильмы онлайн без VPN', '▶ RT Documentary прямой эфир — документальные фильмы онлайн'),
    'karusel-international-live/index.html': ('▶ Карусель International прямой эфир — детские передачи онлайн без VPN', '▶ Карусель International прямой эфир — детские передачи онлайн'),
    'priklyucheniya-live/index.html': ('▶ Приключения прямой эфир — приключения и путешествия онлайн без VPN', '▶ Приключения прямой эфир — путешествия и приключения онлайн'),
    'domashnie-zhivotnye-live/index.html': ('▶ Домашние животные прямой эфир — передачи о питомцах онлайн без VPN', '▶ Домашние животные прямой эфир — передачи о питомцах онлайн'),
    'bolshaya-planeta-live/index.html': ('▶ Большая планета прямой эфир — путешествия и природа онлайн без VPN', '▶ Большая планета прямой эфир — путешествия и природа онлайн'),
    'blog/kak-smotret-russkoe-tv-na-iphone-i-android/index.html': ('Как смотреть российское ТВ на iPhone и Android без приложения — 2026', 'Как смотреть российское ТВ на iPhone и Android без приложения'),
    'en/blog/russian-tv-on-iphone-and-android/index.html': ('How to Watch Russian TV on iPhone and Android Without an App — 2026', 'How to Watch Russian TV on iPhone and Android Without an App'),
    # НТВ Хит: в тексте страницы — сериалы, а не музыка
    'ntv-hit-live/index.html': ('▶ НТВ-Хит прямой эфир — российская музыка онлайн без VPN', '▶ НТВ Хит прямой эфир — сериалы НТВ онлайн без VPN'),
    'en/ntv-hit-live/index.html': ('▶ NTV Hit Live Stream Free | Russian Music — No VPN', '▶ NTV Hit Live Stream Free | Russian Series — No VPN'),
}
DESCS = {
    '': ('▶ Русское ТВ онлайн за рубежом — 58 каналов прямого эфира: Первый канал, Россия 1, НТВ, ТНТ, МУЗ-ТВ, кино, детские. Бесплатно, без регистрации, 24/7.',),
    'en/': ('▶ Watch Russian TV free online — 58 live channels: Perviy Kanal, Rossiya 1, NTV, TNT, MUZ-TV, kids & films. Works worldwide 24/7, no registration.',),
    'en/karusel-live/': ("▶ Watch Karusel live online free — Russian children's cartoons and educational shows. No VPN, no registration, 24/7.",),
    'en/muz-tv-live/': ('▶ Watch MUZ-TV live online free — Russian pop music, clips and charts. No VPN, no registration, 24/7.',),
    'en/ntv-hit-live/': ('▶ Watch NTV Hit live online free — Russian detective series and dramas from NTV. No VPN, no registration, 24/7.',),
    'en/ntv-live/': ('▶ Watch NTV live online free — Russian news, crime reporting and series. No VPN, no registration, 24/7.',),
    'en/rossiya-1-live/': ('▶ Watch Rossiya 1 live online free — Vesti news, talk shows and series. No VPN, no registration, 24/7.',),
    'en/rossiya-24-live/': ('▶ Watch Rossiya 24 live online free — round-the-clock news from Russia. No VPN, no registration. Works worldwide.',),
    'en/soloviev-live/': ('▶ Watch Soloviev Live online free — Russian political talk shows and analysis. No VPN, no registration, 24/7.',),
    'en/tnt-live/': ('▶ Watch TNT live online free — Comedy Club, Russian series and entertainment. No VPN, no registration, 24/7.',),
    'en/viju-tv-live/': ('▶ Watch Viju TV1000 live online free — Russian-language films and series. No VPN, no registration, 24/7.',),
    'en/entertainment/': ('▶ Watch Russian entertainment and documentary channels live online for free: TNT4, Istoriya, Soyuz TV, Prima, RT Documentary. No VPN, 24/7.',),
    'en/hobby/': ('▶ Watch Russian nature, travel, animal and auto channels live online for free: Hunting & Fishing, Moy Mir, Zoopark and more. No VPN, 24/7.',),
    'en/music/': ('▶ Watch Russian music TV and radio live online for free: MUZ-TV, Muzyka Pervogo, Muz Soyuz, FON Music, Strana FM. No VPN, 24/7.',),
    'ntv-hit-live/': ('▶ НТВ Хит онлайн — лучшие сериалы и развлекательные программы НТВ в прямом эфире. Бесплатно, без VPN и регистрации 24/7.',),
    'sport/': ('▶ Спортивные каналы в прямом эфире: FloSports, Viju+ Sport, M1 MMA, Red Bull TV, Unbeaten Boxing. Бесплатно, без регистрации, 24/7.',),
    'russkie-kanaly-za-rubezhom/': ('▶ Смотрите 58 русских каналов за рубежом без VPN: Польша, Германия, США, Великобритания, Франция и другие страны. Бесплатно, 24/7.',),
}


# CTR-правки по данным Search Console (18.10.2026): страницы на позициях 8–45 с показами, но почти без кликов.
# Заголовок задаётся целиком (заменяет любой текущий <title>), описание — через DESCS.
FORCE_TITLES = {
    'en/russian-tv-in-germany/index.html': '▶ Russian TV in Germany — Watch 58 Live Channels Free',
    'en/russian-tv-in-usa/index.html': '▶ Russian TV in the USA — Watch 58 Live Channels Free',
    'en/perviy-kanal-live/index.html': '▶ Channel One Russia Live — Watch Perviy Kanal Online Free',
    'rossiya-24-live/index.html': '▶ Россия 24 — прямой эфир онлайн, смотреть Вести 24 бесплатно',
    'en/rossiya-24-live/index.html': '▶ Rossiya 24 Live — Russian News 24/7 Online Free',
    'karusel-live/index.html': '▶ Карусель — детский канал онлайн, мультики в прямом эфире',
    'muz-tv-live/index.html': '▶ МУЗ-ТВ — прямой эфир онлайн, клипы и хит-парады',
    'rossiya-1-live/index.html': '▶ Россия 1 — прямой эфир онлайн, Вести и сериалы бесплатно',
    'perviy-kanal-live/index.html': '▶ Первый канал — прямой эфир онлайн бесплатно',
    'mir-live/index.html': '▶ Телеканал МИР — прямой эфир онлайн бесплатно',
}
DESCS.update({
    'en/russian-tv-in-germany/': ('▶ Watch Russian TV in Germany online: Perviy Kanal, Rossiya 1, NTV, Rossiya 24 and more live channels. Free, in your browser — no app or sign-up.',),
    'en/russian-tv-in-usa/': ('▶ Watch Russian TV in the USA online: Perviy Kanal, Rossiya 1, NTV, Rossiya 24 and more live channels. Free, in your browser — no app or sign-up.',),
    'en/perviy-kanal-live/': ('▶ Watch Channel One Russia (Perviy Kanal) live online: news, talk shows and series on the main Russian TV channel. Free, no registration.',),
    'rossiya-24-live/': ('▶ Смотрите Россию 24 в прямом эфире: новости России и мира круглосуточно. Бесплатно, в браузере, без регистрации — из любой страны.',),
    'en/rossiya-24-live/': ('▶ Watch Rossiya 24 live: round-the-clock news from Russia and the world. Free in your browser, no registration, from any country.',),
    'karusel-live/': ('▶ Смотрите детский канал «Карусель» онлайн: мультфильмы и развивающие передачи в прямом эфире. Бесплатно, без регистрации, на телефоне и компьютере.',),
    'muz-tv-live/': ('▶ МУЗ-ТВ в прямом эфире: российская музыка, клипы и хит-парады 24/7. Смотрите бесплатно в браузере — без регистрации.',),
    'rossiya-1-live/': ('▶ Смотрите Россию 1 в прямом эфире: Вести, «60 минут», «Прямой эфир», сериалы. Бесплатно, в браузере, без регистрации — из любой страны.',),
    'perviy-kanal-live/': ('▶ Смотрите Первый канал онлайн в прямом эфире: новости, ток-шоу и сериалы. Бесплатно, в браузере, без регистрации — из любой страны.',),
    'mir-live/': ('▶ Телеканал МИР онлайн: новости и программы СНГ в прямом эфире. Бесплатно, в браузере, без регистрации.',),
})
def attr_replace(t, name_attr, old, new):
    return t.replace(f'{name_attr} content="{old}"', f'{name_attr} content="{new}"')


for rel in PAGES:
    t = rd(rel); o = t
    key = rel[:-len('index.html')]
    if rel in TITLES:
        old, new = TITLES[rel]
        t = t.replace('<title>%s</title>' % old, '<title>%s</title>' % new)
        t = t.replace('content="%s"' % old, 'content="%s"' % new)  # og:title / twitter:title, если совпадали
    if rel in FORCE_TITLES:
        t = re.sub(r'<title>.*?</title>', lambda m: '<title>%s</title>' % FORCE_TITLES[rel], t, count=1, flags=re.S)
    if key in DESCS:
        new = DESCS[key][0]
        t = re.sub(r'(<meta name="description" content=")[^"]*(")', lambda m: m.group(1) + new + m.group(2), t, count=1)
    save(rel, t, o, 'titles/descriptions')

# og:description и счётчики на странице «за рубежом»
p = 'russkie-kanaly-za-rubezhom/index.html'
s = rd(p); o = s
s = s.replace('35 русских каналов прямого эфира за рубежом', '58 русских каналов прямого эфира за рубежом')
save(p, s, o, 'titles/descriptions')
# после смены meta description пересобираем description в JSON-LD каналов
for rel in PAGES:
    fix_ld(rel)

# ---------------------------------------------------------------- 7. hreflang
def add_hreflang(rel, ru, en):
    t = rd(rel); o = t
    if 'hreflang' in t:
        return
    block = ('\n<link rel="alternate" hreflang="ru" href="%s"/>\n<link rel="alternate" hreflang="en" href="%s"/>\n'
             '<link rel="alternate" hreflang="x-default" href="%s"/>' % (ru, en, ru))
    t = re.sub(r'(<link rel="canonical" href="[^"]*"\s*/>)', lambda m: m.group(1) + block, t, count=1)
    save(rel, t, o, 'hreflang')


add_hreflang('blog/index.html', 'https://russian-tv.com/blog/', 'https://russian-tv.com/en/blog/')
add_hreflang('sport/index.html', 'https://russian-tv.com/sport/', 'https://russian-tv.com/en/sport/')
p = 'russkie-kanaly-za-rubezhom/index.html'
s = rd(p); o = s
s = re.sub(r'<link rel="alternate" hreflang="en" href="https://russian-tv.com/en/"\s*/>\n?', '', s)
save(p, s, o, 'hreflang')

# повторный запуск поверх пересобранных страниц не должен плодить одинаковые hreflang
HL = re.compile(r'[ \t]*<link rel="alternate" hreflang="[^"]+" href="[^"]+"\s*/>\n?')
for rel in PAGES:
    t = rd(rel); o = t
    seen_hl = set()

    def _dedupe(m):
        k = re.sub(r'\s+', ' ', m.group(0).strip())
        if k in seen_hl:
            return ''
        seen_hl.add(k)
        return m.group(0)
    t = HL.sub(_dedupe, t)
    save(rel, t, o, 'hreflang')

# ---------------------------------------------------------------- 8. внутренние ссылки
p = 'blog/index.html'
s = rd(p); o = s
if '/blog/vesti-onlajn-poslednie-vypuski/' not in s:
    card = ('    <a href="/blog/vesti-onlajn-poslednie-vypuski/" class="post-card">\n'
            '      <div class="post-date">Октябрь 2026</div>\n'
            '      <div class="post-title">Вести онлайн: прямой эфир Россия 1 и Россия 24</div>\n'
            '      <div class="post-excerpt">Где смотреть Вести онлайн бесплатно без регистрации: прямой эфир Вестей на Россия 1 и Россия 24 — из любой страны.</div>\n'
            '    </a>\n')
    s = s.replace('  <div class="post-list">\n', '  <div class="post-list">\n' + card, 1)
save(p, s, o, 'internal links')
p = 'en/index.html'
s = rd(p); o = s
if '/en/blog/' not in s:
    s = s.replace('      <a href="#faq">FAQ</a>\n      <a href="/">Русский</a>', '      <a href="#faq">FAQ</a>\n      <a href="/en/blog/">Blog</a>\n      <a href="/">Русский</a>', 1)
save(p, s, o, 'internal links')

# ---------------------------------------------------------------- 8c. трансляция на ТВ (Google Cast / AirPlay)
CAST_TAG = '<script defer src="/assets/cast.js?v=1"></script>'
for rel in PAGES:
    t = rd(rel); o = t
    if '/assets/player-ui.js' in t and 'assets/cast.js' not in t:
        t = re.sub(r'(<script defer src="/assets/player-ui\.js\?v=\d+"></script>)', lambda m: m.group(1) + '\n' + CAST_TAG, t, count=1)
    save(rel, t, o, 'cast.js')
CAST_LI = {'privacy/index.html': '    <li><strong>Google Cast</strong> — кнопка трансляции на телевизор: в браузерах на основе Chromium подгружается скрипт Google (gstatic.com); подключается без вашего участия, трансляция начинается только после нажатия кнопки.</li>\n',
           'en/privacy/index.html': '    <li><strong>Google Cast</strong> — the cast-to-TV button: in Chromium-based browsers a Google script (gstatic.com) is loaded; casting starts only after you press the button.</li>\n'}
for rel, li in CAST_LI.items():
    t = rd(rel); o = t
    if 'Google Cast' not in t:
        t = re.sub(r'(<li><strong>Microsoft Clarity</strong>[^\n]*</li>\n)', lambda m: m.group(1) + li, t, count=1)
    save(rel, t, o, 'cast.js')

# ---------------------------------------------------------------- 8a. пульсирующий баннер под плеером
# «Подписаться на канал» вёл в Telegram-канал с мини-приложением, а не просто на канал — название сбивало с толку.
PULSE = {'<div class="tg-pulse-text">Подписаться на канал</div>': '<div class="tg-pulse-text">Смотреть каналы в Telegram</div>',
         '<div class="tg-pulse-text">Смотреть в Telegram</div>': '<div class="tg-pulse-text">Смотреть каналы в Telegram</div>',
         '<div class="tg-pulse-text">Subscribe to the channel</div>': '<div class="tg-pulse-text">Watch channels in Telegram</div>',
         '<div class="tg-pulse-text">Watch in Telegram</div>': '<div class="tg-pulse-text">Watch channels in Telegram</div>'}
for rel in PAGES:
    t = rd(rel); o = t
    for old_, new_ in PULSE.items():
        t = t.replace(old_, new_)
    save(rel, t, o, 'pulse banner')

# ---------------------------------------------------------------- 8b. каналы вне каталога — noindex
# Эти страницы работают и доступны посетителям, но их нет в каталоге главной (решение владельца 18.10.2026):
# не индексируются, в sitemap не входят, в «Похожие» не попадают.
NOINDEX_SLUGS = ['kinopokaz-live', 'kinopremiera-live', 'ntv-hit-live', 'retro-live', 'ru-tv-live', 't24-live', 'unikum-live', 'zagorodnaya-zhizn-live']
for slug in NOINDEX_SLUGS:
    for rel in (slug + '/index.html', 'en/' + slug + '/index.html'):
        if not os.path.exists(os.path.join(ROOT, rel)):
            continue
        t = rd(rel); o = t
        if re.search(r'<meta name="robots"', t):
            t = re.sub(r'<meta name="robots" content="[^"]*"\s*/>', '<meta name="robots" content="noindex,follow"/>', t, count=1)
        else:
            t = re.sub(r'(<link rel="canonical" href="[^"]*"\s*/>)', lambda m: m.group(1) + '\n<meta name="robots" content="noindex,follow"/>', t, count=1)
        save(rel, t, o, 'noindex')

# ---------------------------------------------------------------- 9. похожие каналы
CAT_KEYS = ['/novosti/', '/razvlecheniya/', '/kino/', '/detskie/', '/muzyka/', '/hobbi/', '/sport/']
RELATED = {'/novosti/': ['/razvlecheniya/'], '/razvlecheniya/': ['/novosti/', '/kino/'], '/kino/': ['/razvlecheniya/'],
           '/detskie/': ['/razvlecheniya/', '/kino/'], '/muzyka/': ['/razvlecheniya/'], '/hobbi/': ['/razvlecheniya/', '/sport/'],
           '/sport/': ['/hobbi/']}
live_ru = [r for r in PAGES if re.fullmatch(r'[a-z0-9-]+-live/index\.html', r) and 'noindex' not in rd(r)]
slugs = [r.split('/')[0] for r in live_ru]


def category_of(slug):
    t = rd(slug + '/index.html')
    m = re.findall(r'"item": "https://russian-tv\.com(/[a-z]+/)"', t)
    for u in m:
        if u in CAT_KEYS:
            return u
    return None


cat = {s: category_of(s) for s in slugs}
# порядок в кольце — как в боковом списке страницы (сайдбар), остальные в конце по алфавиту
side = []
t0 = rd('ntv-live/index.html')
for m in re.finditer(r'<a href="/([a-z0-9-]+-live)/" class="ch-item-s"', t0):
    if m.group(1) not in side:
        side.append(m.group(1))
order = [s for s in side if s in cat] + sorted(s for s in slugs if s not in side)
rings = OrderedDict((c, [s for s in order if cat[s] == c]) for c in CAT_KEYS)

SIM_RU, SIM_EN = {}, {}
for rel in PAGES:
    t = rd(rel)
    for m in re.finditer(r'<a href="(/(?:en/)?)([a-z0-9-]+-live)/" class="sim-item">.*?</a>', t):
        (SIM_EN if m.group(1) == '/en/' else SIM_RU).setdefault(m.group(2), m.group(0))
# карточки «похожих» для каналов вне главного каталога (их нет в списке главной) — чтобы пересборка с нуля работала
EXTRA_SIM = {
    'ru:kinopokaz-live': '<a href="/kinopokaz-live/" class="sim-item"><div class="sim-icon" style="background:#130818;color:#6a1b9a">КПК</div><div><div class="sim-name">Кинопоказ</div><div class="sim-cat">Кино</div></div><span class="sim-live">LIVE</span></a>',
    'en:kinopokaz-live': '<a href="/en/kinopokaz-live/" class="sim-item"><div class="sim-icon" style="background:#130818;color:#6a1b9a">КПК</div><div><div class="sim-name">Kinopokaz</div><div class="sim-cat">Movies</div></div><span class="sim-live">LIVE</span></a>',
    'ru:kinopremiera-live': '<a href="/kinopremiera-live/" class="sim-item"><div class="sim-icon" style="background:#130818;color:#7b1fa2">КПР</div><div><div class="sim-name">Кинопремьера</div><div class="sim-cat">Кино</div></div><span class="sim-live">LIVE</span></a>',
    'en:kinopremiera-live': '<a href="/en/kinopremiera-live/" class="sim-item"><div class="sim-icon" style="background:#130818;color:#7b1fa2">КПР</div><div><div class="sim-name">Kinopremiera</div><div class="sim-cat">Movies</div></div><span class="sim-live">LIVE</span></a>',
    'ru:ntv-hit-live': '<a href="/ntv-hit-live/" class="sim-item"><div class="sim-icon" style="background:#0a1020;color:#1e88e5">НТВ+</div><div><div class="sim-name">НТВ Хит</div><div class="sim-cat">Новости</div></div><span class="sim-live">LIVE</span></a>',
    'en:ntv-hit-live': '<a href="/en/ntv-hit-live/" class="sim-item"><div class="sim-icon" style="background:#0a1020;color:#1e88e5">НТВ+</div><div><div class="sim-name">NTV Hit</div><div class="sim-cat">News</div></div><span class="sim-live">LIVE</span></a>',
    'ru:retro-live': '<a href="/retro-live/" class="sim-item"><div class="sim-icon" style="background:#140e0a;color:#8d6e63">РТР</div><div><div class="sim-name">Ретро</div><div class="sim-cat">Кино</div></div><span class="sim-live">LIVE</span></a>',
    'en:retro-live': '<a href="/en/retro-live/" class="sim-item"><div class="sim-icon" style="background:#140e0a;color:#8d6e63">РТР</div><div><div class="sim-name">Retro</div><div class="sim-cat">Movies</div></div><span class="sim-live">LIVE</span></a>',
    'ru:ru-tv-live': '<a href="/ru-tv-live/" class="sim-item"><div class="sim-icon" style="background:#180a12;color:#c2185b">RU</div><div><div class="sim-name">RU.TV</div><div class="sim-cat">Музыка</div></div><span class="sim-live">LIVE</span></a>',
    'en:ru-tv-live': '<a href="/en/ru-tv-live/" class="sim-item"><div class="sim-icon" style="background:#180a12;color:#c2185b">RU</div><div><div class="sim-name">RU.TV</div><div class="sim-cat">Music</div></div><span class="sim-live">LIVE</span></a>',
    'ru:t24-live': '<a href="/t24-live/" class="sim-item"><div class="sim-icon" style="background:#081214;color:#00838f">T24</div><div><div class="sim-name">T24</div><div class="sim-cat">Кино</div></div><span class="sim-live">LIVE</span></a>',
    'en:t24-live': '<a href="/en/t24-live/" class="sim-item"><div class="sim-icon" style="background:#081214;color:#00838f">T24</div><div><div class="sim-name">T24</div><div class="sim-cat">Movies</div></div><span class="sim-live">LIVE</span></a>',
    'ru:unikum-live': '<a href="/unikum-live/" class="sim-item"><div class="sim-icon" style="background:#081210;color:#00695c">УНК</div><div><div class="sim-name">Уникум</div><div class="sim-cat">Детские</div></div><span class="sim-live">LIVE</span></a>',
    'en:unikum-live': '<a href="/en/unikum-live/" class="sim-item"><div class="sim-icon" style="background:#081210;color:#00695c">УНК</div><div><div class="sim-name">Unikum</div><div class="sim-cat">Kids</div></div><span class="sim-live">LIVE</span></a>',
    'ru:zagorodnaya-zhizn-live': '<a href="/zagorodnaya-zhizn-live/" class="sim-item"><div class="sim-icon" style="background:#0a1208;color:#558b2f">ЗЖ</div><div><div class="sim-name">Загородная жизнь</div><div class="sim-cat">Хобби</div></div><span class="sim-live">LIVE</span></a>',
    'en:zagorodnaya-zhizn-live': '<a href="/en/zagorodnaya-zhizn-live/" class="sim-item"><div class="sim-icon" style="background:#0a1208;color:#558b2f">ЗЖ</div><div><div class="sim-name">Country Life</div><div class="sim-cat">Hobby</div></div><span class="sim-live">LIVE</span></a>',
}
for k_, v_ in EXTRA_SIM.items():
    lang_, slug_ = k_.split(':', 1)
    (SIM_EN if lang_ == 'en' else SIM_RU).setdefault(slug_, v_)
RU_CAT_LABEL = {}
for s, mk in SIM_RU.items():
    m = re.search(r'class="sim-cat">([^<]*)<', mk)
    if m and cat.get(s):
        RU_CAT_LABEL.setdefault(cat[s], m.group(1))


EN_CAT_LABEL = {}
for s_, mk in SIM_EN.items():
    m = re.search(r'class="sim-cat">([^<]*)<', mk)
    if m and cat.get(s_):
        EN_CAT_LABEL.setdefault(cat[s_], m.group(1))
HOME = {}
for rel_, en_ in (('index.html', False), ('en/index.html', True)):
    h = rd(rel_)
    for m in re.finditer(r'\{\s*id:[\'"][^\'"]+[\'"],\s*name:[\'"]([^\'"]+)[\'"](?:,\s*nameEn:[\'"]([^\'"]+)[\'"])?.*?icon:[\'"]([^\'"]+)[\'"],\s*color:[\'"]([^\'"]+)[\'"],\s*iconBg:[\'"]([^\'"]+)[\'"].*?slug:[\'"]([^\'"]+)[\'"]', h):
        HOME[(en_, m.group(6))] = dict(name=(m.group(2) or m.group(1)) if en_ else m.group(1), icon=m.group(3), color=m.group(4), bg=m.group(5))


def markup(slug, en):
    pool = SIM_EN if en else SIM_RU
    if slug in pool:
        return pool[slug]
    d = HOME.get((en, slug))
    if d and cat.get(slug):
        label = (EN_CAT_LABEL if en else RU_CAT_LABEL).get(cat[slug], '')
        return ('<a href="/%s%s/" class="sim-item"><div class="sim-icon" style="background:%s;color:%s">%s</div>'
                '<div><div class="sim-name">%s</div><div class="sim-cat">%s</div></div><span class="sim-live">LIVE</span></a>'
                % ('en/' if en else '', slug, d['bg'], d['color'], d['icon'], d['name'], label))
    return None


def similar(slug, n=4):
    c = cat[slug]
    ring = rings[c]
    out = []
    if slug in ring:
        i = ring.index(slug)
        for k in range(1, len(ring)):
            cand = ring[(i + k) % len(ring)]
            if cand != slug and cand not in out:
                out.append(cand)
            if len(out) == n:
                return out
    for rc in RELATED.get(c, []):
        rr = rings[rc]
        if not rr:
            continue
        start = (slugs.index(slug) if slug in slugs else 0) % len(rr)
        for k in range(len(rr)):
            cand = rr[(start + k) % len(rr)]
            if cand not in out:
                out.append(cand)
            if len(out) == n:
                return out
    return out


SIM_BOX = re.compile(r'(<div class="sim-box">\s*<h3>[^<]*</h3>\n)(.*?)(\n\s*</div>\s*\n\s*<div class="pop-box">)', re.S)
missing_markup = []
for slug in slugs:
    for en in (False, True):
        rel = ('en/' if en else '') + slug + '/index.html'
        if not os.path.exists(os.path.join(ROOT, rel)):
            continue
        t = rd(rel); o = t
        sel = similar(slug)
        items = []
        for c in sel:
            mk = markup(c, en)
            if not mk:
                missing_markup.append((rel, c)); continue
            items.append(mk)
        if len(items) >= 2:
            t = SIM_BOX.sub(lambda m: m.group(1) + '\n'.join(items) + m.group(3), t, count=1)
        save(rel, t, o, 'similar channels')
if missing_markup:
    print('WARNING: no sim markup for', missing_markup[:5])

# ---------------------------------------------------------------- 10. sitemap
import datetime
try:
    _st = subprocess.run(['git', '-C', ROOT, 'status', '--porcelain'], capture_output=True, text=True).stdout
    MODIFIED = {l[3:].strip() for l in _st.splitlines()}
except Exception:
    MODIFIED = set()
TODAY = datetime.date.today().isoformat()


def git_date(path):
    # страница изменена, но ещё не закоммичена — датой считается сегодняшняя
    if path in MODIFIED:
        return TODAY
    try:
        out = subprocess.run(['git', '-C', ROOT, 'log', '-1', '--format=%cs', '--', path], capture_output=True, text=True).stdout.strip()
        return out or None
    except Exception:
        return None


p = 'sitemap.xml'
s = rd(p); o = s
HREF = {
    'https://russian-tv.com/blog/': ('https://russian-tv.com/blog/', 'https://russian-tv.com/en/blog/'),
    'https://russian-tv.com/en/blog/': ('https://russian-tv.com/blog/', 'https://russian-tv.com/en/blog/'),
    'https://russian-tv.com/sport/': ('https://russian-tv.com/sport/', 'https://russian-tv.com/en/sport/'),
    'https://russian-tv.com/en/sport/': ('https://russian-tv.com/sport/', 'https://russian-tv.com/en/sport/'),
}


def url_entry(m):
    loc = m.group(1)
    path = loc.replace('https://russian-tv.com', '')
    f = path.lstrip('/') + ('index.html' if path.endswith('/') else '')
    d = git_date(f if f else 'index.html') or git_date('index.html')
    xl = ''
    if loc in HREF and 'xhtml:link' not in m.group(0):
        ru, en = HREF[loc]
        xl = ('<xhtml:link rel="alternate" hreflang="ru" href="%s"/><xhtml:link rel="alternate" hreflang="en" href="%s"/>'
              '<xhtml:link rel="alternate" hreflang="x-default" href="%s"/>' % (ru, en, ru))
    links = ''.join(re.findall(r'<xhtml:link[^>]*/>', m.group(0))) or xl
    return '<url><loc>%s</loc>%s<lastmod>%s</lastmod></url>' % (loc, links, d)


s = re.sub(r'<url><loc>([^<]+)</loc>.*?</url>', url_entry, s)
for slug in NOINDEX_SLUGS:
    s = re.sub(r'[ \t]*<url><loc>https://russian-tv\.com/(?:en/)?' + re.escape(slug) + r'/</loc>.*?</url>\n?', '', s)
save(p, s, o, 'sitemap')

for k, v in sorted(changed.items()):
    print('%-22s %d файлов' % (k, len(v)))
