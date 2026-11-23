#!/usr/bin/env python3
"""23.11.2026: «Россия РТР — Европа» (rtrEuro) убрана с сайта по решению владельца; в мини-аппе канал остаётся.
Запускать последним (после gen_recount.py): другие генераторы заново пишут ссылки и число каналов.
Что делает (идемпотентно):
- страницы /rossiya-rtr-evropa-live/ и /en/rossiya-rtr-evropa-live/ — заглушки noindex с переадресацией на «Россия 1» (как у прежних убранных каналов);
- убирает пункты боковых списков, карточки категорий и стран, «Похожие», строки таблиц, элементы ItemList (JSON-LD), данные каналов на главных и /tv/;
- переписывает фразы в статьях и на страницах стран, где канал упоминался в тексте;
- убирает адреса из sitemap.xml;
- число каналов 60 -> 59 (форма слова «каналов» та же), числа на страницах рубрики «Новости».
В конце печатает оставшиеся ссылки на канал, если они есть (их нужно добавить в правила ниже)."""
import sys, os, re, glob
ROOT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else '.')
SLUG, CID = 'rossiya-rtr-evropa-live', 'rtrEuro'
OLD, NEW = 60, 59
HREF = r'href="(?:https://russian-tv\.com)?(?:/en)?/%s/"' % SLUG
A = r'<a\b[^>]*%s[^>]*>[^<]*</a>' % HREF                     # ссылка на канал в тексте
U_RU = r'<a href="/rossiya-rtr-usa-live/">Россия РТР — США</a>'
U_EN = r'<a href="/en/rossiya-rtr-usa-live/">Rossiya RTR — USA</a>'
BLOCK = re.compile(r'[ \t]*<a\b(?=[^>]*\bclass="(?:ch-item-s|pop-item|sim-item|cat-ch-card|ch-card|card)[ "])(?=[^>]*%s)[^>]*>(?:(?!</a>).)*</a>[ \t]*\n?' % HREF, re.S)
ROW = re.compile(r'[ \t]*<tr>(?:(?!</tr>).)*?<a\b[^>]*%s[^>]*>(?:(?!</tr>).)*</tr>\n?' % HREF, re.S)
DATA = re.compile(r'[ \t]*\{\s*id\s*:\s*[\'"]%s[\'"][^\n]*\},?\n' % CID)
TVJSON = re.compile(r'\{"id": "%s", [^}]*\}, ?' % CID)
ITEM = re.compile(r'[ \t]*\{\s*"@type":\s*"ListItem",\s*"position":\s*\d+,\s*"name":\s*"[^"]*",\s*"url":\s*"[^"]*/(?:en/)?%s/"\s*\},?\n?' % SLUG, re.S)
# фразы в тексте: (шаблон, замена); ссылка на «— США» остаётся
PROSE = [
    (r', а для зрителей в Европе есть %s\.' % A, '.'),
    (r' Для зрителей в Европе есть %s, версия канала «Россия» для зарубежной аудитории\.' % A, ''),
    (r'%s и (%s)</td><td>Международные версии канала «Россия» для зрителей за рубежом; сетка' % (A, U_RU), r'\1</td><td>Международная версия канала «Россия» для зрителей за рубежом; сетка'),
    (r'(%s) и %s — версии канала «Россия» для зрителей за рубежом; их сетка' % (U_RU, A), r'\1 — версия канала «Россия» для зрителей за рубежом; её сетка'),
    (r', а также %s — международная версия канала «Россия» для зрителей в Европе\.' % A, '.'),
    (r' %s — международная версия канала «Россия» для зрителей за пределами России\.' % A, ''),
    (r' For viewers abroad there are also versions made for audiences outside Russia: %s and (%s)\.' % (A, U_EN), r' For viewers abroad there is also a version made for audiences outside Russia: \1.'),
    (r', plus %s for audiences in Europe\.' % A, '.'),
    (r' For viewers in Europe there is %s, a version of the Rossiya channel made for audiences abroad\.' % A, ''),
    (r'%s and (%s)</td><td>International versions of the Rossiya channel made for audiences abroad; their schedule' % (A, U_EN), r'\1</td><td>International version of the Rossiya channel made for audiences abroad; its schedule'),
    (r'(%s) and %s are versions of the Rossiya channel made for audiences abroad; their schedule' % (U_EN, A), r'\1 is a version of the Rossiya channel made for audiences abroad; its schedule'),
    (r', plus %s, the international version of the Rossiya channel for audiences in Europe\.' % A, '.'),
    (r' %s is the international version of the Rossiya channel made for viewers outside Russia\.' % A, ''),
    (r'%s · ' % A, ''), (r' · %s' % A, ''),                      # «Смотрите также»: перечисление через точку
    (r'%s, ' % A, ''), (r', %s' % A, ''),                        # «Ещё в эфире»: перечисление через запятую
]
PROSE = [(re.compile(p), r) for p, r in PROSE]
COUNT = re.compile(r'(?<![\d%%.#:\-])\b%d (?=(?:каналов|телеканалов|русск|российск|channels|Channels|Russian|Live|live|TV|ТВ))' % OLD)

