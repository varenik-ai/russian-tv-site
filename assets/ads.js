/* Monetag In-Page Push — only on channel pages (/…-live/), loaded late so it never delays the player.
   Kill switch: set ADS_ENABLED=false (or add ?noads=1 to a URL to test without ads). */
(function () {
  var ADS_ENABLED = true;
  var ZONE = '11593818';              // In-Page Push "Lucky tag"
  var DELAY_MS = 20000;               // wait 20s after page load so playback starts first
  if (!ADS_ENABLED) return;
  if (!/-live\/?$/.test(location.pathname.replace(/index\.html$/, ''))) return;
  if (/[?&]noads=1/.test(location.search)) return;
  function load() {
    try {
      var s = document.createElement('script');
      s.async = true;
      s.dataset.zone = ZONE;
      s.src = 'https://nap5k.com/tag.min.js';
      (document.body || document.documentElement).appendChild(s);
    } catch (e) {}
  }
  function arm() { setTimeout(load, DELAY_MS); }
  if (document.readyState === 'complete') arm(); else window.addEventListener('load', arm);
})();
