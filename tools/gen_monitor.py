#!/usr/bin/env python3
"""16.11.2026: мониторинг запуска каналов. Подключает assets/monitor.js (после hls.js) на всех страницах с плеером и добавляет абзац в политику
конфиденциальности (RU/EN). Скрипт шлёт на rtv-monitor результат запуска канала без cookie, IP и идентификаторов. Идемпотентен."""
import sys, os, re, glob
ROOT = sys.argv[1]
TAG = '<script defer src="/assets/monitor.js?v=3"></script>'
n = 0
for f in glob.glob(os.path.join(ROOT, '**/index.html'), recursive=True):
    s = open(f, encoding='utf-8').read(); o = s
    if 'hls.min.js' not in s or '/assets/monitor.js' in s: continue
    s = re.sub(r'(<script[^>]*hls\.min\.js[^>]*></script>)', lambda m: m.group(1) + '\n' + TAG, s, count=1)
    if s != o: open(f, 'w', encoding='utf-8').write(s); n += 1
RU = ('  <h2>2а. Технические данные о воспроизведении</h2>\n  <p>Чтобы находить каналы, которые не открываются у части зрителей, сайт после запуска канала передаёт на наш сервер результат (пошёл или не пошёл), код ошибки, адрес сервера, '
      'на котором она произошла, тип устройства (телефон, компьютер, телевизор) и браузер. Страну и сети провайдера (номер ASN) определяет Cloudflare по IP-адресу на своей стороне: сам IP-адрес, cookie и любые идентификаторы посетителя мы не получаем и не храним. '
      'Хранятся только суммарные счётчики за день, 90 дней. Если в браузере включён запрет отслеживания (Do Not Track), эти данные не передаются.</p>\n')
EN = ('  <h2>2a. Technical playback data</h2>\n  <p>To find channels that do not open for some viewers, after a channel starts the site sends our server the result (started or not), the error code, the server where it happened, '
      'the device type (phone, computer, TV) and the browser. The country and the ISP network (ASN) are determined by Cloudflare from the IP address on its side: we do not receive or store the IP address, cookies or any visitor identifier. '
      'Only daily totals are kept, for 90 days. If Do Not Track is enabled in the browser, this data is not sent.</p>\n')
for path, txt, marker in (('privacy/index.html', RU, 'Технические данные о воспроизведении'), ('en/privacy/index.html', EN, 'Technical playback data')):
    p = os.path.join(ROOT, path)
    if not os.path.exists(p): continue
    s = open(p, encoding='utf-8').read()
    if marker in s: continue
    m = re.search(r'\n(\s*)<h2>[^<]*(?:[Cc]ookies?|cookie)[^<]*</h2>', s)
    if not m: print('нет места для абзаца в', path); continue
    s = s[:m.start() + 1] + txt + s[m.start() + 1:]
    open(p, 'w', encoding='utf-8').write(s); n += 1
print('gen_monitor: файлов изменено', n)
