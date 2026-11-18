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
    s = re.sub(r'/assets/consent\.js(\?v=\d+)?"', '/assets/consent.js?v=4"', s)
    s = re.sub(r'/assets/ads\.js(\?v=\d+)?"', '/assets/ads.js?v=2"', s)
    # ads.js нужен и на страницах без плеера (категории, страны, блог): баннер и Native Banner Adsterra
    legal = re.match(r'(en/)?(privacy|advertising|about|tv|diag)/index\.html$', rel) or rel in ('404.html',) or 'noindex' in s
    if 'assets/consent.js' in s and 'assets/ads.js' not in s and not legal and '</head>' in s:
        s = s.replace('</head>', '  <script defer src="/assets/ads.js?v=2"></script>\n</head>', 1)
    if s != o: open(f, 'w', encoding='utf-8').write(s); n += 1
RU = ('  <p><strong>Окно согласия.</strong> При первом посещении сайт показывает окно с одной кнопкой «Согласен». Пока вы не нажмёте её, сайтом пользоваться нельзя, а счётчики (Google Analytics, Яндекс.Метрика, Microsoft Clarity) и реклама не загружаются. '
      'Факт согласия хранится только в вашем браузере (localStorage, ключ <code>rtv_consent</code>). Страница политики конфиденциальности доступна без согласия. Отозвать согласие можно кнопкой ниже: она удалит отметку, и окно покажется снова.</p>\n'
      '  <p><button type="button" id="rtv-revoke" onclick="try{localStorage.removeItem(\'rtv_consent\')}catch(e){}location.href=\'/\'" style="border:1px solid #444;background:#1b1b30;color:#fff;border-radius:8px;padding:8px 14px;cursor:pointer">Отозвать согласие</button></p>\n')
EN = ('  <p><strong>Consent window.</strong> On your first visit the site shows a window with a single “I agree” button. Until you click it the site cannot be used, and the counters (Google Analytics, Yandex.Metrica, Microsoft Clarity) and advertising are not loaded. '
      'Your consent is stored only in your browser (localStorage, key <code>rtv_consent</code>). The privacy policy page is available without consent. You can withdraw consent with the button below: it removes the mark and the window is shown again.</p>\n'
      '  <p><button type="button" id="rtv-revoke" onclick="try{localStorage.removeItem(\'rtv_consent\')}catch(e){}location.href=\'/en/\'" style="border:1px solid #444;background:#1b1b30;color:#fff;border-radius:8px;padding:8px 14px;cursor:pointer">Withdraw consent</button></p>\n')
for path, txt, marker in (('privacy/index.html', RU, 'Окно согласия.'), ('en/privacy/index.html', EN, 'Consent window.')):
    p = os.path.join(ROOT, path)
    if not os.path.exists(p): continue
    s = open(p, encoding='utf-8').read()
    if marker in s: continue
    m = re.search(r'\n[ \t]*<h2>4\.', s)
    if not m: print('нет раздела 4 в', path); continue
    s = s[:m.start() + 1] + txt + '\n' + s[m.start() + 1:]
    open(p, 'w', encoding='utf-8').write(s); n += 1
print('gen_consent_wall: файлов изменено', n)
