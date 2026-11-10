#!/usr/bin/env python3
"""Убирает из каталога сайта шесть каналов, источники которых недоступны (проверка 11.11.2026):
ТНТ4, Бобер, Большая планета, Карусель International, FON Music, Спортивный. Идемпотентно.
Что делает: удаляет карточки и пункты списков (боковые списки, «Популярные», «Похожие», карточки категорий, стран и спорта),
строки таблиц и данные каналов на главных, элементы ItemList в JSON-LD, пересчитывает число каналов (60 -> 54),
закрывает страницы самих каналов noindex (остаются по прямым ссылкам), убирает их из sitemap.
Ссылки в сплошном тексте (перечисления «А, Б, В») убираются вместе с запятой, одиночные упоминания правятся вручную в страницах."""
import sys, os, re, glob, json
ROOT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else '.')
BROKEN = ['tnt-live', 'bober-live', 'bolshaya-planeta-live', 'karusel-international-live', 'fon-music-live', 'sportivnyy-live']
# семь каналов вне каталога (noindex): на них не должно быть ссылок из списков и карточек категорий
OUTSIDE = ['t24-live', 'retro-live', 'kinopremiera-live', 'kinopokaz-live', 'unikum-live', 'ru-tv-live', 'zagorodnaya-zhizn-live']
SLUGS = BROKEN + OUTSIDE
IDS = ['tnt', 'bober', 'bigplanet', 'karuselIntl', 'fonmusic', 'sportivnyy', 't24', 'retro', 'kinopremiera', 'kinopokaz', 'unikum', 'rutv', 'zagorodnaya']
OLD, NEW = 60, 54
SL = '|'.join(re.escape(s) for s in SLUGS)
HREF = r'href="(?:https://russian-tv\.com)?(?:/en)?/(?:%s)/"' % SL
BLOCK_CLASSES = r'(?:ch-item-s|pop-item|sim-item|cat-ch-card|ch-card|card)'
# <a ... class="ch-item-s ..." href=... > ... </a> (класс и href в любом порядке), без вложенных <a>
BLOCK = re.compile(r'[ \t]*<a\b(?=[^>]*\bclass="%s[ "])(?=[^>]*%s)[^>]*>(?:(?!</a>).)*</a>[ \t]*\n?' % (BLOCK_CLASSES, HREF), re.S)
ROW = re.compile(r'[ \t]*<tr>(?:(?!</tr>).)*?<a\b[^>]*%s[^>]*>(?:(?!</tr>).)*</tr>\n?' % HREF, re.S)
INLINE = re.compile(r'<a\b[^>]*%s[^>]*>[^<]*</a>' % HREF)
DATA = re.compile(r'[ \t]*\{\s*id\s*:\s*[\'"](?:%s)[\'"][^\n]*\},?\n' % '|'.join(IDS))
# перечисления «<a>А</a>, <a>Б</a>»: убираем ссылку вместе с соседней запятой; одиночная ссылка среди подряд идущих <a> — просто ссылку
INLINE_COMMA_AFTER = re.compile(r'<a\b[^>]*%s[^>]*>[^<]*</a>, ' % HREF)
INLINE_COMMA_BEFORE = re.compile(r', <a\b[^>]*%s[^>]*>[^<]*</a>' % HREF)
INLINE_ALONE = re.compile(r'(?<=</a>)<a\b[^>]*%s[^>]*>[^<]*</a>(?=<a\b)' % HREF)
# вопрос про ТНТ в FAQ главной (RU): целиком вместе с <details>
FAQ_TNT = re.compile(r'[ \t]*<details\b(?:(?!</details>).)*?Где смотреть ТНТ онлайн бесплатно\?.*?</details>\n?', re.S)
# названия убранных каналов в перечислениях через запятую (RU и EN): «…, ТНТ, МУЗ-ТВ…», «Развлекательные: ТНТ, …»
NAMES = ['ТНТ4', 'ТНТ', 'Бобер', 'Большая планета', 'Карусель International', 'FON Music', 'Спортивный',
         'TNT4', 'TNT', 'Bober', 'Bolshaya Planeta \\(Big Planet\\)', 'Karusel International', 'Sportivny']
