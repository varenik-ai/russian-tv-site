#!/usr/bin/env python3
"""Тексты «О канале» для каналов с шаблонным описанием (аудит 18.10.2026) + честный ответ про качество в FAQ.

Для 24 каналов шаблонный блок из 4 абзацев заменяется своим текстом: уникальное вступление, уточнение о содержании
и строка «В той же категории» (формируется из кольца «Похожие каналы», поэтому у каждой страницы своя).
Факты ограничены тем, что известно из каталога (название, категория, формат: ТВ или радио) — без выдуманных дат и цифр.
Тексты стоит перечитать владельцу сайта и дополнить сведениями, которые он знает о каналах.
Идемпотентно: блок распознаётся по маркеру data-about="1".
"""
import sys, os, re, json

ROOT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else '.')


def rd(p):
    return open(os.path.join(ROOT, p), encoding='utf-8').read()


def wr(p, s):
    open(os.path.join(ROOT, p), 'w', encoding='utf-8').write(s)


# slug: (RU вступление, RU уточнение, EN вступление, EN уточнение). {n} — название канала на странице
T = {
    'bober-live': (
        '«{n}» — развлекательный телеканал из категории «Хобби и стиль»: передачи и программы для отдыха и досуга, которые удобно включать фоном.',
        'Подходит для спокойного вечернего просмотра: не нужно следить за каждым выпуском, поэтому канал удобно оставлять включённым.',
        '{n} is an entertainment channel in our Hobby & Lifestyle category: leisure programmes that are easy to leave on in the background.',
        'It suits relaxed evening viewing — you do not need to follow every episode, so it is easy to keep running.'),
    'bolshaya-planeta-live': (
        '«{n}» — познавательный канал о путешествиях, странах и природе: передачи, которые показывают места и культуры со всего мира.',
        'Хороший выбор для семейного просмотра и для тех, кто хочет увидеть страны, куда пока не добраться самому.',
        '{n} is an educational channel about travel, countries and nature, showing places and cultures from around the world.',
        'A good choice for family viewing, and for anyone who wants to see countries they cannot visit yet.'),
    'chestnyy-detektiv-live': (
        '«{n}» — канал детективов и криминальных историй: подборки расследований и сериалов о раскрытии преступлений.',
        'Если вы предпочитаете детективный жанр, здесь он в центре эфира, а не одна из рубрик общего канала.',
        '{n} is a channel of detective and crime stories — investigations and series about solving crimes.',
        'If you prefer the detective genre, it is the focus of the schedule here rather than one section of a general channel.'),
    'domashnie-zhivotnye-live': (
        '«{n}» — канал о домашних питомцах: передачи про уход, повадки животных и истории из жизни владельцев.',
        'Будет интересен тем, у кого дома кошка, собака или другой питомец, и детям, которые любят наблюдать за животными.',
        '{n} is a channel about pets: programmes on care, animal behaviour and stories from owners.',
        'Of interest to anyone with a cat, dog or other pet at home, and to children who like watching animals.'),
    'drive-live': (
        '«{n}» — канал об автомобилях и мотоциклах: передачи о технике, дорогах и автомобильной культуре.',
        'Подойдёт тем, кто следит за автомобильной темой и любит смотреть обзоры техники в прямом эфире.',
        '{n} is a channel about cars and motorcycles: programmes about vehicles, roads and motoring culture.',
        'It fits viewers who follow the motoring world and enjoy vehicle features in a live schedule.'),
    'fon-music-live': (
        '«{n}» — музыкальный канал с клипами в круглосуточном эфире.',
        'Удобен как фон для работы или домашних дел: клипы идут подряд, без сюжета, который нужно отслеживать.',
        '{n} is a music channel that plays clips around the clock.',
        'Handy as background for work or housework: clips run one after another, with no plot to follow.'),
    'karusel-international-live': (
        '«{n}» — международная версия детского канала «Карусель»: мультфильмы и развивающие передачи для малышей и школьников.',
        'Выбор для семей за рубежом, где детям важно слышать русскую речь: канал помогает поддерживать язык в игровой форме.',
        '{n} is the international version of the children’s channel Karusel, with cartoons and educational programmes for toddlers and schoolchildren.',
        'A choice for families abroad who want their children to hear Russian: the channel helps keep the language going through play.'),
    'moskva-24-live': (
        '«{n}» — городской телеканал о Москве: новости, события, транспорт, погода и жизнь столицы.',
        'Полезен тем, кто следит за московскими новостями и хочет видеть повседневную жизнь города, а не только федеральную повестку.',
        '{n} is a city channel about Moscow: news, events, transport, weather and life in the capital.',
        'Useful for anyone following Moscow news who wants everyday city life rather than only the national agenda.'),
    'moy-mir-live': (
        '«{n}» — познавательный телеканал: передачи о мире, науке и жизни.',
        'Подойдёт для вечернего просмотра всей семьёй, когда хочется узнать что-то новое, а не смотреть сериалы.',
        '{n} is an educational channel with programmes about the world, science and life.',
        'Suited to evening family viewing when you want to learn something new rather than watch series.'),
    'muz-soyuz-live': (
        '«{n}» — музыкальный канал: клипы и хиты в прямом эфире.',
        'Хороший вариант, когда нужна музыка в фоне: клипы и хиты идут подряд, без пауз на длинные передачи.',
        '{n} is a music channel with clips and hits on air.',
        'A good option when you need music in the background: clips and hits follow one another without long programmes in between.'),
    'priklyucheniya-live': (
        '«{n}» — канал о приключениях и путешествиях: передачи о необычных местах и маршрутах.',
        'Для тех, кто любит смотреть, как люди открывают новые места, и хочет вдохновения для собственной поездки.',
        '{n} is a channel about adventure and travel: programmes on unusual places and routes.',
        'For viewers who enjoy watching people discover new places and want inspiration for a trip of their own.'),
    'prima-live': (
        '«{n}» — развлекательный телеканал в категории «Развлечения»: программы и передачи для отдыха.',
        'Хороший вариант, если нужен лёгкий эфир без новостной повестки для вечернего расслабления.',
        '{n} is an entertainment channel in our Entertainment category, with programmes for relaxing.',
        'A good option when you want light viewing without a news agenda for the evening.'),
    'rt-documentary-live': (
        '«{n}» — документальный канал RT на русском языке: фильмы и программы о политике, истории, науке и обществе.',
        'Подойдёт любителям документального кино, которые хотят смотреть цикл фильмов в потоке, а не выбирать каждый вручную.',
        '{n} is RT’s Russian-language documentary channel: films and programmes on politics, history, science and society.',
        'Suited to documentary fans who want a stream of films rather than choosing each one by hand.'),
    'ryzhiy-live': (
        '«{n}» — детский развлекательный канал: передачи и программы для детей.',
        'Родителям удобно включить его, когда ребёнок просит что-нибудь посмотреть: канал относится к детской категории сайта.',
        '{n} is a children’s entertainment channel with programmes for kids.',
        'Convenient for parents when a child asks for something to watch: the channel belongs to the site’s kids category.'),
    'sankt-peterburg-live': (
        '«{n}» — региональный телеканал Санкт-Петербурга: городские новости, события и жизнь северной столицы.',
        'Подходит жителям и бывшим жителям города и всем, кого интересует Петербург: местная повестка, а не федеральные новости.',
        '{n} is the regional channel of Saint Petersburg: city news, events and life in the northern capital.',
        'For current and former residents and anyone interested in Petersburg: local news rather than the national agenda.'),
    'soyuz-live': (
        '«{n}» — семейный телеканал с программами для зрителей разного возраста.',
        'Выбор для просмотра всей семьёй: на канале собраны передачи, которые можно смотреть вместе с детьми и старшим поколением.',
        '{n} is a family channel with programmes for viewers of different ages.',
        'A choice for the whole family: the schedule is built from programmes that can be watched together with children and older relatives.'),
    'sportivnyy-live': (
        '«{n}» — спортивный телеканал: трансляции и передачи о спорте.',
        'Подойдёт болельщикам, которые хотят следить за спортивным эфиром в потоке, а не искать отдельные трансляции.',
        '{n} is a sports channel with broadcasts and programmes about sport.',
        'For fans who want to follow a sports schedule as a stream rather than hunt for individual broadcasts.'),
    'strana-fm-live': (
        '«{n}» — радиостанция в формате онлайн-трансляции: музыка в прямом эфире.',
        'Это радио, поэтому видеоряда может не быть — звук идёт как обычный радиоэфир, и канал удобно слушать, свернув страницу.',
        '{n} is a radio station broadcast online: music on air.',
        'This is radio, so there may be no picture — the audio plays as a normal radio feed and you can listen with the page minimised.'),
    'tochka-otryva-live': (
        '«{n}» — канал об экстриме и приключениях: экстремальные виды спорта, активный отдых и путешествия.',
        'Для тех, кому нравятся динамичные кадры и истории о людях, которые выходят за рамки привычного.',
        '{n} is a channel about extreme sport and adventure: extreme sports, outdoor recreation and travel.',
        'For viewers who like dynamic footage and stories of people who go beyond the ordinary.'),
    'trace-sport-stars-live': (
        '«{n}» — спортивный канал о звёздах спорта и спортивной культуре.',
        'Подходит тем, кого интересуют люди спорта и спортивная культура, а не только результаты отдельных матчей.',
        '{n} is a sports channel about sport stars and sporting culture.',
        'Suits viewers interested in the people behind sport and in sporting culture, not only in match results.'),
    'vesti-fm-live': (
        '«{n}» — радиостанция: новости и аналитика в прямом эфире.',
        'Это радиоэфир, поэтому видеоряда может не быть: канал удобно слушать в фоне, пока заняты другим делом.',
        '{n} is a radio station with news and analysis on air.',
        'This is a radio feed, so there may be no picture — handy to listen to in the background while you do something else.'),
    'zdorovoe-tv-live': (
        '«{n}» — канал о здоровье и образе жизни: передачи о медицине, профилактике и здоровых привычках.',
        'Полезен тем, кто хочет разобраться в вопросах самочувствия, но помните: передачи не заменяют консультацию врача.',
        '{n} is a channel about health and lifestyle: programmes on medicine, prevention and healthy habits.',
        'Useful if you want to understand health questions — but remember that the programmes do not replace a doctor’s advice.'),
    'zhivaya-planeta-live': (
        '«{n}» — канал о природе и животном мире планеты: передачи о диких животных и экосистемах.',
        'Хорошо подходит для семейного просмотра: красивая картинка и познавательные сюжеты нравятся и детям, и взрослым.',
        '{n} is a channel about nature and the planet’s wildlife: programmes on wild animals and ecosystems.',
        'Good for family viewing: striking pictures and educational stories appeal to both children and adults.'),
    'zoopark-live': (
        '«{n}» — канал о животных и зоопарках: передачи о жизни обитателей зоопарков и заповедников.',
        'Любимый формат детей: можно включить, когда нужно занять ребёнка чем-то спокойным и познавательным.',
        '{n} is a channel about animals and zoos: programmes about the life of zoo and reserve animals.',
        'A favourite format with children: switch it on when you need something calm and educational for a child.'),
}

