#!/usr/bin/env bash
# Полная пересборка страниц сайта из списка каналов (tools/gen_site.py → CH) и общих скриптов.
# Использование:  tools/run_all.sh [корень_репозитория]      (по умолчанию — текущая папка)
# Требуется: python3, node; для gen_og.py — Pillow (pip install pillow, при необходимости PYTHONPATH=<путь>).
# Все шаги идемпотентны: повторный запуск ничего не меняет, если данные не менялись.
set -euo pipefail
ROOT="${1:-.}"
T="$(cd "$(dirname "$0")" && pwd)"
run() { echo "→ $1"; python3 "$T/$1" "$ROOT"; }

run gen_site.py        # страницы новых каналов (RU+EN), боковые списки, главные, категории, sitemap
run gen_rename.py      # «Кино Детектив» → «Viju TV1000 Русское кино» (закреплённое переименование)
run gen_legal.py       # оговорка для правообладателей в подвале, политика RU/EN
run gen_ads.py         # контакт, страницы для рекламодателей, ссылка в подвале
run gen_consent.py     # убирает встроенные трекеры, подключает assets/consent.js
run gen_encat.py       # EN-страницы категорий, hreflang на RU-категориях
run gen_seo.py         # og:image, число каналов, hreflang в sitemap, ссылки на главной, ItemList, 404
run gen_ux.py          # хлебные крошки с категорией, размеры логотипов, лента каналов для телефонов
run gen_og.py || echo "  (пропущено: нужен Pillow для OG-картинок)"
run gen_blog.py        # статьи блога RU/EN и индексы блога
run gen_quality.py     # выбор качества (hls.js и нативный HLS)
run gen_playerui.py    # единая панель плеера
run gen_homeplayer.py  # те же скрипты и настройки hls.js на главных
run gen_counts.py      # числа каналов на страницах категорий

# версии скриптов в адресах (сброс кеша браузера) для страниц, созданных заново
python3 - "$ROOT" <<'PY'
import sys, glob, os
root = sys.argv[1]
for f in glob.glob(os.path.join(root, '**/*.html'), recursive=True):
    s = open(f, encoding='utf-8').read(); o = s
    s = s.replace('<script src="/assets/consent.js"></script>', '<script src="/assets/consent.js?v=2"></script>')
    if s != o: open(f, 'w', encoding='utf-8').write(s)
PY
echo "готово"
