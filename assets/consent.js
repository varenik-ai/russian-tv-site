/* Выбор по cookie и рекламе + загрузчик счётчиков russian-tv.com (с 18.11.2026, кнопка «Отказаться» с 19.11.2026).
   При первом посещении по центру экрана окно с кнопками «Согласен» и «Отказаться»; остальная страница размыта и недоступна, пока выбор не сделан.
   «Согласен»: загружаются счётчики (GA4, Яндекс.Метрика, Clarity) и реклама, передаются технические данные о воспроизведении (rtv-monitor).
   «Отказаться»: сайт работает как обычно, но счётчики, реклама и передача данных о воспроизведении выключены. Состав сервисов описан в политике конфиденциальности, окно только ссылается на неё.
   Отказ действует на один заход (с 19.11.2026): время отказа хранится в localStorage (rtv_decl), пока посетитель ходит по сайту с перерывами не дольше 30 минут окно не показывается (отметка продлевается на каждой странице),
   а при следующем заходе после перерыва окно показывается снова, и так до согласия. Согласие хранится постоянно: rtv_consent = '1'. Окна нет: на странице политики (RU/EN), /tv/, /404.html, для поисковых и служебных роботов
   (включая Lighthouse) и при ?nowall=1 (счётчики и реклама всё равно ждут согласия). Изменить выбор — кнопка на странице политики. */
(function () {
  window.dataLayer = window.dataLayer || [];
  window.gtag = function () { window.dataLayer.push(arguments); };
  var KEY = 'rtv_consent', granted = false, loaded = false;
  var choice = null, VISIT_MS = 30 * 60 * 1000, DKEY = 'rtv_decl';
  try { choice = localStorage.getItem(KEY); granted = choice === '1'; if (choice === '0') { localStorage.removeItem(KEY); choice = null; } } catch (e) {}   // прежний постоянный отказ ('0') больше не действует
  window.rtvConsentGranted = function () { return granted; };

  function loadTrackers() {
    if (loaded) return; loaded = true;
    gtag('js', new Date()); gtag('config', 'G-XLSJE8NKJE');
    var g = document.createElement('script'); g.async = true; g.src = 'https://www.googletagmanager.com/gtag/js?id=G-XLSJE8NKJE'; document.head.appendChild(g);
    (function (c, l, a, r, i, t, y) { c[a] = c[a] || function () { (c[a].q = c[a].q || []).push(arguments); }; t = l.createElement(r); t.async = 1; t.src = 'https://www.clarity.ms/tag/' + i; y = l.getElementsByTagName(r)[0]; y.parentNode.insertBefore(t, y); })(window, document, 'clarity', 'script', 'xkhl4v4ft0');
    (function (m, e, t, r, i, k, a) { m[i] = m[i] || function () { (m[i].a = m[i].a || []).push(arguments); }; m[i].l = 1 * new Date(); k = e.createElement(t); a = e.getElementsByTagName(t)[0]; k.async = 1; k.src = r; a.parentNode.insertBefore(k, a); })(window, document, 'script', 'https://mc.yandex.ru/metrika/tag.js', 'ym');
    ym(110584472, 'init', { clickmap: true, trackLinks: true, accurateTrackBounce: true, webvisor: false });
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
    ? { h: 'Cookies and advertising', p: 'We use cookies and similar technologies to run the site, count visitors and show ads. Click “I agree” to allow this, or “Decline”: the site will work without analytics and ads.', a: 'Full rules and the list of services — Privacy Policy', b: 'I agree', n: 'Decline', href: '/en/privacy/' }
    : { h: 'Файлы cookie и реклама', p: 'Мы используем cookie и похожие технологии для работы сайта, подсчёта посетителей и показа рекламы. Нажмите «Согласен», чтобы разрешить это, или «Отказаться»: сайт будет работать без аналитики и рекламы.', a: 'Подробные правила и перечень сервисов — Политика конфиденциальности', b: 'Согласен', n: 'Отказаться', href: '/privacy/' };

  var locked = [];
  function show() {
    var d = document.createElement('div');
    d.id = 'rtv-cw'; d.setAttribute('role', 'dialog'); d.setAttribute('aria-modal', 'true'); d.setAttribute('aria-labelledby', 'rtv-cw-h');
    d.style.cssText = 'position:fixed;inset:0;z-index:2147483600;display:flex;align-items:center;justify-content:center;padding:16px;background:rgba(5,5,12,.55);-webkit-backdrop-filter:blur(10px);backdrop-filter:blur(10px)';
    d.innerHTML = '<div style="width:100%;max-width:440px;background:#14141f;border:1px solid #2a2a40;border-radius:16px;padding:24px 22px;color:#f1f1f7;text-align:center;font:15px/1.5 -apple-system,BlinkMacSystemFont,Segoe UI,Roboto,sans-serif;box-shadow:0 20px 60px rgba(0,0,0,.6)">' +
      '<div style="font-size:34px;line-height:1;margin-bottom:8px">🍪</div><h2 id="rtv-cw-h" style="font-size:19px;margin:0 0 10px;font-weight:800"></h2>' +
      '<p style="margin:0 0 14px;color:#c4c4d6;font-size:14px"></p><p style="margin:0 0 18px;font-size:13px"><a target="_blank" rel="noopener" style="color:#7db4ff"></a></p>' +
      '<button type="button" id="rtv-cw-ok" style="width:100%;border:0;border-radius:12px;padding:14px;background:#d52b1e;color:#fff;font:700 16px/1 inherit;cursor:pointer"></button>' +
      '<button type="button" id="rtv-cw-no" style="width:100%;margin-top:10px;border:1px solid #3a3a52;border-radius:12px;padding:13px;background:transparent;color:#c4c4d6;font:600 15px/1 inherit;cursor:pointer"></button></div>';
    var box = d.firstChild;
    box.querySelector('h2').textContent = T.h; box.querySelectorAll('p')[0].textContent = T.p;
    var a = box.querySelector('a'); a.textContent = T.a; a.href = T.href;
    var ok = box.querySelector('#rtv-cw-ok'), no = box.querySelector('#rtv-cw-no'); ok.textContent = T.b; no.textContent = T.n;
    // страница под окном недоступна: размытие, запрет прокрутки и работы с клавиатуры
    Array.prototype.forEach.call(document.body.children, function (n) { if (n.tagName !== 'SCRIPT' && n.tagName !== 'STYLE') { locked.push(n); n.setAttribute('inert', ''); } });
    document.documentElement.style.overflow = 'hidden';
    document.body.appendChild(d);
    function close() { d.parentNode.removeChild(d); locked.forEach(function (n) { n.removeAttribute('inert'); }); document.documentElement.style.overflow = ''; }
    ok.addEventListener('click', function () { grant(); close(); });
    no.addEventListener('click', function () { try { localStorage.setItem(DKEY, String(Date.now())); } catch (e) {} close(); });
    d.addEventListener('keydown', function (e) { if (e.key === 'Tab') { e.preventDefault(); (document.activeElement === ok ? no : ok).focus(); } });
    setTimeout(function () { try { ok.focus(); } catch (e) {} }, 50);
  }
  if (document.body) show(); else document.addEventListener('DOMContentLoaded', show);
})();
