#!/usr/bin/env python3
"""Генерация страниц новых каналов (RU+EN) для russian-tv-site и правка списков.
Запуск: python3 gen_site.py <путь_к_репозиторию>
Идемпотентен: повторный запуск не дублирует каналы.
"""
import re, sys, os, html

ROOT = sys.argv[1]

# cat: news ent kino kids music hobby sport
CATS = {
    'news':  dict(ru='Новости',      ru_tag='📡 Новости',      ru_page='novosti',       ru_bc='Новости',          en='News',          en_tag='📡 News'),
    'ent':   dict(ru='Развлечения',  ru_tag='🎬 Развлечения',  ru_page='razvlecheniya', ru_bc='Развлечения',      en='Entertainment', en_tag='🎬 Entertainment'),
    'kino':  dict(ru='Кино',         ru_tag='🎥 Кино',         ru_page='kino',          ru_bc='Кино каналы',      en='Movies',        en_tag='🎥 Movies'),
    'kids':  dict(ru='Детские',      ru_tag='👶 Детские',      ru_page='detskie',       ru_bc='Детские каналы',   en='Kids',          en_tag='👶 Kids'),
    'music': dict(ru='Музыка',       ru_tag='🎵 Музыка',       ru_page='muzyka',        ru_bc='Музыкальные каналы', en='Music',       en_tag='🎵 Music'),
    'hobby': dict(ru='Хобби',        ru_tag='🌿 Хобби',        ru_page='hobbi',         ru_bc='Хобби',            en='Hobby',         en_tag='🌿 Hobby'),
    'sport': dict(ru='Спорт',        ru_tag='⚽ Спорт',        ru_page='sport',         ru_bc='Спортивные каналы', en='Sport',        en_tag='⚽ Sport'),
}

