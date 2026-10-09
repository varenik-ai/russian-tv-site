#!/usr/bin/env python3
"""EN-страницы категорий (/en/news/ ...) + hreflang на RU-категориях + «Спорт» в навигации. Идемпотентно."""
import sys, os, re, json, subprocess, html
ROOT = sys.argv[1]
def rd(p): return open(os.path.join(ROOT, p), encoding='utf-8').read()
def wr(p, s):
    os.makedirs(os.path.dirname(os.path.join(ROOT, p)), exist_ok=True)
    open(os.path.join(ROOT, p), 'w', encoding='utf-8').write(s)
def esc(s): return html.escape(s, quote=True)

# --- каналы из EN-главной ---
home = rd('en/index.html')
m = re.search(r'const CHANNEL_GROUPS = (\[.*?\n\]);', home, re.S)
open('/tmp/_cg.js', 'w', encoding='utf-8').write('const CHANNEL_GROUPS=' + m.group(1) + ';console.log(JSON.stringify(CHANNEL_GROUPS))')
groups = json.loads(subprocess.run(['node', '/tmp/_cg.js'], capture_output=True, text=True, check=True).stdout)

CATS = [  # en slug, ru slug, group index keyword, label, emoji, title, desc, h1, lead
 ('news', 'novosti', 'News', '📡', 'News'),
 ('entertainment', 'razvlecheniya', 'Entertainment', '🎬', 'Entertainment'),
 ('movies', 'kino', 'Movies', '🎥', 'Movies'),
 ('kids', 'detskie', 'Kids', '👶', 'Kids'),
 ('music', 'muzyka', 'Music', '🎵', 'Music'),
 ('hobby', 'hobbi', 'Hobby', '🌿', 'Hobby'),
 ('sport', 'sport', 'Sport', '⚽', 'Sport'),
]
TXT = {
 'news': ('Russian News Channels Online — Watch Live Free, No VPN', 'Russian news channels', 'Watch Russian news TV live online for free: {names}. No VPN, no registration, 24/7.', 'Russian news channels online'),
 'entertainment': ('Russian Entertainment Channels Online — Live TV, No VPN', 'Russian entertainment channels', 'Watch Russian entertainment, documentary and family channels live online for free: {names}. No VPN, no registration, 24/7.', 'Russian entertainment channels online'),
 'movies': ('Russian Movie Channels Online — Films & Series Live, No VPN', 'Russian movie channels', 'Watch Russian movie and series channels live online for free: {names}. No VPN, no registration, 24/7.', 'Russian movie channels online'),
 'kids': ('Russian Kids Channels Online — Cartoons Live, No VPN', 'Russian kids channels', 'Watch Russian kids channels live online for free: {names}. Cartoons and programmes for children, no VPN, no registration, 24/7.', 'Russian kids channels online'),
 'music': ('Russian Music Channels & Radio Online — Live, No VPN', 'Russian music channels and radio', 'Watch Russian music TV and listen to Russian radio live online for free: {names}. No VPN, no registration, 24/7.', 'Russian music channels and radio online'),
 'hobby': ('Russian Educational & Hobby Channels Online — Live, No VPN', 'Russian educational and hobby channels', 'Watch Russian educational, nature, travel, animal and auto channels live online for free: {names}. No VPN, no registration, 24/7.', 'Russian educational and hobby channels online'),
 'sport': ('Russian Sports Channels Online — Live Sport TV, No VPN', 'Russian sports channels', 'Watch sports channels live online for free: {names}. No VPN, no registration, 24/7.', 'Sports channels online'),
}
RU_TITLES = {'novosti':'Новости','razvlecheniya':'Развлечения','kino':'Кино','detskie':'Детские','muzyka':'Музыка','hobbi':'Хобби','sport':'Спорт'}

base = rd('novosti/index.html')
styles = ''.join(re.findall(r'<style>.*?</style>', base, re.S))
consent = '<script src="/assets/consent.js"></script>'
tg_svg = re.search(r'<a href="https://t\.me/RussiaTV_Hub_Live" target="_blank" class="tg-btn">\s*(<svg.*?</svg>)', base, re.S).group(1)

