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
    t = re.sub(r'<title>.*?</title>', '<title>' + ('Реклама на Russian-TV.com — условия размещения' if ru else 'Advertise on Russian-TV.com') + '</title>', t, 1, flags=re.S)
    t = re.sub(r'(<meta name="description" content=")[^"]*', r'\g<1>' + ('Разместите рекламу на Russian-TV.com. Баннерные и партнёрские размещения для русскоязычной аудитории. Формат, сроки и стоимость — по запросу.' if ru else 'Advertise on Russian-TV.com. Banner and partner placements for a Russian-speaking audience. Format, timing and price on request.'), t, 1)
    t = t.replace('canonical" href="https://russian-tv.com/privacy/"', f'canonical" href="https://russian-tv.com/{slug}/"').replace('canonical" href="https://russian-tv.com/en/privacy/"', f'canonical" href="https://russian-tv.com/{slug}/"')
    t = re.sub(r'<link rel="alternate" hreflang="ru"[^>]*>', '<link rel="alternate" hreflang="ru" href="https://russian-tv.com/advertising/"/>', t)
    t = re.sub(r'<link rel="alternate" hreflang="en"[^>]*>', '<link rel="alternate" hreflang="en" href="https://russian-tv.com/en/advertising/"/>', t)
    t = re.sub(r'<link rel="alternate" hreflang="x-default"[^>]*>', '<link rel="alternate" hreflang="x-default" href="https://russian-tv.com/advertising/"/>', t)
    if ru:
        crumbs = '<a href="/">Главная</a><span>›</span><span>Рекламодателям</span>'
        body = f'''<div class="wrap">
  <h1>Реклама на Russian-TV.com</h1>
  <p class="updated">Последнее обновление: 9 октября 2026 г.</p>

  <h2>Расскажите о своём бренде русскоязычной аудитории</h2>
  <p><strong>Russian-TV.com</strong> — бесплатный онлайн-сервис для просмотра российских телеканалов. Мы предлагаем рекламодателям возможность представить свои товары, услуги и проекты аудитории, которая выбирает онлайн-телевидение.</p>
  <p>Мы открыты к сотрудничеству с компаниями, рекламными агентствами и владельцами интересных проектов. Подберём формат размещения с учётом ваших целей, рекламного бюджета и особенностей предложения.</p>

  <h2>Форматы сотрудничества</h2>
  <ul>
    <li><strong>Баннерная реклама</strong> — рекламные баннеры и графические материалы в доступных рекламных блоках сайта.</li>
    <li><strong>Размещение на отдельных страницах</strong> — главная страница, страницы телеканалов и тематические разделы, в зависимости от доступных рекламных позиций.</li>
    <li><strong>Партнёрские и текстовые размещения</strong> — рекламные публикации и информационные материалы, если они соответствуют тематике сайта и формату площадки.</li>
    <li><strong>Индивидуальные решения</strong> — есть собственная идея или нестандартная задача? Расскажите нам о ней, обсудим варианты.</li>
  </ul>

  <h2>Стоимость размещения</h2>
  <p>Мы подбираем условия индивидуально, а не ограничиваемся фиксированными рекламными пакетами. Стоимость зависит от формата, места и срока размещения, а также объёма кампании. После получения запроса мы предложим подходящие варианты и согласуем стоимость до начала размещения.</p>
  <p>Можно обсудить как отдельное размещение для проверки эффективности, так и долгосрочное сотрудничество.</p>

  <h2>Как разместить рекламу</h2>
  <ol>
    <li>Напишите нам и расскажите о своей компании, продукте или услуге.</li>
    <li>Укажите желаемый формат рекламы, сроки и ориентировочный бюджет, если он уже определён.</li>
    <li>Мы рассмотрим запрос, предложим доступные варианты и согласуем условия. Рекламные материалы отмечаются пометкой «Реклама».</li>
  </ol>

  <h2>Обсудим ваше предложение?</h2>
  <p>Свяжитесь с нами по вопросам размещения рекламы: <a href="mailto:{MAIL}?subject=Реклама%20на%20russian-tv.com"><strong>{MAIL}</strong></a></p>
  <p>Будем рады обсудить сотрудничество и подобрать подходящий формат для вашего проекта.</p>
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

  <h2>Tell a Russian-speaking audience about your brand</h2>
  <p><strong>Russian-TV.com</strong> is a free online service for watching Russian TV channels. We let advertisers present their products, services and projects to an audience that chooses online television.</p>
  <p>We are open to working with companies, advertising agencies and owners of interesting projects. We will choose a placement format that fits your goals, budget and offer.</p>

  <h2>Ways to work together</h2>
  <ul>
    <li><strong>Banner advertising</strong> — banners and graphic materials in the site's available ad blocks.</li>
    <li><strong>Placement on specific pages</strong> — the homepage, channel pages and category sections, depending on available ad positions.</li>
    <li><strong>Partner and text placements</strong> — sponsored publications and informational materials that fit the site's topics and format.</li>
    <li><strong>Custom solutions</strong> — have your own idea or an unusual goal? Tell us about it and we will discuss options.</li>
  </ul>

  <h2>Pricing</h2>
  <p>We set terms individually rather than relying on fixed ad packages. The price depends on the format, position and duration of the placement and the size of the campaign. After receiving your request we will propose suitable options and agree on the price before the placement starts.</p>
  <p>You can start with a single test placement or discuss long-term cooperation.</p>

  <h2>How to advertise</h2>
  <ol>
    <li>Email us and tell us about your company, product or service.</li>
    <li>Specify the desired format, timing and approximate budget, if already set.</li>
    <li>We will review the request, propose available options and agree on terms. Advertising is labelled “Advertisement”.</li>
  </ol>

  <h2>Shall we discuss your proposal?</h2>
  <p>Contact us about advertising: <a href="mailto:{MAIL}?subject=Advertising%20on%20russian-tv.com"><strong>{MAIL}</strong></a></p>
  <p>We will be glad to discuss cooperation and find a suitable format for your project.</p>
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
