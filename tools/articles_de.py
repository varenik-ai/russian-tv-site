# Статьи про Германию (RU + EN) для gen_blog.py, 21.11.2026.
# Факты: Германия — одна часовая зона, центральноевропейское время UTC+1 (с 25.10.2026 по 28.03.2027) и летнее UTC+2; Москва UTC+3 круглый год
# (разница 2 ч зимой, 1 ч летом). Около 1,9 млн человек в Германии говорят дома по-русски (микроперепись 2024, Destatis; цифра по публикациям,
# ссылающимся на исследование). Каналы и ссылки — страницы сайта; правила для вещателей в ЕС владелец согласовал с юристами (21.11.2026).
import json
DE_ZONES = json.dumps([["Berlin, Hamburg, Munich, Cologne, Frankfurt", "Europe/Berlin"]], ensure_ascii=False)
def conv(lang, zones, default='21:00'):
    return f'<div class="rtv-conv" data-lang="{lang}" data-default="{default}" data-zones=\'{zones}\'></div>\n  <script defer src="/assets/moscow-time.js?v=1"></script>'

DE_RU = dict(
  slug='kak-smotret-russkoe-tv-v-germanii',
  date='2026-11-21', date_label='Ноябрь 2026',
  title='Как смотреть русское ТВ в Германии бесплатно (2026)',
  desc='Русское ТВ в Германии бесплатно: время по Москве и Берлину, каналы, телефон, компьютер, Smart TV. Без регистрации, без приложения. Гайд 2026.',
  headline='Как смотреть русское ТВ в Германии — бесплатные каналы, время, устройства',
  crumb='Русское ТВ в Германии', meta='<span>📅 Ноябрь 2026</span><span>🇩🇪 Германия</span><span>⏱ 6 мин</span>',
  h1='Как смотреть русское ТВ в Германии бесплатно в 2026 году',
  alt=('https://russian-tv.com/blog/kak-smotret-russkoe-tv-v-germanii/', 'https://russian-tv.com/en/blog/how-to-watch-russian-tv-in-germany/'),
  body='''  <p><strong>Коротко:</strong> откройте <a href="/">russian-tv.com</a> в любом браузере, выберите канал и нажмите ▶. Сайт работает по всей Германии на компьютере, телефоне, планшете и Smart TV, без регистрации и без приложения. Разница с Москвой — <strong>2 часа зимой и 1 час летом</strong>, поэтому вечерние новости в 21:00 по Москве зимой идут в 19:00 по Германии.</p>

  <div class="cta-box">
    <p>📺 Русское ТВ в Германии — бесплатно, без регистрации и приложения</p>
    <a href="/">▶ Открыть russian-tv.com</a>
  </div>

  <h2>Что можно смотреть</h2>
  <p>На сайте больше пятидесяти русскоязычных каналов в прямом эфире. Для большинства семей основной набор такой же, как дома: <a href="/perviy-kanal-live/">Первый канал</a>, <a href="/rossiya-1-live/">Россия 1</a>, <a href="/ntv-live/">НТВ</a>, <a href="/rossiya-24-live/">Россия 24</a>, а для зрителей в Европе есть <a href="/rossiya-rtr-evropa-live/">Россия РТР — Европа</a>. Из развлекательных: <a href="/sts-live/">СТС</a>, <a href="/ren-tv-live/">РЕН ТВ</a>, <a href="/pyatnica-live/">Пятница!</a>, из спортивных — <a href="/match-tv-live/">Матч ТВ</a>. Есть детское ТВ (<a href="/karusel-live/">Карусель</a>, <a href="/mult-live/">Мульт</a>), кино и документальные каналы. Полный список: <a href="/blog/kakie-kanaly-smotret-po-temam/">какие каналы смотреть по темам</a>.</p>
  <p>Часть каналов — международные версии: сетка и рекламные блоки в них могут отличаться от российского эфира.</p>

  <h2>Время: Москва и Германия</h2>
  <p>Москва живёт по UTC+3 круглый год. В Германии один часовой пояс, но часы переводят: зимой центральноевропейское время (UTC+1), с последнего воскресенья марта летнее (UTC+2). Ближайший переход — 28 марта 2027 года. Разница с Москвой 2 часа с конца октября до конца марта и 1 час летом.</p>
  <table class="channel-table">
    <thead>
      <tr><th>Когда в Москве</th><th>Германия зимой (UTC+1)</th><th>Германия летом (UTC+2)</th></tr>
    </thead>
    <tbody>
      <tr><td>12:00 (полдень)</td><td>10:00</td><td>11:00</td></tr>
      <tr><td>18:00</td><td>16:00</td><td>17:00</td></tr>
      <tr><td>21:00 (вечерние новости, прайм-тайм)</td><td><strong>19:00</strong></td><td><strong>20:00</strong></td></tr>
      <tr><td>00:00 (полночь)</td><td>22:00 накануне</td><td>23:00 накануне</td></tr>
    </tbody>
  </table>
  <p>Хотите точнее? Конвертер ниже считает по сегодняшней дате и сам учитывает летнее время.</p>
  ''' + conv('ru', DE_ZONES) + '''

  <h2>На каком устройстве смотреть</h2>
  <ul>
    <li><strong>Компьютер:</strong> откройте сайт, выберите канал и нажмите ▶; качество можно выбрать в настройках плеера.</li>
    <li><strong>Телефон и планшет:</strong> Safari или Chrome, ничего устанавливать не нужно. Подробнее: <a href="/blog/kak-smotret-russkoe-tv-na-iphone-i-android/">как смотреть на iPhone и Android</a>. Те же каналы есть в <a href="/blog/russkoe-tv-v-telegram-mini-app/">мини-аппе Telegram</a>.</li>
    <li><strong>Телевизор:</strong> откройте russian-tv.com/tv в браузере Smart TV или отправьте эфир с iPhone через AirPlay, а из Chrome — через Cast. Гайд: <a href="/blog/kak-smotret-russkoe-tv-na-smart-tv/">российское ТВ на Smart TV</a>.</li>
  </ul>
  <p>Для комфортного просмотра в хорошем качестве нужно около 5 Мбит/с. Эфир в интернете идёт короткими фрагментами, поэтому он отстаёт от кабельного на несколько секунд, а иногда до полуминуты: это нормально.</p>

  <h2>Русскоязычные в Германии</h2>
  <p>По данным микропереписи Германии 2024 года (Destatis) около 1,9 миллиона человек в стране говорят дома по-русски. Для многих российское телевидение — связь с семьёй, новости из дома и привычные программы, а браузер сегодня самый простой способ их смотреть. Страница с расписанием и подробностями: <a href="/russkie-kanaly-v-germanii/">русское ТВ в Германии</a>.</p>

  <h2>Если канал не грузится</h2>
  <p>Подождите 10–20 секунд: плеер сам переключается на запасной источник. Если не помогло, перезагрузите страницу или выберите другой канал. Подробная памятка: <a href="/blog/kanal-ne-gruzitsya-chto-delat/">канал не грузится, 8 способов</a>.</p>

  <p><em>russian-tv.com — агрегатор общедоступных прямых трансляций, видео на сайте не хранится. Правила, которые касаются просмотра в вашей стране, вы определяете сами; это не юридическая консультация.</em></p>
''',
  faq=[('Можно ли смотреть русское ТВ в Германии бесплатно?', 'Да. russian-tv.com бесплатен: откройте сайт, выберите канал и нажмите ▶. Регистрация и приложение не нужны.'),
       ('Нужен ли VPN для русского ТВ в Германии?', 'Нет, сайт открывается в Германии без VPN. Если VPN включён и картинка тормозит, попробуйте его выключить.'),
       ('Во сколько вечерние новости по российскому ТВ в Германии?', 'Вечерние новости в 21:00 по Москве — это 19:00 в Германии с конца октября до конца марта и 20:00 летом. Время передач меняется, проверяйте на странице канала.'),
       ('Работает ли на телефоне и на телевизоре?', 'Да. На телефоне и планшете сайт открывается в Safari и Chrome. На телевизоре откройте russian-tv.com/tv или отправьте эфир с iPhone (AirPlay) или из Chrome (Cast).'),
       ('Какая скорость интернета нужна?', 'Для комфортного просмотра в хорошем качестве рекомендуем от 5 Мбит/с. При более медленном соединении выберите качество ниже в настройках плеера.'),
       ('Почему эфир отстаёт на несколько секунд?', 'Прямое видео в интернете передаётся короткими фрагментами, это даёт задержку от нескольких секунд до полуминуты. Это нормально.')],
  related=[('Русское ТВ в Германии', '/russkie-kanaly-v-germanii/'), ('Как смотреть российское ТВ на Smart TV', '/blog/kak-smotret-russkoe-tv-na-smart-tv/'), ('Как смотреть российское ТВ на iPhone и Android', '/blog/kak-smotret-russkoe-tv-na-iphone-i-android/'), ('Канал не грузится: что делать', '/blog/kanal-ne-gruzitsya-chto-delat/'), ('Как смотреть российское ТВ за границей', '/blog/kak-smotret-russkoe-tv-za-granicey/')],
)

