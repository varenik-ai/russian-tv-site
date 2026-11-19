# EN-статья «Список российских телеканалов онлайн» (19.11.2026): список строится из самих страниц каналов (рубрика из cat-tag RU-страницы, название из h1 EN-страницы,
# описание из meta description EN-страницы), поэтому всегда совпадает с сайтом. Каналы с noindex (убранные) не попадают.
import os, re, sys, html as _h
_ROOT = sys.argv[1] if len(sys.argv) > 1 else '.'
def _rd(p): return open(os.path.join(_ROOT, p), encoding='utf-8').read()
_CATS = [('novosti', 'News', '/en/news/', 'News channels'), ('kino', 'Movies', '/en/movies/', 'Movie channels'), ('razvlecheniya', 'Entertainment', '/en/entertainment/', 'Entertainment channels'),
         ('muzyka', 'Music', '/en/music/', 'Music channels'), ('sport', 'Sport', '/en/sport/', 'Sports channels'), ('detskie', 'Kids', '/en/kids/', 'Kids channels'), ('hobbi', 'Hobby and discovery', '/en/hobby/', 'Hobby and discovery channels')]
_by = {}
_n = 0
for _d in sorted(os.listdir(_ROOT)):
    if not (_d.endswith('-live') and os.path.isdir(os.path.join(_ROOT, _d)) and os.path.exists(os.path.join(_ROOT, 'en', _d, 'index.html'))): continue
    _r = _rd(_d + '/index.html')
    if 'noindex' in _r.lower()[:6000]: continue
    _c = re.search(r'<a href="https://russian-tv.com/([a-z]+)/" class="cat-tag">', _r)
    _e = _rd('en/' + _d + '/index.html')
    _t = re.search(r'<h1[^>]*>([^<]*)</h1>', _e); _m = re.search(r'<meta name="description" content="([^"]*)"', _e)
    if not (_c and _t and _m): continue
    _name = re.sub(r'^Watch\s+|\s+Live Online Free\s*$', '', _t.group(1)).strip()
    _desc = re.search(r'—\s*(.*?)\.\s*No VPN', _h.unescape(_m.group(1)))
    _by.setdefault(_c.group(1), []).append((_name, _d, (_desc.group(1).strip() if _desc else '')))
    _n += 1
def _block():
    out = ''
    for key, name, hub, title in _CATS:
        rows = sorted(_by.get(key, []), key=lambda x: x[0].lower())
        if not rows: continue
        out += f'  <h2>{title} ({len(rows)})</h2>\n  <table class="channel-table">\n    <thead>\n      <tr><th>Channel</th><th>What it is</th></tr>\n    </thead>\n    <tbody>\n'
        for nm, d, ds in rows:
            ds = (ds[:1].upper() + ds[1:]) if ds else 'Live stream'
            out += f'      <tr><td><a href="/en/{d}/">{_h.escape(nm)}</a></td><td>{_h.escape(ds)}</td></tr>\n'
        out += f'    </tbody>\n  </table>\n  <p>All in one place: <a href="{hub}">{name}</a>.</p>\n\n'
    return out
LIST_EN = dict(
  slug='russian-tv-channels-list-live',
  date='2026-11-19', date_label='November 2026',
  title='List of Russian TV Channels to Watch Live Online (2026)',
  desc=f'A list of {_n} Russian TV channels you can watch live online free: news, movies, entertainment, music, sport, kids. No VPN, no signup, no app.',
  headline=f'List of Russian TV channels you can watch live online — {_n} free channels by category',
  crumb='Russian TV channels list', meta='<span>📅 Published: November 2026</span><span>📺 Channels</span><span>⏱ 6 min read</span>',
  h1=f'List of {_n} Russian TV Channels You Can Watch Live Online for Free (2026)',
  alt=None,
  body=f'''  <p><strong>Short answer:</strong> russian-tv.com streams <strong>{_n} Russian-language channels</strong> live, free and without a VPN, registration or app. Below is the full list by category, with a link to each channel's page. The list is generated from the site itself, so it always matches the catalogue.</p>

  <div class="cta-box">
    <p>📺 Watch Russian TV live — free, no VPN</p>
    <a href="/en/">▶ Open the full catalogue</a>
  </div>

  <h2>How to use the list</h2>
  <ul>
    <li><strong>Pick a channel</strong> in a table below and open its page; the stream starts with ▶.</li>
    <li><strong>Check the time.</strong> Russian channels run on Moscow time (UTC+3). See <a href="/en/blog/moscow-time-to-us-time-zones-russian-tv-schedule/">Moscow time in US time zones</a>, <a href="/en/blog/how-to-watch-russian-tv-in-canada/">Canada</a> and <a href="/en/blog/how-to-watch-russian-tv-in-uk/">the UK</a>. The "Today's schedule" block on each channel page shows the programme in your device's time.</li>
    <li><strong>Not sure which of the big three?</strong> Read <a href="/en/blog/channel-one-vs-rossiya-1-vs-ntv/">Channel One vs Rossiya 1 vs NTV</a>.</li>
    <li><strong>On a TV?</strong> See <a href="/en/blog/russian-tv-on-smart-tv-roku-chromecast-apple-tv/">Russian TV on Smart TV, Roku and more</a>.</li>
  </ul>

{_block()}  <h2>If a channel does not start</h2>
  <p>Streams come from third-party sources, so a channel can occasionally be slow or unavailable in a particular country or on a particular provider. The player switches to a backup source on its own for the main channels; if nothing helps, try another channel or the guide <a href="/en/blog/channel-not-loading-fix/">Channel not loading: 8 fixes</a>.</p>

  <p><em>The list changes when channels are added or removed. russian-tv.com only links to streams that are publicly available on the internet; rules for foreign broadcasts differ between countries, and this page is not legal advice.</em></p>
''',
  faq=[('How many Russian TV channels can I watch online here?', f'The catalogue currently lists {_n} Russian-language channels, grouped into news, movies, entertainment, music, sport, kids and hobby categories.'),
       ('Is it free?', 'Yes. All channels are free, with no registration, no app and no VPN.'),
       ('Which channels are best for news?', 'Rossiya 24 broadcasts news around the clock; Perviy Kanal, Rossiya 1 and NTV carry news bulletins and talk shows; TV Centre offers Moscow-focused news.'),
       ('Are there channels made for viewers abroad?', 'Yes: Rossiya RTR — Europe and Rossiya RTR — USA are versions of the Rossiya channel prepared for audiences outside Russia.'),
       ('Can I watch on a TV?', 'Yes. Open russian-tv.com/tv in the TV browser, or cast from a phone or computer with AirPlay or Chromecast.'),
       ('What time zone are the programmes in?', 'Channels follow Moscow time (UTC+3). The "Today\'s schedule" block on each channel page shows times in your device\'s local time.')],
  related=[('All channels', '/en/'), ('Channel One vs Rossiya 1 vs NTV', '/en/blog/channel-one-vs-rossiya-1-vs-ntv/'), ('Russian TV on Smart TV', '/en/blog/russian-tv-on-smart-tv-roku-chromecast-apple-tv/'), ('How to Watch Russian TV in the USA', '/en/blog/how-to-watch-russian-tv-in-usa/'), ('Channel not loading: how to fix it', '/en/blog/channel-not-loading-fix/')],
)
