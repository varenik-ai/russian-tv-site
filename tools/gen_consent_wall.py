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
    s = re.sub(r'/assets/consent\.js(\?v=\d+)?"', '/assets/consent.js?v=11"', s)
    s = re.sub(r'/assets/ads\.js(\?v=\d+)?"', '/assets/ads.js?v=3"', s)
    s = re.sub(r'/assets/monitor\.js(\?v=\d+)?"', '/assets/monitor.js?v=6"', s)
    # ads.js нужен и на страницах без плеера (категории, страны, блог): баннер и Native Banner Adsterra
    legal = re.match(r'(en/)?(privacy|advertising|about|tv|diag)/index\.html$', rel) or rel in ('404.html',) or 'noindex' in s
    if 'assets/consent.js' in s and 'assets/ads.js' not in s and not legal and '</head>' in s:
        s = s.replace('</head>', '  <script defer src="/assets/ads.js?v=3"></script>\n</head>', 1)
    if s != o: open(f, 'w', encoding='utf-8').write(s); n += 1
RU = ('  <p><strong>Уведомление о cookie.</strong> При первом посещении сайт показывает уведомление внизу страницы с кнопками «Согласен» и «Отказаться»; сайтом можно пользоваться, не отвечая на него. «Согласен» разрешает cookie и похожие технологии для аналитики (Google Analytics, Яндекс.Метрика, Microsoft Clarity) и показа рекламы, а также передачу технических данных о воспроизведении (раздел 2а). '
      '«Отказаться»: сайт работает как обычно; реклама, Яндекс.Метрика и Microsoft Clarity не загружаются, cookie Google Analytics не устанавливаются, данные о воспроизведении не передаются. Google Analytics при этом работает в режиме Google Consent Mode: без cookie и идентификаторов он получает обезличенные технические сигналы (адрес страницы, время, примерная страна и тип устройства), которые Google использует для статистики и моделирования. Отказ действует на один заход: если вы вернётесь на сайт после перерыва более 30 минут, уведомление покажется снова (в странах, где требуется согласие). Пока выбор не сделан, реклама, Яндекс.Метрика и Clarity не загружаются. '
      'Выбор хранится только в вашем браузере (localStorage: <code>rtv_consent</code> = 1 — согласие, <code>rtv_decl</code> — время последнего отказа). Страница политики конфиденциальности доступна без выбора. Региональный режим: в ЕС, Великобритании, Швейцарии, Канаде (а при неопределённой стране — в европейских и канадских часовых поясах) уведомление содержит две равные кнопки, реклама и счётчики включаются только после «Согласен». В США, остальных странах и там, где страна не определена, уведомление не мешает работе сайта: счётчики и реклама включены по умолчанию, отказаться можно кнопкой в уведомлении (в США также по ссылке «Do Not Sell or Share My Personal Information» в подвале); отказ запоминается в <code>rtv_optout</code>. Изменить выбор можно кнопкой ниже: она удалит отметки, и уведомление покажется снова.</p>\n'
      '  <p><button type="button" id="rtv-revoke" onclick="try{localStorage.removeItem(\'rtv_consent\');localStorage.removeItem(\'rtv_decl\');localStorage.removeItem(\'rtv_optout\');localStorage.removeItem(\'rtv_us_ack\')}catch(e){}location.href=\'/\'" style="border:1px solid #444;background:#1b1b30;color:#fff;border-radius:8px;padding:8px 14px;cursor:pointer">Изменить выбор</button></p>\n')
EN = ('  <p><strong>Cookie notice.</strong> On your first visit the site shows a notice at the bottom of the page with “I agree” and “Decline” buttons; you can use the site without answering it. “I agree” allows cookies and similar technologies for analytics (Google Analytics, Yandex.Metrica, Microsoft Clarity) and advertising, and the sending of technical playback data (section 2a). '
      '“Decline”: the site works as usual; advertising, Yandex.Metrica and Microsoft Clarity are not loaded, Google Analytics sets no cookies, and no playback data is sent. Google Analytics runs in Google Consent Mode: without cookies or identifiers it receives anonymous technical signals (page address, time, approximate country and device type), which Google uses for statistics and modelling. A refusal lasts for one visit: if you come back after a break of more than 30 minutes, the notice is shown again (in countries where consent is required). Until you choose, advertising, Yandex.Metrica and Clarity are not loaded. '
      'Your choice is stored only in your browser (localStorage: <code>rtv_consent</code> = 1 — agreed, <code>rtv_decl</code> — time of the last refusal). The privacy policy page is available without a choice. Regional mode: in the EU, the UK, Switzerland and Canada (and, when the country cannot be determined, in European and Canadian time zones) the notice has two equal buttons, and advertising and counters are enabled only after “I agree”. In the USA, in the rest of the world and where the country is unknown the notice does not get in the way: counters and advertising are on by default, and you can opt out with the button in the notice (in the USA also with the “Do Not Sell or Share My Personal Information” link in the footer); the opt-out is remembered in <code>rtv_optout</code>. You can change your choice with the button below: it removes the marks and the notice is shown again.</p>\n'
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
