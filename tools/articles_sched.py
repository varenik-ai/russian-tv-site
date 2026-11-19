# Статья «Московское время в часовых поясах США» (RU + EN), 19.11.2026. Таблицы считаются кодом: Москва UTC+3 круглый год,
# США: ET/CT/MT/PT = UTC-5/-6/-7/-8 зимой и -4/-5/-6/-7 летом (перевод: 1 ноября 2026 назад, 14 марта 2027 вперёд, 7 ноября 2027 назад).
# Время передач в статье не приводится: сетка меняется, актуальная — в блоке «Программа на сегодня» на странице канала (показывает время в поясе устройства).
import json
def _fmt(h, en):
    d = ''
    if h < 0: h += 24; d = 'prev' 
    elif h >= 24: h -= 24; d = 'next'
    if en:
        ap = 'am' if h < 12 else 'pm'; hh = h % 12 or 12
        s = f'{hh}:00 {ap}'
    else:
        s = f'{h}:00'
    if d == 'prev': s += ' <span style="color:var(--muted);font-size:12px">(' + ('previous day' if en else 'накануне') + ')</span>'
    if d == 'next': s += ' <span style="color:var(--muted);font-size:12px">(' + ('next day' if en else 'на следующий день') + ')</span>'
    return s
HOURS = [6, 9, 12, 15, 18, 20, 21, 22, 24]
def table(offs, en):
    hd = ('<th>Moscow time</th><th>Eastern (ET)</th><th>Central (CT)</th><th>Mountain (MT)</th><th>Pacific (PT)</th>' if en else
          '<th>Время в Москве</th><th>Восточное (ET)</th><th>Центральное (CT)</th><th>Горное (MT)</th><th>Тихоокеанское (PT)</th>')
    rows = ''
    for m in HOURS:
        lab = ('00:00 (midnight)' if en else '00:00 (полночь)') if m == 24 else f'{m:02d}:00'
        rows += '<tr><td>' + lab + '</td>' + ''.join('<td>' + (('<strong>' + _fmt(m - 3 + o, en) + '</strong>') if m == 21 else _fmt(m - 3 + o, en)) + '</td>' for o in offs) + '</tr>\n      '
    return f'<table class="channel-table">\n    <thead>\n      <tr>{hd}</tr>\n    </thead>\n    <tbody>\n      {rows}</tbody>\n  </table>'
WIN, SUM = (-5, -6, -7, -8), (-4, -5, -6, -7)
US_ZONES = json.dumps([["New York / Miami", "America/New_York"], ["Chicago", "America/Chicago"], ["Denver", "America/Denver"], ["Phoenix", "America/Phoenix"],
                       ["Los Angeles", "America/Los_Angeles"], ["Anchorage", "America/Anchorage"], ["Honolulu", "Pacific/Honolulu"]], ensure_ascii=False).replace("'", '&#39;')
def conv(lang):
    return f'<div class="rtv-conv" data-lang="{lang}" data-default="21:00" data-zones=\'{US_ZONES}\'></div>\n  <script defer src="/assets/moscow-time.js?v=1"></script>'

