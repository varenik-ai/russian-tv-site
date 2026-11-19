#!/usr/bin/env python3
"""19.11.2026: «Кинокомедия» -> «Viju+ Premiere» (решение владельца). Адрес страницы /kinokomediya-live/ и CH_ID 'kinokomediya' не меняются
(ссылки, индекс поиска, воркеры), меняются название, иконка, описания и тексты «О канале». Идемпотентен; запускается дважды в run_all.sh
(рано, до gen_og, чтобы картинка og получила новое имя, и в конце, после генераторов, которые заново пишут старые заголовки)."""
import sys, os, glob, re
ROOT = sys.argv[1]
NEW = 'Viju+ Premiere'
def esc(s): return ''.join(c if ord(c) < 128 else '\\u%04x' % ord(c) for c in s)
RU_PAGE = 'kinokomediya-live/index.html'
EN_PAGE = 'en/kinokomediya-live/index.html'

def fix_ru_page(s):
    s = re.sub(r'<p>Кинокомедия — специализированный канал, транслирующий комедийные фильмы круглосуточно\..*?</p>',
               f'<p>{NEW} — телеканал с фильмами и сериалами в прямом эфире круглосуточно.</p>', s, flags=re.S)
    s = re.sub(r'<p>В эфире — отечественные и зарубежные комедии всех эпох.*?</p>',
               '<p>В эфире — фильмы и сериалы. Трансляция работает на любом устройстве — компьютере, iPhone, Android и Smart TV — из любой страны.</p>', s, flags=re.S)
    s = s.replace(f'комедии 24/7 без регистрации', 'фильмы и сериалы 24/7 без регистрации')
    s = s.replace('лучшие комедии в прямом эфире', 'фильмы и сериалы в прямом эфире')
    s = s.replace('Комедии 24/7. Прямая трансляция 24/7.', 'Фильмы и сериалы 24/7. Прямая трансляция 24/7.')
    return s

def fix_en_page(s):
    s = re.sub(r'<p>Kinokomediya \(Comedy Cinema\) is a 24/7 channel dedicated entirely to comedy films.*?</p>',
               f'<p>{NEW} is a 24/7 channel with films and series.</p>', s, flags=re.S)
    s = re.sub(r'<p>On air: beloved Soviet comedies, contemporary Russian comedy films.*?</p>',
               '<p>On air: films and TV series. The stream works on any device — desktop, iPhone, Android and Smart TV — from any country.</p>', s, flags=re.S)
    s = s.replace('best Russian comedies', 'films and series').replace('Russian Comedies', 'Films and Series')
    s = s.replace('Comedy films 24/7 — Russian, Soviet and international comedies around the clock.', 'Films and series 24/7, live around the clock.')
    return s

n = 0
files = glob.glob(os.path.join(ROOT, '**/*.html'), recursive=True) + [os.path.join(ROOT, 'sitemap.xml')]
for f in files:
    if '/tools/' in f or '/node_modules/' in f: continue
    try: s = o = open(f, encoding='utf-8').read()
    except Exception: continue
    page = os.path.relpath(f, ROOT)
    if page == RU_PAGE: s = fix_ru_page(s)
    if page == EN_PAGE: s = fix_en_page(s)
    # описания в списках, данных главных и сводках
    s = s.replace("desc:'Комедии 24/7'", "desc:'Фильмы и сериалы 24/7'").replace('desc:"Comedy films 24/7"', 'desc:"Films and series 24/7"')
    s = s.replace('<strong>Кинокомедия</strong> — только комедийные фильмы 24/7', f'<strong>{NEW}</strong> — фильмы и сериалы 24/7')
    s = re.sub(r"tags:\['комедии','юмор'\]", "tags:['фильмы','сериалы']", s)
    # название и значок
    s = s.replace('Кинокомедия', NEW).replace('Kinokomediya', NEW)
    s = s.replace(esc('Кинокомедия'), NEW).replace(esc('Kinokomediya'), NEW)
    s = s.replace('>КМД<', '>VPR<').replace("icon:'КМД'", "icon:'VPR'").replace('icon:"\\u041a\\u041c\\u0414"', 'icon:"VPR"')
    if s != o:
        open(f, 'w', encoding='utf-8').write(s); n += 1
print('Viju+ Premiere: файлов изменено', n)
