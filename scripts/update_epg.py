#!/usr/bin/env python3
"""
update_epg.py — тянет публичный XMLTV-гид iptvx.one, находит наши каналы по
display-name и формирует компактный epg.json на "сегодня" (по МСК).

Запускается по расписанию через GitHub Actions (.github/workflows/update-epg.yml),
не на Cloudflare Worker — там лимит 10мс CPU на бесплатном плане, парсинг
многомегабайтного XML туда физически не влезает.

Каналы, для которых в гиде нет данных (7 нишевых зарубежных спортивных
трансляций — это круглосуточные потоки без сетки передач), просто
отсутствуют в результате — фронтенд в этом случае прячет виджет, а не
показывает выдуманные данные.
"""
import json
import re
import sys
import urllib.request
import gzip
import io
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from xml.etree import ElementTree as ET

EPG_URL = "https://iptvx.one/EPG_NOARCH"
MSK = ZoneInfo("Europe/Moscow")
OUTPUT_PATH = "epg.json"

# внутренний CH_ID (совпадает с ключами STREAMS в russia-worker.js) -> варианты
# отображаемого имени канала в гиде (регистр не важен, ищем точное совпадение,
# затем — вхождение подстроки как запасной вариант)
CHANNEL_ALIASES = {
    "perviy":        ["Первый канал", "Первый"],
    "rossiya1":      ["Россия 1", "Russia 1", "РОССИЯ 1"],
    "ntv":           ["НТВ"],
    "ntv_hit":       ["НТВ Хит", "НТВ+", "NTV Hit", "NTV+"],
    "rossiya24":     ["Россия 24", "Russia 24", "Вести 24", "Россия-24"],
    "pyatyy":        ["Пятый канал", "5 канал"],
    "tvc":           ["ТВЦ", "ТВ Центр", "TVC"],
    "zvezda":        ["Звезда", "Zvezda", "ТВ Звезда"],
    "mir":           ["МИР", "Mir"],
    "ch360":         ["360°", "360 Подмосковье", "Канал 360", "360 Новости"],
    "t24":           ["T24", "Т24"],
    "tnt":           ["ТНТ"],
    "soloviev":      ["Соловьёв LIVE", "Соловьев Live", "Соловьёв Live", "Solovyov Live"],
    "istoriya":      ["История", "Istoriya"],
    "domkino":       ["Дом Кино", "Дом кино"],
    "kinohit":       ["Кинохит"],
    "retro":         ["Ретро"],
    "kinokomediya":  ["Кинокомедия"],
    "kinopremiera":  ["Кинопремьера"],
    "viju":          ["Viju TV1000", "TV 1000", "TV1000"],
    "nasheKino":     ["Наше кино"],
    "rodnoeKino":    ["Родное кино"],
    "kinopokaz":     ["Кинопоказ"],
    "kinosvidanie":  ["Киносвидание"],
    "indiyskoekino": ["Индийское кино"],
    "karusel":       ["Карусель"],
    "mult":          ["Мульт"],
    "muztv":         ["МУЗ-ТВ", "Муз-ТВ", "MUZ-TV", "МУЗ ТВ"],
    "muzykaPervogo": ["Музыка Первого"],
    "rutv":          ["RU.TV", "RU TV"],
    "ohotarybalka":  ["Охота и рыбалка"],
    "zagorodnaya":   ["Загородная жизнь"],
    "unikum":        ["Уникум"],
    # floHockey, floRacing, vijuSport, m1mma, redbull, unbeaten, freesports —
    # намеренно не включены: круглосуточные зарубежные потоки без сетки вещания.
}


def fetch_epg_bytes(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        raw = resp.read()
    # некоторые раздачи EPG отдают gzip даже без .gz в пути
    if raw[:2] == b"\x1f\x8b":
        raw = gzip.decompress(raw)
    return raw


def parse_xmltv_time(s):
    # формат XMLTV: "20260831120000 +0300"
    m = re.match(r"(\d{14})\s*([+-]\d{4})?", s.strip())
    if not m:
        return None
    dt = datetime.strptime(m.group(1), "%Y%m%d%H%M%S")
    offset = m.group(2) or "+0000"
    sign = 1 if offset[0] == "+" else -1
    oh, om = int(offset[1:3]), int(offset[3:5])
    from datetime import timezone
    tz = timezone(sign * timedelta(hours=oh, minutes=om))
    return dt.replace(tzinfo=tz)


def main():
    print(f"Fetching {EPG_URL} ...", file=sys.stderr)
    raw = fetch_epg_bytes(EPG_URL)
    print(f"Fetched {len(raw)} bytes, parsing XML...", file=sys.stderr)

    root = ET.fromstring(raw)

    # 1. Собираем display-name -> channel id из гида
    guide_names_by_id = {}
    for ch in root.findall("channel"):
        cid = ch.get("id")
        if not cid:
            continue
        names = [dn.text.strip() for dn in ch.findall("display-name") if dn.text]
        guide_names_by_id[cid] = names

    # 2. Матчим наши каналы на id гида
    matched = {}  # internal_id -> guide channel id
    for internal_id, aliases in CHANNEL_ALIASES.items():
        found = None
        # точное совпадение в приоритете
        for cid, names in guide_names_by_id.items():
            if any(n.strip().lower() in [a.lower() for a in aliases] for n in names):
                found = cid
                break
        if not found:
            # запасной вариант — вхождение подстроки
            for cid, names in guide_names_by_id.items():
                for n in names:
                    if any(a.lower() in n.lower() for a in aliases):
                        found = cid
                        break
                if found:
                    break
        if found:
            matched[internal_id] = found
        else:
            print(f"WARN: no guide match for '{internal_id}' ({aliases})", file=sys.stderr)

    print(f"Matched {len(matched)}/{len(CHANNEL_ALIASES)} channels", file=sys.stderr)

    guide_id_to_internal = {v: k for k, v in matched.items()}

    # 3. Собираем programme-блоки для совпавших каналов
    now = datetime.now(MSK)
    day_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    day_end = day_start + timedelta(days=1)
    # берём чуть шире (вчера вечер — завтра утро), чтобы не потерять
    # передачу, начавшуюся вчера и идущую сейчас
    window_start = day_start - timedelta(hours=6)
    window_end = day_end + timedelta(hours=6)

    programmes = {k: [] for k in matched}

    for pr in root.findall("programme"):
        cid = pr.get("channel")
        internal_id = guide_id_to_internal.get(cid)
        if not internal_id:
            continue
        start = parse_xmltv_time(pr.get("start", ""))
        stop = parse_xmltv_time(pr.get("stop", ""))
        if not start or not stop:
            continue
        if stop < window_start or start > window_end:
            continue
        title_el = pr.find("title")
        title = title_el.text.strip() if title_el is not None and title_el.text else "Без названия"
        programmes[internal_id].append({
            "title": title,
            "start": start.astimezone(MSK).isoformat(),
            "stop": stop.astimezone(MSK).isoformat(),
        })

    for k in programmes:
        programmes[k].sort(key=lambda p: p["start"])

    # оставляем только каналы, для которых реально нашлись передачи
    channels_out = {k: v for k, v in programmes.items() if v}

    output = {
        "generated_at": now.isoformat(),
        "source": EPG_URL,
        "channels": channels_out,
    }

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, separators=(",", ":"))

    print(f"Wrote {OUTPUT_PATH}: {len(channels_out)} channels with data", file=sys.stderr)


if __name__ == "__main__":
    main()
