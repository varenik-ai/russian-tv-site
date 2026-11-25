/* Выбор по cookie и рекламе + загрузчик счётчиков russian-tv.com (регион: с 18.11.2026 США — мягкий режим с опт-аутом, остальной мир — окно «Согласен/Отказаться») (с 18.11.2026, кнопка «Отказаться» с 18.11.2026).
   С 19.11.2026: внизу страницы карточка (без размытия и блокировки) с кнопками «Согласен» и «Отказаться»; остальная страница размыта и недоступна, пока выбор не сделан.
   «Согласен»: загружаются счётчики (GA4, Яндекс.Метрика, Clarity) и реклама, передаются технические данные о воспроизведении (rtv-monitor).
   «Отказаться»: сайт работает как обычно, но счётчики, реклама и передача данных о воспроизведении выключены. Состав сервисов описан в политике конфиденциальности, окно только ссылается на неё.
   РЕГИОН: страна определяется воркером мониторинга (GET /geo, кэш sessionStorage rtv_cc). США — без блокирующего окна: счётчики и реклама включены по умолчанию (опт-аут, как принято в США),
   внизу уведомление «ОК / Отказаться» и в подвале ссылка «Do Not Sell or Share My Personal Information»; «Отказаться» запоминается (localStorage rtv_optout=1). ЕС, Великобритания, Швейцария,
   Канада и все остальные (в том числе пока страна неизвестна) — блокирующее окно ниже. Юридическую корректность подтверждают юристы владельца.
   Отказ действует на один заход (с 18.11.2026): время отказа хранится в localStorage (rtv_decl), пока посетитель ходит по сайту с перерывами не дольше 30 минут окно не показывается (отметка продлевается на каждой странице),
   а при следующем заходе после перерыва окно показывается снова, и так до согласия. Согласие хранится постоянно: rtv_consent = '1'. Окна нет: на странице политики (RU/EN), /tv/, /404.html, для поисковых и служебных роботов
   (включая Lighthouse) и при ?nowall=1 (счётчики и реклама всё равно ждут согласия). Изменить выбор — кнопка на странице политики. */