# id, slug, cat, ru, en, ru_desc, en_desc, icon, color, bg, ru_kw, en_kw
CH = [
 ('spb','sankt-peterburg-live','news','Санкт-Петербург','Saint Petersburg TV','Телеканал Санкт-Петербурга','Saint Petersburg city channel','СПБ','#1565c0','#080d1a','новости Петербурга','news of St. Petersburg'),
 ('moskva24','moskva-24-live','news','Москва 24','Moskva 24','Новости и жизнь столицы','News and city life of Moscow','М24','#e53935','#1a0808','новости Москвы','Moscow news'),
 ('soyuz','soyuz-live','ent','Союз','Soyuz TV','Семейное телевидение','Family television','СОЮ','#8d6e63','#120e0a','семейное ТВ','family television'),
 ('prima','prima-live','ent','Прима','Prima','Развлекательный канал','Entertainment channel','ПРИ','#ad1457','#180810','развлекательное ТВ','entertainment'),
 ('ryzhiy','ryzhiy-live','kids','Рыжий','Ryzhiy','Развлекательный канал','Entertainment channel','РЫЖ','#e65100','#1a0e08','развлекательное ТВ','entertainment'),
 ('bober','bober-live','hobby','Бобер','Bober','Развлекательный канал','Entertainment channel','БОБ','#8d6e63','#120e0a','развлекательное ТВ','entertainment'),
 ('detektiv','chestnyy-detektiv-live','kino','Честный детектив','Chestnyy Detektiv','Детективы и криминал','Detective and crime programming','ЧД','#546e7a','#0c1216','детективы и криминал','detective and crime'),
 ('rtdoc','rt-documentary-live','ent','RT Documentary','RT Documentary (Russian)','Документальные фильмы на русском','Documentaries in Russian','RTD','#c62828','#180808','документальные фильмы','documentary films'),
 ('karuselIntl','karusel-international-live','kids','Карусель International','Karusel International','Для малышей и детей','For toddlers and kids','КИ','#ff6f00','#1a1200','детские передачи','kids programming'),
 ('muzsoyuz','muz-soyuz-live','music','Муз Союз','Muz Soyuz','Музыка и клипы','Music and video clips','МС','#e91e63','#1a0a10','музыка и клипы','music and clips'),
 ('fonmusic','fon-music-live','music','FON Music','FON Music','Музыкальные клипы','Music video clips','FON','#7b1fa2','#130a18','музыкальные клипы','music video clips'),
 ('stranafm','strana-fm-live','music','Страна FM','Strana FM','Радио — аудио-эфир','Radio — live audio','FM','#e53935','#1a0808','радио','radio'),
 ('vestifm','vesti-fm-live','music','Вести FM','Vesti FM','Радио — новости и аналитика','Radio — news and analysis','ВФМ','#1565c0','#0a0f1a','радио Вести FM','Vesti FM radio'),
 ('moymir','moy-mir-live','hobby','Мой мир','Moy Mir','Познавательное телевидение','Educational television','МИР','#00897b','#081412','познавательное ТВ','educational TV'),
 ('priklyucheniya','priklyucheniya-live','hobby','Приключения','Priklyucheniya (Adventure)','Приключения и путешествия','Adventure and travel','ПРК','#f57f17','#1a1200','приключения и путешествия','adventure and travel'),
 ('tochka','tochka-otryva-live','hobby','Точка отрыва','Tochka Otryva','Экстрим и приключения','Extreme and adventure','ТО','#c62828','#180808','экстрим и приключения','extreme and adventure'),
 ('planeta','zhivaya-planeta-live','hobby','Живая планета','Zhivaya Planeta','Природа и животные','Nature and wildlife','ЖП','#2e7d32','#081208','природа и животные','nature and wildlife'),
 ('zoopark','zoopark-live','hobby','Зоопарк','Zoopark','Животные 24/7','Animals 24/7','ЗОО','#558b2f','#0c1408','передачи о животных','animal programming'),
 ('zhivotnye','domashnie-zhivotnye-live','hobby','Домашние животные','Domashnie Zhivotnye (Pets)','Всё о домашних питомцах','Everything about pets','ДЖ','#558b2f','#0c1408','передачи о питомцах','pet programming'),
 ('drive','drive-live','hobby','Драйв','Drive','Авто и мото','Cars and motorcycles','ДРВ','#37474f','#0d1214','авто и мото','cars and motorcycles'),
 ('zdorovoe','zdorovoe-tv-live','hobby','Здоровое ТВ','Zdorovoe TV','Здоровье и образ жизни','Health and lifestyle','ЗТВ','#00897b','#081412','здоровье и образ жизни','health and lifestyle'),
 ('bigplanet','bolshaya-planeta-live','hobby','Большая планета','Bolshaya Planeta (Big Planet)','Путешествия и природа','Travel and nature','БП','#2e7d32','#081208','путешествия и природа','travel and nature'),
 ('sportivnyy','sportivnyy-live','sport','Спортивный','Sportivny','Спорт 24/7','Sport 24/7','СПО','#d84315','#1a0d08','спорт','sports'),
 ('tracesport','trace-sport-stars-live','sport','Trace Sport Stars','Trace Sport Stars (Russian)','Звёзды спорта','Sports stars','TSS','#0277bd','#080d1a','звёзды спорта','sports stars'),
]
KEYS = ['id','slug','cat','ru','en','ru_desc','en_desc','icon','color','bg','ru_kw','en_kw']
CHANNELS = [dict(zip(KEYS, t)) for t in CH]


