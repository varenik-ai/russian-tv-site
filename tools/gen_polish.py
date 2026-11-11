#!/usr/bin/env python3
"""Правки 11.11.2026 (вечер), идемпотентно. Запускать после gen_fixtext.py.
1) Число каналов в текстах, которые не поймали прежние шаблоны (41/42/40/35/60 -> 54) с правильным склонением:
   «Смотрите 54 русских канала», «к 54 русским телеканалам», «потоки 54 телеканалов», EN «54 live Russian channels».
2) Указание автора логотипа «Москва 24» (CC BY-SA 4.0) на странице /about/ — лицензия требует атрибуции.
3) /about/: «42 телеканалов» -> 54 (то же правило)."""
import sys, os, re, glob, urllib.parse
ROOT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else '.')
N = 54
OLD = r'(?:3[0-9]|4[0-9]|6[01])'          # старые значения (число каналов не бывает 54 в старых текстах)
changed = 0

def count_fix(s):
    # родительный падеж (после «просмотру», «потоки»): каналов / телеканалов
    s = re.sub(r'(просмотру|потоки) %s (российских|русских) (каналов|телеканалов)' % OLD,
               lambda m: f'{m.group(1)} {N} {m.group(2)} {m.group(3)}', s)
    s = re.sub(r'(потоки) %s телеканалов' % OLD, lambda m: f'{m.group(1)} {N} телеканалов', s)
    # дательный падеж
    s = re.sub(r'к %s (русскому|российскому) телеканалу' % OLD,
               lambda m: 'к %d %s телеканалам' % (N, 'русским' if m.group(1) == 'русскому' else 'российским'), s)
    # именительный/винительный: «54 русских канала»
    s = re.sub(r'\b%s (русский|русских|российских) (канал|канала|каналов)\b' % OLD,
               lambda m: f'{N} {"русских" if m.group(1) in ("русский", "русских") else "российских"} канала', s)
    # EN
    s = re.sub(r'\b%s (live Russian TV channels|live Russian channels|Live Channels|Live channels)\b' % OLD,
               lambda m: f'{N} {m.group(1)}', s)
    return s

CREDIT_MARK = '<!--logo-credits-->'
def credit_block():
    fn = 'Лого Москва 24 2015.png'
    url = 'https://commons.wikimedia.org/wiki/File:' + urllib.parse.quote(fn.replace(' ', '_'))
    return (CREDIT_MARK + '\n  <h2>Логотипы и авторские права</h2>\n'
            '  <p>Логотипы телеканалов — товарные знаки их владельцев; они показаны только для обозначения канала в списке.</p>\n'
            f'  <p>Логотип «Москва 24»: файл «{fn}», автор SlavaDash, <a href="{url}" target="_blank" rel="noopener">Wikimedia Commons</a>, '
            'лицензия <a href="https://creativecommons.org/licenses/by-sa/4.0/deed.ru" target="_blank" rel="noopener">CC BY-SA 4.0</a>. '
            'Изменения: уменьшен размер, цвет буквенной части инвертирован стилем для тёмного фона.</p>\n\n  ')

for f in glob.glob(os.path.join(ROOT, '**/*.html'), recursive=True):
    s = open(f, encoding='utf-8').read(); o = s
    s = count_fix(s)
    if f == os.path.join(ROOT, 'about', 'index.html') and CREDIT_MARK not in s:
        s = s.replace('<div class="contact-box">', credit_block() + '<div class="contact-box">', 1)
    if s != o:
        open(f, 'w', encoding='utf-8').write(s); changed += 1
print('gen_polish: изменено файлов', changed)