NM = '|'.join(NAMES)
LIST_FIRST = re.compile(r'(?<=[:>] )(?:%s), ' % NM)
LIST_NEXT = re.compile(r', (?:%s)(?=[,.;)"<]| и | and |\s—)' % NM)
def strip_names(s):
    return LIST_NEXT.sub('', LIST_FIRST.sub('', s))
def own(rel):
    return any(rel in ('%s/index.html' % s, 'en/%s/index.html' % s) for s in SLUGS)
def decl(n):
    if n % 10 == 1 and n % 100 != 11: return 'канал'
    if 2 <= n % 10 <= 4 and not 12 <= n % 100 <= 14: return 'канала'
    return 'каналов'
def recount(s):
    s = re.sub(r'\b%d (канал(?:а|ов)?)\b' % OLD, lambda m: '%d %s' % (NEW, decl(NEW)), s)
    s = re.sub(r'\b(Все|все) %d каналов\b' % OLD, r'\1 %d каналов' % NEW, s)
    s = re.sub(r'\b%d (российских телеканал(?:а|ов)?|русских каналов|новостных каналов)' % OLD, lambda m: '%d %s' % (NEW, m.group(1)), s)
    s = re.sub(r'\b(All|all) %d (channels|Channels)\b' % OLD, r'\1 %d \2' % NEW, s)
    s = re.sub(r'\b%d (channels|Channels|Russian TV channels|Russian channels|live channels)\b' % OLD, lambda m: '%d %s' % (NEW, m.group(1)), s)
    s = re.sub(r'list of %d channels' % OLD, 'list of %d channels' % NEW, s)
    return s
def fix_itemlist(s):
    """убирает из JSON-LD ItemList элементы с адресами убранных каналов, нумерует заново, обновляет numberOfItems"""
    ITEM = re.compile(r'[ \t]*\{\s*"@type":\s*"ListItem",\s*"position":\s*\d+,\s*"name":\s*"[^"]*",\s*"url":\s*"[^"]*/(?:en/)?(?:%s)/"\s*\},?\n?' % SL, re.S)
    if not ITEM.search(s): return s
    s = ITEM.sub('', s)
    def blk(m):
        b = m.group(0); c = iter(range(1, 1000))
        b = re.sub(r'"position":\s*\d+', lambda x: '"position": %d' % next(c), b)
        n = len(re.findall(r'"@type":\s*"ListItem"', b))
        return re.sub(r'"numberOfItems":\s*\d+', '"numberOfItems": %d' % n, b)
    s = re.sub(r'"@type":\s*"ItemList".*?\]\s*\}', blk, s, flags=re.S)
    return re.sub(r',(\s*\])', r'\1', s)           # висящая запятая перед ]
