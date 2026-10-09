/* Cookie consent + gated analytics for russian-tv.com.
   Analytics (GA4, Yandex.Metrika, Microsoft Clarity) and ads load ONLY after the visitor accepts.
   Choice is stored in localStorage ("rtv_consent": "granted" | "denied"). Footer link "Cookie settings" re-opens the banner. */
(function () {
  var KEY = 'rtv_consent';
  var EN = (document.documentElement.lang || '').toLowerCase().indexOf('en') === 0;
  var T = EN ? {
    text: 'We use cookies for analytics and advertising. You can accept or decline — the site works either way.',
    accept: 'Accept', decline: 'Decline', more: 'Privacy policy', settings: 'Cookie settings', privacy: '/en/privacy/'
  } : {
    text: 'Мы используем cookies для аналитики и рекламы. Вы можете принять или отклонить — сайт работает в любом случае.',
    accept: 'Принять', decline: 'Отклонить', more: 'Политика конфиденциальности', settings: 'Настройки cookies', privacy: '/privacy/'
  };
  function get() { try { return localStorage.getItem(KEY); } catch (e) { return null; } }
  function set(v) { try { localStorage.setItem(KEY, v); } catch (e) {} }

  // До согласия — безопасные заглушки (события не копятся и не отправляются).
  window.dataLayer = window.dataLayer || [];
  window.gtag = function () {};
  window.ym = function () {};

  var loaded = false;
  function loadTrackers() {
    if (loaded) return; loaded = true;
    window.gtag = function () { window.dataLayer.push(arguments); };
    gtag('js', new Date()); gtag('config', 'G-XLSJE8NKJE');
    (function (w, d, s, l, i) { w[l] = w[l] || []; w[l].push({ 'gtm.start': new Date().getTime(), event: 'gtm.js' }); var f = d.getElementsByTagName(s)[0], j = d.createElement(s); j.async = true; j.src = 'https://www.googletagmanager.com/gtm.js?id=' + i; f.parentNode.insertBefore(j, f); })(window, document, 'script', 'dataLayer', 'GTM-TWVC9XDN');
    var g = document.createElement('script'); g.async = true; g.src = 'https://www.googletagmanager.com/gtag/js?id=G-XLSJE8NKJE'; document.head.appendChild(g);
    (function (c, l, a, r, i, t, y) { c[a] = c[a] || function () { (c[a].q = c[a].q || []).push(arguments); }; t = l.createElement(r); t.async = 1; t.src = 'https://www.clarity.ms/tag/' + i; y = l.getElementsByTagName(r)[0]; y.parentNode.insertBefore(t, y); })(window, document, 'clarity', 'script', 'xkhl4v4ft0');
    (function (m, e, t, r, i, k, a) { m[i] = m[i] || function () { (m[i].a = m[i].a || []).push(arguments); }; m[i].l = 1 * new Date(); k = e.createElement(t); a = e.getElementsByTagName(t)[0]; k.async = 1; k.src = r; a.parentNode.insertBefore(k, a); })(window, document, 'script', 'https://mc.yandex.ru/metrika/tag.js', 'ym');
    ym(110584472, 'init', { clickmap: true, trackLinks: true, accurateTrackBounce: true, webvisor: true });
    try { window.dispatchEvent(new Event('rtv-consent-granted')); } catch (e) {}
  }
  window.rtvConsentGranted = function () { return get() === 'granted'; };

  var bar;
  function close() { if (bar && bar.parentNode) bar.parentNode.removeChild(bar); bar = null; }
  function show() {
    if (bar || !document.body) return;
    bar = document.createElement('div');
    bar.setAttribute('role', 'dialog'); bar.setAttribute('aria-label', T.settings);
    bar.style.cssText = 'position:fixed;left:0;right:0;bottom:0;z-index:2147483000;background:#12121f;color:#e2e2f0;border-top:1px solid #2a2a40;padding:12px 16px;display:flex;flex-wrap:wrap;gap:10px;align-items:center;justify-content:center;font:13px/1.45 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;box-shadow:0 -4px 20px rgba(0,0,0,.4)';
    var p = document.createElement('span'); p.style.cssText = 'max-width:640px;text-align:center';
    p.appendChild(document.createTextNode(T.text + ' '));
    var a = document.createElement('a'); a.href = T.privacy; a.textContent = T.more; a.style.cssText = 'color:#6ea8ff;text-decoration:underline'; p.appendChild(a);
    function btn(label, primary, fn) {
      var b = document.createElement('button'); b.type = 'button'; b.textContent = label;
      b.style.cssText = 'cursor:pointer;border-radius:8px;padding:8px 18px;font:600 13px inherit;border:1px solid ' + (primary ? '#1a5fd9' : '#4a4a66') + ';background:' + (primary ? '#1a5fd9' : 'transparent') + ';color:#fff';
      b.addEventListener('click', fn); return b;
    }
    bar.appendChild(p);
    bar.appendChild(btn(T.decline, false, function () { set('denied'); close(); }));
    bar.appendChild(btn(T.accept, true, function () { set('granted'); close(); loadTrackers(); }));
    document.body.appendChild(bar);
  }
  function addSettingsLink() {
    var note = document.querySelector('.legal-note');
    if (!note || note.querySelector('[data-cookie-settings]')) return;
    var s = document.createElement('a'); s.href = '#'; s.setAttribute('data-cookie-settings', '1'); s.textContent = T.settings;
    s.style.cssText = 'color:inherit;text-decoration:underline';
    s.addEventListener('click', function (e) { e.preventDefault(); show(); });
    note.appendChild(document.createTextNode(' · ')); note.appendChild(s);
  }
  function init() {
    addSettingsLink();
    var v = get();
    if (v === 'granted') loadTrackers();
    else if (v !== 'denied') show();
  }
  if (get() === 'granted') loadTrackers();
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