CTA_RU = 'Смотреть {n} онлайн бесплатно на russian-tv.com — прямой эфир 24/7 без регистрации.'
CTA_EN = 'Watch {n} online free at russian-tv.com — live 24/7, no registration.'
NEIGH_RU = 'В той же категории: {l}.'
NEIGH_EN = 'More in the same category: {l}.'

DESC_BOX = re.compile(r'(<div class="desc-box">\s*<h2>[^<]*</h2>\s*<div class="cat-tag-wrap">.*?</div>\s*)(.*?)(\s*</div>\s*\n\s*<div class="faq-box">)', re.S)
changed = 0


def sim_names(t):
    box = re.search(r'<div class="sim-box">(.*?)</div>\s*\n\s*<div class="pop-box">', t, re.S)
    return re.findall(r'<div class="sim-name">([^<]*)</div>', box.group(1)) if box else []


for slug, (ru1, ru2, en1, en2) in T.items():
    for en in (False, True):
        rel = ('en/' if en else '') + slug + '/index.html'
        p = os.path.join(ROOT, rel)
        if not os.path.exists(p):
            continue
        t = rd(rel); o = t
        m = DESC_BOX.search(t)
        if not m:
            print('нет блока', rel); continue
        h2 = re.search(r'<h2>(?:О канале|About) ([^<]*)</h2>', m.group(0))
        name = h2.group(1).strip() if h2 else slug
        sims = sim_names(t)
        paras = [(en1 if en else ru1).replace('{n}', name), (en2 if en else ru2),
                 (NEIGH_EN if en else NEIGH_RU).replace('{l}', ', '.join(sims)) if sims else None,
                 (CTA_EN if en else CTA_RU).replace('{n}', name)]
        body = '\n    '.join('<p>%s</p>' % x for x in paras if x)
        marker = '<!--about-->'
        new = m.group(1) + marker + body + m.group(3)
        t = t[:m.start()] + new + t[m.end():]
        if t != o:
            wr(rel, t); changed += 1

