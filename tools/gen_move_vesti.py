#!/usr/bin/env python3
"""16.11.2026: «Вести FM» (информационное радио ВГТРК) перенесён из «Музыки» в «Новости» (RU+EN): боковые списки, главные, карточки и счётчики
категорий, JSON-LD, абзац «Ещё в эфире» (пересоздаётся gen_site), текст блога. Категория в gen_site.py (CH) уже 'news'. Идемпотентен.
Запускать после gen_site.py (в run_all.sh стоит сразу за gen_remove_broken)."""
import sys, os, re, glob
ROOT = sys.argv[1]
def rd(p): return open(os.path.join(ROOT, p), encoding='utf-8').read()
def wr(p, s): open(os.path.join(ROOT, p), 'w', encoding='utf-8').write(s)
SLUG = 'vesti-fm-live'
def item_rx(en):
    pre = '/en' if en else ''
    return re.compile(r'^<a href="%s/%s/" class="ch-item-s[^"]*"[^\n]*</a>\n?' % (pre, SLUG), re.M)
def section_span(s, label):
    marker = f'<div class="cat-label-s">{label}</div>'
    i = s.find(marker)
    if i < 0: return None
    c = [x for x in (s.find('<div class="cat-label-s">', i + len(marker)), s.find('\n    </div>\n  </aside>', i)) if x > 0]
    return (i, min(c)) if c else None
changed = 0
for f in glob.glob(os.path.join(ROOT, '**/index.html'), recursive=True):
    rel = os.path.relpath(f, ROOT); en = rel.startswith('en/')
    s = open(f, encoding='utf-8').read(); o = s
    if 'id="ch-list"' in s:
        m = item_rx(en).search(s)
        if m:
            music = section_span(s, '🎵 Music' if en else 'Музыка'); news = section_span(s, '📡 News' if en else 'Новости')
            if music and news and music[0] < m.start() < music[1]:
                item = m.group(0).rstrip('\n'); s = s[:m.start()] + s[m.end():]
                news = section_span(s, '📡 News' if en else 'Новости')
                s = s[:news[1]].rstrip('\n') + '\n' + item + s[news[1]:]
    if s != o: wr(rel, s); changed += 1
print('боковые списки:', changed)
# главные: убрать запись из группы «Музыка», остаётся в «Новости»
for path, en in (('index.html', False), ('en/index.html', True)):
    s = rd(path); o = s
    ms = list(re.finditer(r'(?m)^[ \t]*\{ id:[\'"]vestifm[\'"].*\},?\n', s))
    if len(ms) > 1:
        for m in reversed(ms):   # с конца, чтобы не сдвигать позиции
            lab = s.rfind('label:', 0, m.start())
            if re.match(r'label:\s*[\'"][^\'"\n]*(Музык|Music)', s[lab:lab + 60]):
                s = s[:m.start()] + s[m.end():]; break
    s = re.sub(r'<p data-seo-new="1">.*?</p>\n?', '', s, flags=re.S)   # gen_site пересоздаст абзац с новой категорией
    if s != o: wr(path, s)
# карточки категорий «Музыка» (RU, EN): убрать Вести FM, пересчитать
def strip_card(s):
    return re.sub(r'\n        <a href="/(?:en/)?%s/" class="cat-ch-card">.*?</a>\n' % SLUG, '\n', s, flags=re.S)
for p, en in (('muzyka/index.html', False), ('en/music/index.html', True)):
    s = rd(p); o = s
    s = strip_card(s)
    n = len(re.findall(r'class="cat-ch-card">', s))
    # JSON-LD ItemList
    def fix_list(m):
        items = [x for x in re.findall(r'\{[^{}]*?"@type":\s*"ListItem"[^{}]*?\}', m.group(2), re.S) if SLUG not in x and 'Vesti FM' not in x and 'Вести FM' not in x]
        return m.group(0)
    s = re.sub(r'"numberOfItems": \d+', f'"numberOfItems": {n}', s)
    s = re.sub(r'<span class="badge">\d+ (каналов|channels)</span>', lambda m: f'<span class="badge">{n} {m.group(1)}</span>', s)
    if en:
        s = s.replace(', Vesti FM', '')
        s = re.sub(r'you can watch \d+ russian music channels', f'you can watch {n} russian music channels', s)
        s = re.sub(r'\s*\{\s*"@type":\s*"ListItem",\s*"position":\s*\d+,\s*"name":\s*"Vesti FM"[^{}]*\},?', '', s)
    else:
        s = re.sub(r'\s*\{\s*"@type":\s*"ListItem",\s*"position":\s*\d+,\s*"name":\s*"Вести FM"[^{}]*\},?', '', s)
    if s != o: wr(p, s)
# блог (RU): радио Вести FM — в «Новостях»
p = 'blog/kakie-kanaly-smotret-po-temam/index.html'
if os.path.exists(os.path.join(ROOT, p)):
    s = rd(p); o = s
    s = s.replace('Да, в разделе «Музыка» доступны радиостанции Страна FM и Вести FM. Видеоряда у радио может не быть.',
                  'Да, в разделе «Музыка» доступна радиостанция Страна FM, а информационное радио Вести FM находится в разделе «Новости». Видеоряда у радио может не быть.')
    s = s.replace('а также радио <a href="/strana-fm-live/">Страна FM</a> и <a href="/vesti-fm-live/">Вести FM</a>. Раздел: <a href="/muzyka/">Музыка</a>.',
                  'а также радио <a href="/strana-fm-live/">Страна FM</a>. Раздел: <a href="/muzyka/">Музыка</a>. Радио <a href="/vesti-fm-live/">Вести FM</a> — информационное, оно в разделе <a href="/novosti/">Новости</a>.')
    if s != o: wr(p, s)
print('готово')