DE_EN = dict(
  slug='how-to-watch-russian-tv-in-germany',
  date='2026-11-21', date_label='November 2026',
  title='How to Watch Russian TV in Germany: Free Live Channels (2026)',
  desc='Watch Russian TV in Germany for free: Moscow and Berlin time, channels, phone, computer and Smart TV. No signup, no app. 2026 guide.',
  headline='How to Watch Russian TV in Germany — free live channels, time, devices',
  crumb='Russian TV in Germany', meta='<span>📅 Published: November 2026</span><span>🇩🇪 Germany</span><span>⏱ 6 min read</span>',
  h1='How to Watch Russian TV in Germany for Free in 2026',
  alt=('https://russian-tv.com/blog/kak-smotret-russkoe-tv-v-germanii/', 'https://russian-tv.com/en/blog/how-to-watch-russian-tv-in-germany/'),
  body='''  <p><strong>Short answer:</strong> open <a href="/en/">russian-tv.com</a> in any browser, pick a channel and press ▶. It works across Germany on a computer, phone, tablet or Smart TV, with no signup and no app. The gap with Moscow is <strong>2 hours in winter and 1 hour in summer</strong>, so the Moscow evening news at 21:00 is at 19:00 in German winter.</p>

  <div class="cta-box">
    <p>📺 Russian TV in Germany — free, no signup, no app</p>
    <a href="/en/">▶ Open russian-tv.com</a>
  </div>

  <h2>What you can watch</h2>
  <p>The site streams more than fifty Russian-language channels live. For most families the core list is the same as at home: <a href="/en/perviy-kanal-live/">Perviy Kanal (Channel One)</a>, <a href="/en/rossiya-1-live/">Rossiya 1</a>, <a href="/en/ntv-live/">NTV</a> and <a href="/en/rossiya-24-live/">Rossiya 24</a>, plus <a href="/en/rossiya-rtr-evropa-live/">Rossiya RTR — Europe</a> for audiences in Europe. For entertainment there are <a href="/en/sts-live/">STS</a>, <a href="/en/ren-tv-live/">REN TV</a> and <a href="/en/pyatnica-live/">Pyatnitsa!</a>, for sport <a href="/en/match-tv-live/">Match TV</a>. There is also children's television (<a href="/en/karusel-live/">Karusel</a>, <a href="/en/mult-live/">Mult</a>), films and documentaries. Full list: <a href="/en/blog/russian-tv-channels-list-live/">Russian TV channels list</a>.</p>
  <p>Some channels are international versions, so their schedule and ad breaks can differ from the Russian broadcast.</p>

  <h2>Time: Moscow and Germany</h2>
  <p>Moscow stays on UTC+3 all year. Germany has one time zone but changes clocks: Central European Time (UTC+1) in winter and Central European Summer Time (UTC+2) from the last Sunday of March. The next change is on 28 March 2027. The gap with Moscow is 2 hours from late October to late March and 1 hour in summer.</p>
  <table class="channel-table">
    <thead>
      <tr><th>Moscow time</th><th>Germany in winter (UTC+1)</th><th>Germany in summer (UTC+2)</th></tr>
    </thead>
    <tbody>
      <tr><td>12:00 (midday)</td><td>10:00 am</td><td>11:00 am</td></tr>
      <tr><td>18:00</td><td>4:00 pm</td><td>5:00 pm</td></tr>
      <tr><td>21:00 (evening news, prime time)</td><td><strong>7:00 pm</strong></td><td><strong>8:00 pm</strong></td></tr>
      <tr><td>00:00 (midnight)</td><td>10:00 pm the evening before</td><td>11:00 pm the evening before</td></tr>
    </tbody>
  </table>
  <p>Want it exact? The converter below uses today's date and handles daylight saving automatically.</p>
  ''' + conv('en', DE_ZONES) + '''

  <h2>Which device to use</h2>
  <ul>
    <li><strong>Computer:</strong> open the site, pick a channel and press ▶; choose the quality in the player settings.</li>
    <li><strong>Phone and tablet:</strong> Safari or Chrome with nothing to install. More: <a href="/en/blog/russian-tv-on-iphone-and-android/">Russian TV on iPhone and Android</a>. The same channels are in the <a href="/en/blog/russian-tv-in-telegram-mini-app/">Telegram mini-app</a>.</li>
    <li><strong>TV:</strong> open russian-tv.com/tv in the Smart TV browser, or send the stream from an iPhone with AirPlay or from Chrome with Cast. Guide: <a href="/en/blog/russian-tv-on-smart-tv-roku-chromecast-apple-tv/">Russian TV on Smart TV, Roku, Chromecast and more</a>.</li>
  </ul>
  <p>About 5 Mbit/s is comfortable for good quality. Live video over the internet is sent in short segments, so it runs a few seconds behind cable and sometimes up to half a minute. That is normal.</p>

  <h2>Russian speakers in Germany</h2>
  <p>According to Germany's 2024 microcensus (Destatis), about 1.9 million people in the country speak Russian at home. For many of them, Russian television is a link with family and news from home, and a browser is now the simplest way to watch it. More details and the schedule: <a href="/en/russian-tv-in-germany/">Russian TV in Germany</a>.</p>

  <h2>If a channel does not load</h2>
  <p>Wait ten to twenty seconds: the player switches to a backup source on its own. If that does not help, reload the page or try another channel. Full checklist: <a href="/en/blog/channel-not-loading-fix/">Channel not loading — 8 fixes</a>.</p>

  <p><em>russian-tv.com is an aggregator of publicly available live streams and does not host video. You decide which rules apply to watching in your country; this is not legal advice.</em></p>
''',
  faq=[('Can I watch Russian TV in Germany for free?', 'Yes. russian-tv.com is free: open the site, choose a channel and press ▶. No signup and no app.'),
       ('Do I need a VPN to watch Russian TV in Germany?', 'No. The site opens in Germany without a VPN. If you use a VPN and the picture lags, try switching it off.'),
       ('What time is the Russian evening news in Germany?', 'The main evening news at 21:00 Moscow time is 19:00 in Germany from late October to late March and 20:00 in summer. Programme times change, so check the channel page.'),
       ('Does it work on a phone and on a TV?', 'Yes. On a phone or tablet the site opens in Safari and Chrome. On a TV open russian-tv.com/tv, or send the stream from an iPhone (AirPlay) or from Chrome (Cast).'),
       ('What internet speed do I need?', 'About 5 Mbit/s is recommended for good quality. On a slower connection choose a lower quality in the player settings.'),
       ('Why is the stream a few seconds behind?', 'Live video over the internet is sent in short segments, which adds a delay of a few seconds up to half a minute. This is normal.')],
  related=[('Russian TV in Germany', '/en/russian-tv-in-germany/'), ('Russian TV on Smart TV, Roku, Chromecast', '/en/blog/russian-tv-on-smart-tv-roku-chromecast-apple-tv/'), ('Russian TV on iPhone and Android', '/en/blog/russian-tv-on-iphone-and-android/'), ('Channel not loading: 8 fixes', '/en/blog/channel-not-loading-fix/'), ('How to Watch Russian TV in the USA', '/en/blog/how-to-watch-russian-tv-in-usa/')],
)
