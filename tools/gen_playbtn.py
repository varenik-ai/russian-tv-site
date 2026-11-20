#!/usr/bin/env python3
"""20.11.2026: современная кнопка play на страницах каналов (RU/EN) вместо синего круга с символом ▶ (по просьбе владельца).
Меняет и стили (.play-btn, .player-overlay), и разметку (векторная иконка вместо текстового символа). Идемпотентен: блок стилей между
/*playbtn2*/ и /*end-playbtn2*/ пересоздаётся при каждом запуске, поэтому правки дизайна достаточно внести сюда. Запускать после gen_site.py
(он пересоздаёт страницы каналов из шаблона)."""
import sys, os, re, glob
ROOT = sys.argv[1]
CSS = '''/*playbtn2*/
    .player-overlay{background:radial-gradient(70% 70% at 50% 42%,rgba(213,43,30,.26) 0%,rgba(213,43,30,0) 70%),linear-gradient(165deg,#171724 0%,#0a0a13 100%);gap:18px;-webkit-tap-highlight-color:transparent}
    .play-btn{position:relative;width:88px;height:88px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:0;background:linear-gradient(145deg,#ff5a4a 0%,#d52b1e 52%,#a31c13 100%);box-shadow:0 12px 34px rgba(213,43,30,.5),inset 0 0 0 1px rgba(255,255,255,.22),inset 0 -6px 14px rgba(0,0,0,.18);transition:transform .28s cubic-bezier(.2,.8,.2,1),box-shadow .28s}
    .play-btn::before,.play-btn::after{content:"";position:absolute;inset:0;border-radius:50%;border:2px solid rgba(255,98,82,.6);pointer-events:none;animation:rtvPlayPulse 2.6s ease-out infinite}
    .play-btn::after{animation-delay:1.3s}
    .play-btn svg{width:36px;height:36px;margin-left:5px;fill:#fff;filter:drop-shadow(0 2px 5px rgba(0,0,0,.35))}
    .player-overlay:hover .play-btn{transform:scale(1.08);box-shadow:0 16px 42px rgba(213,43,30,.62),inset 0 0 0 1px rgba(255,255,255,.3),inset 0 -6px 14px rgba(0,0,0,.18)}
    .player-overlay:active .play-btn{transform:scale(.96)}
    .player-overlay>div:not(.play-btn){color:#c3c3d8!important;font-size:14px!important;font-weight:600;letter-spacing:.02em;text-align:center;padding:0 16px}
    @keyframes rtvPlayPulse{0%{transform:scale(1);opacity:.75}100%{transform:scale(1.75);opacity:0}}
    @media (prefers-reduced-motion:reduce){.play-btn::before,.play-btn::after{animation:none;display:none}}
    /*end-playbtn2*/'''
ICON = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 4.7v14.6a1 1 0 0 0 1.52.85l11.9-7.3a1 1 0 0 0 0-1.7L8.52 3.85A1 1 0 0 0 7 4.7z"/></svg>'
OLD_RULES = re.compile(r'[ \t]*\.play-btn\{width:70px;height:70px;[^}]*\}\n[ \t]*\.play-btn:hover\{[^}]*\}')
BLOCK = re.compile(r'/\*playbtn2\*/.*?/\*end-playbtn2\*/', re.S)
n = 0
for f in glob.glob(os.path.join(ROOT, '**/index.html'), recursive=True):
    if '/tools/' in f or '/node_modules/' in f: continue
    s = o = open(f, encoding='utf-8').read()
    if 'class="play-btn"' not in s: continue
    if '/*playbtn2*/' in s: s = BLOCK.sub(lambda m: CSS.strip(), s, count=1)
    else: s = OLD_RULES.sub(lambda m: '    ' + CSS.strip(), s, count=1)
    s = s.replace('<div class="play-btn">▶</div>', '<div class="play-btn">' + ICON + '</div>')
    s = re.sub(r'<div class="play-btn"><svg.*?</svg></div>', lambda m: '<div class="play-btn">' + ICON + '</div>', s, count=1, flags=re.S)
    if s != o: open(f, 'w', encoding='utf-8').write(s); n += 1
print('gen_playbtn: страниц изменено', n)
