#!/usr/bin/env python3
"""18.11.2026: блок «Watching from the USA, UK and Canada» на EN-страницах основных каналов:
конвертер московского времени (assets/moscow-time.js, Intl, учитывает летнее время) + статичная таблица для случая без JS,
ссылки на страницы стран и новогоднюю статью. Вставляется между </div> блока desc-box и faq-box, маркеры <!--rtv-abroad-->. Идемпотентен."""
import sys, os, re, json
ROOT = sys.argv[1]
CH = {  # slug: (название, фраза про эфир)
 'perviy-kanal-live': ('Channel One Russia', 'Channel One (Perviy Kanal) carries the main evening news, talk shows and the big holiday programmes.'),
 'rossiya-1-live': ('Rossiya 1', 'Rossiya 1 carries the Vesti news, talk shows and series.'),
 'ntv-live': ('NTV', 'NTV carries news, investigative programmes and series.'),
 'rossiya-24-live': ('Rossiya 24', 'Rossiya 24 is the 24-hour news channel, so something is on at any hour.'),
 'tv-centr-live': ('TV Centre', 'TV Centre carries news, Moscow programmes and films.'),
 'rossiya-rtr-evropa-live': ('Rossiya RTR Europe', 'This is the Rossiya RTR feed made for viewers in Europe.'),
 'rossiya-rtr-usa-live': ('Rossiya RTR USA', 'This is the Rossiya RTR feed made for viewers in North America.'),
}
ZONES = [["New York / Toronto", "America/New_York"], ["Chicago", "America/Chicago"], ["Winnipeg", "America/Winnipeg"], ["Denver", "America/Denver"],
         ["Edmonton / Calgary", "America/Edmonton"], ["Los Angeles", "America/Los_Angeles"], ["Vancouver", "America/Vancouver"], ["London", "Europe/London"]]
def block(name, line):
    z = json.dumps(ZONES, ensure_ascii=False).replace("'", "&#39;")
    return f'''<!--rtv-abroad-->
    <div class="desc-box" style="margin-top:16px">
      <h2>Watching {name} from the USA, UK or Canada</h2>
      <p>{line} The stream works in the USA, the UK and Canada without a VPN and without registration. Moscow is on UTC+3 all year and does not change its clocks, so the gap changes when your country switches to or from daylight saving time (for New York it is 8 hours in winter and 7 in summer; for London 3 and 2). Use the converter below.</p>
      <div class="rtv-conv" data-lang="en" data-default="21:00" data-zones='{z}'>
        <noscript><p>Moscow 21:00 in winter (standard time) = 1:00 PM New York and Toronto, 12:00 PM Chicago, 11:00 AM Denver, 10:00 AM Los Angeles, 6:00 PM London (Winnipeg, Edmonton and Vancouver now stay on permanent daylight time, one hour later: 1:00 PM, 12:00 PM, 11:00 AM).</p></noscript>
      </div>
      <p>More: <a href="/en/russian-tv-in-usa/">Russian TV in the USA</a> · <a href="/en/russian-tv-in-uk/">Russian TV in the UK</a> · <a href="/en/russian-tv-in-canada/">Russian TV in Canada</a> · <a href="/en/blog/russian-tv-new-years-eve-usa-uk-canada/">Russian TV on New Year's Eve</a> · <a href="/en/blog/channel-not-loading-fix/">Channel not loading: 8 fixes</a> · <a href="/en/blog/channel-one-vs-rossiya-1-vs-ntv/">Channel One vs Rossiya 1 vs NTV</a></p>
    </div>
    <script defer src="/assets/moscow-time.js?v=1"></script>
<!--/rtv-abroad-->
'''
n = 0
for slug, (name, line) in CH.items():
    p = os.path.join(ROOT, 'en', slug, 'index.html')
    if not os.path.exists(p): print('нет', slug); continue
    s = o = open(p, encoding='utf-8').read()
    b = block(name, line)
    if '<!--rtv-abroad-->' in s:
        s = re.sub(r'<!--rtv-abroad-->.*?<!--/rtv-abroad-->\n', lambda m: b, s, count=1, flags=re.S)
    else:
        i = s.find('<div class="faq-box">')
        if i < 0: print('нет faq-box', slug); continue
        j = s.rfind('\n', 0, i)
        s = s[:j + 1] + '    ' + b + '\n' + s[j + 1:]
    if s != o: open(p, 'w', encoding='utf-8').write(s); n += 1
print('gen_channel_abroad: страниц изменено', n)
