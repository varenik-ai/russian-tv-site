#!/usr/bin/env python3
"""Правки по аудиту 11.11.2026 (идемпотентно). Запускать после gen_remove_broken.py.
1) Латинская «o» в слове «Киносвидание» -> кириллическая (страницы, README, gen_blog.py).
2) RU-шаблоны FAQ на страницах каналов: название канала в кавычках после слова «канал» (иначе не склоняется: «о Кинохит»).
3) Описания в боковых списках каналов (<div class="ch-desc-s">) убираются из разметки: в EN они были обрезаны на середине слова.
4) JSON-LD: SearchAction удалён (поиск по ?q= не реализован).
5) og:* на юридических страницах; у /about/ убран односторонний hreflang (EN-адрес — заглушка-редирект).
6) Сообщение «Ничего не найдено» в поиске по каналам (главные и страницы каналов).
7) Склонение числа в «54 российских телеканала», «54 русских канала»; короткий title у «Москва. Доверие»."""
import sys, os, re, glob
ROOT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else '.')
LAT_O = 'Кин' + 'o' + 'свидание'      # с латинской o
CYR_O = 'Киносвидание'
OGIMG = 'https://russian-tv.com/og-image.jpg'
def rd(p): return open(os.path.join(ROOT, p), encoding='utf-8').read()
def wr(p, s): open(os.path.join(ROOT, p), 'w', encoding='utf-8').write(s)

FAQ = [   # (регулярка с группой имени N, замена)
 (r'Частые вопросы о (?!канале )%s', 'Частые вопросы о канале «%s»'),
 (r'Как смотреть (?!канал )%s онлайн бесплатно\?', 'Как смотреть канал «%s» онлайн бесплатно?'),
 (r'трансляция %s запустится автоматически', 'трансляция канала «%s» запустится автоматически'),
 (r'Можно ли смотреть (?!канал )%s за рубежом\?', 'Можно ли смотреть канал «%s» за рубежом?'),
 (r'Да! %s онлайн доступен из любой точки мира', 'Да! Канал «%s» доступен онлайн из любой точки мира'),
 (r'Доступен ли (?!канал )%s на iPhone и Android\?', 'Доступен ли канал «%s» на iPhone и Android?'),
 (r'Нужна ли регистрация для просмотра (?!канала )%s\?', 'Нужна ли регистрация для просмотра канала «%s»?'),
 (r'Смотреть (?!канал )%s онлайн бесплатно на russian-tv\.com', 'Смотреть канал «%s» онлайн бесплатно на russian-tv.com'),
]
CH_SEARCH_OLD = "      label.style.display = hasVisible ? '' : 'none';\n    });\n  });\n}"
CH_SEARCH_NEW = ("      label.style.display = hasVisible ? '' : 'none';\n    });\n"
 "    var box = document.querySelector('.ch-list-scroll'), em = document.getElementById('ch-empty');\n"
 "    if (!em && box) { em = document.createElement('div'); em.id = 'ch-empty'; em.style.cssText = 'padding:16px 8px;color:var(--muted);font-size:14px;display:none'; em.textContent = (document.documentElement.lang || '').indexOf('en') === 0 ? 'Nothing found' : 'Ничего не найдено'; box.appendChild(em); }\n"
 "    if (em) { var any = false; items.forEach(function(e) { if (e.style.display !== 'none') any = true; }); em.style.display = any ? 'none' : 'block'; }\n"
 "  });\n}")
HOME_OLD = re.compile(r"(      grp\.appendChild\(item\);\n    \}\);\n  \}\);\n)(\})")
def home_new(en):
    msg = 'Nothing found' if en else 'Ничего не найдено'
    return (r"\1  if (!sidebar.querySelector('.cat-group')) { const e = document.createElement('div'); e.className = 'ch-empty'; "
            "e.style.cssText = 'padding:16px 8px;color:var(--muted);font-size:14px'; e.textContent = '%s'; sidebar.appendChild(e); }\n\\2" % msg)
n = 0
for f in glob.glob(os.path.join(ROOT, '**/*.html'), recursive=True):
    rel = os.path.relpath(f, ROOT)
    if rel.startswith(('tools/', 'node_modules/')): continue
    s = o = open(f, encoding='utf-8').read()
    s = s.replace(LAT_O, CYR_O)
    s = re.sub(r'<div class="ch-desc-s">.*?</div>', '', s)
    s = re.sub(r',\s*"potentialAction":\s*\{"@type":\s*"SearchAction".*?"query-input":\s*"[^"]*"\}', '', s, flags=re.S)
    s = re.sub(r',\s*"potentialAction":\s*\{"@type":\s*"SearchAction",\s*"target":\s*\{[^}]*\},\s*"query-input":\s*"[^"]*"\}', '', s)
    if re.search(r'<html lang="ru"', s) and re.search(r'-live/index\.html$', rel):
        m = re.search(r'<h2>О канале (.+?)</h2>', s)
        if m:
            name = re.escape(m.group(1))
            for pat, rep in FAQ:
                s = re.sub(pat % name, lambda x, rep=rep, nm=m.group(1): rep % nm, s)
    if CH_SEARCH_OLD in s: s = s.replace(CH_SEARCH_OLD, CH_SEARCH_NEW)
    if rel in ('index.html', 'en/index.html') and 'ch-empty' not in s:
        s = HOME_OLD.sub(home_new(rel.startswith('en/')), s)
    s = re.sub(r'(\b54 (?:российских )?)телеканалов\b', r'\1телеканала', s)
    s = re.sub(r'\b54 (русских|российских) каналов\b', r'54 \1 канала', s)
    if rel == 'moskva-doverie-live/index.html':
        s = s.replace('Москва. Доверие прямой эфир — московское телевидение онлайн без VPN', 'Москва. Доверие прямой эфир — онлайн без VPN')
    if rel in ('privacy/index.html', 'advertising/index.html', 'en/privacy/index.html', 'en/advertising/index.html') and 'og:title' not in s:
        t = re.search(r'<title>([^<]*)</title>', s).group(1); d = re.search(r'<meta name="description" content="([^"]*)"', s)
        d = d.group(1) if d else t
        url = 'https://russian-tv.com/' + rel[:-len('index.html')]
        add = ('  <meta property="og:type" content="website"/>\n  <meta property="og:title" content="%s"/>\n  <meta property="og:description" content="%s"/>\n'
               '  <meta property="og:url" content="%s"/>\n  <meta property="og:image" content="%s"/>\n  <meta name="twitter:card" content="summary_large_image"/>\n') % (t, d, url, OGIMG)
        s = s.replace('</head>', add + '</head>', 1)
    if rel == 'about/index.html':   # EN-адрес /en/about/ — заглушка-редирект, взаимного hreflang быть не может
        s = re.sub(r'\s*<link rel="alternate" hreflang="[a-z-]+" href="[^"]*"/>', '', s)
    if s != o: open(f, 'w', encoding='utf-8').write(s); n += 1
# исходники, где было латинское слово
for p in ('README.md', 'tools/gen_blog.py'):
    fp = os.path.join(ROOT, p)
    if os.path.exists(fp):
        t = open(fp, encoding='utf-8').read()
        if LAT_O in t: open(fp, 'w', encoding='utf-8').write(t.replace(LAT_O, CYR_O)); n += 1
print('fixtext: файлов изменено', n)