(function () {
  window.dataLayer = window.dataLayer || [];
  window.gtag = function () { window.dataLayer.push(arguments); };
  var KEY = 'rtv_consent', granted = false, loaded = false, OKEY = 'rtv_optout', AKEY = 'rtv_us_ack';
  var choice = null, VISIT_MS = 30 * 60 * 1000, DKEY = 'rtv_decl';
  try { choice = localStorage.getItem(KEY); granted = choice === '1'; if (choice === '0') { localStorage.removeItem(KEY); choice = null; } } catch (e) {}   // прежний постоянный отказ ('0') больше не действует
  window.rtvConsentGranted = function () { return granted; };

  // Google Consent Mode v2 (с 18.11.2026, решение владельца): Google Analytics загружается сразу, но без согласия analytics_storage = denied
  // (без cookie и идентификаторов, только обезличенные сигналы для модели Google); рекламные разрешения Google всегда denied (рекламу Google на сайте мы не показываем).
  // «Согласен» (или США без отказа) -> analytics_storage = granted. Яндекс.Метрика и Clarity по-прежнему грузятся только после согласия.
  var BOT = /bot|crawl|spider|slurp|bingpreview|lighthouse|pagespeed|facebookexternalhit|twitterbot|telegrambot|whatsapp|applebot|duckduckbot|baiduspider|headlesschrome|gtmetrix/i.test(navigator.userAgent || '');
  // 25.11.2026: в мягком режиме (SOFT_ALL) аналитика и так включается всем, кто не отказался (а отказавшимся GA не загружается вовсе, см. DECL),
  // поэтому analytics_storage = granted ставится сразу, до первого события. Раньше granted приходил только после ответа /geo (до 1,5 с), и первый
  // page_view / session_start новой сессии уходил без cookie: GA терял нового пользователя и источник перехода (поиск, рефералы).
  var SOFT_ALL_EARLY = true;   // держать в синхроне с SOFT_ALL ниже
  gtag('consent', 'default', { ad_storage: 'denied', ad_user_data: 'denied', ad_personalization: 'denied', analytics_storage: (granted || SOFT_ALL_EARLY) ? 'granted' : 'denied' });
  var DECL = false; try { DECL = localStorage.getItem(OKEY) === '1'; } catch (e) {}
  if (!BOT && !DECL) {
    gtag('js', new Date()); gtag('config', 'G-XLSJE8NKJE', { allow_google_signals: false, allow_ad_personalization_signals: false });
    var g = document.createElement('script'); g.async = true; g.src = 'https://www.googletagmanager.com/gtag/js?id=G-XLSJE8NKJE'; document.head.appendChild(g);
  }
  var anal = false;
  window.rtvAnalyticsAllowed = function () { return anal; };   // счётчики и мониторинг (отдельно от рекламы: rtvConsentGranted)
  function loadAnalytics() {
    if (anal) return; anal = true;
    gtag('consent', 'update', { analytics_storage: 'granted' });
    (function (c, l, a, r, i, t, y) { c[a] = c[a] || function () { (c[a].q = c[a].q || []).push(arguments); }; t = l.createElement(r); t.async = 1; t.src = 'https://www.clarity.ms/tag/' + i; y = l.getElementsByTagName(r)[0]; y.parentNode.insertBefore(t, y); })(window, document, 'clarity', 'script', 'xkhl4v4ft0');
    (function (m, e, t, r, i, k, a) { m[i] = m[i] || function () { (m[i].a = m[i].a || []).push(arguments); }; m[i].l = 1 * new Date(); k = e.createElement(t); a = e.getElementsByTagName(t)[0]; k.async = 1; k.src = r; a.parentNode.insertBefore(k, a); })(window, document, 'script', 'https://mc.yandex.ru/metrika/tag.js', 'ym');
    ym(110584472, 'init', { clickmap: true, trackLinks: true, accurateTrackBounce: true, webvisor: false });
  }
  function loadAdsOnly() {   // «Отказаться» (с 19.11.2026): счётчики выключены, реклама работает
    if (loaded) return; loaded = true;
    try { window.dispatchEvent(new Event('rtv-consent-granted')); } catch (e) {}
  }
  function loadTrackers() {
    if (loaded) return; loaded = true; loadAnalytics();
    try { window.dispatchEvent(new Event('rtv-consent-granted')); } catch (e) {}
  }
  function grant() { granted = true; try { localStorage.setItem(KEY, '1'); localStorage.removeItem(DKEY); } catch (e) {} loadTrackers(); }

  if (granted) { loadTrackers(); return; }
  // отказался недавно (заход продолжается): окна нет, счётчиков и рекламы нет; отметка продлевается
  try { var dt = parseInt(localStorage.getItem(DKEY) || '0', 10); if (dt && Date.now() - dt < VISIT_MS) { localStorage.setItem(DKEY, String(Date.now())); return; } } catch (e) {}

  var path = location.pathname.replace(/index\.html$/, '');
  var UA = navigator.userAgent || '';
  var noWall = /^\/(en\/)?privacy\/?$/.test(path) || /^\/tv\/?$/.test(path) || /404\.html$/.test(path) ||
    /bot|crawl|spider|slurp|yandex|bingpreview|lighthouse|pagespeed|facebookexternalhit|twitterbot|telegrambot|whatsapp|applebot|duckduckbot|baiduspider|headlesschrome|gtmetrix/i.test(UA) ||
    /[?&]nowall=1/.test(location.search);
  if (noWall) return;

  var en = /^\/en(\/|$)/.test(path) || /^en/i.test(document.documentElement.lang || '');
  var T = en
    ? { h: 'Cookies', p: 'We use cookies and similar technologies to run the site, count visitors and for partner services. Click “I agree” to allow this, or “Decline”: the site will work without tracking cookies and partner services.', a: 'Full rules and the list of services — Privacy Policy', b: 'I agree', n: 'Decline', href: '/en/privacy/' }
    : { h: 'Файлы cookie', p: 'Мы используем cookie и похожие технологии для работы сайта, подсчёта посетителей и сервисов партнёров. Нажмите «Согласен», чтобы разрешить это, или «Отказаться»: сайт будет работать без отслеживающих cookie и сервисов партнёров.', a: 'Подробные правила и перечень сервисов — Политика конфиденциальности', b: 'Согласен', n: 'Отказаться', href: '/privacy/' };

  // --- ЕС, Великобритания, Швейцария, Канада и страна неизвестна: карточка внизу страницы с двумя равными кнопками (с 19.11.2026; прежнее блокирующее окно убрано) ---
  function show() {
    var d = document.createElement('div');
    d.id = 'rtv-cw'; d.setAttribute('role', 'dialog'); d.setAttribute('aria-labelledby', 'rtv-cw-h');
    d.style.cssText = 'position:fixed;left:12px;right:12px;bottom:12px;z-index:2147483600;max-width:680px;margin:0 auto;background:#14141f;color:#f1f1f7;border:1px solid #2a2a40;border-radius:12px;padding:12px 14px;font:13px/1.45 -apple-system,BlinkMacSystemFont,Segoe UI,Roboto,sans-serif;box-shadow:0 8px 30px rgba(0,0,0,.55)';
    var bs = 'flex:1 1 0;min-width:110px;border:1px solid #3a3a52;border-radius:8px;padding:10px 14px;font:700 13px/1 inherit;cursor:pointer;color:#fff;';
    d.innerHTML = '<div id="rtv-cw-h" style="font-weight:700;margin-bottom:3px"></div><div style="color:#c4c4d6;font-size:12px"></div>' +
      '<div style="font-size:12px;margin:3px 0 10px"><a target="_blank" rel="noopener" style="color:#7db4ff"></a></div>' +
      '<div style="display:flex;gap:10px"><button type="button" id="rtv-cw-ok" style="' + bs + 'background:#d52b1e;border-color:#d52b1e"></button><button type="button" id="rtv-cw-no" style="' + bs + 'background:#2a2a40"></button></div>';
    d.children[0].textContent = T.h; d.children[1].textContent = T.p;
    var a = d.querySelector('a'); a.textContent = T.a; a.href = T.href;
    var ok = d.querySelector('#rtv-cw-ok'), no = d.querySelector('#rtv-cw-no'); ok.textContent = T.b; no.textContent = T.n;
    document.body.appendChild(d);
    function close() { if (d.parentNode) d.parentNode.removeChild(d); }
    ok.addEventListener('click', function () { grant(); close(); });
    no.addEventListener('click', function () { try { localStorage.setItem(DKEY, String(Date.now())); } catch (e) {} close(); });
  }
  // --- США: мягкий режим (опт-аут) ---
  var tUS = en
    ? { p: 'We use cookies, analytics and partner services to run this site.', ok: 'OK', no: 'Opt out', a: 'Privacy Policy', ds: 'Do Not Sell or Share My Personal Information', href: '/en/privacy/' }
    : { p: 'Мы используем cookie, аналитику и сервисы партнёров для работы сайта.', ok: 'ОК', no: 'Отказаться', a: 'Политика конфиденциальности', ds: 'Do Not Sell or Share My Personal Information', href: '/privacy/' };
  // остальной мир (не ЕС/Великобритания/Швейцария/Канада): тот же мягкий режим, кнопка «Согласен», без ссылки «Do Not Sell»
  var tOW = { p: tUS.p, ok: en ? 'I agree' : 'Согласен', no: en ? 'Decline' : 'Отказаться', a: tUS.a, ds: tUS.ds, href: tUS.href };
  function softUS(isUS) {
    if (!isUS) tUS = tOW;
    try { if (localStorage.getItem(OKEY) === '1') { granted = true; loadAdsOnly(); return; } } catch (e) {}   // «Отказаться» (с 19.11.2026): счётчики и мониторинг выключены, реклама работает
    granted = true; loadTrackers();
    var ack = false; try { ack = localStorage.getItem(AKEY) === '1'; } catch (e) {}
    function foot() {
      var f = document.querySelector('footer'); if (!f || f.querySelector('#rtv-ds')) return;
      if (!isUS) return;
      var d = document.createElement('div'); d.id = 'rtv-ds'; d.style.cssText = 'margin-top:8px;font-size:12px';
      d.innerHTML = '<a style="color:inherit;text-decoration:underline"></a>'; var a = d.firstChild; a.textContent = tUS.ds; a.href = tUS.href; f.appendChild(d);
    }
    function bar() {
      if (ack) return;
      var b = document.createElement('div'); b.id = 'rtv-us';
      b.style.cssText = 'position:fixed;left:12px;right:12px;bottom:12px;z-index:2147483000;max-width:640px;margin:0 auto;background:#14141f;color:#f1f1f7;border:1px solid #2a2a40;border-radius:12px;padding:12px 14px;font:13px/1.45 -apple-system,BlinkMacSystemFont,Segoe UI,Roboto,sans-serif;display:flex;flex-wrap:wrap;gap:8px 12px;align-items:center;box-shadow:0 8px 30px rgba(0,0,0,.5)';
      b.innerHTML = '<span style="flex:1 1 220px"></span><a target="_blank" rel="noopener" style="color:#7db4ff"></a><button type="button" id="rtv-us-ok" style="border:0;border-radius:8px;padding:8px 16px;background:#d52b1e;color:#fff;font:700 13px/1 inherit;cursor:pointer"></button><button type="button" id="rtv-us-no" style="border:1px solid #3a3a52;border-radius:8px;padding:8px 14px;background:transparent;color:#c4c4d6;font:600 13px/1 inherit;cursor:pointer"></button>';
      var sp = b.children[0], a = b.children[1], ok = b.children[2], no = b.children[3];
      sp.textContent = tUS.p; a.textContent = tUS.a; a.href = tUS.href; ok.textContent = tUS.ok; no.textContent = tUS.no;
      ok.addEventListener('click', function () { try { localStorage.setItem(AKEY, '1'); } catch (e) {} b.parentNode.removeChild(b); });
      no.addEventListener('click', function () { try { localStorage.setItem(OKEY, '1'); localStorage.setItem(AKEY, '1'); } catch (e) {} location.reload(); });
      document.body.appendChild(b);
    }
    function ready() { bar(); foot(); }
    if (document.body) ready(); else document.addEventListener('DOMContentLoaded', ready);
  }
  function getCC(cb) {
    var cc = null; try { cc = sessionStorage.getItem('rtv_cc'); } catch (e) {}
    if (cc) return cb(cc);
    var done = false, t = setTimeout(function () { if (!done) { done = true; cb('XX'); } }, 1500);
    try {
      fetch('https://rtv-monitor.dyaltd.workers.dev/geo').then(function (r) { return r.json(); }).then(function (j) {
        if (done) return; done = true; clearTimeout(t); var c = (j && j.cc) || 'XX'; try { sessionStorage.setItem('rtv_cc', c); } catch (e) {} cb(c);
      }).catch(function () { if (!done) { done = true; clearTimeout(t); cb('XX'); } });
    } catch (e) { if (!done) { done = true; clearTimeout(t); cb('XX'); } }
  }
  var STRICT = ' AT BE BG HR CY CZ DK EE FI FR DE GR HU IE IT LV LT LU MT NL PL PT RO SK SI ES SE IS LI NO GB CH CA ';
  // страна не определилась (XX): с 19.11.2026 мягкий режим «остального мира»; исключение — часовой пояс браузера в Европе (кроме России, Беларуси, Украины, Турции) или Канаде: там осторожная карточка
  function tzStrict() {
    var tz = ''; try { tz = Intl.DateTimeFormat().resolvedOptions().timeZone || ''; } catch (e) {}
    if (/^Europe\/(Moscow|Kaliningrad|Samara|Volgograd|Saratov|Astrakhan|Ulyanovsk|Kirov|Simferopol|Minsk|Kiev|Kyiv|Uzhgorod|Zaporozhye|Istanbul|Chisinau|Tiraspol)$/.test(tz)) return false;
    return /^Europe\//.test(tz) || /^Atlantic\/Reykjavik$/.test(tz) || /^America\/(Toronto|Montreal|Vancouver|Edmonton|Winnipeg|Halifax|St_Johns|Regina|Moncton|Glace_Bay|Iqaluit|Yellowknife|Whitehorse|Dawson|Thunder_Bay|Nipigon|Rainy_River|Swift_Current|Goose_Bay|Cambridge_Bay|Inuvik|Rankin_Inlet|Resolute|Pangnirtung|Atikokan|Blanc-Sablon|Creston|Dawson_Creek|Fort_Nelson)$/.test(tz);
  }
  // ВРЕМЕННО (с 19.11.2026): мягкий режим во всех странах, как в «остальном мире» (решение владельца); вернуть региональную карточку — SOFT_ALL = false
  var SOFT_ALL = true;   // при возврате региональной карточки (false) поставить и SOFT_ALL_EARLY = false в начале файла
  function decide() { getCC(function (cc) { if (SOFT_ALL && cc !== 'US') softUS(false); else if (cc === 'US') softUS(true); else if (STRICT.indexOf(' ' + cc + ' ') >= 0 || (cc === 'XX' && tzStrict())) show(); else softUS(false); }); }
  if (document.body) decide(); else document.addEventListener('DOMContentLoaded', decide);
})();
