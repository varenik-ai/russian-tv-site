/* Monetag In-Page Push — channel pages (/…-live/) and the home pages (/, /en/), loaded late so it never delays the player.
   Loads ONLY after the visitor accepted cookies (see /assets/consent.js).
   Kill switch: set ADS_ENABLED=false (or add ?noads=1 to a URL to test without ads). */
(function () {
  var ADS_ENABLED = true;
  var ZONE = '11593818';              // In-Page Push "Lucky tag"
  var DELAY_MS = 20000;               // wait 20s after page load so playback starts first
  if (!ADS_ENABLED) return;
  var path = location.pathname.replace(/index\.html$/, '');
  var isChannel = /-live\/?$/.test(path);
  var isHome = path === '/' || path === '/en/' || path === '/en';
  if (!isChannel && !isHome) return;
  if (/[?&]noads=1/.test(location.search)) return;
  var armed = false;
  function load() {
    try {
      var s = document.createElement('script');
      s.async = true;
      s.dataset.zone = ZONE;
      s.src = 'https://nap5k.com/tag.min.js';
      (document.body || document.documentElement).appendChild(s);
    } catch (e) {}
  }
  function arm() { if (armed) return; armed = true; setTimeout(load, DELAY_MS); }
  function start() {
    if (window.rtvConsentGranted && window.rtvConsentGranted()) arm();
    else window.addEventListener('rtv-consent-granted', arm);
  }
  if (document.readyState === 'complete') start(); else window.addEventListener('load', start);
})();

/* Adsterra Banner 300x250 — test, to the right of the player on wide desktop screens only (channel pages /…-live/).
   The player column (960px) is left-aligned next to the channel list; the block is shown only when 300px + gap fit between
   the column and the window edge (about ≥1760px wide) and a mouse is present. On phones, tablets and smaller screens nothing
   is loaded and the layout is untouched.
   Kill switch: BANNER_ENABLED=false (or ?noads=1). Ad unit: Adsterra site 6187633, unit 32178193. */
(function () {
  var BANNER_ENABLED = true;
  var KEY = '825d215f35b6e7c6a1f929819767001a';
  var DELAY_MS = 3000;
  if (!BANNER_ENABLED) return;
  var path = location.pathname.replace(/index\.html$/, '');
  if (!/-live\/?$/.test(path)) return;
  if (/[?&]noads=1/.test(location.search)) return;
  var armed = false;
  function show() {
    try {
      if (!window.matchMedia || !matchMedia('(hover:hover)').matches) return;
      var col = document.querySelector('.main-col'), pl = document.getElementById('player-wrap');
      if (!col || !pl || document.getElementById('rtv-ban')) return;
      function fits() { return col.getBoundingClientRect().right + 12 + 300 <= document.documentElement.clientWidth - 8; }
      if (!fits()) return;
      var st = document.createElement('style');
      st.textContent = '.main-col{position:relative}' +
        '#rtv-ban{position:absolute;left:calc(100% + 12px);width:300px;font:11px/1.2 sans-serif;color:#8b8ba0}' +
        '#rtv-ban small{display:block;margin:0 0 4px}#rtv-ban .box{width:300px;height:250px}' +
        '#rtv-ban.off{display:none}';
      document.head.appendChild(st);
      var en = /^en/i.test(document.documentElement.lang || '');
      var d = document.createElement('div'); d.id = 'rtv-ban';
      d.style.top = pl.offsetTop + 'px';
      d.innerHTML = '<small>' + (en ? 'Advertisement' : 'Реклама') + '</small><div class="box"></div>';
      col.appendChild(d);
      window.addEventListener('resize', function () { d.className = fits() ? '' : 'off'; });
      window.atOptions = { key: KEY, format: 'iframe', height: 250, width: 300, params: {} };
      var s = document.createElement('script');
      s.async = true; s.src = 'https://www.highrevenueformat.com/' + KEY + '/invoke.js';
      d.style.visibility = 'hidden';            // no ad (no fill / blocked) = no empty label or gap
      var t0 = Date.now(), iv = setInterval(function () {
        if (d.querySelector('iframe')) { d.style.visibility = 'visible'; clearInterval(iv); }
        else if (Date.now() - t0 > 10000) { clearInterval(iv); d.parentNode && d.parentNode.removeChild(d); }
      }, 500);
      d.querySelector('.box').appendChild(s);
    } catch (e) {}
  }
  function arm() { if (armed) return; armed = true; setTimeout(show, DELAY_MS); }
  function start() {
    if (window.rtvConsentGranted && window.rtvConsentGranted()) arm();
    else window.addEventListener('rtv-consent-granted', arm);
  }
  if (document.readyState === 'complete') start(); else window.addEventListener('load', start);
})();
