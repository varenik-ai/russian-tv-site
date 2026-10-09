#!/usr/bin/env python3
"""Заменяет встроенные трекеры на assets/consent.js (загрузка только после согласия). Идемпотентно."""
import sys, os, glob, re
ROOT = sys.argv[1]
GTAG_SRC = re.compile(r'[ \t]*<script async src="https://www\.googletagmanager\.com/gtag/js\?id=G-XLSJE8NKJE"></script>\n?')
GTAG_INL = re.compile(r'[ \t]*<script>window\.dataLayer=window\.dataLayer\|\|\[\];function gtag\(\)\{dataLayer\.push\(arguments\);\}gtag\(\'js\',new Date\(\)\);gtag\(\'config\',\'G-XLSJE8NKJE\'\);</script>\n?')
CLARITY = re.compile(r'[ \t]*<script type="text/javascript">\(function\(c,l,a,r,i,t,y\)\{c\[a\]=c\[a\]\|\|function\(\)\{\(c\[a\]\.q=c\[a\]\.q\|\|\[\]\)\.push\(arguments\)\};t=l\.createElement\(r\).*?"clarity","script","xkhl4v4ft0"\);</script>\n?', re.S)
METRIKA = re.compile(r'[ \t]*<script type="text/javascript">\(function\(m,e,t,r,i,k,a\)\{m\[i\]=m\[i\]\|\|function\(\).*?ym\(110584472,"init",\{[^}]*\}\);</script>\n?', re.S)
PIXEL = re.compile(r'[ \t]*<noscript><div><img src="https://mc\.yandex\.ru/watch/110584472"[^>]*/></div></noscript>\n?')
n = 0
for f in glob.glob(os.path.join(ROOT, '**/*.html'), recursive=True):
    s = open(f, encoding='utf-8').read(); o = s
    if 'consent.js' in s: continue
    if 'googletagmanager.com/gtag' not in s and 'mc.yandex.ru/metrika' not in s: continue
    m = GTAG_SRC.search(s)
    pos = m.start() if m else s.find('</head>')
    for rx in (GTAG_SRC, GTAG_INL, CLARITY, METRIKA, PIXEL):
        s = rx.sub('', s)
    tag = '<script src="/assets/consent.js"></script>\n'
    pos = min(pos, len(s)); 
    # вставляем туда, где был первый трекер
    if m and pos <= len(s): s = s[:pos] + '  ' + tag + s[pos:]
    else: s = s.replace('</head>', '  ' + tag + '</head>', 1)
    if s != o: open(f, 'w', encoding='utf-8').write(s); n += 1
print('pages gated:', n)
left = 0
for f in glob.glob(os.path.join(ROOT, '**/*.html'), recursive=True):
    s = open(f, encoding='utf-8').read()
    if re.search(r'googletagmanager\.com/gtag|mc\.yandex\.ru/metrika|clarity\.ms/tag|mc\.yandex\.ru/watch', s): left += 1; print('LEFT', f)
print('pages with raw trackers left:', left)

# --- второй проход: Google Tag Manager (inline + noscript iframe) ---
GTM_INL = re.compile(r'[ \t]*<!-- Google Tag Manager -->\s*<script>\(function\(w,d,s,l,i\)\{.*?GTM-TWVC9XDN\'\);</script>\s*<!-- End Google Tag Manager -->\n?', re.S)
GTM_NS = re.compile(r'[ \t]*<!-- Google Tag Manager \(noscript\) -->\s*<noscript><iframe src="https://www\.googletagmanager\.com/ns\.html\?id=GTM-TWVC9XDN"[^>]*></iframe></noscript>\s*<!-- End Google Tag Manager \(noscript\) -->\n?', re.S)
g = 0
for f in glob.glob(os.path.join(ROOT, '**/*.html'), recursive=True):
    s = open(f, encoding='utf-8').read(); o = s
    s = GTM_INL.sub('', s); s = GTM_NS.sub('', s)
    s = re.sub(r'[ \t]*<script>\(function\(w,d,s,l,i\)\{w\[l\]=w\[l\]\|\|\[\];.*?GTM-TWVC9XDN\'\);</script>\n?', '', s, flags=re.S)
    s = re.sub(r'[ \t]*<noscript><iframe src="https://www\.googletagmanager\.com/ns\.html\?id=GTM-TWVC9XDN"[^>]*></iframe></noscript>\n?', '', s)
    if s != o: open(f, 'w', encoding='utf-8').write(s); g += 1
print('GTM removed from pages:', g)
rem = [f for f in glob.glob(os.path.join(ROOT, '**/*.html'), recursive=True) if 'GTM-TWVC9XDN' in open(f, encoding='utf-8').read()]
print('pages still containing GTM id:', len(rem), rem[:3])
