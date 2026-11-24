#!/usr/bin/env python3
"""24.11.2026: в боковых списках страниц, созданных из старого шаблона (gen_site.py, коммит 827dc43), остался пункт «ТНТ4» (EN «TNT4») в рубрике «Новости».
Канал tnt теперь основной ТНТ (рубрика «Развлечения»): пункт переименовывается в «ТНТ»/«TNT» и переносится сразу после «Пятница!». Идемпотентен."""
import sys, os, re, glob
ROOT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else '.')
ITEM = re.compile(r'<a href="(/en)?/tnt-live/" class="ch-item-s( active)?" data-name="(ТНТ4|TNT4)" aria-label="(?:ТНТ4|TNT4)">.*?</a>\n?', re.S)
n = 0
for f in glob.glob(os.path.join(ROOT, '**/index.html'), recursive=True):
    if '/tools/' in f or '/.git/' in f: continue
    s = o = open(f, encoding='utf-8').read()
    s = s.replace('content="ТНТ4 — юмор', 'content="ТНТ — юмор')   # og:description страницы ТНТ
    # любые ссылки на /tnt-live/ (блок «Популярные» и др.): название ТНТ4/TNT4 -> ТНТ/TNT
    s = re.sub(r'<a\b[^>]*href="(?:/en)?/tnt-live/"[^>]*>.*?</a>', lambda x: x.group(0).replace('ТНТ4', 'ТНТ').replace('TNT4', 'TNT') if 'class="ch-item-s' not in x.group(0) else x.group(0), s, flags=re.S)
    m = ITEM.search(s)
    if not m:
        if s != o: open(f, 'w', encoding='utf-8').write(s); n += 1
        continue
    new_name = 'ТНТ' if m.group(3) == 'ТНТ4' else 'TNT'
    blk = m.group(0).replace('data-name="%s" aria-label="%s"' % (m.group(3), m.group(3)), 'data-name="%s" aria-label="%s"' % (new_name, new_name)).replace('<div class="ch-name-s">%s</div>' % m.group(3), '<div class="ch-name-s">%s</div>' % new_name)
    s = s[:m.start()] + s[m.end():]
    if not blk.endswith('\n'): blk += '\n'
    pm = re.search(r'<a href="(?:/en)?/pyatnica-live/" class="ch-item-s[^"]*"[^>]*>.*?</a>\n?', s, re.S)
    if pm: s = s[:pm.end()] + ('' if pm.group(0).endswith('\n') else '\n') + blk + s[pm.end():]
    else: s = s[:m.start()] + blk + s[m.start():]
    if s != o: open(f, 'w', encoding='utf-8').write(s); n += 1
print('gen_fix_tnt_sidebar: страниц изменено', n)