def stub(lang):
    home = 'https://russian-tv.com/en/' if lang == 'en' else 'https://russian-tv.com/'
    to = home + 'rossiya-1-live/'
    title = '▶ Russia RTR — Europe' if lang == 'en' else '▶ Россия РТР — Европа'
    text = ('This channel is no longer streamed on the site. <a href="%s">Watch Rossiya 1</a> or <a href="%s">see all current channels</a>.' if lang == 'en'
            else 'Этот канал больше не транслируется на сайте. <a href="%s">Смотреть «Россия 1»</a> или <a href="%s">все текущие каналы</a>.') % (to, home)
    return ('<!DOCTYPE html>\n<html lang="%s">\n<head>\n  <meta charset="UTF-8"/>\n  <meta http-equiv="refresh" content="0; url=%s"/>\n'
            '  <link rel="canonical" href="%s"/>\n  <meta name="robots" content="noindex, follow"/>\n  <title>%s</title>\n</head>\n<body>\n  <p>%s</p>\n</body>\n</html>\n'
            % (lang, to, to, title, text))

def fix_itemlist(s):
    if not ITEM.search(s): return s
    s = ITEM.sub('', s)
    def blk(m):
        b = m.group(0); c = iter(range(1, 1000))
        b = re.sub(r'"position":\s*\d+', lambda x: '"position": %d' % next(c), b)
        n = len(re.findall(r'"@type":\s*"ListItem"', b))
        return re.sub(r'"numberOfItems":\s*\d+', '"numberOfItems": %d' % n, b)
    s = re.sub(r'"@type":\s*"ItemList".*?\]\s*\}', blk, s, flags=re.S)
    return re.sub(r',(\s*\])', r'\1', s)

changed, left = 0, []
for lang, rel in (('ru', SLUG + '/index.html'), ('en', 'en/' + SLUG + '/index.html')):
    p = os.path.join(ROOT, rel)
    if os.path.exists(p) and open(p, encoding='utf-8').read() != stub(lang):
        open(p, 'w', encoding='utf-8').write(stub(lang)); changed += 1
for f in glob.glob(os.path.join(ROOT, '**/*.html'), recursive=True):
    rel = os.path.relpath(f, ROOT)
    if rel.startswith(('tools/', 'node_modules/', '.git/')) or SLUG in rel: continue
    s = o = open(f, encoding='utf-8').read()
    if SLUG in s or CID in s:
        for rx, rep in PROSE[:13]: s = rx.sub(rep, s)            # сначала фразы (строки таблиц с «— США» должны остаться)
        s = BLOCK.sub('', s); s = ROW.sub('', s); s = DATA.sub('', s); s = TVJSON.sub('', s); s = fix_itemlist(s)
        for rx, rep in PROSE[13:]: s = rx.sub(rep, s)
    s = COUNT.sub('%d ' % NEW, s)
    s = re.sub(r'\b(Все|все|All|all) %d\b' % OLD, r'\1 %d' % NEW, s)
    if rel in ('novosti/index.html', 'en/news/index.html'):           # число каналов рубрики — по карточкам
        n = len(re.findall(r'class="cat-ch-card"', s)) or len(re.findall(r'class="card"', s))
        s = re.sub(r'(<span class="badge">)\d+ (каналов|канала|канал|channels?)(</span>)', lambda m: '%s%d %s%s' % (m.group(1), n, m.group(2), m.group(3)), s)
    if s != o: open(f, 'w', encoding='utf-8').write(s); changed += 1
    if re.search(HREF, s): left.append(rel)
sm = os.path.join(ROOT, 'sitemap.xml')
if os.path.exists(sm):
    s = o = open(sm, encoding='utf-8').read()
    s = re.sub(r'[ \t]*<url>(?:(?!</url>).)*?<loc>[^<]*/%s/</loc>(?:(?!</url>).)*</url>\n?' % SLUG, '', s, flags=re.S)
    s = re.sub(r'[ \t]*<xhtml:link[^>]*/%s/"\s*/>\n?' % SLUG, '', s)
    if s != o: open(sm, 'w', encoding='utf-8').write(s); changed += 1
    if SLUG in s: left.append('sitemap.xml')
print('gen_remove_rtr_euro: файлов изменено', changed)
if left: print('  ВНИМАНИЕ: остались ссылки на канал:', ', '.join(sorted(left)[:20]))
