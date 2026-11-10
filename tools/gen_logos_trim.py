#!/usr/bin/env python3
"""Логотипы каналов без пустых полей: viewBox обрезается до реального содержимого (+3%), чтобы в маленьких плитках логотип
занимал всю плитку и читался. Оригиналы (assets/logos/*.svg) не меняются; обрезанные копии: assets/logos/trim/*.svg.
Границы содержимого (x, y, ширина, высота в координатах исходного viewBox) измерены в браузере через getBBox() 10.11.2026.
Все исходные логотипы нарисованы под тёмный фон (белые буквы + цветные элементы), поэтому плитки остаются тёмными. Идемпотентно."""
import sys, os, re
ROOT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else '.')
BBOX = {
 'perviy': (298, 101, 184, 239), 'rossiya1': (40, 53, 159, 37), 'ntv': (239, 116, 362, 240), 'rossiya24': (48, 64, 192, 45),
 'pyatyy': (160, 117, 448, 159), 'logo-tv-centr': (216, 155, 467, 239), 'logo-mir': (189, 49, 273, 273),
 'logo-zvezda': (57, 102, 495, 138), 'logo-karusel': (228, 193, 1000, 417), 'logo-rutv': (155, 80, 487, 240),
 'logo-solovev-live': (281, 165, 841, 290), 'logo-tnt': (640, 459, 1280, 521), 'logo-muz-tv': (223, 60, 195, 240),
}
src_dir = os.path.join(ROOT, 'assets/logos'); out_dir = os.path.join(src_dir, 'trim'); os.makedirs(out_dir, exist_ok=True)
for name, (x, y, w, h) in BBOX.items():
    s = open(os.path.join(src_dir, name + '.svg'), encoding='utf-8', errors='ignore').read()
    p = max(w, h) * 0.03
    vb = '%g %g %g %g' % (x - p, y - p, w + 2 * p, h + 2 * p)
    m = re.search(r'<svg\b[^>]*>', s)
    tag = m.group(0)
    tag2 = re.sub(r'\sviewBox="[^"]*"', ' viewBox="%s"' % vb, tag)
    tag2 = re.sub(r'\swidth="[^"]*"', ' width="%d"' % round(w + 2 * p), tag2)
    tag2 = re.sub(r'\sheight="[^"]*"', ' height="%d"' % round(h + 2 * p), tag2)
    tag2 = tag2.replace(' overflow="visible"', '')
    open(os.path.join(out_dir, name + '.svg'), 'w', encoding='utf-8').write(s.replace(tag, tag2, 1))
print('logos trim:', len(BBOX), 'файлов')
