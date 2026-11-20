#!/usr/bin/env python3
"""21.11.2026: мета-тег подтверждения владения сайтом для Bing Webmaster Tools на главных страницах (RU и EN). Идемпотентен.
Тег нельзя убирать: иначе Bing снимет подтверждение."""
import sys, os
ROOT = sys.argv[1]
TAG = '<meta name="msvalidate.01" content="3C2D7AEE14006BDD73C4B61407322587" />'
n = 0
for p in ('index.html', 'en/index.html'):
    f = os.path.join(ROOT, p); s = open(f, encoding='utf-8').read()
    if 'msvalidate.01' in s: continue
    i = s.find('<head>')
    if i < 0: print('нет <head>', p); continue
    j = s.find('\n', i)
    s = s[:j + 1] + '  ' + TAG + '\n' + s[j + 1:]
    open(f, 'w', encoding='utf-8').write(s); n += 1
print('gen_bing_verify: страниц изменено', n)