SCHED_EN = dict(
  slug='moscow-time-to-us-time-zones-russian-tv-schedule',
  date='2026-11-19', date_label='November 2026',
  title='Moscow Time to EST, CST, MST, PST: Russian TV Schedule Guide',
  desc='Convert Moscow time to US time zones for Russian TV: tables for winter and summer, Arizona, Alaska and Hawaii, and how to find today\'s schedule.',
  headline='Moscow Time to US Time Zones — conversion tables and Russian TV schedule guide',
  crumb='Moscow time in US time zones', meta='<span>📅 Published: November 2026</span><span>🇺🇸 USA</span><span>⏱ 6 min read</span>',
  h1='Moscow Time to EST, CST, MST and PST: A Russian TV Schedule Guide for the USA',
  alt=('https://russian-tv.com/blog/vremya-po-moskve-v-chasovyh-pojasah-ssha/', 'https://russian-tv.com/en/blog/moscow-time-to-us-time-zones-russian-tv-schedule/'),
  body='''  <p><strong>Short answer:</strong> Moscow is <strong>8 hours ahead of New York in winter and 7 hours ahead in summer</strong> (9 and 8 for Chicago, 10 and 9 for Denver, 11 and 10 for Los Angeles). Moscow never changes its clocks (it is on UTC+3 all year); the US does, so the gap changes twice a year. The tables below convert the main hours, and the converter does any time for you.</p>

  <div class="cta-box">
    <p>📺 Watch Russian TV live in the USA — free, no VPN</p>
    <a href="/en/russian-tv-in-usa/">▶ Open Russian TV in the USA</a>
  </div>

  <h2>Why the gap changes</h2>
  <p>Russia abolished seasonal clock changes, so Moscow stays on UTC+3. The US moves to daylight saving time: the clocks went back on November 1, 2026 and go forward on March 14, 2027 (and back again on November 7, 2027). As a result, in the Eastern time zone the gap is 8 hours in winter (UTC−5) and 7 hours in summer (UTC−4); the other zones shift in the same way.</p>

  <h2>Winter table (early November to mid-March)</h2>
  <p>Valid now, until the clocks change on March 14, 2027. Moscow 21:00, the usual prime-time hour, is in bold.</p>

  ''' + table(WIN, True) + '''

  <h2>Summer table (mid-March to early November)</h2>
  <p>During US daylight saving time everything is one hour later than in the winter table (Moscow 21:00 becomes 2:00 pm Eastern).</p>

  ''' + table(SUM, True) + '''

  <h2>Exceptions: Arizona, Alaska, Hawaii</h2>
  <ul>
    <li><strong>Arizona (Phoenix)</strong> does not change its clocks and stays on UTC−7 all year (like Mountain time in winter): Moscow 21:00 is 11:00 am all year.</li>
    <li><strong>Alaska (Anchorage)</strong> is UTC−9 in winter and UTC−8 in summer: Moscow 21:00 is 9:00 am in winter and 10:00 am in summer.</li>
    <li><strong>Hawaii (Honolulu)</strong> does not change its clocks and stays on UTC−10 all year: Moscow 21:00 is 8:00 am all year.</li>
  </ul>

  <h2>Converter for any time</h2>
  <p>Enter a Moscow time and see the local time in each major US city. The converter uses today's date, so it follows winter and summer time on its own:</p>

  ''' + conv('en') + '''

  <h2>How to find today's schedule</h2>
  <p>Programme times change from season to season, so this article does not list them. The reliable way is the <strong>"Today's schedule"</strong> block on every channel page, for example on <a href="/en/perviy-kanal-live/">Perviy Kanal</a>, <a href="/en/rossiya-1-live/">Rossiya 1</a>, <a href="/en/ntv-live/">NTV</a> or <a href="/en/rossiya-24-live/">Rossiya 24</a>. The block shows the programme and a marker for what is on air now, and the times are displayed in <strong>your device's local time</strong>, so there is nothing to convert.</p>

  <h2>Planning your day: what the gap means</h2>
  <ul>
    <li><strong>Moscow evening = your lunch or midday.</strong> Prime time at 21:00 Moscow is 1:00 pm on the East Coast and 10:00 am on the West Coast in winter, so evening news and shows are daytime viewing in the USA.</li>
    <li><strong>Moscow morning = your night.</strong> Moscow 9:00 is 1:00 am Eastern in winter, so morning programmes are best skipped or watched in the repeat.</li>
    <li><strong>News at any hour.</strong> <a href="/en/rossiya-24-live/">Rossiya 24</a> broadcasts round the clock, so there is always something live.</li>
    <li><strong>Moscow midnight is afternoon.</strong> On December 31, Moscow midnight is 4:00 pm Eastern and 1:00 pm Pacific; see our <a href="/en/blog/russian-tv-new-years-eve-usa-uk-canada/">New Year's Eve guide</a>.</li>
    <li><strong>Watch the day marker.</strong> Early Moscow hours fall on the previous evening in the USA (see "previous day" in the tables), so check the date before you plan.</li>
  </ul>

  <h2>Which channel for which time</h2>
  <p>For daytime US viewing the main federal channels (<a href="/en/perviy-kanal-live/">Perviy Kanal</a>, <a href="/en/rossiya-1-live/">Rossiya 1</a>, <a href="/en/ntv-live/">NTV</a>) are on at your lunch hour. North America also has <a href="/en/rossiya-rtr-usa-live/">Rossiya RTR — USA</a>, a version of the Rossiya channel made for audiences abroad, whose schedule can differ from the domestic channel. If you are on a phone or a TV, see <a href="/en/blog/russian-tv-on-iphone-and-android/">Russian TV on iPhone and Android</a>, and for the basics read <a href="/en/blog/how-to-watch-russian-tv-in-usa/">How to Watch Russian TV in the USA for Free</a>.</p>

  <p><em>Schedules are set by the broadcasters and change. The tables are calculated from time-zone rules; check the channel page for the current programme.</em></p>
''',
  faq=[('What is the time difference between Moscow and New York?', 'Eight hours in winter (Moscow is UTC+3, New York is UTC−5) and seven hours in summer (New York is UTC−4). Moscow 9:00 pm is 1:00 pm in New York in winter and 2:00 pm in summer.'),
       ('When do the US clocks change in 2026 and 2027?', 'The clocks went back on November 1, 2026, and go forward on March 14, 2027. Moscow does not change its clocks.'),
       ('What time is Moscow 9:00 pm on the West Coast?', 'It is 10:00 am Pacific time in winter and 11:00 am in summer.'),
       ('Does Arizona change its clocks?', 'No. Arizona (except the Navajo Nation) stays on UTC−7 all year, so Moscow 21:00 is 11:00 am there in every season.'),
       ('Where can I see today\'s Russian TV programme in my local time?', 'On each channel page, the "Today\'s schedule" block shows the programme in your device\'s local time, with a marker for what is on air now.'),
       ('Do I need a VPN to watch Russian TV in the USA?', 'No. russian-tv.com works in the USA without a VPN, registration or an app.')],
  related=[('Russian TV in the USA', '/en/russian-tv-in-usa/'), ('How to Watch Russian TV in the USA', '/en/blog/how-to-watch-russian-tv-in-usa/'), ('Russian TV on New Year\'s Eve', '/en/blog/russian-tv-new-years-eve-usa-uk-canada/'), ('Russian TV in Canada', '/en/blog/how-to-watch-russian-tv-in-canada/'), ('Channel not loading: how to fix it', '/en/blog/channel-not-loading-fix/')],
)

