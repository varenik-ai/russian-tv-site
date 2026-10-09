#!/usr/bin/env python3
"""Почта dyaltd@gmail.com, страницы для рекламодателей (RU/EN), ссылка в подвале. Идемпотентно."""
import sys, os, glob, re
ROOT = sys.argv[1]
MAIL = 'dyaltd@gmail.com'
def rd(p): return open(os.path.join(ROOT, p), encoding='utf-8').read()
def wr(p, s):
    os.makedirs(os.path.dirname(os.path.join(ROOT, p)), exist_ok=True)
    open(os.path.join(ROOT, p), 'w', encoding='utf-8').write(s)

# 1. почта
for p in ('privacy/index.html', 'about/index.html', 'en/privacy/index.html'):
    s = rd(p); wr(p, s.replace('support@russian-tv.com', MAIL))

# 2. страницы для рекламодателей на базе страницы privacy
def make(lang):
    base = rd('privacy/index.html' if lang == 'ru' else 'en/privacy/index.html')
    ru = lang == 'ru'
    slug = 'advertising' if ru else 'en/advertising'
    t = base
    t = re.sub(r'<title>.*?</title>', '<title>' + ('Реклама на сайте — Russian-TV.com' if ru else 'Advertise on Russian-TV.com') + '</title>', t, 1, flags=re.S)
    t = re.sub(r'(<meta name="description" content=")[^"]*', r'\g<1>' + ('Реклама на Russian-TV.com: размещение баннеров и спонсорских блоков на страницах российских телеканалов онлайн. Контакт для рекламодателей.' if ru else 'Advertise on Russian-TV.com: banner and sponsored placements on pages of Russian TV channels online. Contact for advertisers.'), t, 1)
    t = t.replace('canonical" href="https://russian-tv.com/privacy/"', f'canonical" href="https://russian-tv.com/{slug}/"').replace('canonical" href="https://russian-tv.com/en/privacy/"', f'canonical" href="https://russian-tv.com/{slug}/"')
    t = re.sub(r'<link rel="alternate" hreflang="ru"[^>]*>', '<link rel="alternate" hreflang="ru" href="https://russian-tv.com/advertising/"/>', t)
    t = re.sub(r'<link rel="alternate" hreflang="en"[^>]*>', '<link rel="alternate" hreflang="en" href="https://russian-tv.com/en/advertising/"/>', t)
    t = re.sub(r'<link rel="alternate" hreflang="x-default"[^>]*>', '<link rel="alternate" hreflang="x-default" href="https://russian-tv.com/advertising/"/>', t)
    if ru:
        crumbs = '<a href="/">Главная</a><span>›</span><span>Рекламодателям</span>'
        body = f'''<div class="wrap">
  <h1>Реклама на Russian-TV.com</h1>
  <p class="updated">Последнее обновление: 9 октября 2026 г.</p>

  <p><strong>Russian-TV.com</strong> — бесплатный сервис для просмотра российских телеканалов онлайн, ориентированный на русскоязычных зрителей по всему миру. Мы размещаем рекламу на страницах сайта и готовы обсудить размещение вашего проекта.</p>

  <h2>Что можно разместить</h2>
  <ul>
    <li><strong>Баннер под плеером</strong> на страницах каналов — 728×90 (десктоп) и 320×100 (мобильные).</li>
    <li><strong>Блок 300×250</strong> рядом с разделом «Похожие каналы».</li>
    <li><strong>Баннер на главной странице</strong> над списком каналов или под ним.</li>
    <li><strong>Спонсорская интеграция</strong> на страницах отдельного канала или раздела (новости, кино, детские, музыка, хобби, спорт).</li>
  </ul>

  <h2>Как это работает</h2>
  <p>Опишите проект и пожелания по размещению — мы предложим подходящие страницы, форматы и условия. Рекламные материалы отмечаются пометкой «Реклама».</p>

  <h2>Контакт для рекламодателей</h2>
  <p>Напишите нам: <a href="mailto:{MAIL}?subject=Реклама%20на%20russian-tv.com"><strong>{MAIL}</strong></a></p>
</div>'''
        foot = '''<footer>
  <div>🇷🇺 <a href="/">Русское ТВ</a> — бесплатное российское ТВ онлайн</div>
  <div style="margin-top:6px">
    <a href="/">Все каналы</a>
    <a href="/about/">О сайте</a>
    <a href="/privacy/">Политика конфиденциальности</a>
    <a href="/en/advertising/">English</a>
  </div>
</footer>'''
    else:
        crumbs = '<a href="/en/">Home</a><span>›</span><span>Advertise</span>'
        body = f'''<div class="wrap">
  <h1>Advertise on Russian-TV.com</h1>
  <p class="updated">Last updated: October 9, 2026</p>

  <p><strong>Russian-TV.com</strong> is a free service for watching Russian TV channels online, aimed at Russian-speaking viewers around the world. We run advertising on the site and are happy to discuss placing your project.</p>

  <h2>What you can place</h2>
  <ul>
    <li><strong>Banner below the player</strong> on channel pages — 728×90 (desktop) and 320×100 (mobile).</li>
    <li><strong>300×250 block</strong> next to the “Similar channels” section.</li>
    <li><strong>Homepage banner</strong> above or below the channel list.</li>
    <li><strong>Sponsored placement</strong> on a specific channel or category page (news, movies, kids, music, hobby, sport).</li>
  </ul>

  <h2>How it works</h2>
  <p>Describe your project and placement wishes — we will suggest suitable pages, formats and terms. Advertising materials are labelled “Advertisement”.</p>

  <h2>Contact for advertisers</h2>
  <p>Email us: <a href="mailto:{MAIL}?subject=Advertising%20on%20russian-tv.com"><strong>{MAIL}</strong></a></p>
</div>'''
        foot = '''<footer>
  <div>🇷🇺 <a href="/en/">Russian TV</a> — free Russian TV online</div>
  <div style="margin-top:6px">
    <a href="/en/">All channels</a>
    <a href="/en/privacy/">Privacy Policy</a>
    <a href="/advertising/">Русский</a>
  </div>
</footer>'''
    i = t.find('<div class="breadcrumb">'); j = t.find('</div>', i) + 6
    t = t[:i] + '<div class="breadcrumb">\n  ' + crumbs + '\n</div>' + t[j:]
    a = t.find('<div class="wrap">'); b = t.find('</div>\n<footer>')
    t = t[:a] + body + t[b:]
    fa = t.find('<footer>'); fb = t.find('</footer>') + 9
    t = t[:fa] + foot + t[fb:]
    wr(f'{slug}/index.html', t)
make('ru'); make('en')

# 3. ссылка в подвале всех страниц (в блоке legal-note)
n = 0
for f in glob.glob(os.path.join(ROOT, '**/*.html'), recursive=True):
    s = open(f, encoding='utf-8').read(); o = s
    if 'class="legal-note"' not in s or 'advertising/' in s.split('class="legal-note"')[1][:900]: continue
    if s.count('подробнее</a>.</div>'):
        s = s.replace('подробнее</a>.</div>', 'подробнее</a>. · <a href="/advertising/" style="color:inherit;text-decoration:underline">Рекламодателям</a></div>', 1)
    elif s.count('details</a>.</div>'):
        s = s.replace('details</a>.</div>', 'details</a>. · <a href="/en/advertising/" style="color:inherit;text-decoration:underline">Advertise with us</a></div>', 1)
    if s != o: open(f, 'w', encoding='utf-8').write(s); n += 1
print('footer ad links:', n)
