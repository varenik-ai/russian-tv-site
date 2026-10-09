#!/usr/bin/env python3
"""Новые статьи блога (RU+EN), индексы блога. Идемпотентно."""
import sys, os, re, json, html
ROOT = sys.argv[1]
def rd(p): return open(os.path.join(ROOT, p), encoding='utf-8').read()
def wr(p, s):
    os.makedirs(os.path.dirname(os.path.join(ROOT, p)), exist_ok=True)
    open(os.path.join(ROOT, p), 'w', encoding='utf-8').write(s)
def esc(s): return html.escape(s, quote=True)
DATE = '2026-10-09'
TOTAL = 58

RU_T = rd('blog/kak-smotret-russkoe-tv-na-smart-tv/index.html')
EN_T = rd('en/blog/how-to-watch-russian-tv-in-usa/index.html')

def head(tpl, lang, slug_path, title, desc, headline, crumbs, faq, alt=None):
    h = tpl[:tpl.find('</head>')]
    url = f'https://russian-tv.com/{slug_path}/'
    h = re.sub(r'<title>.*?</title>', f'<title>{esc(title)}</title>', h, 1, flags=re.S)
    h = re.sub(r'(<meta name="description" content=")[^"]*', lambda m: m.group(1) + esc(desc), h, 1)
    h = re.sub(r'(<link rel="canonical" href=")[^"]*', lambda m: m.group(1) + url, h, 1)
    h = re.sub(r'(<meta property="og:title" content=")[^"]*', lambda m: m.group(1) + esc(headline), h, 1)
    h = re.sub(r'(<meta property="og:description" content=")[^"]*', lambda m: m.group(1) + esc(desc), h, 1)
    h = re.sub(r'(<meta property="og:url" content=")[^"]*', lambda m: m.group(1) + url, h, 1)
    inl = 'ru-RU' if lang == 'ru' else 'en'
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Article", "headline": headline, "description": desc,
         "author": {"@type": "Organization", "name": "Русское ТВ" if lang == 'ru' else "Russian TV", "url": "https://russian-tv.com"},
         "publisher": {"@type": "Organization", "name": "Русское ТВ" if lang == 'ru' else "Russian TV", "url": "https://russian-tv.com"},
         "mainEntityOfPage": url, "datePublished": DATE, "dateModified": DATE, "inLanguage": inl,
         "image": "https://russian-tv.com/og-image.jpg"},
        {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(crumbs)]},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub(r'<[^>]+>', '', a)}} for q, a in faq]},
    ]}
    h = re.sub(r'<script type="application/ld\+json">.*?</script>', lambda m: '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False, indent=2) + '</script>', h, 1, flags=re.S)
    if alt:
        ru_u, en_u = alt
        links = (f'  <link rel="alternate" hreflang="ru" href="{ru_u}"/>\n  <link rel="alternate" hreflang="en" href="{en_u}"/>\n  <link rel="alternate" hreflang="x-default" href="{ru_u}"/>\n')
        h = h.replace(f'<link rel="canonical" href="{url}"/>\n', f'<link rel="canonical" href="{url}"/>\n' + links, 1)
    return h + '</head>\n'

def tail_of(tpl):
    b = tpl[tpl.find('<body'):]
    return b

def faq_html(faq, lang):
    return ''.join(f'\n    <details{" open" if i == 0 else ""}>\n      <summary>{esc(q)} <span>▾</span></summary>\n      <p>{a}</p>\n    </details>' for i, (q, a) in enumerate(faq))

# ================= RU =================
def ru_article(slug, title, desc, headline, crumb_name, meta, h1, body, faq, related, alt=None):
    tpl = RU_T
    hd = head(tpl, 'ru', f'blog/{slug}', title, desc, headline,
              [('Главная', 'https://russian-tv.com/'), ('Блог', 'https://russian-tv.com/blog/'), (crumb_name, f'https://russian-tv.com/blog/{slug}/')], faq, alt)
    b = tpl[tpl.find('<body'):]
    i = b.find('<div class="breadcrumb">'); j = b.find('<div class="wrap">')
    pre = b[:i]
    k = b.find('<footer>')
    foot = b[k:]
    rel = ''.join(f'\n      <li><a href="{u}">{n}</a></li>' for n, u in related)
    art = f'''<div class="breadcrumb">
  <a href="/">Главная</a><span>›</span><a href="/blog/">Блог</a><span>›</span><span>{esc(crumb_name)}</span>
</div>
<div class="wrap">
  <div class="meta">{meta}</div>
  <h1>{esc(h1)}</h1>
{body}
  <h2>Часто задаваемые вопросы</h2>
  <div class="faq">{faq_html(faq, 'ru')}
  </div>

  <div class="cta" style="margin-top:32px">
    <p>Смотрите {TOTAL} российских каналов — бесплатно, без VPN</p>
    <a href="/">▶ Открыть russian-tv.com</a>
  </div>

  <div style="background:var(--bg2);border:1px solid var(--border);border-radius:var(--radius);padding:18px;margin-top:20px">
    <p style="color:var(--text);font-weight:700;margin-bottom:10px">Читайте также</p>
    <ul style="margin:0;padding-left:18px">{rel}
    </ul>
  </div>
</div>
'''
    wr(f'blog/{slug}/index.html', hd + pre + art + foot)

RU_ARTICLES = [
 dict(slug='kak-smotret-russkoe-tv-na-iphone-i-android',
  title='Как смотреть российское ТВ на iPhone и Android без приложения — 2026',
  desc='Как смотреть российские телеканалы на iPhone и Android прямо в браузере: без приложений, без VPN и регистрации. Советы по Safari, Chrome и Telegram.',
  headline='Российское ТВ на iPhone и Android без приложения — пошаговая инструкция',
  crumb='Российское ТВ на iPhone и Android', meta='<span>📅 Октябрь 2026</span><span>📱 iPhone и Android</span><span>⏱ 4 мин</span>',
  h1='Как смотреть российское ТВ на iPhone и Android без приложения',
  alt=('https://russian-tv.com/blog/kak-smotret-russkoe-tv-na-iphone-i-android/', 'https://russian-tv.com/en/blog/russian-tv-on-iphone-and-android/'),
  body='''  <p>Чтобы смотреть российские каналы на телефоне, не нужно ничего устанавливать: сайт <a href="/">russian-tv.com</a> работает прямо в мобильном браузере. Откройте сайт, выберите канал и нажмите ▶.</p>

  <div class="step-box">
    <h3>iPhone и iPad (Safari)</h3>
    <ol>
      <li>Откройте <strong>Safari</strong> и перейдите на <strong>russian-tv.com</strong></li>
      <li>Выберите канал — например, <a href="/ntv-live/">НТВ</a> или <a href="/rossiya-24-live/">Россия 24</a></li>
      <li>Нажмите ▶ в плеере. Для полного экрана используйте кнопку ⛶ в плеере</li>
      <li>Чтобы вернуться к каналу одним касанием: «Поделиться» → «На экран Домой»</li>
    </ol>
  </div>

  <div class="step-box">
    <h3>Android (Chrome)</h3>
    <ol>
      <li>Откройте <strong>Chrome</strong> и перейдите на <strong>russian-tv.com</strong></li>
      <li>Выберите канал и нажмите ▶</li>
      <li>Чтобы добавить сайт на главный экран: ⋮ → «Добавить на главный экран»</li>
    </ol>
  </div>

  <h2>Через Telegram</h2>
  <p>Если вы пользуетесь Telegram, откройте мини-приложение из канала <a href="https://t.me/RussiaTV_Hub_Live" target="_blank" rel="noopener">@RussiaTV_Hub_Live</a>: каналы сгруппированы по темам, а переключаться между ними удобно одним касанием.</p>

  <h2>Советы для комфортного просмотра</h2>
  <ul>
    <li><strong>Wi-Fi лучше мобильного интернета:</strong> видео потребляет заметный трафик, особенно в HD.</li>
    <li><strong>Если звук не включился,</strong> нажмите на значок звука в плеере: браузеры иногда запускают видео без звука.</li>
    <li><strong>Перевернуть экран:</strong> для просмотра на весь экран удобнее горизонтальная ориентация.</li>
    <li><strong>Нет движения кадра?</strong> Обновите страницу или переключитесь на другой канал и вернитесь — подробности в статье <a href="/blog/kanal-ne-gruzitsya-chto-delat/">«Канал не грузится: что делать»</a>.</li>
  </ul>

  <div class="highlight"><p>💡 Все трансляции взяты из открытых источников; сайт не хранит видео. Список каналов по темам: <a href="/blog/kakie-kanaly-smotret-po-temam/">какие каналы смотреть</a>.</p></div>
''',
  faq=[('Нужно ли устанавливать приложение?', 'Нет. Сайт работает в браузере Safari или Chrome. Дополнительно есть мини-приложение в Telegram.'),
       ('Нужен ли VPN на телефоне?', 'Нет, VPN не требуется. Достаточно обычного интернета.'),
       ('Как добавить сайт на главный экран?', 'На iPhone: «Поделиться» → «На экран Домой». На Android (Chrome): меню ⋮ → «Добавить на главный экран».')],
  related=[('Как смотреть российское ТВ на Smart TV', '/blog/kak-smotret-russkoe-tv-na-smart-tv/'), ('Какие каналы смотреть по темам', '/blog/kakie-kanaly-smotret-po-temam/'), ('Канал не грузится: что делать', '/blog/kanal-ne-gruzitsya-chto-delat/')]),

 dict(slug='kakie-kanaly-smotret-po-temam',
  title='Какие российские каналы смотреть онлайн: подборка по темам — 2026',
  desc='Российские телеканалы онлайн по темам: новости, кино, развлечения, детские, музыка и радио, хобби и спорт. Куда нажать, чтобы смотреть бесплатно без VPN.',
  headline='Какие российские каналы смотреть онлайн — подборка по темам',
  crumb='Каналы по темам', meta='<span>📅 Октябрь 2026</span><span>📺 Каналы</span><span>⏱ 4 мин</span>',
  h1='Какие российские каналы смотреть онлайн: подборка по темам',
  body='''  <p>На <a href="/">russian-tv.com</a> собрано {total} российских каналов в прямом эфире. Чтобы не потеряться в списке, ниже — подборка по темам со ссылками на каждый канал.</p>

  <h2>Новости</h2>
  <p><a href="/perviy-kanal-live/">Первый канал</a>, <a href="/rossiya-1-live/">Россия 1</a>, <a href="/ntv-live/">НТВ</a>, <a href="/rossiya-24-live/">Россия 24</a>, <a href="/pyatyy-kanal-live/">Пятый канал</a>, <a href="/tv-centr-live/">ТВЦ</a>, <a href="/mir-live/">МИР</a>, <a href="/zvezda-live/">Звезда</a>, <a href="/kanal-360-live/">360°</a>, <a href="/moskva-24-live/">Москва 24</a>, <a href="/sankt-peterburg-live/">Санкт-Петербург</a>, <a href="/soloviev-live/">Соловьёв Live</a>. Все — в разделе <a href="/novosti/">Новости</a>.</p>

  <h2>Кино</h2>
  <p><a href="/dom-kino-live/">Дом Кино</a>, <a href="/kinohit-live/">Кинохит</a>, <a href="/kinokomediya-live/">Кинокомедия</a>, <a href="/viju-tv-live/">Viju TV1000</a>, <a href="/kino-detektiv-live/">Viju TV1000 Русское кино</a>, <a href="/nashe-kino-live/">Наше кино</a>, <a href="/rodnoe-kino-live/">Родное кино</a>, <a href="/kinosvidanie-live/">Кинoсвидание</a>, <a href="/indiyskoekino-live/">Индийское кино</a>, <a href="/kino-ekshn-live/">Кино Экшн</a>, <a href="/chestnyy-detektiv-live/">Честный детектив</a>. Раздел: <a href="/kino/">Кино</a>.</p>

  <h2>Развлечения и познавательное</h2>
  <p><a href="/tnt-live/">ТНТ4</a>, <a href="/istoriya-live/">История</a>, <a href="/prima-live/">Прима</a>, <a href="/soyuz-live/">Союз</a>, <a href="/rt-documentary-live/">RT Documentary</a>. Раздел: <a href="/razvlecheniya/">Развлечения</a>.</p>

  <h2>Детям</h2>
  <p><a href="/karusel-live/">Карусель</a>, <a href="/karusel-international-live/">Карусель International</a>, <a href="/mult-live/">Мульт</a>, <a href="/ryzhiy-live/">Рыжий</a>. Раздел: <a href="/detskie/">Детские</a>.</p>

  <h2>Музыка и радио</h2>
  <p><a href="/muz-tv-live/">МУЗ-ТВ</a>, <a href="/muzyka-pervogo-live/">Музыка Первого</a>, <a href="/muz-soyuz-live/">Муз Союз</a>, <a href="/fon-music-live/">FON Music</a>, а также радио <a href="/strana-fm-live/">Страна FM</a> и <a href="/vesti-fm-live/">Вести FM</a>. Раздел: <a href="/muzyka/">Музыка</a>.</p>

  <h2>Хобби, природа и путешествия</h2>
  <p><a href="/ohota-i-rybalka-live/">Охота и рыбалка</a>, <a href="/moy-mir-live/">Мой мир</a>, <a href="/priklyucheniya-live/">Приключения</a>, <a href="/tochka-otryva-live/">Точка отрыва</a>, <a href="/zhivaya-planeta-live/">Живая планета</a>, <a href="/zoopark-live/">Зоопарк</a>, <a href="/domashnie-zhivotnye-live/">Домашние животные</a>, <a href="/drive-live/">Драйв</a>, <a href="/zdorovoe-tv-live/">Здоровое ТВ</a>, <a href="/bolshaya-planeta-live/">Большая планета</a>, <a href="/bober-live/">Бобер</a>. Раздел: <a href="/hobbi/">Хобби</a>.</p>

  <h2>Спорт</h2>
  <p><a href="/flosports-hockey-live/">FloSports Hockey</a>, <a href="/flosports-racing-live/">FloSports Racing</a>, <a href="/viju-sport-live/">Viju+ Sport</a>, <a href="/m1-mma-live/">M1 Global MMA</a>, <a href="/red-bull-tv-live/">Red Bull TV</a>, <a href="/unbeaten-boxing-live/">Unbeaten Boxing</a>, <a href="/world-freesports-live/">World of Freesports</a>, <a href="/sportivnyy-live/">Спортивный</a>, <a href="/trace-sport-stars-live/">Trace Sport Stars</a>. Раздел: <a href="/sport/">Спорт</a>.</p>

  <div class="highlight"><p>💡 Не знаете, с чего начать? Откройте раздел «Новости» или «Кино» — это самые популярные категории. Если канал не запускается, переключитесь на другой и вернитесь через минуту.</p></div>
'''.replace('{total}', str(TOTAL)),
  faq=[('Сколько каналов доступно на сайте?', f'Сейчас на сайте {TOTAL} российских каналов в семи категориях: новости, развлечения, кино, детские, музыка, хобби и спорт.'),
       ('Все ли каналы бесплатные?', 'Да, все каналы доступны бесплатно, без регистрации и без подписки.'),
       ('Есть ли радио?', 'Да, в разделе «Музыка» доступны радиостанции Страна FM и Вести FM. Видеоряда у радио может не быть.')],
  related=[('Российское ТВ на iPhone и Android', '/blog/kak-smotret-russkoe-tv-na-iphone-i-android/'), ('Первый канал, Россия 1 и НТВ — в чём разница', '/blog/pervyy-kanal-rossiya-1-ntv-v-chem-raznica/'), ('Где смотреть спорт на русских каналах', '/blog/gde-smotret-futbol-i-sport-na-russkih-kanalah/')]),

 dict(slug='kanal-ne-gruzitsya-chto-delat',
  title='Канал не грузится или зависает: 8 способов исправить — 2026',
  desc='Российский канал онлайн не загружается или зависает? 8 простых способов исправить: обновить страницу, сменить канал, проверить сеть, браузер и VPN.',
  headline='Канал не грузится или зависает: 8 способов исправить',
  crumb='Канал не грузится', meta='<span>📅 Октябрь 2026</span><span>🛠 Решение проблем</span><span>⏱ 3 мин</span>',
  h1='Канал не грузится или зависает: что делать',
  alt=('https://russian-tv.com/blog/kanal-ne-gruzitsya-chto-delat/', 'https://russian-tv.com/en/blog/channel-not-loading-fix/'),
  body='''  <p>Прямые трансляции идут от сторонних источников, поэтому иногда канал может запускаться дольше или подвисать. Вот что обычно помогает.</p>

  <div class="step-box">
    <ol>
      <li><strong>Подождите 10–20 секунд.</strong> Плеер сам переключается между несколькими серверами, это занимает время.</li>
      <li><strong>Обновите страницу</strong> (или нажмите кнопку перезагрузки в плеере).</li>
      <li><strong>Переключитесь на другой канал и вернитесь</strong> через минуту — источник мог временно перегрузиться.</li>
      <li><strong>Проверьте интернет.</strong> Для HD нужно около 5 Мбит/с; на мобильной сети попробуйте перейти на Wi-Fi.</li>
      <li><strong>Выключите VPN или смените сервер VPN.</strong> Сайт работает без VPN, а некоторые VPN замедляют видео.</li>
      <li><strong>Обновите браузер</strong> (Chrome, Safari, Firefox, Edge) до последней версии.</li>
      <li><strong>Отключите блокировщики рекламы</strong> для сайта, если трансляция не стартует: они иногда блокируют служебные запросы плеера.</li>
      <li><strong>Попробуйте другое устройство или браузер.</strong> Если на телефоне не работает, проверьте на компьютере.</li>
    </ol>
  </div>

  <h2>Если зависает только один канал</h2>
  <p>Это значит, что временно проблемы у источника этого канала. Подождите несколько минут или посмотрите похожий канал из той же темы — каналы по темам собраны в <a href="/blog/kakie-kanaly-smotret-po-temam/">подборке</a>.</p>

  <h2>Если хотите сообщить о проблеме</h2>
  <p>Напишите в Telegram-канал <a href="https://t.me/RussiaTV_Hub_Live" target="_blank" rel="noopener">@RussiaTV_Hub_Live</a> с названием канала и описанием проблемы.</p>
''',
  faq=[('Почему канал зависает?', 'Трансляции идут от сторонних источников. Иногда источник перегружен или временно недоступен — тогда помогает обновление страницы или подождать несколько минут.'),
       ('Нужен ли VPN?', 'Нет, сайт работает без VPN. Если VPN включён и видео тормозит, попробуйте его отключить.'),
       ('Какая скорость интернета нужна?', 'Для комфортного просмотра в HD рекомендуем от 5 Мбит/с.')],
  related=[('Российское ТВ на iPhone и Android', '/blog/kak-smotret-russkoe-tv-na-iphone-i-android/'), ('Как смотреть российское ТВ на Smart TV', '/blog/kak-smotret-russkoe-tv-na-smart-tv/'), ('Какие каналы смотреть по темам', '/blog/kakie-kanaly-smotret-po-temam/')]),
]
for a in RU_ARTICLES:
    ru_article(a['slug'], a['title'], a['desc'], a['headline'], a['crumb'], a['meta'], a['h1'], a['body'], a['faq'], a['related'], a.get('alt'))

# ================= EN =================
def en_article(slug, title, desc, headline, crumb_name, meta, h1, body, faq, related, alt=None):
    tpl = EN_T
    hd = head(tpl, 'en', f'en/blog/{slug}', title, desc, headline,
              [('Home', 'https://russian-tv.com/en/'), ('Blog', 'https://russian-tv.com/en/blog/'), (crumb_name, f'https://russian-tv.com/en/blog/{slug}/')], faq, alt)
    b = tpl[tpl.find('<body'):]
    i = b.find('<div class="breadcrumb">')
    pre = b[:i]; foot = b[b.find('<footer>'):]
    rel = ''.join(f'\n      <li><a href="{u}">{n}</a></li>' for n, u in related)
    art = f'''<div class="breadcrumb">
  <a href="/en/">Home</a><span>›</span><a href="/en/blog/">Blog</a><span>›</span>
  <span>{esc(crumb_name)}</span>
</div>

<div class="article-wrap">
  <div class="article-meta">{meta}</div>

  <h1>{esc(h1)}</h1>
{body}
  <h2>Frequently Asked Questions</h2>
  <div class="faq">{faq_html(faq, 'en')}
  </div>

  <div class="cta-box" style="margin-top:36px">
    <p>Ready to watch? {TOTAL} Russian channels — free, no VPN</p>
    <a href="/en/">▶ Open russian-tv.com</a>
  </div>

  <div class="related-links">
    <h3>Related pages</h3>
    <ul>{rel}
    </ul>
  </div>
</div>

'''
    wr(f'en/blog/{slug}/index.html', hd + pre + art + foot)

EN_ARTICLES = [
 dict(slug='russian-tv-on-iphone-and-android',
  title='How to Watch Russian TV on iPhone and Android Without an App — 2026',
  desc='Watch Russian TV channels on iPhone and Android right in your browser — no app, no VPN, no registration. Tips for Safari, Chrome and Telegram.',
  headline='Russian TV on iPhone and Android — no app needed',
  crumb='Russian TV on iPhone and Android', meta='<span>📅 October 2026</span><span>📱 iPhone & Android</span><span>⏱ 4 min read</span>',
  h1='How to Watch Russian TV on iPhone and Android Without an App',
  alt=('https://russian-tv.com/blog/kak-smotret-russkoe-tv-na-iphone-i-android/', 'https://russian-tv.com/en/blog/russian-tv-on-iphone-and-android/'),
  body='''  <p>You don't need to install anything to watch Russian channels on your phone: <a href="/en/">russian-tv.com</a> works right in the mobile browser. Open the site, pick a channel and press ▶.</p>

  <h2>iPhone and iPad (Safari)</h2>
  <ol>
    <li>Open <strong>Safari</strong> and go to <strong>russian-tv.com</strong></li>
    <li>Pick a channel — for example <a href="/en/ntv-live/">NTV</a> or <a href="/en/rossiya-24-live/">Rossiya 24</a></li>
    <li>Press ▶ in the player; use ⛶ for full screen</li>
    <li>To open it with one tap: Share → Add to Home Screen</li>
  </ol>

  <h2>Android (Chrome)</h2>
  <ol>
    <li>Open <strong>Chrome</strong> and go to <strong>russian-tv.com</strong></li>
    <li>Pick a channel and press ▶</li>
    <li>To add the site to your home screen: ⋮ → Add to Home screen</li>
  </ol>

  <h2>Via Telegram</h2>
  <p>If you use Telegram, open the mini-app from the channel <a href="https://t.me/RussiaTV_Hub_Live" target="_blank" rel="noopener">@RussiaTV_Hub_Live</a>: channels are grouped by topic and switching is one tap.</p>

  <h2>Tips for smooth playback</h2>
  <ul>
    <li><strong>Wi-Fi is better than mobile data:</strong> video uses a lot of traffic, especially in HD.</li>
    <li><strong>No sound?</strong> Tap the speaker icon in the player — browsers sometimes start video muted.</li>
    <li><strong>Rotate your phone</strong> for full-screen viewing.</li>
    <li><strong>Frozen picture?</strong> Reload the page or switch channels and come back — see <a href="/en/blog/channel-not-loading-fix/">Channel not loading: how to fix it</a>.</li>
  </ul>
''',
  faq=[('Do I need to install an app?', 'No. The site works in Safari or Chrome. There is also an optional Telegram mini-app.'),
       ('Do I need a VPN on my phone?', 'No. A regular internet connection is enough.'),
       ('How do I add the site to my home screen?', 'iPhone: Share → Add to Home Screen. Android (Chrome): ⋮ menu → Add to Home screen.')],
  related=[('Watch Russian channels by topic', '/en/news/'), ('Movies channels', '/en/movies/'), ('Channel not loading: how to fix it', '/en/blog/channel-not-loading-fix/')]),
 dict(slug='channel-not-loading-fix',
  title='Russian TV Channel Not Loading or Freezing? 8 Fixes — 2026',
  desc='Russian channel online not loading or freezing? 8 simple fixes: reload, switch channel, check your connection, browser and VPN.',
  headline='Russian TV channel not loading or freezing — 8 fixes',
  crumb='Channel not loading', meta='<span>📅 October 2026</span><span>🛠 Troubleshooting</span><span>⏱ 3 min read</span>',
  h1='Russian TV Channel Not Loading or Freezing: What to Do',
  alt=('https://russian-tv.com/blog/kanal-ne-gruzitsya-chto-delat/', 'https://russian-tv.com/en/blog/channel-not-loading-fix/'),
  body='''  <p>Live streams come from third-party sources, so a channel may sometimes start slowly or freeze. This usually helps:</p>
  <ol>
    <li><strong>Wait 10–20 seconds.</strong> The player switches between several servers on its own.</li>
    <li><strong>Reload the page</strong> (or use the reload button in the player).</li>
    <li><strong>Switch to another channel and come back</strong> in a minute — the source may be temporarily overloaded.</li>
    <li><strong>Check your connection.</strong> HD needs about 5 Mbit/s; on mobile data try Wi-Fi.</li>
    <li><strong>Turn VPN off or change the VPN server.</strong> The site works without a VPN, and some VPNs slow video down.</li>
    <li><strong>Update your browser</strong> (Chrome, Safari, Firefox, Edge).</li>
    <li><strong>Disable ad blockers</strong> for the site if the stream does not start — they sometimes block the player's service requests.</li>
    <li><strong>Try another device or browser.</strong> If it fails on your phone, check on a computer.</li>
  </ol>

  <h2>If only one channel freezes</h2>
  <p>That means the source of this particular channel has a temporary problem. Wait a few minutes or watch a similar channel from the same topic: <a href="/en/news/">News</a>, <a href="/en/movies/">Movies</a>, <a href="/en/entertainment/">Entertainment</a>, <a href="/en/kids/">Kids</a>, <a href="/en/music/">Music</a>, <a href="/en/hobby/">Hobby</a>, <a href="/en/sport/">Sport</a>.</p>

  <h2>Report a problem</h2>
  <p>Write to the Telegram channel <a href="https://t.me/RussiaTV_Hub_Live" target="_blank" rel="noopener">@RussiaTV_Hub_Live</a> with the channel name and a short description.</p>
''',
  faq=[('Why does a channel freeze?', 'Streams come from third-party sources. Sometimes a source is overloaded or temporarily unavailable — reloading or waiting a few minutes helps.'),
       ('Do I need a VPN?', 'No, the site works without a VPN. If a VPN is on and video lags, try turning it off.'),
       ('What internet speed do I need?', 'We recommend at least 5 Mbit/s for comfortable HD viewing.')],
  related=[('Russian TV on iPhone and Android', '/en/blog/russian-tv-on-iphone-and-android/'), ('How to Watch Russian TV in the USA', '/en/blog/how-to-watch-russian-tv-in-usa/'), ('All channels', '/en/')]),
]
for a in EN_ARTICLES:
    en_article(a['slug'], a['title'], a['desc'], a['headline'], a['crumb'], a['meta'], a['h1'], a['body'], a['faq'], a['related'], a.get('alt'))

# ================= индексы блога =================
idx = rd('blog/index.html')
if 'kakie-kanaly-smotret-po-temam' not in idx:
    cards = ''
    for a in RU_ARTICLES:
        cards += (f'    <a href="/blog/{a["slug"]}/" class="post-card">\n      <div class="post-date">Октябрь 2026</div>\n      <div class="post-title">{esc(a["h1"])}</div>\n      <div class="post-excerpt">{esc(a["desc"])}</div>\n    </a>\n')
    idx = idx.replace('<div class="post-list">\n', '<div class="post-list">\n' + cards, 1)
    wr('blog/index.html', idx)

# EN индекс блога на базе RU индекса
en_idx = idx
en_idx = re.sub(r'<html lang="ru"', '<html lang="en"', en_idx)
body_start = en_idx.find('<body')
posts = [('how-to-watch-russian-tv-in-usa', 'September 2026', 'How to Watch Russian TV in the USA for Free in 2026', 'Step-by-step guide to watching Russian TV channels online in the USA for free. No VPN, no subscription.')] + \
        [(a['slug'], 'October 2026', a['h1'], a['desc']) for a in EN_ARTICLES]
cards = ''.join(f'    <a href="/en/blog/{s}/" class="post-card">\n      <div class="post-date">{d}</div>\n      <div class="post-title">{esc(t)}</div>\n      <div class="post-excerpt">{esc(x)}</div>\n    </a>\n' for s, d, t, x in posts)
head_part = en_idx[:body_start]
head_part = re.sub(r'<title>.*?</title>', '<title>Russian TV Blog — Guides and Tips | Russian-TV.com</title>', head_part, 1, flags=re.S)
head_part = re.sub(r'(<meta name="description" content=")[^"]*', r'\1Guides, tips and articles about watching Russian television online — at home and abroad.', head_part, 1)
head_part = re.sub(r'(<link rel="canonical" href=")[^"]*', r'\1https://russian-tv.com/en/blog/', head_part, 1)
head_part = re.sub(r'<script type="application/ld\+json">.*?</script>', '', head_part, flags=re.S)
head_part = re.sub(r'(<meta property="og:(?:title|description)" content=")[^"]*', lambda m: m.group(1) + ('Russian TV Blog' if 'title' in m.group(0) else 'Guides, tips and articles about watching Russian television online.'), head_part)
head_part = re.sub(r'(<meta property="og:url" content=")[^"]*', r'\1https://russian-tv.com/en/blog/', head_part)
head_part = head_part.replace('property="og:locale" content="ru_RU"', 'property="og:locale" content="en_US"')
head_part = head_part.replace('<link rel="canonical" href="https://russian-tv.com/en/blog/"/>', '<link rel="canonical" href="https://russian-tv.com/en/blog/"/>\n  <link rel="alternate" hreflang="ru" href="https://russian-tv.com/blog/"/>\n  <link rel="alternate" hreflang="en" href="https://russian-tv.com/en/blog/"/>\n  <link rel="alternate" hreflang="x-default" href="https://russian-tv.com/blog/"/>', 1)
foot_nav = ('<footer>\n  <div>🇷🇺 <a href="/en/">Russian TV</a> — free Russian TV online</div>\n  <div style="margin-top:6px">\n    <a href="/en/">All channels</a>\n    <a href="/en/blog/">Blog</a>\n    <a href="/en/privacy/">Privacy Policy</a>\n    <a href="https://t.me/RussiaTV_Hub_Live" target="_blank">Telegram</a>\n  </div>\n  <div class="legal-note" style="text-align:center;margin:10px auto 0;max-width:760px;padding:0 12px;font-size:11px;line-height:1.5;color:#8b8ba0">Stream links are taken from publicly available sources. At the request of a rights holder, a stream will be removed after proof of rights ownership is provided — <a href="/en/privacy/#rightsholders" style="color:inherit;text-decoration:underline">details</a>. · <a href="/en/advertising/" style="color:inherit;text-decoration:underline">Advertise with us</a></div>\n</footer>\n</body>\n</html>\n')
bd = en_idx[body_start:en_idx.find('<footer>')]
bd = re.sub(r'<div class="post-list">.*?</div>\s*</div>\s*$', lambda m: '<div class="post-list">\n' + cards + '  </div>\n</div>\n\n', bd, 1, flags=re.S)
bd = bd.replace('<a href="/" class="logo"><span style="font-size:26px">🇷🇺</span><span class="logo-text"><span class="r">Рус</span><span class="w">ское</span></span><span class="b">ТВ</span></a>', '<a href="/en/" class="logo"><span style="font-size:26px">🇷🇺</span><span class="logo-text"><span class="r">Rus</span><span class="w">sian</span></span><span class="b">TV</span></a>')
bd = bd.replace('Подписаться', 'Subscribe').replace('<a href="/">Главная</a><span>›</span>\n  <span>Блог</span>', '<a href="/en/">Home</a><span>›</span>\n  <span>Blog</span>')
bd = bd.replace('<h1>Блог о русском ТВ</h1>', '<h1>Russian TV Blog</h1>').replace('Гайды, инструкции и статьи о просмотре российского телевидения — дома и за границей.', 'Guides, tips and articles about watching Russian television online — at home and abroad.')
wr('en/blog/index.html', head_part + bd + foot_nav)
print('blog done')
