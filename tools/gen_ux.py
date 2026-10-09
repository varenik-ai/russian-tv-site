#!/usr/bin/env python3
"""UX/SEO: размеры логотипов, хлебные крошки с категорией (RU/EN), ссылки на EN-категории, мобильный переключатель каналов, удаление старых страниц."""
import sys, os, re, glob, shutil
ROOT = sys.argv[1]
RU_CAT = {'Новости':'novosti','Развлечения':'razvlecheniya','Кино':'kino','Детские':'detskie','Музыка':'muzyka','Хобби':'hobbi','Спорт':'sport'}
EN_CAT = {'News':'news','Entertainment':'entertainment','Movies':'movies','Kids':'kids','Music':'music','Hobby':'hobby','Sport':'sport'}
IMG = re.compile(r'(<div class="ch-icon-s ch-logo-s"><img src="[^"]*" alt="[^"]*" loading="lazy")(?![^>]*width=)(>)')
n = 0
for f in glob.glob(os.path.join(ROOT, '**/index.html'), recursive=True):
    rel = os.path.relpath(f, ROOT)
    s = open(f, encoding='utf-8').read(); o = s
    if 'noindex' in s[:3000]: continue
    en = '<html lang="en"' in s[:400]
    if 'id="ch-list"' in s:
        s = IMG.sub(r'\1 width="30" height="30"\2', s)
        m = re.search(r'<span class="cat-badge">([^<]*)</span>', s)
        cat = m.group(1) if m else None
        if en and cat in EN_CAT:
            slug = EN_CAT[cat]
            s = s.replace('<a href="/en/">Channels</a>', f'<a href="/en/{slug}/">{cat}</a>', 1)
            s = re.sub(r'\{"@type": "ListItem", "position": 2, "name": "([^"]*)", "item": "(https://russian-tv\.com/en/[^"]+)"\}',
                       lambda mm: f'{{"@type": "ListItem", "position": 2, "name": "{cat}", "item": "https://russian-tv.com/en/{slug}/"}},\n        {{"@type": "ListItem", "position": 3, "name": "{mm.group(1)}", "item": "{mm.group(2)}"}}', s, count=1) if '"position": 3' not in s else s
        elif not en and cat in RU_CAT:
            slug = RU_CAT[cat]
            s = s.replace('<a href="/#channels">Каналы</a>', f'<a href="/{slug}/">{cat}</a>', 1)
        if '/assets/site-ux.js' not in s:
            s = s.replace('</body>', '<script defer src="/assets/site-ux.js?v=2"></script>\n</body>', 1)
    if en:
        s = re.sub(r'href="/en/\?cat=(news|entertainment|movies|kids|music|hobby|sport)"', r'href="/en/\1/"', s)
    if s != o: open(f, 'w', encoding='utf-8').write(s); n += 1
print('pages updated:', n)
for d in ('setanta-sports-1-live', 'setanta-sports-2-live', 'belarus-5-live'):
    p = os.path.join(ROOT, d)
    if os.path.isdir(p): shutil.rmtree(p); print('removed', d)
