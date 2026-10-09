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
    t = re.sub(r'(<meta name="description" content=")[^"]*', r'\g<1>' + ('Реклама на Russian-TV.com: индивидуальные условия размещения для русскоязычной аудитории по всему миру. Форматы и стоимость обсуждаем под вашу задачу.' if ru else 'Advertise on Russian-TV.com: custom placements for a Russian-speaking audience worldwide. Formats and pricing are tailored to your goals.'), t, 1)
    t = t.replace('canonical" href="https://russian-tv.com/privacy/"', f'canonical" href="https://russian-tv.com/{slug}/"').replace('canonical" href="https://russian-tv.com/en/privacy/"', f'canonical" href="https://russian-tv.com/{slug}/"')
    t = re.sub(r'<link rel="alternate" hreflang="ru"[^>]*>', '<link rel="alternate" hreflang="ru" href="https://russian-tv.com/advertising/"/>', t)
    t = re.sub(r'<link rel="alternate" hreflang="en"[^>]*>', '<link rel="alternate" hreflang="en" href="https://russian-tv.com/en/advertising/"/>', t)
    t = re.sub(r'<link rel="alternate" hreflang="x-default"[^>]*>', '<link rel="alternate" hreflang="x-default" href="https://russian-tv.com/advertising/"/>', t)
    if ru:
        crumbs = '<a href="/">Главная</a><span>›</span><span>Рекламодателям</span>'
        body = f'''<div class="wrap">
  <h1>Реклама на Russian-TV.com</h1>
  <p class="updated">Последнее обновление: 9 октября 2026 г.</p>

  <p><strong>Russian-TV.com</strong> — бесплатный сервис для просмотра российских телеканалов онлайн. Нас смотрят русскоязычные зрители по всему миру: эмигранты, путешественники, студенты и все, кто хочет быть на связи с родным языком и новостями. Если ваш проект интересен этой аудитории, давайте обсудим сотрудничество.</p>

  <h2>Как мы работаем с рекламодателями</h2>
  <p>У нас нет жёсткого прайса и стандартных пакетов. Формат, место и сроки подбираем индивидуально под вашу задачу и бюджет — от небольшого тестового размещения до долгосрочного партнёрства.</p>

  <h2>Что можно обсудить</h2>
  <ul>
    <li><strong>Рекламные блоки и баннеры</strong> на главной странице, страницах каналов и тематических разделов — любого формата, который подходит вашему проекту.</li>
    <li><strong>Спонсорство и партнёрство</strong> — привязка к конкретному каналу или теме (новости, кино, детские, музыка, хобби, спорт).</li>
    <li><strong>Нативные и текстовые размещения</strong>, упоминания в статьях блога, подборках и описаниях каналов.</li>
    <li><strong>Свои идеи</strong> — если у вас нестандартная задача, расскажите о ней, и мы подумаем, как её решить.</li>
  </ul>

  <h2>Как начать</h2>
  <ol>
    <li>Напишите нам и коротко расскажите о проекте и о том, какого результата вы ждёте.</li>
    <li>Мы предложим подходящие страницы, формат, сроки и стоимость.</li>
    <li>Согласуем материалы и запускаем размещение. Рекламные материалы отмечаются пометкой «Реклама».</li>
  </ol>

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

  <p><strong>Russian-TV.com</strong> is a free service for watching Russian TV channels online. Our viewers are Russian speakers around the world: expats, travellers, students and anyone who wants to stay connected to their language and news. If your project is relevant to this audience, let's talk.</p>

  <h2>How we work with advertisers</h2>
  <p>We have no fixed rate card or standard packages. Format, placement and timing are tailored to your goals and budget — from a small test run to a long-term partnership.</p>

  <h2>What we can discuss</h2>
  <ul>
    <li><strong>Ad blocks and banners</strong> on the homepage, channel pages and category pages — in whatever format suits your project.</li>
    <li><strong>Sponsorship and partnerships</strong> tied to a specific channel or topic (news, movies, kids, music, hobby, sport).</li>
    <li><strong>Native and text placements</strong>, mentions in blog articles, selections and channel descriptions.</li>
    <li><strong>Your own ideas</strong> — if you have an unusual goal, tell us and we will work out how to approach it.</li>
  </ul>

  <h2>How to get started</h2>
  <ol>
    <li>Email us a short description of your project and what you want to achieve.</li>
    <li>We will propose suitable pages, format, timing and price.</li>
    <li>We agree on the materials and launch. Advertising is labelled “Advertisement”.</li>
  </ol>

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