MORE = {
 'moskva24': ('Новости, события и жизнь Москвы в прямом эфире.','News, events and daily life in Moscow, live.'),
 'spb': ('Региональный телеканал Санкт-Петербурга: городские новости, события и жизнь северной столицы.','A regional channel for Saint Petersburg: city news, events and life in the northern capital.'),
 'soyuz': ('Семейный телеканал с программами для зрителей разного возраста.','A family channel with programming for viewers of all ages.'),
 'prima': ('Развлекательный телеканал: передачи и программы для отдыха.','An entertainment channel: shows and programmes for relaxing.'),
 'ryzhiy': ('Развлекательный телеканал: передачи и программы для отдыха.','An entertainment channel: shows and programmes for relaxing.'),
 'bober': ('Развлекательный телеканал: передачи и программы для отдыха.','An entertainment channel: shows and programmes for relaxing.'),
 'detektiv': ('Подборки детективных и криминальных историй и расследований.','Selections of detective and crime stories and investigations.'),
 'rtdoc': ('Документальные фильмы и программы на русском языке.','Documentary films and programmes in Russian.'),
 'karuselIntl': ('Международная версия детского канала «Карусель»: мультфильмы и развивающие передачи.','The international version of the kids channel Karusel: cartoons and educational programmes.'),
 'muzsoyuz': ('Музыкальный канал: клипы и хиты в прямом эфире.','A music channel: video clips and hits, live.'),
 'fonmusic': ('Музыкальный канал с клипами в прямом эфире 24/7.','A music channel with video clips, live 24/7.'),
 'stranafm': ('Радиоэфир в формате онлайн-трансляции: музыка в прямом эфире. Видеоряд может отсутствовать — это радио.','A radio broadcast as an online stream: live music. Video may be absent — this is radio.'),
 'vestifm': ('Радио «Вести FM»: новости и аналитика в прямом эфире. Видеоряд может отсутствовать — это радиоэфир.','Vesti FM radio: live news and analysis. Video may be absent — this is a radio broadcast.'),
 'moymir': ('Познавательный телеканал: передачи о мире, науке и жизни.','An educational channel: programmes about the world, science and life.'),
 'priklyucheniya': ('Передачи о приключениях, путешествиях и необычных местах.','Programmes about adventure, travel and unusual places.'),
 'tochka': ('Экстремальные виды спорта, активный отдых и приключения.','Extreme sports, outdoor activities and adventure.'),
 'planeta': ('Передачи о природе и животном мире планеты.','Programmes about nature and wildlife around the planet.'),
 'zoopark': ('Передачи о животных и зоопарках.','Programmes about animals and zoos.'),
 'zhivotnye': ('Передачи о домашних питомцах: уход, повадки, истории.','Programmes about pets: care, behaviour and stories.'),
 'drive': ('Передачи об автомобилях, мотоциклах и технике.','Programmes about cars, motorcycles and machines.'),
 'zdorovoe': ('Передачи о здоровье, медицине и здоровом образе жизни.','Programmes about health, medicine and a healthy lifestyle.'),
 'bigplanet': ('Путешествия, природа и страны мира.','Travel, nature and countries of the world.'),
 'sportivnyy': ('Спортивные трансляции и передачи.','Sports broadcasts and programmes.'),
 'tracesport': ('Передачи о звёздах спорта и спортивной культуре.','Programmes about sports stars and sports culture.'),
}

RU_LABEL = {k: v['ru'] for k, v in CATS.items()}                 # RU sidebar labels
EN_LABEL = {'news':'📡 News','ent':'🎬 Entertainment','kino':'🎥 Movies','kids':'👶 Kids','music':'🎵 Music','hobby':'🌿 Hobby','sport':'⚽ Sport'}

def rd(p):
    with open(os.path.join(ROOT, p), encoding='utf-8') as f: return f.read()
def wr(p, s):
    full = os.path.join(ROOT, p)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, 'w', encoding='utf-8') as f: f.write(s)
def esc(s): return html.escape(s, quote=True)
def lc1(s): return s if (len(s)>1 and s[1].isupper()) else s[:1].lower()+s[1:]

# ---------- сайдбар ----------
def sb_item(ch, lang, active=False):
    name = ch['ru'] if lang == 'ru' else ch['en']
    desc = ch['ru_desc'] if lang == 'ru' else ch['en_desc']
    href = f"/{ch['slug']}/" if lang == 'ru' else f"/en/{ch['slug']}/"
    cls = 'ch-item-s active' if active else 'ch-item-s'
    return (f'<a href="{href}" class="{cls}" data-name="{esc(name)}" aria-label="{esc(name)}">'
            f'<div class="ch-icon-s" style="background:{ch["bg"]};color:{ch["color"]}">{esc(ch["icon"])}</div>'
            f'<div><div class="ch-name-s">{esc(name)}</div><div class="ch-desc-s">{esc(desc)}</div></div>'
            f'<div class="live-dot-s"></div></a>')

