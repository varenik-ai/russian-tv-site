#!/usr/bin/env python3
"""Персональные OG-картинки 1200x630 для страниц каналов. Запуск: PYTHONPATH=pylib python3 gen_og.py <repo>"""
import sys, os, re, json, subprocess
from PIL import Image, ImageDraw, ImageFont
ROOT = sys.argv[1]
home = open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read()
m = re.search(r'const CHANNEL_GROUPS = (\[.*?\n\]);', home, re.S)
open('/tmp/_cg2.js', 'w', encoding='utf-8').write('const CHANNEL_GROUPS=' + m.group(1) + ';console.log(JSON.stringify(CHANNEL_GROUPS))')
groups = json.loads(subprocess.run(['node', '/tmp/_cg2.js'], capture_output=True, text=True, check=True).stdout)
FB = '/System/Library/Fonts/Supplemental/Arial Bold.ttf'
def font(sz): return ImageFont.truetype(FB, sz)
def hexrgb(h):
    h = h.lstrip('#'); return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
os.makedirs(os.path.join(ROOT, 'assets/og'), exist_ok=True)
def fit(draw, text, maxw, start):
    sz = start
    while sz > 28 and draw.textlength(text, font=font(sz)) > maxw: sz -= 4
    return font(sz)
cnt = 0
for g in groups:
    for ch in g['channels']:
        slug = ch.get('slug'); 
        if not slug: continue
        W, H = 1200, 630
        img = Image.new('RGB', (W, H), (10, 10, 20))
        d = ImageDraw.Draw(img)
        accent = hexrgb(ch['color']); bg = hexrgb(ch['iconBg'])
        for y in range(H):  # вертикальный градиент
            t = y / H
            d.line([(0, y), (W, y)], fill=(int(10 + 14*t), int(10 + 10*t), int(20 + 34*t)))
        d.rectangle([0, 0, 18, H], fill=accent)
        # плашка-иконка
        d.rounded_rectangle([90, 160, 390, 460], radius=48, fill=tuple(min(255, c + 26) for c in bg), outline=accent, width=6)
        ic = ch['icon']; f = fit(d, ic, 240, 150)
        tw = d.textlength(ic, font=f); d.text((240 - tw/2, 310), ic, font=f, fill=accent, anchor='lm')
        # название
        name = ch['name']; f = fit(d, name, 700, 92)
        d.text((450, 250), name, font=f, fill=(240, 240, 250), anchor='lm')
        d.text((450, 340), 'Прямой эфир · бесплатно · без VPN', font=font(34), fill=(160, 165, 190), anchor='lm')
        d.rounded_rectangle([450, 390, 640, 450], radius=14, fill=(204, 0, 0))
        d.text((545, 420), '● LIVE 24/7', font=font(30), fill=(255, 255, 255), anchor='mm')
        d.text((90, 560), 'russian-tv.com', font=font(40), fill=accent, anchor='lm')
        d.text((1110, 560), 'Русское ТВ · Russian TV', font=font(30), fill=(140, 145, 170), anchor='rm')
        img.save(os.path.join(ROOT, 'assets/og', slug + '.jpg'), 'JPEG', quality=82, optimize=True)
        cnt += 1
print('og images:', cnt)
# подключаем на страницах
done = 0
for g in groups:
    for ch in g['channels']:
        slug = ch.get('slug')
        if not slug: continue
        url = f'https://russian-tv.com/assets/og/{slug}.jpg'
        for p in (f'{slug}/index.html', f'en/{slug}/index.html'):
            fp = os.path.join(ROOT, p)
            if not os.path.exists(fp): continue
            s = open(fp, encoding='utf-8').read(); o = s
            s = s.replace('content="https://russian-tv.com/og-image.jpg"', f'content="{url}"')
            if s != o: open(fp, 'w', encoding='utf-8').write(s); done += 1
print('pages with personal og:image:', done)
