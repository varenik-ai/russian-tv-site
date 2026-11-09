#!/usr/bin/env python3
"""Светлые варианты логотипов для боковых списков каналов: почти белые заливки (#EE… и светлее) заменяются тёмно-синим #14213d,
чтобы логотип читался на светлой плитке. Оригиналы (для тёмных мест сайта и мини-аппа) не меняются.
Результат: assets/logos/light/<имя>.svg только для логотипов, где есть светлые заливки. Идемпотентно."""
import sys, os, re, glob
ROOT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else '.')
DARK = '#14213d'
HEX = re.compile(r'#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b')
def is_light(h):
    if len(h) == 3: h = ''.join(c * 2 for c in h)
    r, g, b = (int(h[i:i+2], 16) for i in (0, 2, 4))
    return min(r, g, b) >= 0xEE
src_dir = os.path.join(ROOT, 'assets/logos'); out_dir = os.path.join(src_dir, 'light')
os.makedirs(out_dir, exist_ok=True)
made = []
for f in sorted(glob.glob(os.path.join(src_dir, '*.svg'))):
    s = open(f, encoding='utf-8', errors='ignore').read()
    cnt = 0
    def sub(m):
        global cnt
        if is_light(m.group(1)): cnt += 1; return DARK
        return m.group(0)
    t = HEX.sub(sub, s)
    t = re.sub(r'(fill|stroke|stop-color)(=["\']|:\s*)white\b', lambda m: (globals().__setitem__('cnt', cnt + 1) or m.group(1) + m.group(2) + DARK), t)
    if cnt:
        open(os.path.join(out_dir, os.path.basename(f)), 'w', encoding='utf-8').write(t); made.append(os.path.basename(f))
print('logos light:', len(made), 'файлов:', ', '.join(made))