def grp(label):
    for g in groups:
        if g['label'].endswith(label): return g['channels']
    return []

def build(c):
    en_slug, ru_slug, label, emo, _ = c
    chs = grp(label)
    title, kw, desc_t, h1 = TXT[en_slug]
    names = ', '.join((x.get('nameEn') or x['name']) for x in chs[:6])
    desc = desc_t.format(names=names)
    url = f'https://russian-tv.com/en/{en_slug}/'; ru_url = f'https://russian-tv.com/{ru_slug}/'
    cards = ''
    for x in chs:
        nm = x.get('nameEn') or x['name']
        cards += (f'\n        <a href="/en/{x["slug"]}/" class="cat-ch-card">\n          <div class="cat-ch-icon" style="background:{x["iconBg"]};color:{x["color"]}">{esc(x["icon"])}</div>\n'
                  f'          <div class="cat-ch-name">{esc(nm)}</div>\n          <div class="cat-ch-desc">{esc(x["desc"])}</div>\n'
                  f'          <div class="cat-ch-live"><span class="cat-live-dot"></span>LIVE</div>\n        </a>\n')
    nav = ''.join(f'\n    <a href="/en/{s}/"{" class=\'cur\'" if s == en_slug else ""}>{e} {l}</a>' for s, _, l, e, _ in CATS)
    foot_nav = ''.join(f'\n    <a href="/en/{s}/">{l}</a>' for s, _, l, e, _ in CATS)
    n = len(chs)
    faq = [
      (f'Where can I watch {kw.lower()} online for free?', f'On russian-tv.com you can watch {n} {kw.lower()} live: {names} and more. Streams run 24/7 without registration or VPN.'),
      (f'Can I watch {kw.lower()} from abroad?', f'Yes. All channels on this page are available from any country on russian-tv.com without a VPN.'),
      ('Do I need to register?', 'No. Every channel is free and works without registration or subscription.'),
    ]
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "WebPage", "@id": url, "url": url, "name": title, "description": desc, "inLanguage": "en", "isPartOf": {"@id": "https://russian-tv.com/en/#website"}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://russian-tv.com/en/"},
            {"@type": "ListItem", "position": 2, "name": h1, "item": url}]},
        {"@type": "CollectionPage", "name": title, "url": url, "numberOfItems": n, "description": desc},
        {"@type": "ItemList", "name": h1, "numberOfItems": n, "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": (x.get('nameEn') or x['name']), "url": f'https://russian-tv.com/en/{x["slug"]}/'} for i, x in enumerate(chs)]},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]},
    ]}
    faq_html = ''.join(f'\n    <details>\n      <summary>{esc(q)} <span>▾</span></summary>\n      <p>{esc(a)}</p>\n    </details>' for q, a in faq)
    ogimg = 'https://russian-tv.com/og-image.jpg'
    page = f'''<!DOCTYPE html>
<html lang="en" prefix="og: https://ogp.me/ns#">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>▶ {esc(title)}</title>
  <meta name="description" content="▶ {esc(desc)}"/>
  <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1"/>
  <link rel="canonical" href="{url}"/>
  <link rel="alternate" hreflang="ru" href="{ru_url}"/>
  <link rel="alternate" hreflang="en" href="{url}"/>
  <link rel="alternate" hreflang="x-default" href="{ru_url}"/>
  <link rel="icon" type="image/svg+xml" href="/favicon.svg"/>
  <link rel="icon" sizes="120x120" href="/favicon-120.png"/>
  <link rel="icon" type="image/png" sizes="192x192" href="/favicon-192.png"/>
  <link rel="shortcut icon" href="/favicon.ico"/>
  <meta name="theme-color" content="#003580"/>
  <meta property="og:type" content="website"/>
  <meta property="og:site_name" content="Russian TV"/>
  <meta property="og:title" content="{esc(title)}"/>
  <meta property="og:description" content="{esc(desc)}"/>
  <meta property="og:url" content="{url}"/>
  <meta property="og:locale" content="en_US"/>
  <meta property="og:image" content="{ogimg}"/>
  <meta property="og:image:width" content="1200"/>
  <meta property="og:image:height" content="630"/>
  <meta name="twitter:card" content="summary_large_image"/>
  <meta name="twitter:title" content="{esc(title)}"/>
  <meta name="twitter:description" content="{esc(desc)}"/>
  <meta name="twitter:image" content="{ogimg}"/>
  <script type="application/ld+json">{json.dumps(ld, ensure_ascii=False, indent=2)}</script>
  {consent}
  {styles}
</head>
<body>
<header>
  <a href="/en/" class="logo"><span style="font-size:26px">🇷🇺</span><span class="logo-text"><span class="r">Rus</span><span class="w">sian</span></span><span class="b">TV</span></a>
  <a href="https://t.me/RussiaTV_Hub_Live" target="_blank" class="tg-btn">
    {tg_svg}
    Subscribe
  </a>
</header>
<div class="breadcrumb">
  <a href="/en/">Home</a><span>›</span>
  <span>{esc(h1)}</span>
</div>
<div class="wrap">
  <div class="page-header">
    <h1>{esc(h1[0].upper() + h1[1:])}</h1>
    <div class="meta">
      <span class="badge">{n} channels</span>
      <span class="live-badge"><span class="live-dot"></span>LIVE 24/7</span>
    </div>
  </div>

  <nav class="cat-nav" aria-label="Categories">{nav}
  </nav>

  <div class="ch-grid">
{cards}
  </div>

  <div class="seo-box">
    <h2>{esc(h1)} — watch free</h2>
    <p>{esc(desc)} All streams come from publicly available sources; the site does not host video.</p>
  </div>

  <div class="faq-box" style="margin-top:16px">
    <h2>Frequently asked questions</h2>{faq_html}
  </div>
</div>

<footer>
  <div>🇷🇺 <a href="/en/">Russian TV</a> — free Russian TV online</div>
  <div style="margin-top:6px">{foot_nav}
    <a href="https://t.me/RussiaTV_Hub_Live" target="_blank">Telegram</a>
  </div>
  <div class="legal-note" style="text-align:center;margin:10px auto 0;max-width:760px;padding:0 12px;font-size:11px;line-height:1.5;color:#8b8ba0">Stream links are taken from publicly available sources. At the request of a rights holder, a stream will be removed after proof of rights ownership is provided — <a href="/en/privacy/#rightsholders" style="color:inherit;text-decoration:underline">details</a>. · <a href="/en/advertising/" style="color:inherit;text-decoration:underline">Advertise with us</a></div>
</footer>
</body>
</html>
'''
    wr(f'en/{en_slug}/index.html', page)

