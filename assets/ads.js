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
