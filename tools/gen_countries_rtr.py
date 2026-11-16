#!/usr/bin/env python3
"""16.11.2026: карточка «Россия РТР — Европа» на страницах европейских стран, «Россия РТР — США» на страницах США и Канады (RU и EN).
Австралия и Израиль не меняются. Карточка вставляется после «Россия 24» в блоке «Популярные каналы». Идемпотентно."""
import sys, os, re
ROOT = sys.argv[1]
EU = ['avstrii','belgii','chehii','estonii','finlyandii','frantsii','germanii','gretsii','ispanii','italii','latvii','litve',
      'niderlandakh','norvegii','polshe','portugalii','shvetsii','shveytsarii','velikobritanii']
EU_EN = ['austria','belgium','czech-republic','estonia','finland','france','germany','greece','spain','italy','latvia','lithuania',
         'netherlands','norway','poland','portugal','sweden','switzerland','uk']
AM = ['ssha','kanade']; AM_EN = ['usa','canada']
CARD = {
 ('ru','eu'): ('rossiya-rtr-evropa-live','РТР','#1a0808','#D52B1E','Россия РТР — Европа','Международная версия канала «Россия»'),
 ('ru','am'): ('rossiya-rtr-usa-live','РТР','#0a0f1a','#1565c0','Россия РТР — США','Международная версия канала «Россия»'),
 ('en','eu'): ('rossiya-rtr-evropa-live','РТР','#1a0808','#D52B1E','Russia RTR — Europe','International version of the Russia channel'),
 ('en','am'): ('rossiya-rtr-usa-live','РТР','#0a0f1a','#1565c0','Russia RTR — USA','International version of the Russia channel'),
}
def card(lang, grp):
    slug, ic, bg, col, name, desc = CARD[(lang, grp)]
    href = f'/en/{slug}/' if lang == 'en' else f'/{slug}/'
    return (f'      <a href="{href}" class="ch-card">\n        <div class="ch-icon" style="background:{bg};color:{col}">{ic}</div>\n'
            f'        <div class="ch-name">{name}</div>\n        <div class="ch-desc">{desc}</div>\n'
            f'        <div class="ch-live"><span class="live-dot"></span>LIVE</div>\n      </a>\n')
targets = [(f'russkie-kanaly-v-{c}/index.html', 'ru', 'eu') for c in EU] + [(f'russkie-kanaly-v-{c}/index.html', 'ru', 'am') for c in AM] \
        + [(f'en/russian-tv-in-{c}/index.html', 'en', 'eu') for c in EU_EN] + [(f'en/russian-tv-in-{c}/index.html', 'en', 'am') for c in AM_EN]
n = 0
for rel, lang, grp in targets:
    p = os.path.join(ROOT, rel)
    if not os.path.exists(p): print('нет страницы', rel); continue
    s = open(p, encoding='utf-8').read()
    slug = CARD[(lang, grp)][0]
    if f'/{slug}/"' in s: continue
    rx = re.compile(r'(      <a href="/(?:en/)?rossiya-24-live/" class="ch-card">.*?      </a>\n)', re.S)
    m = rx.search(s)
    if not m: print('нет карточки Россия 24', rel); continue
    s = s[:m.end()] + card(lang, grp) + s[m.end():]
    open(p, 'w', encoding='utf-8').write(s); n += 1
print(f'gen_countries_rtr: страниц изменено {n}')