# FAQ: честный ответ про качество на всех страницах каналов (вместо «HD-качестве»)
QUAL_RU = re.compile(r'(?<=[>"])[^<>"]{1,60} транслируется в HD-качестве\. Рекомендуем интернет от 5 Мбит/с для стабильного просмотра\.')
QUAL_EN = re.compile(r'(?<=[>"])The stream is broadcast in HD quality\. We recommend a connection of at least 5 Mbps for stable viewing\.')
NEW_RU = 'Качество зависит от источника трансляции и вашего интернета. Если у канала несколько уровней качества, в плеере появляется кнопка ⚙ — при слабой связи выберите уровень ниже.'
NEW_EN = 'Quality depends on the stream source and your connection. If the channel offers several quality levels, a ⚙ button appears in the player — pick a lower level on a slow connection.'
qn = 0
for f in os.listdir(ROOT):
    pass
for dirpath, dirs, files in os.walk(ROOT):
    if '/tools' in dirpath or '/node_modules' in dirpath or '/.git' in dirpath:
        continue
    if 'index.html' not in files:
        continue
    p = os.path.join(dirpath, 'index.html')
    t = open(p, encoding='utf-8').read(); o = t
    t = QUAL_RU.sub(NEW_RU, t); t = QUAL_EN.sub(NEW_EN, t)
    if t != o:
        open(p, 'w', encoding='utf-8').write(t); qn += 1
print('тексты каналов: %d страниц, FAQ про качество: %d страниц' % (changed, qn))