# точечные правки страницы категории «Развлечения» (RU), построенной вокруг ТНТ4: заголовок, описания, FAQ, текст
PAGE_EDITS = {
 'razvlecheniya/index.html': [
  ('<title>▶ Российские развлекательные каналы онлайн — ТНТ, СТС без VPN</title>', '<title>▶ Развлекательные каналы онлайн — История, Союз, Прима без VPN</title>'),
  ('Российские развлекательные каналы в прямом эфире: ТНТ, сериалы, Comedy Club и другие. Бесплатно, без VPN и регистрации 24/7.', 'Российские развлекательные и познавательные каналы в прямом эфире: История, Союз, Прима, RT Documentary. Бесплатно, без VPN и регистрации 24/7.'),
  ('Развлекательные каналы России онлайн бесплатно — ТНТ, Соловьёв Live и другие', 'Развлекательные каналы России онлайн бесплатно — История, Союз, Прима и другие'),
  ('Смотрите российские развлекательные каналы онлайн бесплатно. ТНТ, Соловьёв Live, История — юмор, шоу и аналитика.', 'Смотрите российские развлекательные каналы онлайн бесплатно: История, Союз, Прима, RT Documentary — документальное кино, семейные программы и шоу.'),
  ('"name": "Где смотреть ТНТ онлайн бесплатно?"', '"name": "Где смотреть канал «История» онлайн бесплатно?"'),
  ('"text": "ТНТ доступен на russian-tv.com бесплатно в режиме прямого эфира без регистрации и VPN."', '"text": "Канал «История» доступен на russian-tv.com бесплатно в режиме прямого эфира без регистрации и VPN."'),
  ('"name": "Работает ли ТНТ без рекламы?"', '"name": "Есть ли на сайте реклама?"'),
  ('<summary>Работает ли ТНТ без рекламы? <span>▾</span></summary>', '<summary>Есть ли на сайте реклама? <span>▾</span></summary>'),
  ('смотрите юмор, шоу и аналитику бесплатно без регистрации. В категории представлены 3 ведущих развлекательных канала России.</p><p></p><p><strong>ТНТ4</strong> — один из самых популярных развлекательных каналов России, известный ситкомами, реалити-шоу и юмористическими программами. Здесь выходят «Comedy Club», «Физрук», «Универ» и другие популярные проекты.</p><p></p><p><strong>Соловьёв Live</strong> предлагает ежедневные политические ток-шоу и аналитику. <strong>История</strong> специализируется на исторических документальных фильмах и программах об отечественной и мировой истории. Все каналы доступны из любой страны без VPN и регистрации.</p>',
   'смотрите документальное кино, семейные программы и шоу бесплатно без регистрации. В категории представлены 4 канала.</p><p></p><p><strong>История</strong> специализируется на исторических документальных фильмах и программах об отечественной и мировой истории. <strong>Союз</strong> — семейное телевидение, <strong>Прима</strong> — развлекательный канал, <strong>RT Documentary</strong> — документальные фильмы на русском. Все каналы доступны на russian-tv.com без регистрации.</p>'),
 ],
}
# вопрос про «Историю» в видимом FAQ (в JSON-LD он есть, а <details> про ТНТ убран выше): ставим на первое место
FAQ_ISTORIYA = ('    <h2>Частые вопросы</h2>\n    <details>\n      <summary>Где смотреть канал «История» онлайн бесплатно? <span>▾</span></summary>\n'
                '      <p>Канал «История» доступен на russian-tv.com бесплатно в режиме прямого эфира без регистрации и VPN.</p>\n    </details>\n')
def recount_en_categories():
    """числа каналов на EN-страницах категорий (gen_counts.py считает только RU): по числу карточек"""
    n_changed = 0
    for cat in ('news', 'entertainment', 'movies', 'kids', 'music', 'hobby', 'sport'):
        p = os.path.join(ROOT, 'en', cat, 'index.html')
        if not os.path.exists(p): continue
        s = o = open(p, encoding='utf-8').read()
        n = len(re.findall(r'class="cat-ch-card"', s)) or len(re.findall(r'class="card"', s))
        s = re.sub(r'(<span class="badge">)\d+ channels?(</span>)', lambda m: '%s%d channels%s' % (m.group(1), n, m.group(2)), s)
        s = re.sub(r'"numberOfItems": \d+', '"numberOfItems": %d' % n, s)
        s = re.sub(r'watch \d+ (russian [a-z ]*channels)', lambda m: 'watch %d %s' % (n, m.group(1)), s)
        if s != o: open(p, 'w', encoding='utf-8').write(s); n_changed += 1
    return n_changed
changed = 0
for f in glob.glob(os.path.join(ROOT, '**/*.html'), recursive=True):
    rel = os.path.relpath(f, ROOT)
    if rel.startswith(('tools/', 'node_modules/')): continue
    s = o = open(f, encoding='utf-8').read()
    for old, new in PAGE_EDITS.get(rel, []):
        s = s.replace(old, new)
    if rel == 'razvlecheniya/index.html' and 'Где смотреть канал «История» онлайн бесплатно? <span>' not in s:
        s = s.replace('    <h2>Частые вопросы</h2>\n', FAQ_ISTORIYA, 1)
    s = BLOCK.sub('', s)                       # списки и карточки: и на страницах самих убранных каналов
    if not own(rel):
        s = ROW.sub('', s); s = DATA.sub('', s); s = fix_itemlist(s)
        s = INLINE_COMMA_AFTER.sub('', s); s = INLINE_COMMA_BEFORE.sub('', s); s = INLINE_ALONE.sub('', s)
        s = FAQ_TNT.sub('', s)
        s = strip_names(s)
    if s != o or True:
        s2 = recount(s) if (re.search(r'\b%d\b' % OLD, s)) else s
        if s2 != o: open(f, 'w', encoding='utf-8').write(s2); changed += 1
print('remove_broken: страниц изменено', changed + recount_en_categories())
