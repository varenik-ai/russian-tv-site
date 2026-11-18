#!/usr/bin/env python3
"""18.11.2026: окно согласия (assets/consent.js) и новая реклама (assets/ads.js v2). Приводит версии скриптов на всех страницах
(consent.js?v=4, ads.js?v=2) и дополняет раздел «Cookies» политики конфиденциальности (RU/EN): окно согласия, хранение в localStorage, отзыв. Идемпотентен."""
import sys, os, re, glob
ROOT = sys.argv[1]
n = 0
for f in glob.glob(os.path.join(ROOT, '**/*.html'), recursive=True):
    rel = os.path.relpath(f, ROOT)
    if rel.startswith(('node_modules', 'tools')): continue
    s = open(f, encoding='utf-8').read(); o = s
    s = re.sub(r'/assets/consent\.js(\?v=\d+)?"', '/assets/consent.js?v=5"', s)
    s = re.sub(r'/assets/ads\.js(\?v=\d+)?"', '/assets/ads.js?v=2"', s)
    s = re.sub(r'/assets/monitor\.js(\?v=\d+)?"', '/assets/monitor.js?v=4"', s)
    # ads.js нужен и на страницах без плеера (категории, страны, блог): баннер и Native Banner Adsterra
    legal = re.match(r'(en/)?(privacy|advertising|about|tv|diag)/index\.html$', rel) or rel in ('404.html',) or 'noindex' in s
    if 'assets/consent.js' in s and 'assets/ads.js' not in s and not legal and '</head>' in s:
        s = s.replace('</head>', '  <script defer src="/assets/ads.js?v=2"></script>\n</head>', 1)
    if s != o: open(f, 'w', encoding='utf-8').write(s); n += 1
RU = ('  <p><strong>Окно согласия.</strong> При первом посещении сайт показывает окно с кнопками «Согласен» и «Отказаться». «Согласен» разрешает cookie и похожие технологии для аналитики (Google Analytics, Яндекс.Метрика, Microsoft Clarity) и показа рекламы, а также передачу технических данных о воспроизведении (раздел 2а). '
      '«Отказаться»: сайт работает как обычно, но эти сервисы и реклама не загружаются, а данные о воспроизведении не передаются. Пока выбор не сделан, сайтом пользоваться нельзя. '
      'Выбор хранится только в вашем браузере (localStorage, ключ <code>rtv_consent</code>: 1 — согласен, 0 — отказался). Страница политики конфиденциальности доступна без выбора. Изменить выбор можно кнопкой ниже: она удалит отметку, и окно покажется снова.</p>\n'
      '  <p><button type="button" id="rtv-revoke" onclick="try{localStorage.removeItem(\'rtv_consent\')}catch(e){}location.href=\'/\'" style="border:1px solid #444;background:#1b1b30;color:#fff;border-radius:8px;padding:8px 14px;cursor:pointer">Изменить выбор</button></p>\n')
EN = ('  <p><strong>Consent window.</strong> On your first visit the site shows a window with “I agree” and “Decline” buttons. “I agree” allows cookies and similar technologies for analytics (Google Analytics, Yandex.Metrica, Microsoft Clarity) and advertising, and the sending of technical playback data (section 2a). '
      '“Decline”: the site works as usual, but these services and advertising are not loaded and no playback data is sent. Until you choose, the site cannot be used. '
      'Your choice is stored only in your browser (localStorage, key <code>rtv_consent</code>: 1 — agreed, 0 — declined). The privacy policy page is available without a choice. You can change your choice with the button below: it removes the mark and the window is shown again.</p>\n'
      '  <p><button type="button" id="rtv-revoke" onclick="try{localStorage.removeItem(\'rtv_consent\')}catch(e){}location.href=\'/en/\'" style="border:1px solid #444;background:#1b1b30;color:#fff;border-radius:8px;padding:8px 14px;cursor:pointer">Change my choice</button></p>\n')
for path, txt, marker in (('privacy/index.html', RU, 'Окно согласия.'), ('en/privacy/index.html', EN, 'Consent window.')):
    p = os.path.join(ROOT, path)
    if not os.path.exists(p): continue
    s = open(p, encoding='utf-8').read()
    blk = re.compile(r'  <p><strong>(?:Окно согласия|Consent window)\.</strong>.*?</button></p>\n', re.S)
    if blk.search(s):
        s2 = blk.sub(lambda _m: txt, s, count=1)
        if s2 != s: open(p, 'w', encoding='utf-8').write(s2); n += 1
        continue
    m = re.search(r'\n[ \t]*<h2>4\.', s)
    if not m: print('нет раздела 4 в', path); continue
    s = s[:m.start() + 1] + txt + '\n' + s[m.start() + 1:]
    open(p, 'w', encoding='utf-8').write(s); n += 1
print('gen_consent_wall: файлов изменено', n)

# раздел 2а: данные о воспроизведении передаются на сайте только после «Согласен»
for path, old, new in (('privacy/index.html', 'эти данные не передаются.</p>', 'эти данные не передаются. На сайте они передаются только после нажатия «Согласен».</p>'),
                       ('en/privacy/index.html', 'this data is not sent.</p>', 'this data is not sent. On the site it is sent only after you click “I agree”.</p>')):
    p = os.path.join(ROOT, path)
    if not os.path.exists(p): continue
    t = open(p, encoding='utf-8').read()
    if old in t and new not in t:
        open(p, 'w', encoding='utf-8').write(t.replace(old, new, 1)); print('gen_consent_wall: уточнён раздел 2а в', path)