SCHED_RU = dict(
  slug='vremya-po-moskve-v-chasovyh-pojasah-ssha',
  date='2026-11-19', date_label='Ноябрь 2026',
  title='Время по Москве в США: таблица EST, CST, MST, PST',
  desc='Московское время в часовых поясах США для российского ТВ: таблицы на зиму и лето, Аризона, Аляска, Гавайи и как найти программу на сегодня.',
  headline='Время по Москве в часовых поясах США — таблицы пересчёта и как смотреть программу',
  crumb='Время по Москве в США', meta='<span>📅 Ноябрь 2026</span><span>🇺🇸 США</span><span>⏱ 5 мин</span>',
  h1='Московское время в часовых поясах США: таблицы EST, CST, MST и PST для российского ТВ',
  alt=('https://russian-tv.com/blog/vremya-po-moskve-v-chasovyh-pojasah-ssha/', 'https://russian-tv.com/en/blog/moscow-time-to-us-time-zones-russian-tv-schedule/'),
  body='''  <p><strong>Коротко:</strong> Москва <strong>впереди Нью-Йорка на 8 часов зимой и на 7 часов летом</strong> (для Чикаго 9 и 8, для Денвера 10 и 9, для Лос-Анджелеса 11 и 10). Москва часы не переводит (UTC+3 круглый год), США переводят, поэтому разница меняется дважды в год. Таблицы ниже переводят основные часы, а конвертер посчитает любое время.</p>

  <div class="cta-box">
    <p>📺 Российское ТВ в США — бесплатно, без VPN</p>
    <a href="/russkie-kanaly-v-ssha/">▶ Открыть «Русское ТВ в США»</a>
  </div>

  <h2>Почему разница меняется</h2>
  <p>Россия отказалась от сезонного перевода часов, поэтому Москва всегда на UTC+3. США переходят на летнее время: часы перевели назад 1 ноября 2026 года и переведут вперёд 14 марта 2027 года (и снова назад 7 ноября 2027 года). В восточном поясе разница зимой 8 часов (UTC−5), летом 7 (UTC−4); остальные пояса сдвигаются так же.</p>

  <h2>Зимняя таблица (с начала ноября до середины марта)</h2>
  <p>Действует сейчас, до перевода часов 14 марта 2027 года. Московские 21:00, обычный прайм-тайм, выделены жирным.</p>

  ''' + table(WIN, False) + '''

  <h2>Летняя таблица (с середины марта до начала ноября)</h2>
  <p>В период летнего времени США всё на час позже, чем в зимней таблице (московские 21:00 становятся 14:00 по восточному времени).</p>

  ''' + table(SUM, False) + '''

  <h2>Исключения: Аризона, Аляска, Гавайи</h2>
  <ul>
    <li><strong>Аризона (Финикс)</strong> часы не переводит и весь год на UTC−7 (как горное время зимой): московские 21:00 — это 11:00 круглый год.</li>
    <li><strong>Аляска (Анкоридж)</strong> зимой UTC−9, летом UTC−8: московские 21:00 — это 9:00 зимой и 10:00 летом.</li>
    <li><strong>Гавайи (Гонолулу)</strong> часы не переводят и весь год на UTC−10: московские 21:00 — это 8:00 круглый год.</li>
  </ul>

  <h2>Конвертер для любого времени</h2>
  <p>Введите московское время и увидите местное в крупных городах США. Конвертер берёт сегодняшнюю дату и сам учитывает зимнее и летнее время:</p>

  ''' + conv('ru') + '''

  <h2>Как узнать программу на сегодня</h2>
  <p>Время передач меняется от сезона к сезону, поэтому в статье мы его не приводим. Надёжный способ — блок <strong>«Программа на сегодня»</strong> на странице каждого канала, например <a href="/perviy-kanal-live/">Первого канала</a>, <a href="/rossiya-1-live/">России 1</a>, <a href="/ntv-live/">НТВ</a> или <a href="/rossiya-24-live/">России 24</a>. В нём показаны передачи и отметка того, что идёт сейчас, а время выводится в <strong>местном времени вашего устройства</strong>, ничего пересчитывать не нужно.</p>

  <h2>Планируем день: что значит разница</h2>
  <ul>
    <li><strong>Московский вечер — ваш обед или день.</strong> Прайм-тайм в 21:00 по Москве — это 13:00 на Восточном побережье и 10:00 на Западном зимой, так что вечерние новости и передачи в США смотрят днём.</li>
    <li><strong>Московское утро — ваша ночь.</strong> Москва 9:00 — это 1:00 по восточному времени зимой, поэтому утренние программы лучше пропустить или посмотреть в повторе.</li>
    <li><strong>Новости в любой час.</strong> <a href="/rossiya-24-live/">Россия 24</a> идёт круглосуточно, так что живой эфир есть всегда.</li>
    <li><strong>Московская полночь — это день.</strong> 31 декабря полночь по Москве — 16:00 по восточному времени и 13:00 по тихоокеанскому; смотрите <a href="/blog/novogodnyaya-noch-russkoe-tv-za-granicey/">новогоднюю статью</a>.</li>
    <li><strong>Следите за датой.</strong> В таблицах есть отметки «накануне» и «на следующий день»: например, ранним утром в Москве на Западном побережье ещё вечер предыдущего дня.</li>
  </ul>

  <h2>Какой канал на какое время</h2>
  <p>Для дневного просмотра в США подходят главные федеральные каналы (<a href="/perviy-kanal-live/">Первый</a>, <a href="/rossiya-1-live/">Россия 1</a>, <a href="/ntv-live/">НТВ</a>): они идут в ваш обеденный час. Для Северной Америки есть и <a href="/rossiya-rtr-usa-live/">Россия РТР — США</a>, версия канала «Россия» для аудитории за рубежом, сетка которой может отличаться от российской. На телефоне или телевизоре читайте <a href="/blog/kak-smotret-russkoe-tv-na-iphone-i-android/">Российское ТВ на iPhone и Android</a>, а основы — в статье <a href="/blog/kak-smotret-russkoe-tv-za-granicey/">«Как смотреть российское ТВ за границей»</a>.</p>

  <p><em>Сетку вещания определяют телеканалы, и она меняется. Таблицы рассчитаны по правилам часовых поясов; актуальную программу смотрите на странице канала.</em></p>
''',
  faq=[('Какая разница во времени между Москвой и Нью-Йорком?', 'Восемь часов зимой (Москва UTC+3, Нью-Йорк UTC−5) и семь часов летом (Нью-Йорк UTC−4). 21:00 по Москве — это 13:00 в Нью-Йорке зимой и 14:00 летом.'),
       ('Когда в США переводят часы в 2026 и 2027 годах?', 'Часы перевели назад 1 ноября 2026 года и переведут вперёд 14 марта 2027 года. Москва часы не переводит.'),
       ('Сколько времени на Западном побережье, когда в Москве 21:00?', 'Зимой 10:00 по тихоокеанскому времени, летом 11:00.'),
       ('Переводит ли Аризона часы?', 'Нет. Аризона (кроме территории навахо) весь год живёт по UTC−7, поэтому московские 21:00 там всегда 11:00.'),
       ('Где посмотреть программу российского ТВ на сегодня в моём времени?', 'На странице каждого канала в блоке «Программа на сегодня»: время показано в местном времени вашего устройства, с отметкой того, что идёт сейчас.'),
       ('Нужен ли VPN, чтобы смотреть российское ТВ в США?', 'Нет. russian-tv.com работает в США без VPN, регистрации и приложения.')],
  related=[('Русское ТВ в США', '/russkie-kanaly-v-ssha/'), ('Как смотреть российское ТВ за границей', '/blog/kak-smotret-russkoe-tv-za-granicey/'), ('Российское ТВ в новогоднюю ночь за границей', '/blog/novogodnyaya-noch-russkoe-tv-za-granicey/'), ('Как смотреть российское ТВ в Канаде', '/blog/kak-smotret-russkoe-tv-v-kanade/'), ('Канал не грузится: что делать', '/blog/kanal-ne-gruzitsya-chto-delat/')],
)
