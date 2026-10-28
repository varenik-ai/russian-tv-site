#!/usr/bin/env python3
"""Редиректы для удалённых адресов и внутренние ссылки (страны, блог) в подвале главных. Идемпотентно."""
import sys, os
ROOT = sys.argv[1]
def rd(p): return open(os.path.join(ROOT, p), encoding='utf-8').read()
def wr(p, s):
    os.makedirs(os.path.dirname(os.path.join(ROOT, p)), exist_ok=True)
    open(os.path.join(ROOT, p), 'w', encoding='utf-8').write(s)

# 1. Заглушки-редиректы (GitHub Pages: без серверных правил). Старый адрес → актуальный.
REDIRECTS = {'univer-tv-live/index.html': '/razvlecheniya/', 'en/about/index.html': '/about/'}
for path, to in REDIRECTS.items():
    wr(path, '<!DOCTYPE html>\n<html lang="ru"><head><meta charset="UTF-8"/>'
       '<meta name="viewport" content="width=device-width, initial-scale=1.0"/>'
       '<title>Страница перемещена — Русское ТВ</title>'
       '<link rel="canonical" href="https://russian-tv.com%s"/>'
       '<meta name="robots" content="noindex, follow"/>'
       '<meta http-equiv="refresh" content="0; url=%s"/>'
       '<script>location.replace("%s")</script></head>'
       '<body><p>Страница перемещена: <a href="%s">перейти</a>.</p></body></html>\n' % (to, to, to, to))

# 2. Ссылки на страницы стран и статьи блога в подвале главных
RU_C = [('ssha','США'),('velikobritanii','Великобритания'),('germanii','Германия'),('kanade','Канада'),('frantsii','Франция'),('ispanii','Испания'),('italii','Италия'),('polshe','Польша'),('izraile','Израиль'),('latvii','Латвия'),('litve','Литва'),('estonii','Эстония'),('finlyandii','Финляндия'),('avstrii','Австрия'),('avstralii','Австралия'),('belgii','Бельгия'),('chehii','Чехия'),('gretsii','Греция'),('niderlandakh','Нидерланды'),('norvegii','Норвегия'),('portugalii','Португалия'),('shvetsii','Швеция'),('shveytsarii','Швейцария')]
EN_C = [('usa','USA'),('uk','UK'),('germany','Germany'),('canada','Canada'),('france','France'),('spain','Spain'),('italy','Italy'),('poland','Poland'),('israel','Israel'),('latvia','Latvia'),('lithuania','Lithuania'),('estonia','Estonia'),('finland','Finland'),('austria','Austria'),('australia','Australia'),('belgium','Belgium'),('czech-republic','Czech Republic'),('greece','Greece'),('netherlands','Netherlands'),('norway','Norway'),('portugal','Portugal'),('sweden','Sweden'),('switzerland','Switzerland')]
RU_B = [('kak-smotret-russkoe-tv-za-granicey','Как смотреть за границей'),('kak-smotret-russkoe-tv-na-iphone-i-android','На iPhone и Android'),('kak-smotret-russkoe-tv-na-smart-tv','На Smart TV'),('kakie-kanaly-smotret-po-temam','Каналы по темам'),('kanal-ne-gruzitsya-chto-delat','Канал не грузится'),('pervyy-kanal-rossiya-1-ntv-v-chem-raznica','Первый, Россия 1, НТВ'),('vesti-onlajn-poslednie-vypuski','Вести онлайн'),('gde-smotret-futbol-i-sport-na-russkih-kanalah','Футбол и спорт')]
EN_B = [('how-to-watch-russian-tv-in-usa','Russian TV in the USA'),('russian-tv-on-iphone-and-android','On iPhone and Android'),('channel-not-loading-fix','Channel not loading')]
def block(lang):
    if lang == 'ru':
        c = ''.join('<a href="/russkie-kanaly-v-%s/">%s</a>' % x for x in RU_C)
        b = ''.join('<a href="/blog/%s/">%s</a>' % x for x in RU_B)
        t1, t2, all_ = 'Русские каналы по странам', 'Статьи', '<a href="/russkie-kanaly-za-rubezhom/">Все страны</a>'
    else:
        c = ''.join('<a href="/en/russian-tv-in-%s/">%s</a>' % x for x in EN_C)
        b = ''.join('<a href="/en/blog/%s/">%s</a>' % x for x in EN_B)
        t1, t2, all_ = 'Russian TV by country', 'Articles', ''
    return ('<!--links-->\n  <nav class="footer-seo" style="max-width:1100px;margin:18px auto 0;padding:0 12px;font-size:12px;line-height:2;color:#8b8ba0;text-align:center">'
            '<div><b>%s:</b> %s%s</div><div><b>%s:</b> %s</div></nav><!--/links-->\n' % (t1, c, all_, t2, b))
STYLE = '<style id="footer-seo-css">.footer-seo a{color:inherit;text-decoration:none;margin:0 7px;white-space:nowrap}.footer-seo a:hover{color:var(--text);text-decoration:underline}</style>'
for page, lang in (('index.html', 'ru'), ('en/index.html', 'en')):
    s = rd(page)
    if '<!--links-->' in s:
        a, rest = s.split('<!--links-->', 1); rest = rest.split('<!--/links-->\n', 1)[1]; s = a + rest.lstrip(' ')
    marker = '</div>\n  <div style="text-align:center;margin-top:16px;font-size:11px'
    if marker not in s:
        print('маркер не найден:', page); continue
    s = s.replace(marker, '</div>\n  ' + block(lang) + '  <div style="text-align:center;margin-top:16px;font-size:11px', 1)
    if 'footer-seo-css' not in s:
        s = s.replace('</head>', STYLE + '</head>', 1)
    wr(page, s)
