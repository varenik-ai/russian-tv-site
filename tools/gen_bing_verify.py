#!/usr/bin/env python3
"""Мета-теги подтверждения владения сайтом на главных страницах (RU и EN). Идемпотентен. Теги нельзя убирать: иначе сервис снимет подтверждение.
21.11.2026: Bing Webmaster Tools (msvalidate.01). 23.11.2026: рекламная сеть Kadam (kadam-verification)."""
import sys, os
ROOT = sys.argv[1]
TAGS = [('msvalidate.01', '<meta name="msvalidate.01" content="3C2D7AEE14006BDD73C4B61407322587" />'),
        ('kadam-verification', '<meta name="kadam-verification" content="kadam72b9f386fc2d4018bd159c97759a226e" />')]
n = 0
for p in ('index.html', 'en/index.html'):
    f = os.path.join(ROOT, p); s = o = open(f, encoding='utf-8').read()
    for key, tag in TAGS:
        if key in s: continue
        i = s.find('<head>')
        if i < 0: print('нет <head>', p); break
        j = s.find('\n', i)
        s = s[:j + 1] + '  ' + tag + '\n' + s[j + 1:]
    if s != o: open(f, 'w', encoding='utf-8').write(s); n += 1
print('gen_bing_verify: страниц изменено', n)
