#!/usr/bin/env python3
"""18.11.2026: окно согласия (assets/consent.js) и новая реклама (assets/ads.js v2). Приводит версии скриптов на всех страницах
(consent.js?v=4, ads.js?v=3) и дополняет раздел «Cookies» политики конфиденциальности (RU/EN): окно согласия, хранение в localStorage, отзыв. Идемпотентен."""
import sys, os, re, glob
ROOT = sys.argv[1]
n = 0
for f in glob.glob(os.path.join(ROOT, '**/*.html'), recursive=True):
    rel = os.path.relpath(f, ROOT)
    if rel.startswith(('node_modules', 'tools')): continue
    s = open(f, encoding='utf-8').read(); o = s
    s = re.sub(r'/assets/consent\.js(\?v=\d+)?"', '/assets/consent.js?v=13"', s)
    s = re.sub(r'/assets/ads\.js(\?v=\d+)?"', '/assets/ads.js?v=3"', s)
    s = re.sub(r'/assets/monitor\.js(\?v=\d+)?"', '/assets/monitor.js?v=7"', s)
    # ads.js нужен и на страницах без плеера (категории, страны, блог): баннер и Native Banner Adsterra
    legal = re.match(r'(en/)?(privacy|advertising|about|tv|diag)/index\.html$', rel) or rel in ('404.html',) or 'noindex' in s
    if 'assets/consent.js' in s and 'assets/ads.js' not in s and not legal and '</head>' in s:
        s = s.replace('</head>', '  <script defer src="/assets/ads.js?v=3"></script>\n</head>', 1)
    if s != o: open(f, 'w', encoding='utf-8').write(s); n += 1
RU = ('  <p><strong>Уведомление о cookie.</strong> При первом посещении сайт показывает уведомление внизу страницы с кнопками «Согласен» и «Отказаться»; сайтом можно пользоваться, не отвечая на него. По умолчанию включены счётчики (Google Analytics, Яндекс.Метрика, Microsoft Clarity), показ рекламы и передача технических данных о воспроизведении (раздел 2а); «Согласен» закрывает уведомление. '
      '«Отказаться»: сайт работает как обычно; реклама отключается, а счётчики (для статистики сайта) и технические данные о воспроизведении остаются включёнными. '
      'Выбор хранится только в вашем браузере (localStorage: <code>rtv_consent</code> = 1 — согласие, <code>rtv_optout</code> = 1 — отказ от рекламы). Страница политики конфиденциальности доступна без выбора. Уведомление одинаково во всех странах; в США в подвале также есть ссылка «Do Not Sell or Share My Personal Information». Изменить выбор можно кнопкой ниже: она удалит отметки, и уведомление покажется снова.</p>\n'
      '  <p><button type="button" id="rtv-revoke" onclick="try{localStorage.removeItem(\'rtv_consent\');localStorage.removeItem(\'rtv_decl\');localStorage.removeItem(\'rtv_optout\');localStorage.removeItem(\'rtv_us_ack\')}catch(e){}location.href=\'/\'" style="border:1px solid #444;background:#1b1b30;color:#fff;border-radius:8px;padding:8px 14px;cursor:pointer">Изменить выбор</button></p>\n')
EN = ('  <p><strong>Cookie notice.</strong> On your first visit the site shows a notice at the bottom of the page with “I agree” and “Decline” buttons; you can use the site without answering it. By default counters (Google Analytics, Yandex.Metrica, Microsoft Clarity), advertising and the sending of technical playback data (section 2a) are on; “I agree” closes the notice. '
      '“Decline”: the site works as usual; advertising is switched off, while the counters (for site statistics) and technical playback data stay on. '
      'Your choice is stored only in your browser (localStorage: <code>rtv_consent</code> = 1 — agreed, <code>rtv_optout</code> = 1 — advertising declined). The privacy policy page is available without a choice. The notice is the same in all countries; in the USA the footer also has a “Do Not Sell or Share My Personal Information” link. You can change your choice with the button below: it removes the marks and the notice is shown again.</p>\n'
      '  <p><button type="button" id="rtv-revoke" onclick="try{localStorage.removeItem(\'rtv_consent\');localStorage.removeItem(\'rtv_decl\');localStorage.removeItem(\'rtv_optout\');localStorage.removeItem(\'rtv_us_ack\')}catch(e){}location.href=\'/en/\'" style="border:1px solid #444;background:#1b1b30;color:#fff;border-radius:8px;padding:8px 14px;cursor:pointer">Change my choice</button></p>\n')
for path, txt, marker in (('privacy/index.html', RU, 'Окно согласия.'), ('en/privacy/index.html', EN, 'Consent window.')):
    p = os.path.join(ROOT, path)
    if not os.path.exists(p): continue
    s = open(p, encoding='utf-8').read()
    blk = re.compile(r'  <p><strong>(?:Окно согласия|Уведомление о cookie|Consent window|Cookie notice)\.</strong>.*?</button></p>\n', re.S)
    s2 = blk.sub('', s)                       # убрать все прежние блоки (в том числе дубли), затем вставить один актуальный
    m = re.search(r'\n[ \t]*<h2>4\.', s2)
    if not m: print('нет раздела 4 в', path); continue
    s2 = s2[:m.start() + 1] + txt + '\n' + s2[m.start() + 1:]
    if s2 != s: open(p, 'w', encoding='utf-8').write(s2); n += 1
print('gen_consent_wall: файлов изменено', n)

# раздел 2а: данные о воспроизведении передаются на сайте только после «Согласен»
for path, old, new in (('privacy/index.html', 'эти данные не передаются.</p>', 'эти данные не передаются. На сайте они передаются только после нажатия «Согласен».</p>'),
                       ('en/privacy/index.html', 'this data is not sent.</p>', 'this data is not sent. On the site it is sent only after you click “I agree”.</p>')):
    p = os.path.join(ROOT, path)
    if not os.path.exists(p): continue
    t = open(p, encoding='utf-8').read()
    if old in t and new not in t:
        open(p, 'w', encoding='utf-8').write(t.replace(old, new, 1)); print('gen_consent_wall: уточнён раздел 2а в', path)