def insert_sidebar(page, lang):
    """Добавляет недостающие новые каналы в конец своей категории сайдбара."""
    if 'id="ch-list"' not in page: return page
    for cat in CATS:
        label = RU_LABEL[cat] if lang == 'ru' else EN_LABEL[cat]
        marker = f'<div class="cat-label-s">{label}</div>'
        i = page.find(marker)
        if i < 0: continue
        j_cands = [page.find('<div class="cat-label-s">', i + len(marker)), page.find('\n    </div>\n  </aside>', i)]
        j_cands = [x for x in j_cands if x > 0]
        if not j_cands: continue
        j = min(j_cands)
        block = page[i:j]
        add = ''
        for ch in CHANNELS:
            if ch['cat'] != cat: continue
            href = f"/{ch['slug']}/" if lang == 'ru' else f"/en/{ch['slug']}/"
            if f'<a href="{href}" class="ch-item-s' in page: continue
            add += sb_item(ch, lang) + '\n'
        if add:
            block = block.rstrip('\n') + '\n' + add
            page = page[:i] + block + page[j:]
    return page

# ---------- страницы каналов ----------
SB_RE = re.compile(r'(<div class="ch-list-scroll" id="ch-list">)(.*?)(\n    </div>\n  </aside>)', re.S)
REL_RE = re.compile(r'(<div class="sim-box">\s*<h3>[^<]*</h3>)(.*?)(\n    </div>\n\n    <div class="pop-box">)', re.S)

def sim_items(lang, cat, selfslug):
    """Похожие каналы: берём из уже существующих страниц той же категории (по сайдбару)."""
    import subprocess
    p = 'kino-detektiv-live/index.html' if lang == 'ru' else 'en/kino-detektiv-live/index.html'
    sb = SB_RE.search(subprocess.run(['git','-C',ROOT,'show','827dc43:'+p],capture_output=True,text=True,encoding='utf-8',check=True).stdout).group(2)
    label = RU_LABEL[cat] if lang == 'ru' else EN_LABEL[cat]
    i = sb.find(f'<div class="cat-label-s">{label}</div>')
    j = sb.find('<div class="cat-label-s">', i + 5)
    seg = sb[i:j if j > 0 else len(sb)]
    items = re.findall(r'<a href="(/[^"]+)" class="ch-item-s[^"]*" data-name="([^"]*)"[^>]*><div class="ch-icon-s" style="([^"]*)">([^<]*)</div>', seg)
    out = []
    for href, name, style, icon in items:
        if selfslug in href: continue
        out.append((href, name, style, icon))
        if len(out) == 4: break
    for c in CHANNELS:
        if len(out) >= 4: break
        if c['cat'] != cat or c['slug'] == selfslug: continue
        out.append((f"/{c['slug']}/" if lang == 'ru' else f"/en/{c['slug']}/", c['ru'] if lang == 'ru' else c['en'], f"background:{c['bg']};color:{c['color']}", c['icon']))
    return out

def build_related(lang, ch):
    cat = CATS[ch['cat']]
    items = sim_items(lang, ch['cat'], ch['slug'])
    cn = cat['ru'] if lang == 'ru' else cat['en']
    rows = ''.join(
        f'<a href="{h}" class="sim-item"><div class="sim-icon" style="{st}">{ic}</div><div><div class="sim-name">{nm}</div><div class="sim-cat">{cn}</div></div><span class="sim-live">LIVE</span></a>\n'
        for h, nm, st, ic in items)
    return rows.rstrip('\n')

