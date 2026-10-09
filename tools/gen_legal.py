#!/usr/bin/env python3
"""Юридическая оговорка для правообладателей: подвал всех страниц + раздел в политике конфиденциальности (RU/EN)."""
import sys, os, glob, re
ROOT = sys.argv[1]
def rd(p): return open(os.path.join(ROOT, p), encoding='utf-8').read()
def wr(p, s):
    os.makedirs(os.path.dirname(os.path.join(ROOT, p)) or ROOT, exist_ok=True)
    open(os.path.join(ROOT, p), 'w', encoding='utf-8').write(s)

RU_SEC = '''  <h2 id="rightsholders">4.1. Правообладателям: удаление трансляций</h2>
  <p>Ссылки на трансляции, размещённые на сайте, взяты из открытых источников в сети Интернет. Russian-TV.com не хранит, не записывает и не загружает видеоконтент. Если вы являетесь правообладателем и считаете, что размещённая ссылка нарушает ваши права, направьте обращение на <strong>support@russian-tv.com</strong> с указанием канала (адреса страницы) и приложите документы, подтверждающие права на контент. Трансляция будет удалена с сайта после предъявления доказательств правообладания.</p>

'''
EN_SEC = RU_SEC  # заменяется ниже

# ---- RU privacy ----
s = rd('privacy/index.html')
if 'id="rightsholders"' not in s:
    s = s.replace('  <h2>5. Ваши права</h2>', RU_SEC + '  <h2>5. Ваши права</h2>', 1)
    s = s.replace('Последнее обновление: 16 сентября 2026 г.', 'Последнее обновление: 9 октября 2026 г.')
    s = s.replace('<h2>4. Контент третьих сторон</h2>', '<h2>4. Контент третьих сторон</h2>', 1)
if 'hreflang="en"' not in s:
    s = s.replace('<link rel="canonical" href="https://russian-tv.com/privacy/"/>', '<link rel="canonical" href="https://russian-tv.com/privacy/"/>\n  <link rel="alternate" hreflang="ru" href="https://russian-tv.com/privacy/"/>\n  <link rel="alternate" hreflang="en" href="https://russian-tv.com/en/privacy/"/>\n  <link rel="alternate" hreflang="x-default" href="https://russian-tv.com/privacy/"/>', 1)
wr('privacy/index.html', s)

