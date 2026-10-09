#!/usr/bin/env python3
"""Кино Детектив -> Viju TV1000 Русское кино (по факту эфира). Идемпотентно."""
import sys, os, glob, re
ROOT = sys.argv[1]
NEW_RU, NEW_EN = 'Viju TV1000 Русское кино', 'Viju TV1000 Russian Cinema'
RU_ESC = '\\u041a\\u0438\\u043d\\u043e \\u0414\\u0435\\u0442\\u0435\\u043a\\u0442\\u0438\\u0432'   # "Кино Детектив" как \\uXXXX на EN-главной
NEW_RU_ESC = NEW_RU.encode('ascii','backslashreplace').decode().replace('\\\\','\\')
def esc(s): return ''.join(c if ord(c) < 128 else '\\u%04x' % ord(c) for c in s)
n = 0
for f in glob.glob(os.path.join(ROOT, '**/*.html'), recursive=True) + [os.path.join(ROOT, 'sitemap.xml')]:
    s = open(f, encoding='utf-8').read(); o = s
    page = os.path.relpath(f, ROOT)
    s = s.replace('Детективы и триллеры 24/7', 'Русское кино и сериалы 24/7')
    s = s.replace('Detective films and thrillers 24/7', 'Russian films and series 24/7')
    s = s.replace('Кино Детектив', NEW_RU).replace('Kino Detektiv', NEW_EN)
    s = s.replace(esc('Кино Детектив'), esc(NEW_RU))
    s = s.replace('>ДТК<', '>VRK<').replace("icon:'ДТК'", "icon:'VRK'").replace('icon:"\\u0414\\u0422\\u041a"', 'icon:"VRK"')
    if page in ('kino-detektiv-live/index.html', 'en/kino-detektiv-live/index.html'):
        s = s.replace('детективы онлайн без VPN', 'русское кино онлайн без VPN')
        s = s.replace('детективы и криминальные фильмы в прямом эфире', 'русское кино и сериалы в прямом эфире')
        s = s.replace('Russian Detectives', 'Russian Cinema').replace('Russian detective and crime films', 'Russian films and series')
        s = re.sub(r'<p>' + re.escape(NEW_RU) + r' — специализированный канал.*?</p>\n\s*<p>В эфире — классические.*?</p>\n\s*<p>Смотреть .*?</p>',
                   f'<p>{NEW_RU} — телеканал с русским кино и сериалами в прямом эфире круглосуточно.</p>\n'
                   f'    <p>В эфире — российские фильмы и сериалы разных жанров. Трансляция работает на любом устройстве — компьютере, iPhone, Android и Smart TV — из любой страны мира.</p>\n'
                   f'    <p>Смотреть {NEW_RU} онлайн бесплатно на russian-tv.com — 24/7 без регистрации.</p>', s, flags=re.S)
        s = re.sub(r'<p>' + re.escape(NEW_EN) + r' is a 24/7 channel dedicated to.*?</p>\n\s*<p>On air:.*?</p>\n\s*<p>Watch .*?</p>',
                   f'<p>{NEW_EN} is a 24/7 channel with Russian films and series.</p>\n'
                   f'    <p>On air: Russian movies and TV series in many genres. The stream works on any device — desktop, iPhone, Android and Smart TV — from any country.</p>\n'
                   f'    <p>Watch {NEW_EN} online free at russian-tv.com — 24/7, no VPN, no registration.</p>', s, flags=re.S)
    if s != o:
        open(f, 'w', encoding='utf-8').write(s); n += 1
print('renamed in files:', n)