def make_page_ru(ch, T):
    n, cat = ch['ru'], CATS[ch['cat']]
    sb = SB_RE.search(T); sb_html = sb.group(2)
    rel = REL_RE.search(T)
    t = T.replace(sb.group(0), '@@SB@@').replace(rel.group(0), '@@REL@@')
    t = t.replace('Кино Детектив', n).replace('kino-detektiv-live', ch['slug']).replace("const CH_ID = 'kinodetektiv'", f"const CH_ID = '{ch['id']}'")
    desc = ch['ru_desc']
    t = t.replace('детективы онлайн без VPN', f"{ch['ru_kw']} онлайн без VPN")
    t = t.replace('детективы и криминальные фильмы в прямом эфире', f"{ch['ru_kw']} в прямом эфире")
    t = t.replace('Детективы и триллеры 24/7', desc)
    t = t.replace('Кино каналы', cat['ru_bc'])
    t = t.replace('https://russian-tv.com/kino/', f"https://russian-tv.com/{cat['ru_page']}/")
    t = t.replace('🎥 Кино', cat['ru_tag'])
    t = t.replace('<span class="cat-badge">Кино</span>', f'<span class="cat-badge">{cat["ru"]}</span>')
    t = re.sub(r'<p>' + re.escape(n) + r' — специализированный канал.*?</p>\n\s*<p>В эфире — классические.*?</p>\n\s*<p>Смотреть .*?</p>',
               f'<p>{n} — {lc1(desc)}. Прямой эфир доступен круглосуточно, без регистрации и без VPN.</p>\n'
               f'    <p>{MORE[ch["id"]][0]}</p>\n'
               f'    <p>Трансляция {n} работает на любом устройстве — компьютере, iPhone, Android и Smart TV — из любой страны мира.</p>\n'
               f'    <p>Смотреть {n} онлайн бесплатно на russian-tv.com — 24/7 без регистрации.</p>', t, flags=re.S)
    sb_new = sb_html.replace('ch-item-s active', 'ch-item-s')
    t = t.replace('@@SB@@', sb.group(1) + sb_new + sb.group(3))
    t = t.replace('@@REL@@', rel.group(1) + '\n      ' + build_related('ru', ch) + rel.group(3))
    t = insert_sidebar(t, 'ru')
    t = t.replace(f'<a href="/{ch["slug"]}/" class="ch-item-s"', f'<a href="/{ch["slug"]}/" class="ch-item-s active"')
    t = t.replace(f'<div class="lang-switch"><a href="/{ch["slug"]}/" class="active">RU</a><a href="/en/{ch["slug"]}/">EN</a></div>', f'<div class="lang-switch"><a href="/{ch["slug"]}/" class="active">RU</a><a href="/en/{ch["slug"]}/">EN</a></div>')
    return t

def make_page_en(ch, T):
    n, cat = ch['en'], CATS[ch['cat']]
    sb = SB_RE.search(T); sb_html = sb.group(2)
    rel = REL_RE.search(T)
    t = T.replace(sb.group(0), '@@SB@@').replace(rel.group(0), '@@REL@@')
    t = t.replace('Kino Detektiv', n).replace('kino-detektiv-live', ch['slug']).replace("const CH_ID = 'kinodetektiv'", f"const CH_ID = '{ch['id']}'")
    t = t.replace('Russian Detectives', ch['en_kw'][:1].upper()+ch['en_kw'][1:])
    t = t.replace('Russian detective and crime films', ch['en_kw'])
    t = t.replace('Detective films and thrillers 24/7', ch['en_desc'])
    t = t.replace('<span class="cat-badge">Movies</span>', f'<span class="cat-badge">{cat["en"]}</span>')
    t = t.replace('/en/?cat=movies" class="cat-tag">🎥 Movies', f'/en/?cat={ {"news":"news","ent":"entertainment","kino":"movies","kids":"kids","music":"music","hobby":"hobby","sport":"sport"}[ch["cat"]] }" class="cat-tag">{cat["en_tag"]}')
    t = re.sub(r'<p>' + re.escape(n) + r' is a 24/7 channel dedicated to.*?</p>\n\s*<p>On air:.*?</p>\n\s*<p>Watch .*?</p>',
               f'<p>{n} — {lc1(ch["en_desc"])}. Live 24/7, free, no VPN and no registration.</p>\n'
               f'    <p>{MORE[ch["id"]][1]}</p>\n'
               f'    <p>The {n} stream works on any device — desktop, iPhone, Android and Smart TV — from any country.</p>\n'
               f'    <p>Watch {n} online free at russian-tv.com — 24/7, no VPN, no registration.</p>', t, flags=re.S)
    t = t.replace('@@SB@@', sb.group(1) + sb_html.replace('ch-item-s active', 'ch-item-s') + sb.group(3))
    rel_items = build_related('en', ch)
    t = t.replace('@@REL@@', rel.group(1) + '\n      ' + rel_items + rel.group(3))
    t = insert_sidebar(t, 'en')
    t = t.replace(f'<a href="/en/{ch["slug"]}/" class="ch-item-s"', f'<a href="/en/{ch["slug"]}/" class="ch-item-s active"')
    return t


