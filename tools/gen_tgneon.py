"""Неон у баннера «Подписывайся в Telegram» над плеером (компьютеры, от 1025 px): крупный шрифт и мерцание как у
неисправной неоновой вывески. Идемпотентно. Добавляет CSS сразу после правила .tg-banner-desk-arrow во встроенных стилях.
Метка: /*tgneon2*/ (старая версия /*tgneon*/ заменяется)."""
import sys, os, glob
ROOT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else '.')
ANCHORS = ['.tg-banner-desk-arrow{font-size:15px;opacity:.6;flex-shrink:0}}',   # страницы каналов (минифицированный CSS)
           '.tg-banner-desk-arrow { font-size:15px; opacity:.6; flex-shrink:0; }',  # главная RU (внутри @media 901px)
           '.tg-banner-desk-arrow{font-size:15px;opacity:.6;flex-shrink:0}\n']  # главная EN
LEGACY = '/*tgneon*/@media(min-width:1025px){.tg-banner-desk{border:2px solid #2aa9e0;background:linear-gradient(135deg,#071a33,#06283f);animation:tgNeon 1.6s ease-in-out infinite}.tg-banner-desk-icon{box-shadow:0 0 12px #229ED9;animation:tgNeonIcon 1.6s ease-in-out infinite}.tg-banner-desk-text b{text-shadow:0 0 8px rgba(63,195,255,.9)}.tg-banner-desk-arrow{color:#7fdcff;opacity:1;animation:tgNeonArrow 1.6s ease-in-out infinite}}@keyframes tgNeon{0%,100%{box-shadow:0 0 4px rgba(63,195,255,.5),0 0 12px rgba(34,158,217,.35),inset 0 0 6px rgba(63,195,255,.15);border-color:#2aa9e0}50%{box-shadow:0 0 8px #3fc3ff,0 0 24px rgba(34,158,217,.8),0 0 44px rgba(34,158,217,.45),inset 0 0 14px rgba(63,195,255,.35);border-color:#7fe0ff}}@keyframes tgNeonIcon{0%,100%{transform:scale(1)}50%{transform:scale(1.12)}}@keyframes tgNeonArrow{0%,100%{transform:translateX(0)}50%{transform:translateX(4px)}}@media(prefers-reduced-motion:reduce){.tg-banner-desk,.tg-banner-desk-icon,.tg-banner-desk-arrow{animation:none}}'
# мерцание: ступенчатое (step-end), длинная пауза «горит», короткие сбои. Проценты цикла 4,2 с.
FLICKER = [(0,1),(3,0),(5,1),(7,0),(8.5,1),(10,0),(11,1),(52,0),(54,1),(55.5,0),(57,1),(58,0),(59,1),(100,1)]
def kf(name, on, off):
    return '@keyframes %s{%s}' % (name, ''.join('%s%%{%s}' % (('%g' % t), on if v else off) for t, v in FLICKER))
CSS = (
 '/*tgneon2*/@media(min-width:1025px){'
 '.tg-banner-desk{padding:14px 20px;gap:14px;border:2px solid #7fe0ff;background:linear-gradient(135deg,#071a33,#06283f);'
 'box-shadow:0 0 8px #3fc3ff,0 0 24px rgba(34,158,217,.8),0 0 44px rgba(34,158,217,.45),inset 0 0 14px rgba(63,195,255,.35);animation:tgNeon 4.2s step-end infinite}'
 '.tg-banner-desk-icon{width:40px;height:40px;box-shadow:0 0 14px #229ED9;animation:tgNeonIco 4.2s step-end infinite}'
 '.tg-banner-desk-icon svg{width:22px;height:22px}'
 '.tg-banner-desk-text{font-size:17px;line-height:1.3}'
 '.tg-banner-desk-text b{font-size:20px;letter-spacing:.2px;color:#fff;text-shadow:0 0 6px #fff,0 0 12px #3fc3ff,0 0 24px #229ED9;animation:tgNeonTxt 4.2s step-end infinite}'
 '.tg-banner-desk-arrow{font-size:24px;color:#9fe6ff;opacity:1;text-shadow:0 0 10px #3fc3ff;animation:tgNeonTxt 4.2s step-end infinite}}'
 + kf('tgNeon', 'border-color:#7fe0ff;box-shadow:0 0 8px #3fc3ff,0 0 24px rgba(34,158,217,.8),0 0 44px rgba(34,158,217,.45),inset 0 0 14px rgba(63,195,255,.35)',
                'border-color:#15506d;box-shadow:0 0 0 transparent,inset 0 0 0 transparent')
 + kf('tgNeonIco', 'box-shadow:0 0 14px #229ED9;filter:none', 'box-shadow:none;filter:brightness(.55)')
 + kf('tgNeonTxt', 'color:#fff;text-shadow:0 0 6px #fff,0 0 12px #3fc3ff,0 0 24px #229ED9', 'color:#5d7f93;text-shadow:none')
 + '@media(prefers-reduced-motion:reduce){.tg-banner-desk,.tg-banner-desk-icon,.tg-banner-desk-text b,.tg-banner-desk-arrow{animation:none}}'
)
n = skipped = 0
for f in glob.glob(os.path.join(ROOT, '**/*.html'), recursive=True):
    s = open(f, encoding='utf-8').read()
    if 'class="tg-banner-desk"' not in s or '/*tgneon2*/' in s: continue
    if LEGACY in s:
        open(f, 'w', encoding='utf-8').write(s.replace(LEGACY, CSS, 1)); n += 1; continue
    a = next((x for x in ANCHORS if x in s), None)
    if not a: skipped += 1; print('нет якоря:', os.path.relpath(f, ROOT)); continue
    open(f, 'w', encoding='utf-8').write(s.replace(a, a + CSS, 1)); n += 1
print('tgneon:', n, 'страниц изменено,', skipped, 'без якоря')
