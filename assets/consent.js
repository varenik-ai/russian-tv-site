/* Analytics and ads loader for russian-tv.com.
   No consent banner: GA4, Yandex.Metrika (Webvisor disabled), Microsoft Clarity and the
   Monetag ads script (assets/ads.js) load right away. */
(function () {
  window.dataLayer = window.dataLayer || [];
  window.gtag = function () { window.dataLayer.push(arguments); };
  window.rtvConsentGranted = function () { return true; };
  var loaded = false;
  function loadTrackers() {
    if (loaded) return; loaded = true;
    gtag('js', new Date()); gtag('config', 'G-XLSJE8NKJE');
    var g = document.createElement('script'); g.async = true; g.src = 'https://www.googletagmanager.com/gtag/js?id=G-XLSJE8NKJE'; document.head.appendChild(g);
    (function (c, l, a, r, i, t, y) { c[a] = c[a] || function () { (c[a].q = c[a].q || []).push(arguments); }; t = l.createElement(r); t.async = 1; t.src = 'https://www.clarity.ms/tag/' + i; y = l.getElementsByTagName(r)[0]; y.parentNode.insertBefore(t, y); })(window, document, 'clarity', 'script', 'xkhl4v4ft0');
    (function (m, e, t, r, i, k, a) { m[i] = m[i] || function () { (m[i].a = m[i].a || []).push(arguments); }; m[i].l = 1 * new Date(); k = e.createElement(t); a = e.getElementsByTagName(t)[0]; k.async = 1; k.src = r; a.parentNode.insertBefore(k, a); })(window, document, 'script', 'https://mc.yandex.ru/metrika/tag.js', 'ym');
    ym(110584472, 'init', { clickmap: true, trackLinks: true, accurateTrackBounce: true, webvisor: false });
    try { window.dispatchEvent(new Event('rtv-consent-granted')); } catch (e) {}
  }
  loadTrackers();
})();