# ---------- главные страницы ----------
HOME_RU = {'news':'Новости','ent':'Развлечения','kino':'Кино','kids':'Детские','music':'Музыка','hobby':'Хобби','sport':'Спорт'}
HOME_EN = {'news':'News','ent':'Entertainment','kino':'Movies','kids':'Kids','music':'Music','hobby':'Hobby','sport':'Sport'}
TAGS = {'news':'новости','ent':'развлечения','kino':'кино','kids':'дети','music':'музыка','hobby':'хобби','sport':'спорт'}

def patch_home(path, lang):
    s = rd(path)
    for cat in CATS:
        lab = HOME_RU[cat] if lang == 'ru' else HOME_EN[cat]
        m = re.search(r'\n  \{ label:[\'"][^\'"\n]*' + re.escape(lab) + r'[^\'"\n]*[\'"], channels:\[\n', s)
        if not m: print('home group not found', path, lab); continue
        end = s.find('\n  ]},', m.end())
        block = s[m.end():end]
        add = ''
        for ch in CHANNELS:
            if ch['cat'] != cat or f"id:'{ch['id']}'" in block or f'id:"{ch["id"]}"' in block: continue
            if lang == 'ru':
                add += (f"    {{ id:'{ch['id']}', name:'{ch['ru']}', desc:'{ch['ru_desc']}', icon:'{ch['icon']}', color:'{ch['color']}', iconBg:'{ch['bg']}', "
                        f"tags:['{TAGS[cat]}','{ch['ru_kw']}'], slug:'{ch['slug']}' }},\n")
            else:
                add += (f'    {{ id:"{ch["id"]}", name:"{ch["ru"]}", nameEn:"{ch["en"]}", desc:"{ch["en_desc"]}", icon:"{ch["icon"]}", color:"{ch["color"]}", iconBg:"{ch["bg"]}", slug:"{ch["slug"]}" }},\n')
        if add:
            block2 = block.rstrip('\n') + '\n' + add.rstrip('\n')
            s = s[:m.end()] + block2 + s[end:]
    wr(path, s)

def decl(n):
    if n % 10 == 1 and n % 100 != 11: return 'канал'
    if 2 <= n % 10 <= 4 and not 12 <= n % 100 <= 14: return 'канала'
    return 'каналов'

