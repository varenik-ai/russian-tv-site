#!/usr/bin/env python3
"""Удаление Патриота и перенос каналов между категориями (подготовка; затем gen_site/gen_seo/... расставят по новым местам). Идемпотентно."""
import sys, os, re, glob, shutil
ROOT = sys.argv[1]
def rd(p): return open(os.path.join(ROOT, p), encoding='utf-8').read()
def wr(p, s): open(os.path.join(ROOT, p), 'w', encoding='utf-8').write(s)
REMOVE = ['patriot-live']
MOVE_OLD = {'soloviev-live': ('Развлечения', 'Новости', '🎬 Entertainment', '📡 News', 'razvlecheniya', 'novosti')}  # старые каналы: переносим готовую разметку
RELOC_NEW = ['ryzhiy-live', 'bober-live', 'chestnyy-detektiv-live']   # новые: удаляем отовсюду, gen_site вернёт на правильное место

def item_rx(slug, en): 
    pre = '/en' if en else ''
    return re.compile(r'^<a href="%s/%s/" class="ch-item-s[^"]*"[^\n]*</a>\n?' % (pre, re.escape(slug)), re.M)

def section_span(s, label):
    marker = f'<div class="cat-label-s">{label}</div>'
    i = s.find(marker)
    if i < 0: return None
    c = [x for x in (s.find('<div class="cat-label-s">', i + len(marker)), s.find('\n    </div>\n  </aside>', i)) if x > 0]
    return (i, min(c)) if c else None

def decl(n):
    if n % 10 == 1 and n % 100 != 11: return 'канал'
    if 2 <= n % 10 <= 4 and not 12 <= n % 100 <= 14: return 'канала'
    return 'каналов'

def recount_page(s, old, new):
    s = re.sub(r'\b%d (канал(?:а|ов)?)\b' % old, lambda m: f'{new} {decl(new)}', s)
    s = re.sub(r'\b%d (новостных каналов)' % old, lambda m: f'{new} {m.group(1)}', s)
    s = s.replace('"numberOfItems": %d' % old, '"numberOfItems": %d' % new)
    return s

pages = [f for f in glob.glob(os.path.join(ROOT, '**/index.html'), recursive=True)]
changed = 0
captured = {}
for f in pages:
    rel = os.path.relpath(f, ROOT)
    s = open(f, encoding='utf-8').read(); o = s
    en = rel.startswith('en/')
    if 'id="ch-list"' in s:
        for slug in REMOVE + RELOC_NEW:
            s = item_rx(slug, en).sub('', s)
            s = re.sub(r'<a href="%s/%s/" class="sim-item">.*?</a>\n?' % ('/en' if en else '', re.escape(slug)), '', s, flags=re.S)
        for slug, (rl, nl, el, nel, rcat, ncat) in MOVE_OLD.items():
            m = item_rx(slug, en).search(s)
            if not m: continue
            item = m.group(0).rstrip('\n'); s = s[:m.start()] + s[m.end():]
            sp = section_span(s, nel if en else nl)
            if sp and item not in s: s = s[:sp[1]].rstrip('\n') + '\n' + item + s[sp[1]:]
    # Патриот: убрать ссылки в оставшихся блоках
    s = re.sub(r'<a href="%s/patriot-live/" class="sim-item">.*?</a>\n?' % ('/en' if en else ''), '', s, flags=re.S)
    s = re.sub(r'(?m)^[ \t]*\{ id:[\'"](?:patriot|ryzhiy|bober|detektiv)[\'"].*\},?\n', '', s)
    s = re.sub(r'<p data-seo-new="1">.*?</p>\n?', '', s, flags=re.S)
    if s != o: wr(rel, s); changed += 1
print('pages touched:', changed)

# главные: перенос soloviev между группами
for path, en in (('index.html', False), ('en/index.html', True)):
    s = rd(path)
    m = re.search(r'(?m)^[ \t]*\{ id:[\'"]soloviev[\'"].*\},?\n', s)
    if m:
        line = m.group(0).rstrip('\n'); line = line if line.endswith(',') else line + ','
        s = s[:m.start()] + s[m.end():]
        lab = 'News' if en else 'Новости'
        mm = re.search(r'\n  \{ label:[\'"][^\'"\n]*' + lab + r'[^\'"\n]*[\'"], channels:\[\n', s)
        e = s.find('\n  ]},', mm.end())
        if line not in s: s = s[:e].rstrip('\n') + '\n' + line + s[e:]
        wr(path, s)
    # ItemList (RU): убрать patriot и перенумеровать
    mm = re.search(r'"@type":"ItemList".*?"itemListElement":\[(.*?)\]\}', s, re.S)
    if mm and 'patriot-live' in mm.group(1):
        items = [x for x in re.findall(r'\{"@type":"ListItem","position":\d+,"name":"[^"]*","url":"[^"]*"\}', mm.group(1)) if 'patriot-live' not in x]
        items = [re.sub(r'"position":\d+', f'"position":{i+1}', x) for i, x in enumerate(items)]
        s = s[:mm.start(1)] + ',\n        '.join(items) + s[mm.end(1):]
        s = re.sub(r'("@type":"ItemList","name":"[^"]*","numberOfItems":)\d+', lambda m2: m2.group(1) + str(len(items)), s, count=1)
        wr(path, s)

# RU-страницы категорий: убрать карточки, перенести soloviev, пересчитать
def cards(s): return len(re.findall(r'class="cat-ch-card">', s))
CARD = re.compile(r'\n        <a href="/%s/" class="cat-ch-card">.*?</a>\n', re.S)
for cat in ('razvlecheniya', 'novosti', 'kino', 'detskie', 'muzyka', 'hobbi'):
    p = f'{cat}/index.html'; s = rd(p); o = s; old = cards(s)
    for slug in REMOVE + RELOC_NEW + list(MOVE_OLD):
        if cat == 'novosti' and slug in MOVE_OLD: continue
        mm = re.search(CARD.pattern % re.escape(slug), s, re.S)
        if mm:
            if slug in MOVE_OLD: captured[slug] = mm.group(0)
            s = s[:mm.start()] + s[mm.end():]
    n = cards(s)
    if n != old: s = recount_page(s, old, n)
    if s != o: wr(p, s)
p = 'novosti/index.html'; s = rd(p); o = s; old = cards(s)
for slug, blk in captured.items():
    if f'href="/{slug}/"' not in s:
        last = s.rfind('class="cat-ch-card">'); e = s.find('</a>', last) + 4
        s = s[:e] + '\n' + blk.strip('\n') + s[e:]
n = cards(s)
if n != old: s = recount_page(s, old, n)
if s != o: wr(p, s)

# файлы
for slug in REMOVE:
    for d in (slug, f'en/{slug}'):
        shutil.rmtree(os.path.join(ROOT, d), ignore_errors=True)
    og = os.path.join(ROOT, 'assets/og', slug + '.jpg')
    if os.path.exists(og): os.remove(og)
print('done')
