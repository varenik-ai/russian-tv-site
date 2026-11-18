# Тексты страниц США / Великобритании / Канады (EN и RU) для gen_country_content.py.
# Числа: США — Бюро переписи США (говорящие по-русски дома: 854 955 в 2010, 905 843 по ACS 2011); Канада — перепись 2021, Statistics Canada
# (русский язык чаще всего дома: 125 780 человек). Для Великобритании число не приводится (не удалось подтвердить по ONS).
# Время в таблицах — стандартное (зимнее); Москва UTC+3 круглый год.

# Ряды таблицы «Москва → у вас»: [(метка, [значения по колонкам])]
MSK_MOMENTS_EN = ['Moscow 12:00 (midday)', 'Moscow 18:00', 'Moscow 21:00 (evening news, prime time)', 'Moscow 00:00 (midnight)']
MSK_MOMENTS_RU = ['Москва 12:00 (полдень)', 'Москва 18:00', 'Москва 21:00 (вечерние новости, прайм-тайм)', 'Москва 00:00 (полночь)']

COUNTRIES = {
 'usa': dict(
  en_path='en/russian-tv-in-usa', ru_path='russkie-kanaly-v-ssha',
  en_zones=[('Eastern', 'New York, Boston, Miami', ['4:00 am', '10:00 am', '1:00 pm', '4:00 pm']),
            ('Central', 'Chicago, Houston', ['3:00 am', '9:00 am', '12:00 pm', '3:00 pm']),
            ('Mountain', 'Denver, Phoenix', ['2:00 am', '8:00 am', '11:00 am', '2:00 pm']),
            ('Pacific', 'Los Angeles, Seattle, San Francisco', ['1:00 am', '7:00 am', '10:00 am', '1:00 pm'])],
  ru_zones=[('Восточное (Eastern)', 'Нью-Йорк, Бостон, Майами', ['4:00', '10:00', '13:00', '16:00']),
            ('Центральное (Central)', 'Чикаго, Хьюстон', ['3:00', '9:00', '12:00', '15:00']),
            ('Горное (Mountain)', 'Денвер, Финикс', ['2:00', '8:00', '11:00', '14:00']),
            ('Тихоокеанское (Pacific)', 'Лос-Анджелес, Сиэтл, Сан-Франциско', ['1:00', '7:00', '10:00', '13:00'])],
  en_intro='''<p>russian-tv.com streams 56 Russian TV channels live in your browser from anywhere in the United States: no VPN, no app, no sign-up. The line-up covers the national channels (Perviy Kanal, Rossiya 1, NTV, Rossiya 24), cinema, children's television, music and documentaries, plus <a href="/en/rossiya-rtr-usa-live/">Rossiya RTR — USA</a>, the international version of the Rossiya channel made for audiences abroad.</p>
    <p>For a Russian speaker in the US the practical question is rarely "can I find a stream" but "what time is it in Moscow". Russian television runs on Moscow time, which is eight to eleven hours ahead of the US mainland, so the shows you may remember from home air at very different hours of your day. The table below does the maths for you.</p>''',
  en_when='''<p>Moscow stays on UTC+3 all year, but US clocks change twice a year. The times below are for standard time (from early November to mid-March); during daylight saving time your local time is one hour later for the same Moscow moment. The key idea: <strong>the Moscow evening is your lunchtime, and the Moscow night is your afternoon.</strong></p>''',
  en_how='''<ol style="margin:8px 0 12px 20px">
      <li><strong>On a computer:</strong> open <a href="/en/">russian-tv.com</a>, pick a channel and press ▶. The quality adjusts to your connection; use the settings button to choose a lower or higher level.</li>
      <li><strong>On iPhone, iPad or Android:</strong> use Safari or Chrome. There is nothing to install; see <a href="/en/blog/russian-tv-on-iphone-and-android/">Russian TV on iPhone and Android</a>. The Telegram mini-app from <a href="https://t.me/RussiaTV_Hub_Live" target="_blank" rel="noopener">@RussiaTV_Hub_Live</a> groups the same channels by topic.</li>
      <li><strong>On a TV:</strong> open <strong>russian-tv.com/tv</strong> in the TV's browser, or send the stream from an iPhone with AirPlay or from Chrome with Cast.</li>
    </ol>''',
  en_people='''<p>The US has one of the largest Russian-speaking communities outside the former Soviet Union. According to the U.S. Census Bureau, about 855,000 people spoke Russian at home in the 2010 census, and the American Community Survey estimated roughly 906,000 in 2011; the communities are concentrated in New York (above all Brighton Beach in Brooklyn), the Los Angeles area, Chicago, the San Francisco Bay Area, Seattle, Boston, Philadelphia and South Florida (Sunny Isles Beach). Many of these viewers know Russian-language television from home and now watch it on a laptop or phone instead of a cable package.</p>''',
  en_faq=[
   ('How can I watch Russian TV in the USA?', 'Open russian-tv.com in any browser, choose a channel and press play. The site works in all US states with no VPN, no app and no registration.'),
   ('Do I need a VPN to watch Russian TV in the USA?', 'No. russian-tv.com is available from the United States without a VPN. If you use a VPN and the picture lags, try switching it off.'),
   ('Is it free?', 'Yes. All channels are free to watch, with no registration or subscription. The site is supported by advertising.'),
   ('What time is the Russian evening news in the USA?', 'The main evening news on Moscow time at 9:00 pm is 1:00 pm Eastern and 10:00 am Pacific in winter (one hour later during daylight saving time). Programme times change, so check the channel page.'),
   ('Can I watch on my TV?', 'Yes. Open russian-tv.com/tv in the TV browser, or cast from an iPhone (AirPlay) or from Chrome (Cast).'),
   ('Does it work on iPhone and Android?', 'Yes, in Safari and Chrome without installing anything. There is also an optional Telegram mini-app.'),
   ('Why is the stream a few seconds behind cable?', 'Live video over the internet is sent in short segments, which adds a delay of a few seconds up to half a minute. This is normal.'),
   ('A channel does not load. What should I do?', 'Wait ten to twenty seconds (the player switches to a backup source on its own), reload the page, or try another channel. More tips: Channel not loading — 8 fixes.'),
   ('Is this site the official broadcaster?', 'No. russian-tv.com is an aggregator of publicly available live streams and does not host video. Rights holders can contact the site to request removal of a link. The site cannot give legal advice about viewing rules in your state.'),
   ('How do I watch the Russian New Year broadcast from the USA?', "See our guide: on December 31 Moscow midnight is 4:00 pm Eastern and 1:00 pm Pacific. Details and channels: Russian TV on New Year's Eve."),
  ],
  ru_intro='''<p>russian-tv.com показывает 56 российских каналов в прямом эфире в браузере из любой точки США: без VPN, приложения и регистрации. В списке федеральные каналы (Первый канал, Россия 1, НТВ, Россия 24), кино, детское ТВ, музыка и документальные программы, а также <a href="/rossiya-rtr-usa-live/">Россия РТР — США</a> — международная версия канала «Россия» для зрителей за рубежом.</p>
    <p>Для русскоязычного зрителя в США главный вопрос — не «где найти трансляцию», а «который час в Москве». Российское телевидение работает по московскому времени, разница с материковой частью США от 8 до 11 часов, поэтому передачи, привычные по России, идут в совсем другие часы вашего дня. Таблица ниже считает за вас.</p>''',
  ru_when='''<p>Москва живёт по UTC+3 круглый год, а в США часы переводят дважды в год. В таблице стандартное (зимнее) время, с начала ноября до середины марта; летом по местному времени тот же московский момент на час позже. Главное правило: <strong>московский вечер — это ваш обед, а московская ночь — ваш день.</strong></p>''',
  ru_how='''<ol style="margin:8px 0 12px 20px">
      <li><strong>Компьютер:</strong> откройте <a href="/">russian-tv.com</a>, выберите канал и нажмите ▶; качество подстраивается под соединение, в настройках плеера его можно выбрать вручную.</li>
      <li><strong>iPhone, iPad, Android:</strong> Safari или Chrome, ничего устанавливать не нужно: <a href="/blog/kak-smotret-russkoe-tv-na-iphone-i-android/">как смотреть на телефоне</a>. Мини-апп Telegram из канала <a href="https://t.me/RussiaTV_Hub_Live" target="_blank" rel="noopener">@RussiaTV_Hub_Live</a> собирает те же каналы по темам.</li>
      <li><strong>Телевизор:</strong> откройте <strong>russian-tv.com/tv</strong> в браузере телевизора или отправьте эфир с iPhone через AirPlay, из Chrome — через Cast. Гайд: <a href="/blog/kak-smotret-russkoe-tv-na-smart-tv/">Smart TV</a>.</li>
    </ol>''',
  ru_people='''<p>В США одна из крупнейших русскоязычных общин за пределами бывшего СССР. По данным Бюро переписи США, дома говорили по-русски около 855 тысяч человек (перепись 2010 года), а опрос American Community Survey оценил число в 906 тысяч в 2011 году. Общины сосредоточены в Нью-Йорке (особенно Брайтон-Бич в Бруклине), в районе Лос-Анджелеса, Чикаго, Сан-Франциско и заливе, Сиэтле, Бостоне, Филадельфии и на юге Флориды (Санни-Айлс-Бич). Многие зрители знают российское телевидение по дому и теперь смотрят его на ноутбуке и телефоне вместо платного пакета.</p>''',
  ru_faq=[
   ('Как смотреть русское ТВ в США?', 'Откройте russian-tv.com в браузере, выберите канал и нажмите ▶. Сайт работает во всех штатах без VPN, приложения и регистрации.'),
   ('Нужен ли VPN для русского ТВ в США?', 'Нет, russian-tv.com доступен из США без VPN. Если VPN включён и картинка тормозит, попробуйте его выключить.'),
   ('Это бесплатно?', 'Да, все каналы бесплатны, без регистрации и подписки. Сайт существует за счёт рекламы.'),
   ('Во сколько вечерние новости по российскому ТВ в США?', 'Вечерние новости в 21:00 по Москве — это 13:00 по восточному и 10:00 по тихоокеанскому времени зимой (летом на час позже). Время передач меняется, проверяйте на странице канала.'),
   ('Можно ли смотреть на телевизоре?', 'Да. Откройте russian-tv.com/tv в браузере телевизора или отправьте эфир с iPhone (AirPlay) или из Chrome (Cast).'),
   ('Работает ли на iPhone и Android?', 'Да, в Safari и Chrome без установки приложений; есть и необязательный мини-апп Telegram.'),
   ('Почему эфир отстаёт от кабельного на несколько секунд?', 'Прямое видео в интернете передаётся короткими фрагментами, это даёт задержку от нескольких секунд до полуминуты. Это нормально.'),
   ('Канал не грузится, что делать?', 'Подождите 10–20 секунд (плеер сам переходит на запасной источник), перезагрузите страницу или включите другой канал. Подробнее: «Канал не грузится: 8 способов».'),
   ('Сайт — официальный вещатель?', 'Нет. russian-tv.com — агрегатор общедоступных прямых трансляций, видео на сайте не хранится. Правообладатели могут обратиться на сайт с просьбой убрать ссылку. Юридических консультаций о правилах просмотра в вашем штате сайт не даёт.'),
   ('Как смотреть российский Новый год из США?', 'См. статью: 31 декабря полночь по Москве — 16:00 по восточному и 13:00 по тихоокеанскому времени. Подробности и каналы: «Российское ТВ в новогоднюю ночь за границей».'),
  ],
  cities=[('New York / Brooklyn', 'russian-tv-in-new-york'), ('Los Angeles', 'russian-tv-in-los-angeles'), ('Chicago', 'russian-tv-in-chicago')],
 ),
 'uk': dict(
  en_path='en/russian-tv-in-uk', ru_path='russkie-kanaly-v-velikobritanii',
  en_zones=[('UK (GMT in winter)', 'London, Manchester, Birmingham, Edinburgh', ['9:00 am', '3:00 pm', '6:00 pm', '9:00 pm'])],
  ru_zones=[('Великобритания (зимой GMT)', 'Лондон, Манчестер, Бирмингем, Эдинбург', ['9:00', '15:00', '18:00', '21:00'])],
  en_intro='''<p>russian-tv.com streams 56 Russian TV channels live in your browser from anywhere in the United Kingdom: no VPN, no app, no sign-up. The channels cover national news (Perviy Kanal, Rossiya 1, NTV, Rossiya 24), cinema, children's television, music and documentaries. <a href="/en/rossiya-rtr-evropa-live/">Rossiya RTR — Europe</a> is the international version of the Rossiya channel made for viewers outside Russia.</p>
    <p>The UK sits close to Moscow's clock, which makes live Russian television easy to follow: Moscow is three hours ahead in winter and two hours ahead in summer, so the Moscow evening is your afternoon and early evening. The table below shows the exact times.</p>''',
  en_when='''<p>Moscow stays on UTC+3 all year, while the UK changes between GMT in winter and British Summer Time (UTC+1) from late March to late October. The times below are for winter (GMT); in summer, add one hour. The key idea: <strong>the main Moscow evening programmes fall into your afternoon and early evening</strong>, so you can follow news and prime-time shows live without staying up late.</p>''',
  en_how='''<ol style="margin:8px 0 12px 20px">
      <li><strong>On a computer:</strong> open <a href="/en/">russian-tv.com</a>, pick a channel and press ▶. Use the settings button to choose a lower or higher quality.</li>
      <li><strong>On iPhone, iPad or Android:</strong> use Safari or Chrome with nothing to install: <a href="/en/blog/russian-tv-on-iphone-and-android/">Russian TV on iPhone and Android</a>. The Telegram mini-app from <a href="https://t.me/RussiaTV_Hub_Live" target="_blank" rel="noopener">@RussiaTV_Hub_Live</a> offers the same channels grouped by topic.</li>
      <li><strong>On a TV:</strong> open <strong>russian-tv.com/tv</strong> in the TV's browser, or send the stream from an iPhone with AirPlay or from Chrome with Cast.</li>
    </ol>''',
  en_people='''<p>Russian speakers in the UK live mostly in London, with large communities also in Manchester, Birmingham and Edinburgh, and many arrived as students, professionals and families over the past decades. Most of them can now watch Russian television the same way they watch everything else: in a browser on a laptop or phone, without a satellite dish or a special set-top box.</p>''',
  en_faq=[
   ('How can I watch Russian TV in the UK?', 'Open russian-tv.com in any browser, choose a channel and press play. The site works across the UK with no VPN, no app and no registration.'),
   ('Do I need a VPN to watch Russian TV in the UK?', 'No. russian-tv.com is available from the UK without a VPN. If you use a VPN and the picture lags, try switching it off.'),
   ('Is it free?', 'Yes. All channels are free, with no registration or subscription. The site is supported by advertising.'),
   ('What time is the Russian evening news in the UK?', 'The main evening news at 9:00 pm Moscow time is 6:00 pm in the UK in winter (GMT) and 7:00 pm in summer (BST). Programme times change, so check the channel page.'),
   ('Can I watch on my TV?', 'Yes. Open russian-tv.com/tv in the TV browser, or send the stream from an iPhone (AirPlay) or from Chrome (Cast).'),
   ('Does it work on iPhone and Android?', 'Yes, in Safari and Chrome without installing anything. There is also an optional Telegram mini-app.'),
   ('Why is the stream a few seconds behind cable?', 'Live video over the internet is sent in short segments, which adds a delay of a few seconds up to half a minute. This is normal.'),
   ('A channel does not load. What should I do?', 'Wait ten to twenty seconds (the player switches to a backup source on its own), reload the page, or try another channel. More tips: Channel not loading — 8 fixes.'),
   ('Is this site the official broadcaster?', 'No. russian-tv.com is an aggregator of publicly available live streams and does not host video. Rights holders can contact the site to request removal of a link. The site cannot give legal advice about viewing rules in the UK.'),
   ('How do I watch the Russian New Year broadcast from the UK?', "On December 31 Moscow midnight is 9:00 pm in London. See Russian TV on New Year's Eve for times and channels."),
  ],
  ru_intro='''<p>russian-tv.com показывает 56 российских каналов в прямом эфире в браузере из любой точки Великобритании: без VPN, приложения и регистрации. В списке федеральные каналы (Первый канал, Россия 1, НТВ, Россия 24), кино, детское ТВ, музыка и документальные программы. <a href="/rossiya-rtr-evropa-live/">Россия РТР — Европа</a> — международная версия канала «Россия» для зрителей за пределами России.</p>
    <p>Великобритания близка к московскому времени, что упрощает просмотр российского ТВ в эфире: Москва впереди на три часа зимой и на два летом, поэтому московский вечер приходится на ваши день и ранний вечер. Точное время — в таблице ниже.</p>''',
  ru_when='''<p>Москва живёт по UTC+3 круглый год, а в Великобритании зимой время GMT, а с конца марта до конца октября — летнее BST (UTC+1). В таблице зимнее время (GMT), летом добавьте час. Главное: <strong>основные московские вечерние программы приходятся на ваш день и ранний вечер</strong>, поэтому новости и вечерний прайм-тайм можно смотреть в эфире, не засиживаясь допоздна.</p>''',
  ru_how='''<ol style="margin:8px 0 12px 20px">
      <li><strong>Компьютер:</strong> откройте <a href="/">russian-tv.com</a>, выберите канал и нажмите ▶; качество можно выбрать в настройках плеера.</li>
      <li><strong>iPhone, iPad, Android:</strong> Safari или Chrome, ничего устанавливать не нужно: <a href="/blog/kak-smotret-russkoe-tv-na-iphone-i-android/">как смотреть на телефоне</a>. Мини-апп Telegram из канала <a href="https://t.me/RussiaTV_Hub_Live" target="_blank" rel="noopener">@RussiaTV_Hub_Live</a> собирает те же каналы по темам.</li>
      <li><strong>Телевизор:</strong> откройте <strong>russian-tv.com/tv</strong> в браузере телевизора или отправьте эфир с iPhone через AirPlay, из Chrome — через Cast. Гайд: <a href="/blog/kak-smotret-russkoe-tv-na-smart-tv/">Smart TV</a>.</li>
    </ol>''',
  ru_people='''<p>Русскоязычные жители Великобритании живут в основном в Лондоне, крупные общины есть также в Манчестере, Бирмингеме и Эдинбурге; многие приехали учиться, работать или с семьями за последние десятилетия. Российское телевидение теперь можно смотреть так же, как всё остальное: в браузере на ноутбуке или телефоне, без спутниковой тарелки и специальной приставки.</p>''',
  ru_faq=[
   ('Как смотреть русское ТВ в Великобритании?', 'Откройте russian-tv.com в браузере, выберите канал и нажмите ▶. Сайт работает по всей Великобритании без VPN, приложения и регистрации.'),
   ('Нужен ли VPN для русского ТВ в Великобритании?', 'Нет, russian-tv.com доступен из Великобритании без VPN. Если VPN включён и картинка тормозит, попробуйте его выключить.'),
   ('Это бесплатно?', 'Да, все каналы бесплатны, без регистрации и подписки. Сайт существует за счёт рекламы.'),
   ('Во сколько вечерние новости по российскому ТВ в Великобритании?', 'Вечерние новости в 21:00 по Москве — это 18:00 по лондонскому времени зимой (GMT) и 19:00 летом (BST). Время передач меняется, проверяйте на странице канала.'),
   ('Можно ли смотреть на телевизоре?', 'Да. Откройте russian-tv.com/tv в браузере телевизора или отправьте эфир с iPhone (AirPlay) или из Chrome (Cast).'),
   ('Работает ли на iPhone и Android?', 'Да, в Safari и Chrome без установки приложений; есть и необязательный мини-апп Telegram.'),
   ('Почему эфир отстаёт от кабельного на несколько секунд?', 'Прямое видео в интернете передаётся короткими фрагментами, это даёт задержку от нескольких секунд до полуминуты. Это нормально.'),
   ('Канал не грузится, что делать?', 'Подождите 10–20 секунд (плеер сам переходит на запасной источник), перезагрузите страницу или включите другой канал. Подробнее: «Канал не грузится: 8 способов».'),
   ('Сайт — официальный вещатель?', 'Нет. russian-tv.com — агрегатор общедоступных прямых трансляций, видео на сайте не хранится. Правообладатели могут обратиться на сайт с просьбой убрать ссылку. Юридических консультаций о правилах просмотра в Великобритании сайт не даёт.'),
   ('Как смотреть российский Новый год из Великобритании?', 'Полночь по Москве 31 декабря — 21:00 в Лондоне. Время и каналы: «Российское ТВ в новогоднюю ночь за границей».'),
  ],
  cities=[('London', 'russian-tv-in-london')],
 ),
 'canada': dict(
  en_path='en/russian-tv-in-canada', ru_path='russkie-kanaly-v-kanade',
  en_zones=[('Newfoundland', "St. John's", ['5:30 am', '11:30 am', '2:30 pm', '5:30 pm']),
            ('Atlantic', 'Halifax, Moncton', ['5:00 am', '11:00 am', '2:00 pm', '5:00 pm']),
            ('Eastern', 'Toronto, Montreal, Ottawa', ['4:00 am', '10:00 am', '1:00 pm', '4:00 pm']),
            ('Central (Saskatchewan)', 'Regina, Saskatoon', ['3:00 am', '9:00 am', '12:00 pm', '3:00 pm']),
            ('Manitoba (permanent daylight time, UTC−5)', 'Winnipeg', ['4:00 am', '10:00 am', '1:00 pm', '4:00 pm']),
            ('Alberta (permanent daylight time, UTC−6)', 'Edmonton, Calgary', ['3:00 am', '9:00 am', '12:00 pm', '3:00 pm']),
            ('British Columbia (permanent daylight time, UTC−7)', 'Vancouver, Victoria', ['2:00 am', '8:00 am', '11:00 am', '2:00 pm'])],
  ru_zones=[('Ньюфаундлендское', 'Сент-Джонс', ['5:30', '11:30', '14:30', '17:30']),
            ('Атлантическое', 'Галифакс, Монктон', ['5:00', '11:00', '14:00', '17:00']),
            ('Восточное (Eastern)', 'Торонто, Монреаль, Оттава', ['4:00', '10:00', '13:00', '16:00']),
            ('Саскачеван (Central)', 'Реджайна, Саскатун', ['3:00', '9:00', '12:00', '15:00']),
            ('Манитоба (постоянное летнее время, UTC−5)', 'Виннипег', ['4:00', '10:00', '13:00', '16:00']),
            ('Альберта (постоянное летнее время, UTC−6)', 'Эдмонтон, Калгари', ['3:00', '9:00', '12:00', '15:00']),
            ('Британская Колумбия (постоянное летнее время, UTC−7)', 'Ванкувер, Виктория', ['2:00', '8:00', '11:00', '14:00'])],
  en_intro='''<p>russian-tv.com streams 56 Russian TV channels live in your browser from anywhere in Canada: no VPN, no app, no sign-up. The channels include the national networks (Perviy Kanal, Rossiya 1, NTV, Rossiya 24), cinema, children's television, music and documentaries, plus <a href="/en/rossiya-rtr-usa-live/">Rossiya RTR — USA</a>, the international version of the Rossiya channel for audiences abroad.</p>
    <p>Canada spans six time zones, from Newfoundland to the Pacific coast, so "what time is it in Moscow" depends on where you live. Moscow is six and a half to ten hours ahead of Canada in winter. The table below lists every Canadian zone.</p>''',
  en_when='''<p>Moscow stays on UTC+3 all year, while Canadian clocks change between standard time (from early November to mid-March) and daylight saving time. The times below are for winter; in summer, your local time is one hour later for the same Moscow moment in most of the country. Since 2026 British Columbia, Alberta and Manitoba no longer change clocks, so the table lists them on their year-round time. A practical rule: <strong>the Moscow evening news and prime time are your lunchtime and afternoon</strong>, and the Moscow night is your afternoon, so family viewing often happens at lunchtime or at the weekend.</p>''',
  en_how='''<ol style="margin:8px 0 12px 20px">
      <li><strong>On a computer:</strong> open <a href="/en/">russian-tv.com</a>, pick a channel and press ▶. Use the settings button to choose a lower or higher quality.</li>
      <li><strong>On iPhone, iPad or Android:</strong> use Safari or Chrome with nothing to install: <a href="/en/blog/russian-tv-on-iphone-and-android/">Russian TV on iPhone and Android</a>. The Telegram mini-app from <a href="https://t.me/RussiaTV_Hub_Live" target="_blank" rel="noopener">@RussiaTV_Hub_Live</a> offers the same channels grouped by topic.</li>
      <li><strong>On a TV:</strong> open <strong>russian-tv.com/tv</strong> in the TV's browser, or send the stream from an iPhone with AirPlay or from Chrome with Cast.</li>
    </ol>''',
  en_people='''<p>According to the 2021 Census of Canada, about 126,000 people (125,780 in Statistics Canada's figures) speak Russian most often at home. The largest communities are in the Greater Toronto Area (including Vaughan, Richmond Hill and Thornhill), Montreal, Vancouver, Calgary, Edmonton and Winnipeg. For many of them, Russian television is a link with family and news from home, and the browser is now the simplest way to watch it.</p>''',
  en_faq=[
   ('How can I watch Russian TV in Canada?', 'Open russian-tv.com in any browser, choose a channel and press play. The site works across Canada with no VPN, no app and no registration.'),
   ('Do I need a VPN to watch Russian TV in Canada?', 'No. russian-tv.com is available from Canada without a VPN. If you use a VPN and the picture lags, try switching it off.'),
   ('Is it free?', 'Yes. All channels are free, with no registration or subscription. The site is supported by advertising.'),
   ('What time is the Russian evening news in Canada?', 'The main evening news at 9:00 pm Moscow time is 1:00 pm in Toronto and 11:00 am in Vancouver in winter (British Columbia, Alberta and Manitoba stopped changing their clocks in 2026). Programme times change, so check the channel page.'),
   ('Can I watch on my TV?', 'Yes. Open russian-tv.com/tv in the TV browser, or send the stream from an iPhone (AirPlay) or from Chrome (Cast).'),
   ('Does it work on iPhone and Android?', 'Yes, in Safari and Chrome without installing anything. There is also an optional Telegram mini-app.'),
   ('Why is the stream a few seconds behind cable?', 'Live video over the internet is sent in short segments, which adds a delay of a few seconds up to half a minute. This is normal.'),
   ('A channel does not load. What should I do?', 'Wait ten to twenty seconds (the player switches to a backup source on its own), reload the page, or try another channel. More tips: Channel not loading — 8 fixes.'),
   ('Is this site the official broadcaster?', 'No. russian-tv.com is an aggregator of publicly available live streams and does not host video. Rights holders can contact the site to request removal of a link. The site cannot give legal advice about viewing rules in your province.'),
   ('How do I watch the Russian New Year broadcast from Canada?', "On December 31 Moscow midnight is 4:00 pm in Toronto, 2:00 pm in Vancouver and 5:30 pm in St. John's. See Russian TV on New Year's Eve for times and channels."),
  ],
  ru_intro='''<p>russian-tv.com показывает 56 российских каналов в прямом эфире в браузере из любой точки Канады: без VPN, приложения и регистрации. В списке федеральные каналы (Первый канал, Россия 1, НТВ, Россия 24), кино, детское ТВ, музыка и документальные программы, а также <a href="/rossiya-rtr-usa-live/">Россия РТР — США</a> — международная версия канала «Россия» для зрителей за рубежом.</p>
    <p>Канада занимает шесть часовых поясов, от Ньюфаундленда до Тихоокеанского побережья, поэтому ответ на вопрос «который час в Москве» зависит от того, где вы живёте. Москва впереди Канады зимой на 6,5–10 часов. В таблице ниже все канадские пояса.</p>''',
  ru_when='''<p>Москва живёт по UTC+3 круглый год, а в Канаде часы переводят между стандартным и летним временем. В таблице зимнее время (с начала ноября до середины марта); летом в большей части страны тот же московский момент на час позже. С 2026 года Британская Колумбия, Альберта и Манитоба часы не переводят, для них указано постоянное время. Практическое правило: <strong>московские вечерние новости и прайм-тайм — это ваши день и обед</strong>, поэтому семейный просмотр часто переносят на обед или на выходные.</p>''',
  ru_how='''<ol style="margin:8px 0 12px 20px">
      <li><strong>Компьютер:</strong> откройте <a href="/">russian-tv.com</a>, выберите канал и нажмите ▶; качество можно выбрать в настройках плеера.</li>
      <li><strong>iPhone, iPad, Android:</strong> Safari или Chrome, ничего устанавливать не нужно: <a href="/blog/kak-smotret-russkoe-tv-na-iphone-i-android/">как смотреть на телефоне</a>. Мини-апп Telegram из канала <a href="https://t.me/RussiaTV_Hub_Live" target="_blank" rel="noopener">@RussiaTV_Hub_Live</a> собирает те же каналы по темам.</li>
      <li><strong>Телевизор:</strong> откройте <strong>russian-tv.com/tv</strong> в браузере телевизора или отправьте эфир с iPhone через AirPlay, из Chrome — через Cast. Гайд: <a href="/blog/kak-smotret-russkoe-tv-na-smart-tv/">Smart TV</a>.</li>
    </ol>''',
  ru_people='''<p>По переписи Канады 2021 года около 126 тысяч человек (125 780 по данным Statistics Canada) чаще всего говорят дома по-русски. Крупнейшие общины — в Большом Торонто (включая Вон, Ричмонд-Хилл и Торнхилл), Монреале, Ванкувере, Калгари, Эдмонтоне и Виннипеге. Для многих российское телевидение — связь с семьёй и новости из дома, а браузер сегодня самый простой способ его смотреть.</p>''',
  ru_faq=[
   ('Как смотреть русское ТВ в Канаде?', 'Откройте russian-tv.com в браузере, выберите канал и нажмите ▶. Сайт работает по всей Канаде без VPN, приложения и регистрации.'),
   ('Нужен ли VPN для русского ТВ в Канаде?', 'Нет, russian-tv.com доступен из Канады без VPN. Если VPN включён и картинка тормозит, попробуйте его выключить.'),
   ('Это бесплатно?', 'Да, все каналы бесплатны, без регистрации и подписки. Сайт существует за счёт рекламы.'),
   ('Во сколько вечерние новости по российскому ТВ в Канаде?', 'Вечерние новости в 21:00 по Москве — это 13:00 в Торонто и 11:00 в Ванкувере зимой (Британская Колумбия, Альберта и Манитоба в 2026 году перестали переводить часы). Время передач меняется, проверяйте на странице канала.'),
   ('Можно ли смотреть на телевизоре?', 'Да. Откройте russian-tv.com/tv в браузере телевизора или отправьте эфир с iPhone (AirPlay) или из Chrome (Cast).'),
   ('Работает ли на iPhone и Android?', 'Да, в Safari и Chrome без установки приложений; есть и необязательный мини-апп Telegram.'),
   ('Почему эфир отстаёт от кабельного на несколько секунд?', 'Прямое видео в интернете передаётся короткими фрагментами, это даёт задержку от нескольких секунд до полуминуты. Это нормально.'),
   ('Канал не грузится, что делать?', 'Подождите 10–20 секунд (плеер сам переходит на запасной источник), перезагрузите страницу или включите другой канал. Подробнее: «Канал не грузится: 8 способов».'),
   ('Сайт — официальный вещатель?', 'Нет. russian-tv.com — агрегатор общедоступных прямых трансляций, видео на сайте не хранится. Правообладатели могут обратиться на сайт с просьбой убрать ссылку. Юридических консультаций о правилах просмотра в вашей провинции сайт не даёт.'),
   ('Как смотреть российский Новый год из Канады?', 'Полночь по Москве 31 декабря — 16:00 в Торонто, 14:00 в Ванкувере и 17:30 в Сент-Джонсе. Время и каналы: «Российское ТВ в новогоднюю ночь за границей».'),
  ],
  cities=[('Toronto', 'russian-tv-in-toronto'), ('Montreal', 'russian-tv-in-montreal')],
 ),
}