def patch_category(cat):
    page = CATS[cat]['ru_page'] + '/index.html'
    s = rd(page)
    new = [c for c in CHANNELS if c['cat'] == cat and f'/{c["slug"]}/' not in s]
    if not new: return
    if cat == 'sport':
        old = len(re.findall(r'<a class="card" href=', s))
        add = ''.join(f'  <a class="card" href="https://russian-tv.com/{c["slug"]}/">\n    <div class="card-icon" style="background:{c["bg"]};color:{c["color"]}">{esc(c["icon"])}</div>\n    <h2>{esc(c["ru"])}</h2>\n    <p>{esc(c["ru_desc"])}</p>\n  </a>\n' for c in new)
        i = s.find('</div>', s.rfind('<a class="card"'))
        s = s[:i] + add.lstrip(' ').replace('<a class="card"', '<a class="card"', 1) + s[i:] if False else s[:s.find('\n</div>', s.rfind('<a class="card"'))] + '\n' + add.rstrip('\n') + s[s.find('\n</div>', s.rfind('<a class="card"')):]
        n = old + len(new)
        s = re.sub(r'\b%d (спортивных (?:каналов|телеканалов))' % old, lambda m: f'{n} {m.group(1)}', s)
        s = s.replace('"numberOfItems": %d' % old, '"numberOfItems": %d' % n)
        last = s.rfind('{"@type":"ListItem","position":%d' % old)
        e = s.find('\n', last)
        items = ''.join(f',\n          {{"@type":"ListItem","position":{old+k+1},"name":"{c["ru"]}","url":"https://russian-tv.com/{c["slug"]}/"}}' for k, c in enumerate(new))
        s = s[:e].rstrip() + items + s[e:] if s[:e].rstrip().endswith('}') else s
    else:
        old = len(re.findall(r'class="cat-ch-card">', s))
        add = ''.join(f'\n        <a href="/{c["slug"]}/" class="cat-ch-card">\n          <div class="cat-ch-icon" style="background:{c["bg"]};color:{c["color"]}">{esc(c["icon"])}</div>\n          <div class="cat-ch-name">{esc(c["ru"])}</div>\n          <div class="cat-ch-desc">{esc(c["ru_desc"])}</div>\n          <div class="cat-ch-live"><span class="cat-live-dot"></span>LIVE</div>\n        </a>\n' for c in new)
        last = s.rfind('class="cat-ch-card">')
        e = s.find('</a>', last) + 4
        s = s[:e] + '\n' + add.rstrip('\n') + s[e:]
        n = old + len(new)
        s = re.sub(r'\b%d (канал(?:а|ов)?)\b' % old, lambda m: f'{n} {decl(n)}', s)
        s = re.sub(r'\b%d (новостных каналов)' % old, lambda m: f'{n} {m.group(1)}', s)
        s = s.replace('"numberOfItems": %d' % old, '"numberOfItems": %d' % n)
    wr(page, s)

def patch_sitemap():
    s = rd('sitemap.xml')
    add = ''
    for c in CHANNELS:
        for loc in (f'https://russian-tv.com/{c["slug"]}/', f'https://russian-tv.com/en/{c["slug"]}/'):
            if f'<loc>{loc}</loc>' in s: continue
            add += f'  <url><loc>{loc}</loc><changefreq>weekly</changefreq><priority>0.7</priority><lastmod>2026-10-09</lastmod></url>\n'
    if add: s = s.replace('</urlset>', add + '</urlset>')
    wr('sitemap.xml', s)

def main():
    import subprocess
    def tpl(p):
        return subprocess.run(['git','-C',ROOT,'show','827dc43:'+p],capture_output=True,text=True,encoding='utf-8',check=True).stdout
    T_RU = tpl('kino-detektiv-live/index.html')
    T_EN = tpl('en/kino-detektiv-live/index.html')
    # 1. новые страницы
    for ch in CHANNELS:
        wr(f'{ch["slug"]}/index.html', make_page_ru(ch, T_RU))
        wr(f'en/{ch["slug"]}/index.html', make_page_en(ch, T_EN))
    # 2. сайдбар на всех остальных страницах каналов
    new_slugs = {c['slug'] for c in CHANNELS}
    changed = 0
    for base, lang in (('', 'ru'), ('en/', 'en')):
        d = os.path.join(ROOT, base) if base else ROOT
        for name in sorted(os.listdir(d)):
            if name in new_slugs or not name.endswith('-live'): continue
            p = f'{base}{name}/index.html'
            if not os.path.exists(os.path.join(ROOT, p)): continue
            s = rd(p)
            s2 = insert_sidebar(s, lang)
            if s2 != s: wr(p, s2); changed += 1
    print('sidebars updated:', changed)
    patch_home('index.html','ru'); patch_home('en/index.html','en')
    for cat in CATS: patch_category(cat)
    patch_sitemap()

if __name__ == '__main__':
    main()
