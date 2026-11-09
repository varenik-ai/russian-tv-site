#!/usr/bin/env python3
"""Подключает assets/pop.js (Monetag OnClick) на все страницы и добавляет раздел о рекламе в политику. Идемпотентно.
Пропускает страницы-редиректы и файл подтверждения Google. Запускается последним, после gen_tv.py."""
import sys, os, glob
ROOT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else '.')
TAG = '<script defer src="/assets/pop.js?v=4"></script>'
POLICY = {
    'privacy/index.html': ('  <h2>5. Ваши права</h2>',
        '  <h2 id="ads">4.3. Реклама</h2>\n'
        '  <p>На сайте показывается реклама сетей Monetag и Adsterra: баннеры (в том числе блок 300×250 рядом с плеером на широких экранах компьютеров) и рекламная страница, которая может открываться в новой вкладке или окне после клика по сайту. '
        'Рекламные скрипты загружаются с серверов этих сетей, которые могут получать ваш IP-адрес, сведения о браузере и устройстве и использовать cookies. '
        'Сайт запоминает в браузере (sessionStorage), что реклама в новой вкладке уже показана, чтобы не повторять её в той же вкладке. '
        'Подробнее: <a href="https://monetag.com/privacy/" rel="noopener nofollow">политика конфиденциальности Monetag</a>, '
        '<a href="https://monetag.com/opt-out/" rel="noopener nofollow">отказ от персонализации</a>, <a href="https://adsterra.com/privacy-policy/" rel="noopener nofollow">политика конфиденциальности Adsterra</a>.</p>\n\n'),
    'en/privacy/index.html': ('  <h2>5. Your rights</h2>',
        '  <h2 id="ads">4.3. Advertising</h2>\n'
        '  <p>The site shows ads from the Monetag and Adsterra networks: banners (including a 300×250 block next to the player on wide desktop screens) and an ad page that may open in a new tab or window after a click on the site. '
        'Ad scripts load from these networks\' servers, which may receive your IP address and browser and device details and may use cookies. '
        'The site stores a note in your browser (sessionStorage) that the new-tab ad has been shown, so it does not repeat in the same tab. '
        'More: <a href="https://monetag.com/privacy/" rel="noopener nofollow">Monetag privacy policy</a>, '
        '<a href="https://monetag.com/opt-out/" rel="noopener nofollow">opt out of personalization</a>, <a href="https://adsterra.com/privacy-policy/" rel="noopener nofollow">Adsterra privacy policy</a>.</p>\n\n'),
}
n = 0
for f in glob.glob(os.path.join(ROOT, '**/*.html'), recursive=True):
    rel = os.path.relpath(f, ROOT)
    if rel.startswith(('tools/', 'node_modules/')) or os.path.basename(rel).startswith('google'):
        continue
    s = open(f, encoding='utf-8').read(); o = s
    if 'http-equiv="refresh"' not in s and 'assets/pop.js' not in s and '</head>' in s:
        s = s.replace('</head>', '  ' + TAG + '\n</head>', 1)
    if rel in POLICY and 'id="ads"' not in s:
        mark, par = POLICY[rel]
        assert mark in s, rel
        s = s.replace(mark, par + mark, 1)
    if s != o:
        open(f, 'w', encoding='utf-8').write(s); n += 1
print('pop.js:', n, 'страниц изменено')
