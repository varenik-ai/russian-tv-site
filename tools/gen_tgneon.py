#!/usr/bin/env python3
"""Пульсирующий неон у баннера «Подписывайся в Telegram» над плеером (компьютеры, от 1025 px). Идемпотентно.
Добавляет CSS сразу после правила .tg-banner-desk-arrow во встроенных стилях страницы. Метка: /*tgneon*/."""
import sys, os, glob
ROOT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else '.')
ANCHORS = ['.tg-banner-desk-arrow{font-size:15px;opacity:.6;flex-shrink:0}}',   # страницы каналов (минифицированный CSS)
           '.tg-banner-desk-arrow { font-size:15px; opacity:.6; flex-shrink:0; }',  # главная RU (внутри @media 901px)
           '.tg-banner-desk-arrow{font-size:15px;opacity:.6;flex-shrink:0}\n']  # главная EN
CSS = (
 '/*tgneon*/@media(min-width:1025px){'
 '.tg-banner-desk{border:2px solid #2aa9e0;background:linear-gradient(135deg,#071a33,#06283f);animation:tgNeon 1.6s ease-in-out infinite}'
 '.tg-banner-desk-icon{box-shadow:0 0 12px #229ED9;animation:tgNeonIcon 1.6s ease-in-out infinite}'
 '.tg-banner-desk-text b{text-shadow:0 0 8px rgba(63,195,255,.9)}'
 '.tg-banner-desk-arrow{color:#7fdcff;opacity:1;animation:tgNeonArrow 1.6s ease-in-out infinite}}'
 '@keyframes tgNeon{0%,100%{box-shadow:0 0 4px rgba(63,195,255,.5),0 0 12px rgba(34,158,217,.35),inset 0 0 6px rgba(63,195,255,.15);border-color:#2aa9e0}'
 '50%{box-shadow:0 0 8px #3fc3ff,0 0 24px rgba(34,158,217,.8),0 0 44px rgba(34,158,217,.45),inset 0 0 14px rgba(63,195,255,.35);border-color:#7fe0ff}}'
 '@keyframes tgNeonIcon{0%,100%{transform:scale(1)}50%{transform:scale(1.12)}}'
 '@keyframes tgNeonArrow{0%,100%{transform:translateX(0)}50%{transform:translateX(4px)}}'
 '@media(prefers-reduced-motion:reduce){.tg-banner-desk,.tg-banner-desk-icon,.tg-banner-desk-arrow{animation:none}}'
)
n = skipped = 0
for f in glob.glob(os.path.join(ROOT, '**/*.html'), recursive=True):
    s = open(f, encoding='utf-8').read()
    if 'class="tg-banner-desk"' not in s or '/*tgneon*/' in s: continue
    a = next((x for x in ANCHORS if x in s), None)
    if not a: skipped += 1; print('нет якоря:', os.path.relpath(f, ROOT)); continue
    open(f, 'w', encoding='utf-8').write(s.replace(a, a + CSS, 1)); n += 1
print('tgneon:', n, 'страниц изменено,', skipped, 'без якоря')