for c in CATS: build(c)

# --- RU категории: hreflang + Спорт в навигации ---
for en_slug, ru_slug, *_ in CATS:
    p = f'{ru_slug}/index.html'
    s = rd(p); o = s
    if 'hreflang="en"' not in s:
        alt = (f'  <link rel="alternate" hreflang="ru" href="https://russian-tv.com/{ru_slug}/"/>\n'
               f'  <link rel="alternate" hreflang="en" href="https://russian-tv.com/en/{en_slug}/"/>\n'
               f'  <link rel="alternate" hreflang="x-default" href="https://russian-tv.com/{ru_slug}/"/>\n')
        s = re.sub(r'(  <link rel="canonical" href="https://russian-tv\.com/%s/"/>\n)' % ru_slug, r'\1' + alt.replace('\\', '\\\\'), s, 1)
    if ru_slug != 'sport' and '<a href="/sport/"' not in s:
        s = re.sub(r'(\s*<a href="/hobbi/"[^>]*>🌿 Хобби</a>)', r'\1\n    <a href="/sport/" >⚽ Спорт</a>', s, 1)
        s = re.sub(r'(\s*<a href="/hobbi/">Хобби</a>)', r'\1\n    <a href="/sport/">Спорт</a>', s, 1)
    if s != o: wr(p, s)

# --- EN канальные страницы: ссылки на категории ---
CATMAP = {'News': 'news', 'Entertainment': 'entertainment', 'Movies': 'movies', 'Kids': 'kids', 'Music': 'music', 'Hobby': 'hobby', 'Sport': 'sport'}
for en_slug, *_ in CATS:
    pass
print('EN category pages built:', len(CATS))
