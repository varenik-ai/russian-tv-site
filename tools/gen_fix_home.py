#!/usr/bin/env python3
"""16.11.2026: страховка для главных страниц (RU и EN). Генераторы добавляют строки каналов в CHANNEL_GROUPS, не ставя запятую после предыдущей строки:
из-за этого на главной (RU) был SyntaxError и не рисовался список каналов. Шаг ставит запятую после каждой строки `{ id:... }` внутри CHANNEL_GROUPS
(завершающая запятая в JS допустима), затем проверяет синтаксис скриптов главных через node и завершается ошибкой, если он сломан. Идёт последним в run_all.sh. Идемпотентен."""
import sys, os, re, subprocess, tempfile
ROOT = sys.argv[1]
bad = 0
for rel in ('index.html', 'en/index.html'):
    p = os.path.join(ROOT, rel)
    s = open(p, encoding='utf-8').read(); o = s
    s = re.sub(r'(?m)^([ \t]*\{ id:[\'"][^\n]*\})[ \t]*$', r'\1,', s)
    if s != o: open(p, 'w', encoding='utf-8').write(s); print('gen_fix_home: запятые поправлены в', rel)
    for m in re.finditer(r'<script(?![^>]*\bsrc=)([^>]*)>(.*?)</script>', s, re.S):
        if 'ld+json' in m.group(1) or not m.group(2).strip(): continue
        with tempfile.NamedTemporaryFile('w', suffix='.js', delete=False, encoding='utf-8') as t: t.write(m.group(2))
        r = subprocess.run(['node', '--check', t.name], capture_output=True, text=True); os.unlink(t.name)
        if r.returncode: bad += 1; print('SyntaxError в', rel, r.stderr.strip().split('\n')[0][:200])
if bad: sys.exit(1)
print('gen_fix_home: скрипты главных страниц в порядке')
