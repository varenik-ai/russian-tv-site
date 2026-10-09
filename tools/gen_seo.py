#!/usr/bin/env python3
"""SEO/UX улучшения для russian-tv-site. Запуск: python3 gen_seo.py <репо>. Идемпотентен."""
import re, os, sys, glob, importlib.util

ROOT = sys.argv[1]
spec = importlib.util.spec_from_file_location('g', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gen_site.py'))
sys.argv = [sys.argv[0], ROOT]
g = importlib.util.module_from_spec(spec); spec.loader.exec_module(g)
CHANNELS = g.CHANNELS

TOTAL = 58
OGIMG = 'https://russian-tv.com/og-image.jpg'
TODAY = '2026-10-09'

def rd(p):
    with open(os.path.join(ROOT, p), encoding='utf-8') as f: return f.read()
def wr(p, s):
    with open(os.path.join(ROOT, p), 'w', encoding='utf-8') as f: f.write(s)

pages = {}
for f in glob.glob(os.path.join(ROOT, '**/index.html'), recursive=True):
    rel = os.path.relpath(f, ROOT)
    pages['/' + rel[:-10]] = rel
pages['/'] = 'index.html'
pages = {('/' if p == '/' else (p if p.endswith('/') else p + '/')): f for p, f in pages.items()}
def is_stub(s): return 'noindex' in s[:3000]
stubs = {p for p, f in pages.items() if is_stub(rd(f))}

# --- A. og:image / twitter ---
def fix_social(s):
    add = ''
    if 'property="og:image"' not in s:
        add += f'  <meta property="og:image" content="{OGIMG}"/>\n  <meta property="og:image:width" content="1200"/>\n  <meta property="og:image:height" content="630"/>\n'
    if 'name="twitter:card"' not in s:
        add += '  <meta name="twitter:card" content="summary_large_image"/>\n'
    if 'name="twitter:image"' not in s:
        add += f'  <meta name="twitter:image" content="{OGIMG}"/>\n'
    if add and '</head>' in s:
        s = s.replace('</head>', add + '</head>', 1)
    return s

# --- C. единое число каналов ---
def fix_counts(s):
    n = TOTAL
    pats = [
        (r'(Все|все) (?:34|35|41|42|58|59) канал(?:а|ов)?\b', lambda m: f'{m.group(1)} {n} каналов'),
        (r'\b(?:34|35|41|42|58|59) канал(?:а|ов)?\b', lambda m: f'{n} каналов'),
        (r'\b(?:34|35|41|42|58|59) российских телеканал(?:а|ов)?\b', lambda m: f'{n} российских телеканалов'),
        (r'\b(All|all) (?:34|35|41|42|58|59) (channels|Channels)\b', lambda m: f'{m.group(1)} {n} {m.group(2)}'),
        (r'\b(?:34|35|41|42|58|59) (channels|Channels|Russian TV channels|Russian channels|Russian TV Channels|live channels|Live channels|Live Channels)\b', lambda m: f'{n} {m.group(1)}'),
    ]
    for p, rep in pats: s = re.sub(p, rep, s)
    s = s.replace('"numberOfItems":34', f'"numberOfItems":{n}').replace('"numberOfItems": 34', f'"numberOfItems": {n}')
    return s

# --- D. короткие EN title ---
def fix_title(s):
    m = re.search(r'<title>([^<]*)</title>', s)
    if m and len(m.group(1)) > 66 and ' | ' in m.group(1) and ' — No VPN' in m.group(1):
        t = m.group(1)
        short = t.split(' | ')[0] + ' — No VPN'
        s = s.replace(m.group(0), f'<title>{short}</title>', 1)
    return s

# --- G. resource hints на страницах каналов ---
def fix_hints(s):
    if '/stream?channel=' not in s and "CH_ID" not in s: return s
    hint = '  <link rel="preconnect" href="https://stream.russian-tv.com" crossorigin/>\n  <link rel="dns-prefetch" href="https://cdnjs.cloudflare.com"/>\n'
    if 'href="https://stream.russian-tv.com"' in s: return s
    return s.replace('<meta charset="UTF-8"/>\n', '<meta charset="UTF-8"/>\n' + hint, 1) if '<meta charset="UTF-8"/>\n' in s else s

changed = 0
for p, f in pages.items():
    if p in stubs: continue
    s = rd(f); o = s
    s = fix_social(s); s = fix_counts(s)
    if p.startswith('/en/'): s = fix_title(s)
    if p.endswith('-live/'): s = fix_hints(s)
    if s != o: wr(f, s); changed += 1
print('pages changed:', changed)

# --- B. sitemap с hreflang ---
sm = rd('sitemap.xml')
urls = re.findall(r'<loc>https://russian-tv.com([^<]+)</loc>', sm)
urls = [u for u in urls if u not in stubs and u in pages]
for p in pages:  # добавляем живые страницы, которых нет в sitemap (кроме служебных)
    if p in stubs or p in urls: continue
    if p.startswith('/blog/') or p.startswith('/en/blog/'): continue
    pass
for extra in sorted(pages):
    if extra not in stubs and extra not in urls and extra != '/404.html': urls.append(extra)
def prio(u):
    m = re.search(r'<loc>https://russian-tv.com%s</loc><changefreq>[^<]*</changefreq><priority>([^<]*)</priority>' % re.escape(u), sm)
    return m.group(1) if m else '0.7'
def freq(u):
    m = re.search(r'<loc>https://russian-tv.com%s</loc><changefreq>([^<]*)</changefreq>' % re.escape(u), sm)
    return m.group(1) if m else 'weekly'
def lm(u):
    m = re.search(r'<loc>https://russian-tv.com%s</loc>.*?<lastmod>([^<]*)</lastmod>' % re.escape(u), sm)
    old = m.group(1) if m else TODAY
    if u.endswith('-live/') or u in ('/', '/en/', '/novosti/', '/kino/', '/muzyka/', '/detskie/', '/razvlecheniya/', '/hobbi/', '/sport/'):
        return TODAY
    return old
out = ['<?xml version="1.0" encoding="UTF-8"?>',
       '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
def pair(u):
    if u == '/': return '/en/'
    if u == '/en/': return '/'
    if u.startswith('/en/'): ru = u[3:]; return ru if ru in pages and ru not in stubs else None
    en = '/en' + u
    return en if en in pages and en not in stubs else None
for u in urls:
    alt = pair(u)
    line = f'  <url><loc>https://russian-tv.com{u}</loc>'
    if alt:
        ru_u, en_u = (u, alt) if not u.startswith('/en/') and u != '/en/' else (alt, u)
        line += (f'<xhtml:link rel="alternate" hreflang="ru" href="https://russian-tv.com{ru_u}"/>'
                 f'<xhtml:link rel="alternate" hreflang="en" href="https://russian-tv.com{en_u}"/>'
                 f'<xhtml:link rel="alternate" hreflang="x-default" href="https://russian-tv.com{ru_u}"/>')
    line += f'<changefreq>{freq(u)}</changefreq><priority>{prio(u)}</priority><lastmod>{lm(u)}</lastmod></url>'
    out.append(line)
out.append('</urlset>')
wr('sitemap.xml', '\n'.join(out) + '\n')
print('sitemap urls:', len(urls))

# --- H. статические ссылки на новые каналы на главных (для краулеров) ---
def home_links(path, lang):
    s = rd(path)
    if 'data-seo-new="1"' in s: return
    style = 'style="color:var(--accent2);text-decoration:underline"'
    groups = {}
    for c in CHANNELS: groups.setdefault(c['cat'], []).append(c)
    labels_ru = {'news':'Новости','ent':'Развлечения','kino':'Кино','kids':'Детские','music':'Музыка и радио','hobby':'Познавательные и хобби','sport':'Спорт'}
    labels_en = {'news':'News','ent':'Entertainment','kino':'Movies','kids':'Kids','music':'Music & radio','hobby':'Educational & hobby','sport':'Sport'}
    parts = []
    for cat in ('news','ent','kino','kids','music','hobby','sport'):
        if cat not in groups: continue
        links = ', '.join(
            (f'<a href="/{c["slug"]}/" {style}>{c["ru"]}</a>' if lang == 'ru' else f'<a href="/en/{c["slug"]}/" {style}>{c["en"]}</a>')
            for c in groups[cat])
        parts.append(f'<strong>{(labels_ru if lang == "ru" else labels_en)[cat]}:</strong> {links}.')
    head = 'Ещё в эфире:' if lang == 'ru' else 'Also on air:'
    block = f'    <p data-seo-new="1"><strong>{head}</strong> ' + ' '.join(parts) + '</p>\n'
    key = '<strong>Развлечения:</strong>' if lang == 'ru' else '<strong>Entertainment:</strong>'
    i = s.find(key)
    if i < 0: print('home block not found', path); return
    e = s.find('</p>', i) + 5
    s = s[:e] + block + s[e:]
    wr(path, s)
home_links('index.html', 'ru'); home_links('en/index.html', 'en')

# --- E. 404 ---
if not os.path.exists(os.path.join(ROOT, '404.html')):
    cats = [('Новости','/novosti/'),('Кино','/kino/'),('Развлечения','/razvlecheniya/'),('Детские','/detskie/'),('Музыка','/muzyka/'),('Хобби','/hobbi/'),('Спорт','/sport/')]
    pop = [('Первый канал','/perviy-kanal-live/'),('Россия 1','/rossiya-1-live/'),('НТВ','/ntv-live/'),('Россия 24','/rossiya-24-live/'),('ТНТ4','/tnt-live/'),('МУЗ-ТВ','/muz-tv-live/')]
    li = lambda xs: ''.join(f'<a href="{u}">{n}</a>' for n, u in xs)
    wr('404.html', f'''<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<meta name="robots" content="noindex, follow"/>
<title>Страница не найдена — Русское ТВ</title>
<style>body{{margin:0;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;background:#0a0a14;color:#e8e8f0;text-align:center;padding:48px 16px}}h1{{font-size:28px;margin:0 0 8px}}p{{color:#9a9ab0;margin:0 0 24px}}.l{{display:flex;flex-wrap:wrap;gap:10px;justify-content:center;max-width:640px;margin:0 auto 28px}}.l a{{background:#1a1a2e;border:1px solid #2a2a40;border-radius:20px;padding:8px 16px;color:#e8e8f0;text-decoration:none}}.l a:hover{{border-color:#4a7bd8}}.b{{display:inline-block;background:#1a5fd9;color:#fff;border-radius:10px;padding:12px 24px;text-decoration:none;font-weight:700}}</style>
</head>
<body>
<h1>Такой страницы нет</h1>
<p>Возможно, канал переехал или адрес введён с ошибкой. Выберите раздел или популярный канал:</p>
<div class="l">{li(cats)}</div>
<div class="l">{li(pop)}</div>
<a class="b" href="/">Все {TOTAL} каналов</a>
<p style="margin-top:28px"><a href="/en/" style="color:#9a9ab0">English version</a></p>
</body>
</html>
''')
    print('404.html created')

# --- I. ItemList главных: добавить новые каналы, чтобы numberOfItems совпадал со списком ---
def itemlist(path, lang):
    s = rd(path)
    m = re.search(r'"@type":"ItemList".*?"itemListElement":\[(.*?)\]\}', s, re.S)
    if not m: print('no ItemList', path); return
    body = m.group(1)
    n = len(re.findall(r'"@type":"ListItem"', body))
    add = ''
    for c in CHANNELS:
        if f'/{c["slug"]}/' in body: continue
        n += 1
        url = f'https://russian-tv.com/{c["slug"]}/' if lang == 'ru' else f'https://russian-tv.com/en/{c["slug"]}/'
        name = c['ru'] if lang == 'ru' else c['en']
        add += f',\n        {{"@type":"ListItem","position":{n},"name":"{name}","url":"{url}"}}'
    if not add: return
    s = s[:m.start(1)] + body.rstrip() + add + s[m.end(1):]
    s = re.sub(r'("@type":"ItemList","name":"[^"]*","numberOfItems":)\d+', lambda mm: mm.group(1) + str(n), s, count=1)
    wr(path, s)
itemlist('index.html', 'ru'); itemlist('en/index.html', 'en')

# --- J. грамматика: «все N каналов доступен» -> «доступны» ---
for p, f in pages.items():
    if p in stubs: continue
    s = rd(f)
    s2 = re.sub(r'(?i)(все \d+ каналов) доступен\b', r'\1 доступны', s)
    if s2 != s: wr(f, s2)
