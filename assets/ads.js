/* Monetag In-Page Push — only the home pages (/, /en/) since 18.11.2026 (was: channel pages too), loaded late so it never delays the player.
   Loads ONLY after the visitor accepted cookies (see /assets/consent.js).
   Kill switch: set ADS_ENABLED=false (or add ?noads=1 to a URL to test without ads). */
(function () {
  if (/SmartTV|SMART-TV|Tizen|Web0S|WebOS|HbbTV|NetCast|AppleTV|BRAVIA|CrKey/i.test(navigator.userAgent || '') || /Android.*\bTV\b|AFT[A-Z]/.test(navigator.userAgent || '')) return;   // на телевизорах рекламы нет (с 18.11.2026)
  var ADS_ENABLED = true;
  var ZONE = '11593818';              // In-Page Push "Lucky tag"
  var DELAY_MS = 20000;               // wait 20s after page load so playback starts first
  if (!ADS_ENABLED) return;
  var path = location.pathname.replace(/index\.html$/, '');
  var isHome = path === '/' || path === '/en/' || path === '/en';
  if (!isHome) return;   // с 18.11.2026 только главные: на страницах каналов остаётся баннер Adsterra (у Monetag за 14-18.11 $0,095 против $2,00 у Adsterra)
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

/* Adsterra Banner 300x250 — test, channel pages (/…-live/).
   Wide screens (a mouse and room for 300px + gap between the left-aligned player column and the window edge, about ≥1760px):
   shown to the right of the player. All other screens (phones, tablets, laptops): shown centered right under the player
   status line, hidden until the ad actually loads (no empty gap). No ad (no fill / blocked) = the block is removed after 10s.
   DESKTOP_ONLY (since 11.11.2026): shown only where a mouse exists (hover:hover). Adsterra stats 9-11.11: desktop CPM $0.40,
   mobile $0.13, tablet $0.04, TV $0 — mobile gave 5 of 10 clicks (CTR 2.1%, likely accidental taps under the player) for $0.03.
   Set DESKTOP_ONLY=false to bring it back on touch screens.
   Kill switch: BANNER_ENABLED=false (or ?noads=1). Ad unit: Adsterra site 6187633, unit 32178193. */
(function () {
  if (/SmartTV|SMART-TV|Tizen|Web0S|WebOS|HbbTV|NetCast|AppleTV|BRAVIA|CrKey/i.test(navigator.userAgent || '') || /Android.*\bTV\b|AFT[A-Z]/.test(navigator.userAgent || '')) return;   // на телевизорах рекламы нет (с 18.11.2026)
  var BANNER_ENABLED = true;
  var DESKTOP_ONLY = true;
  var KEY = '825d215f35b6e7c6a1f929819767001a';
  var DELAY_MS = 3000;
  if (!BANNER_ENABLED) return;
  var path = location.pathname.replace(/index\.html$/, '');
  if (!/-live\/?$/.test(path)) return;
  if (/[?&]noads=1/.test(location.search)) return;
  if (DESKTOP_ONLY && !(window.matchMedia && matchMedia('(hover:hover)').matches)) return;
  var armed = false;
  function show() {
    try {
      var col = document.querySelector('.main-col'), pl = document.getElementById('player-wrap');
      if (!col || !pl || document.getElementById('rtv-ban')) return;
      function fits() { return col.getBoundingClientRect().right + 12 + 300 <= document.documentElement.clientWidth - 8; }
      var wide = !!(window.matchMedia && matchMedia('(hover:hover)').matches) && fits();
      var st = document.createElement('style');
      st.textContent = '#rtv-ban{width:300px;max-width:100%;font:11px/1.2 sans-serif;color:#8b8ba0}' +
        '#rtv-ban small{display:block;margin:0 0 4px}#rtv-ban .box{width:300px;max-width:100%;height:250px;overflow:hidden}' +
        '#rtv-ban.off{display:none}' +
        '#rtv-ban.side{position:absolute;left:calc(100% + 12px)}#rtv-ban.under{margin:4px auto 12px}';
      document.head.appendChild(st);
      var en = /^en/i.test(document.documentElement.lang || '');
      var d = document.createElement('div'); d.id = 'rtv-ban';
      d.innerHTML = '<small>' + (en ? 'Advertisement' : 'Реклама') + '</small><div class="box"></div>';
      if (wide) {
        col.style.position = 'relative';
        d.className = 'side'; d.style.top = pl.offsetTop + 'px'; d.style.visibility = 'hidden';
        col.appendChild(d);
        window.addEventListener('resize', function () { d.className = fits() ? 'side' : 'off'; });
      } else {
        d.className = 'under'; d.style.display = 'none';
        var anchor = document.getElementById('status') || pl;
        anchor.parentNode.insertBefore(d, anchor.nextSibling);
      }
      window.atOptions = { key: KEY, format: 'iframe', height: 250, width: 300, params: {} };
      var s = document.createElement('script');
      s.async = true; s.src = 'https://www.highrevenueformat.com/' + KEY + '/invoke.js';
      var t0 = Date.now(), iv = setInterval(function () {
        if (d.querySelector('iframe')) { d.style.visibility = 'visible'; d.style.display = ''; clearInterval(iv); }
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

/* Adsterra Social Bar — computers and tablets (not phones), channel pages and home pages. Added 11.11.2026.
   Ad unit: Adsterra site 6187633, unit 32210618 (SocialBar_1). Loads only after the visitor accepted cookies, 30s after page load
   (Monetag In-Page Push starts at 20s, so the two never appear together).
   Device test: a mouse (hover:hover) = computer; no mouse and the short side of the screen >= 600 px = tablet; phones are skipped.
   Kill switch: SOCIALBAR_ENABLED=false (or ?noads=1). */
(function () {
  var SOCIALBAR_ENABLED = false;   // выключен 18.11.2026: CTR 27,6% (случайные клики по бару) — риск блокировки аккаунта Adsterra за недействительный трафик; давал 44% дохода Adsterra ($0,87 из $2,00 за 14-18.11)
  var SRC = 'https://bancadeltempoidea.org/14/9c2fe622f1cae087085580e782928d0c';
  var DELAY_MS = 30000;
  if (!SOCIALBAR_ENABLED) return;
  var path = location.pathname.replace(/index\.html$/, '');
  var isChannel = /-live\/?$/.test(path);
  var isHome = path === '/' || path === '/en/' || path === '/en';
  if (!isChannel && !isHome) return;
  if (/[?&]noads=1/.test(location.search)) return;
  var mouse = !!(window.matchMedia && matchMedia('(hover:hover)').matches);
  var tablet = Math.min(screen.width || 0, screen.height || 0) >= 600;
  if (!mouse && !tablet) return;
  var armed = false;
  function load() {
    try {
      var s = document.createElement('script');
      s.setAttribute('data-cfasync', 'false');
      s.src = SRC;
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

/* ===== Реклама Adsterra: новые места (18.11.2026) и «по странам» (18.11.2026) =====
   Все блоки грузятся только после согласия (assets/consent.js) и не показываются на телевизорах (CPM около $0.005 за 1661 показ).
   Устройства: компьютер = есть мышь (hover:hover); планшет = нет мыши, короткая сторона экрана >= 600 px; телефон = остальное.
   Страна посетителя берётся у воркера мониторинга (GET /geo, кэш в sessionStorage). Слои по CPM Adsterra за 14-18.11.2026:
     A (дорогие: США $2.52, Великобритания $1.57, Канада $0.97, Швеция $0.53, Польша $0.27, Германия $0.22, Франция $0.24, Болгария $0.15 ...):
       полный набор — баннер 300x250, второй баннер 300x250 внизу, Native Banner, Popunder (раз в 24 ч);
     B (остальные): баннер 300x250 и Native Banner;
     C (дешёвые: Литва $0.034, Казахстан $0.02, Эстония $0.018, Молдова $0.01 ...): только баннер 300x250 (остальное денег не приносит).
   Места: 1) баннер 300x250 (блок 32178193) на страницах БЕЗ плеера (главная — правая колонка, категории, страны, блог): компьютеры и планшеты;
   2) второй баннер 300x250 (тот же блок) внизу страницы: слой A, компьютеры и планшеты; 3) Native Banner (блок 32348558) внизу: слои A и B;
   4) баннер 320x50 (блок 32348559) внизу: только телефоны, все слои; 5) Popunder (блок 32349106): слой A, компьютеры и планшеты, раз в 24 часа,
   на страницах каналов после 3 минут на странице, на остальных через 15 секунд (скрипт открывает рекламу при следующем клике посетителя).
   Отключить: ADS2_ENABLED=false (всё), POPUNDER_ENABLED=false (только Popunder) или ?noads=1. */
(function () {
  var ADS2_ENABLED = true, POPUNDER_ENABLED = true;
  var UA = navigator.userAgent || '';
  if (!ADS2_ENABLED || /[?&]noads=1/.test(location.search)) return;
  if (/SmartTV|SMART-TV|Tizen|Web0S|WebOS|HbbTV|NetCast|AppleTV|BRAVIA|CrKey/i.test(UA) || /Android.*\bTV\b|AFT[A-Z]/.test(UA)) return;
  var path = location.pathname.replace(/index\.html$/, '');
  var en = /^\/en(\/|$)/.test(path);
  var isChannel = /-live\/?$/.test(path);
  var isHome = path === '/' || path === '/en/' || path === '/en';
  var isLegal = /^\/(en\/)?(privacy|advertising|about)\/?$/.test(path) || /^\/(tv|diag)\/?$/.test(path);
  if (isLegal) return;
  var mouse = !!(window.matchMedia && matchMedia('(hover:hover)').matches);
  var tablet = !mouse && Math.min(screen.width || 0, screen.height || 0) >= 600;
  var phone = !mouse && !tablet;
  var label = en ? 'Advertisement' : 'Реклама';
  var TIER_A = 'US CA GB IE AU NZ DE AT CH FR NL SE NO DK PL ES IT BG'.split(' ');
  var TIER_C = 'LT LV EE KZ MD GE AM AZ BY UZ KG TJ RU'.split(' ');
  function tierOf(cc) { return TIER_A.indexOf(cc) >= 0 ? 'A' : TIER_C.indexOf(cc) >= 0 ? 'C' : 'B'; }
  function getCC(cb) {
    var cc = null; try { cc = sessionStorage.getItem('rtv_cc'); } catch (e) {}
    if (cc) return cb(cc);
    var done = false, t = setTimeout(function () { if (!done) { done = true; cb('XX'); } }, 2500);
    try {
      fetch('https://rtv-monitor.dyaltd.workers.dev/geo').then(function (r) { return r.json(); }).then(function (j) {
        if (done) return; done = true; clearTimeout(t); cc = (j && j.cc) || 'XX'; try { sessionStorage.setItem('rtv_cc', cc); } catch (e) {} cb(cc);
      }).catch(function () { if (!done) { done = true; clearTimeout(t); cb('XX'); } });
    } catch (e) { if (!done) { done = true; clearTimeout(t); cb('XX'); } }
  }
  function wrap(id, inner) {
    var d = document.createElement('div'); d.id = id;
    d.style.cssText = 'display:none;margin:16px auto;text-align:center;max-width:100%;font:11px/1.2 sans-serif;color:#8b8ba0';
    d.innerHTML = '<small style="display:block;margin:0 0 4px">' + label + '</small>' + inner;
    return d;
  }
  function beforeFooter(d) { var f = document.querySelector('footer'); if (f && f.parentNode) f.parentNode.insertBefore(d, f); else document.body.appendChild(d); }
  function reveal(d, ms) {   // показать блок, когда реклама загрузилась; нет рекламы за ms — убрать блок
    var t0 = Date.now(), iv = setInterval(function () {
      if (d.querySelector('iframe') || (d.querySelector('div[id^=container-]') && d.querySelector('div[id^=container-]').children.length)) { d.style.display = ''; clearInterval(iv); }
      else if (Date.now() - t0 > ms) { clearInterval(iv); d.parentNode && d.parentNode.removeChild(d); }
    }, 500);
  }
  function banner(key, w, h, host, id) {
    var d = wrap(id, '<div class="b" style="width:' + w + 'px;max-width:100%;height:' + h + 'px;overflow:hidden;margin:0 auto"></div>');
    return { el: d, run: function () {
      window.atOptions = { key: key, format: 'iframe', height: h, width: w, params: {} };
      var s = document.createElement('script'); s.async = true; s.src = host; d.querySelector('.b').appendChild(s); reveal(d, 10000);
    } };
  }
  var K300 = '825d215f35b6e7c6a1f929819767001a', H300 = 'https://www.highrevenueformat.com/' + K300 + '/invoke.js';
  var ready = false;
  function go(cc) {
    var tier = tierOf(cc);
    // 1) баннер 300x250 на страницах без плеера (все слои)
    if (!isChannel && (mouse || tablet)) setTimeout(function () {
      try {
        var b = banner(K300, 300, 250, H300, 'rtv-ban-page');
        var side = isHome ? document.querySelector('aside.right-sidebar') : null, box = document.querySelector('.seo-box');
        if (side) side.appendChild(b.el); else if (box && box.parentNode) box.parentNode.insertBefore(b.el, box); else beforeFooter(b.el);
        b.run();
      } catch (e) {}
    }, 3000);
    // 2) второй баннер 300x250 внизу страницы (слой A)
    if (tier === 'A' && (mouse || tablet)) setTimeout(function () {
      try { var b = banner(K300, 300, 250, H300, 'rtv-ban-bottom'); beforeFooter(b.el); b.run(); } catch (e) {}
    }, 8000);
    // 3) Native Banner (слои A и B)
    if (tier !== 'C' && (mouse || tablet)) setTimeout(function () {
      try {
        var key = '38aed55c67286ad1a2b32153e5337ddb';
        var d = wrap('rtv-native', '<div id="container-' + key + '"></div>'); d.style.width = '100%'; d.style.maxWidth = '728px';
        beforeFooter(d);
        var s = document.createElement('script'); s.async = true; s.setAttribute('data-cfasync', 'false'); s.src = 'https://bancadeltempoidea.org/21/' + key;
        document.body.appendChild(s); reveal(d, 12000);
      } catch (e) {}
    }, 10000);
    // 4) телефоны: баннер 320x50 в конце страницы (все слои)
    if (phone) setTimeout(function () {
      try {
        var b = banner('9b2a79adb0850bb0ed0eb4fa77cb79dd', 320, 50, 'https://bancadeltempoidea.org/22/9b2a79adb0850bb0ed0eb4fa77cb79dd', 'rtv-ban-mobile');
        beforeFooter(b.el); b.run();
      } catch (e) {}
    }, 6000);
    // 5) Popunder (слой A, компьютеры и планшеты, раз в 24 часа)
    if (POPUNDER_ENABLED && tier === 'A' && (mouse || tablet)) setTimeout(function () {
      try {
        var last = 0; try { last = parseInt(localStorage.getItem('rtv_pop_ts') || '0', 10); } catch (e) {}
        if (last && Date.now() - last < 24 * 3600 * 1000) return;
        if (document.hidden) return;
        try { localStorage.setItem('rtv_pop_ts', String(Date.now())); } catch (e) {}
        var s = document.createElement('script'); s.setAttribute('data-cfasync', 'false'); s.src = 'https://aarems.org/1/12110736e4d0def0bbede4c70cb28a15';
        (document.head || document.documentElement).appendChild(s);
      } catch (e) {}
    }, isChannel ? 180000 : 15000);
  }
  function arm() { if (ready) return; ready = true; getCC(go); }
  function start() {
    if (window.rtvConsentGranted && window.rtvConsentGranted()) arm();
    else window.addEventListener('rtv-consent-granted', arm);
  }
  if (document.readyState === 'complete') start(); else window.addEventListener('load', start);
})();