# ---- EN privacy ----
ru = s
en = ru
rep = [
 ('<html lang="ru"', '<html lang="en"'),
 ('<title>Политика конфиденциальности — Russian-TV.com</title>', '<title>Privacy Policy — Russian-TV.com</title>'),
 ('content="Политика конфиденциальности сайта Russian-TV.com. Информация о сборе данных, использовании cookies и аналитике."', 'content="Privacy policy of Russian-TV.com: data collection, cookies, analytics and notice for rights holders."'),
 ('<link rel="canonical" href="https://russian-tv.com/privacy/"/>', '<link rel="canonical" href="https://russian-tv.com/en/privacy/"/>'),
 ('<span class="r">Рус</span><span class="w">ское</span></span><span class="b">ТВ</span>', '<span class="r">Rus</span><span class="w">sian</span></span><span class="b">TV</span>'),
 ('<a href="/">Главная</a><span>›</span><a href="/about/">О сайте</a><span>›</span><span>Политика конфиденциальности</span>', '<a href="/en/">Home</a><span>›</span><span>Privacy Policy</span>'),
 ('<h1>Политика конфиденциальности</h1>', '<h1>Privacy Policy</h1>'),
 ('Последнее обновление: 9 октября 2026 г.', 'Last updated: October 9, 2026'),
]
for a, b in rep: en = en.replace(a, b)
i = en.find('<div class="wrap">'); j = en.find('</div>\n<footer>')
body = '''<div class="wrap">
  <h1>Privacy Policy</h1>
  <p class="updated">Last updated: October 9, 2026</p>

  <p>This privacy policy describes what data the <strong>russian-tv.com</strong> website collects and how it is used.</p>

  <h2>1. What we collect</h2>
  <p>Russian-TV.com does not require registration and does not directly collect personal data. However, the following may be recorded automatically when you visit the site:</p>
  <ul>
    <li>IP address (anonymised by analytics systems)</li>
    <li>Browser type and operating system</li>
    <li>Pages you view and the time of your visit</li>
    <li>Visitor country (IP-based geolocation, no exact address)</li>
  </ul>

  <h2>2. Analytics and tracking</h2>
  <p>The site uses the following analytics tools:</p>
  <ul>
    <li><strong>Google Analytics 4 (GA4)</strong> — aggregated traffic statistics. Data is sent to Google. More: <a href="https://policies.google.com/privacy" target="_blank" rel="noopener">Google policy</a>.</li>
    <li><strong>Google Tag Manager</strong> — management of analytics tags.</li>
    <li><strong>Yandex Metrica</strong> — additional analytics (Webvisor is disabled). Data is sent to Yandex. More: <a href="https://yandex.com/legal/confidential/" target="_blank" rel="noopener">Yandex policy</a>.</li>
    <li><strong>Microsoft Clarity</strong> — user behaviour analysis (heatmaps, anonymous session recordings).</li>
  </ul>

  <h2>3. Cookies</h2>
  <p>The site uses cookies — small files that your browser stores on your device. They are needed for analytics and for remembering user settings. You can disable cookies in your browser settings, but some site features may not work correctly.</p>

  <h2>4. Third-party content</h2>
  <p>Russian-TV.com is an aggregator and does not store video content. Streams come from third parties via HLS. When a stream plays, your browser connects directly to the source server, which may mean your IP address is shared with that server.</p>

  <h2 id="rightsholders">4.1. For rights holders: removal of streams</h2>
  <p>Links to streams on this site are taken from publicly available sources on the Internet. Russian-TV.com does not store, record or upload video content. If you are a rights holder and believe that a link infringes your rights, send a request to <strong>support@russian-tv.com</strong> stating the channel (page address) and attach documents proving your rights to the content. The stream will be removed from the site after proof of rights ownership is provided.</p>

  <h2>5. Your rights</h2>
  <p>You may request information about data that may be associated with your visit, or ask for its deletion. Contact: <strong>support@russian-tv.com</strong></p>

  <h2>6. Changes to this policy</h2>
  <p>We reserve the right to update this policy. The date of the latest update is shown at the top of the document.</p>

  <h2>7. Contact</h2>
  <p>For privacy questions: <strong>support@russian-tv.com</strong></p>
'''
en = en[:i] + body + en[j:]
fi = en.find('<footer>'); fj = en.find('</footer>') + 9
en = en[:fi] + '''<footer>
  <div>🇷🇺 <a href="/en/">Russian TV</a> — free Russian TV online</div>
  <div style="margin-top:6px">
    <a href="/en/">All channels</a>
    <a href="/en/privacy/">Privacy Policy</a>
    <a href="/privacy/">Русский</a>
  </div>
</footer>''' + en[fj:]
wr('en/privacy/index.html', en)

# ---- подвалы всех страниц + ссылки на политику ----
NOTE_RU = ('<div class="legal-note" style="text-align:center;margin:10px auto 0;max-width:760px;padding:0 12px;font-size:11px;line-height:1.5;color:#8b8ba0">'
           'Ссылки на трансляции взяты из открытых источников. По обращению правообладателя трансляция будет удалена после предъявления доказательств правообладания — '
           '<a href="/privacy/#rightsholders" style="color:inherit;text-decoration:underline">подробнее</a>.</div>\n')
NOTE_EN = ('<div class="legal-note" style="text-align:center;margin:10px auto 0;max-width:760px;padding:0 12px;font-size:11px;line-height:1.5;color:#8b8ba0">'
           'Stream links are taken from publicly available sources. At the request of a rights holder, a stream will be removed after proof of rights ownership is provided — '
           '<a href="/en/privacy/#rightsholders" style="color:inherit;text-decoration:underline">details</a>.</div>\n')
n = 0
for f in glob.glob(os.path.join(ROOT, '**/*.html'), recursive=True):
    rel = os.path.relpath(f, ROOT)
    if rel == '404.html': continue
    s = open(f, encoding='utf-8').read(); o = s
    if '<footer' not in s or 'noindex' in s[:3000]: continue
    en_page = '<html lang="en"' in s[:400]
    if 'class="legal-note"' not in s:
        s = s.replace('</footer>', ('  ' + (NOTE_EN if en_page else NOTE_RU)) + '</footer>', 1)
    s = s.replace('<a href="#">Конфиденциальность</a>', '<a href="/privacy/">Конфиденциальность</a>')
    s = s.replace('<a href="#">Privacy</a>', '<a href="/en/privacy/">Privacy</a>')
    if s != o: open(f, 'w', encoding='utf-8').write(s); n += 1
print('footers updated:', n)
