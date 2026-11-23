#!/usr/bin/env python3
"""23.11.2026: страница «НТВ Хит» (RU/EN) — вместо плеера сообщение со ссылкой на НТВ (по просьбе владельца).
Поток cdn.ntv.ru/th_hit живой, но без CORS и с 403 по Referer russian-tv.com: в браузере на сайте не играет (мониторинг: 100% неудач).
Заставка плеера заменяется блоком с кнопкой «Смотреть НТВ»; пустой <div id="overlay" hidden> оставлен, чтобы скрипт страницы не падал. Идемпотентен."""
import sys, os, re
ROOT = sys.argv[1]
TXT = {
 'ntv-hit-live/index.html': ('НТВ Хит сейчас недоступен на сайте: правообладатель не разрешает показ потока на сторонних сайтах.', 'Смотреть НТВ', '/ntv-live/',
                             'Канал временно недоступен — смотрите НТВ'),
 'en/ntv-hit-live/index.html': ('NTV Hit is not available on the site right now: the rights holder does not allow its stream on third-party sites.', 'Watch NTV', '/en/ntv-live/',
                                'Channel temporarily unavailable — watch NTV'),
}
OV = re.compile(r'<div class="player-overlay" id="overlay">.*?</div>\s*</div>(?=\s*<button class="fs-btn")', re.S)
NOTE = re.compile(r'<div class="player-overlay rtv-off".*?<div id="overlay" hidden></div>', re.S)
n = 0
for rel, (msg, btn, href, status) in TXT.items():
    p = os.path.join(ROOT, rel)
    if not os.path.exists(p): continue
    s = o = open(p, encoding='utf-8').read()
    block = ('<div class="player-overlay rtv-off" style="cursor:default;padding:0 20px;text-align:center">'
             '<div style="color:#e8e8f2!important;font-size:16px!important;max-width:520px;line-height:1.45">%s</div>'
             '<a href="%s" style="display:inline-block;padding:12px 26px;border-radius:999px;background:linear-gradient(145deg,#ff5a4a,#d52b1e);color:#fff;font-weight:800;text-decoration:none">%s →</a>'
             '</div><div id="overlay" hidden></div>') % (msg, href, btn)
    s = NOTE.sub(block, s) if 'rtv-off' in s else OV.sub(block, s, count=1)
    s = re.sub(r'(<div class="player-status" id="status">)[^<]*(</div>)', lambda m: m.group(1) + status + m.group(2), s, count=1)
    if s != o: open(p, 'w', encoding='utf-8').write(s); n += 1
print('gen_ntv_hit_notice: страниц изменено', n)
