/* Согласие на cookie/рекламу и загрузчик счётчиков russian-tv.com (с 18.11.2026).
   При первом посещении поверх страницы по центру показывается окно с одной кнопкой «Согласен» (остальной экран размыт и недоступен).
   Без согласия сайтом пользоваться нельзя, счётчики (GA4, Яндекс.Метрика, Clarity) и реклама не загружаются.
   Согласие хранится в localStorage (ключ rtv_consent). Исключения, где окна нет: страницы политики конфиденциальности (RU/EN, чтобы её можно было прочитать),
   /tv/ (браузер телевизора), /404.html, поисковые и служебные роботы (в том числе Lighthouse), адрес с ?nowall=1 (проверка; счётчики и реклама всё равно ждут согласия).
   Отзыв согласия: кнопка на странице политики (удаляет rtv_consent). */
(function () {
  window.dataLayer = window.dataLayer || [];
  window.gtag = function () { window.dataLayer.push(arguments); };
  var KEY = 'rtv_consent', granted = false, loaded = false;
  try { granted = localStorage.getItem(KEY) === '1'; } catch (e) {}
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
  function grant() { granted = true; try { localStorage.setItem(KEY, '1'); } catch (e) {} loadTrackers(); }

  if (granted) { loadTrackers(); return; }

  var path = location.pathname.replace(/index\.html$/, '');
  var UA = navigator.userAgent || '';
  var noWall = /^\/(en\/)?privacy\/?$/.test(path) || /^\/tv\/?$/.test(path) || /404\.html$/.test(path) ||
    /bot|crawl|spider|slurp|yandex|bingpreview|lighthouse|pagespeed|facebookexternalhit|twitterbot|telegrambot|whatsapp|applebot|duckduckbot|baiduspider|headlesschrome|gtmetrix/i.test(UA) ||
    /[?&]nowall=1/.test(location.search);
  if (noWall) return;

  var en = /^\/en(\/|$)/.test(path) || /^en/i.test(document.documentElement.lang || '');
  var T = en
    ? { h: 'Cookies and advertising', p: 'This site is free and is paid for by advertising. We use cookies and similar technologies to run the site, measure traffic and show ads. By clicking “I agree” you consent to this. Without consent the site cannot be used.', a: 'Privacy Policy', b: 'I agree', href: '/en/privacy/' }
    : { h: 'Файлы cookie и реклама', p: 'Сайт бесплатный и существует за счёт рекламы. Мы используем cookie и похожие технологии для работы сайта, подсчёта посетителей и показа рекламы. Нажимая «Согласен», вы соглашаетесь на их использование. Без согласия пользоваться сайтом нельзя.', a: 'Политика конфиденциальности', b: 'Согласен', href: '/privacy/' };

  var locked = [];
  function show() {
    var d = document.createElement('div');
    d.id = 'rtv-cw'; d.setAttribute('role', 'dialog'); d.setAttribute('aria-modal', 'true'); d.setAttribute('aria-labelledby', 'rtv-cw-h');
    d.style.cssText = 'position:fixed;inset:0;z-index:2147483600;display:flex;align-items:center;justify-content:center;padding:16px;background:rgba(5,5,12,.55);-webkit-backdrop-filter:blur(10px);backdrop-filter:blur(10px)';
    d.innerHTML = '<div style="width:100%;max-width:440px;background:#14141f;border:1px solid #2a2a40;border-radius:16px;padding:24px 22px;color:#f1f1f7;text-align:center;font:15px/1.5 -apple-system,BlinkMacSystemFont,Segoe UI,Roboto,sans-serif;box-shadow:0 20px 60px rgba(0,0,0,.6)">' +
      '<div style="font-size:34px;line-height:1;margin-bottom:8px">🍪</div><h2 id="rtv-cw-h" style="font-size:19px;margin:0 0 10px;font-weight:800"></h2>' +
      '<p style="margin:0 0 14px;color:#c4c4d6;font-size:14px"></p><p style="margin:0 0 18px;font-size:13px"><a target="_blank" rel="noopener" style="color:#7db4ff"></a></p>' +
      '<button type="button" id="rtv-cw-ok" style="width:100%;border:0;border-radius:12px;padding:14px;background:#d52b1e;color:#fff;font:700 16px/1 inherit;cursor:pointer"></button></div>';
    var box = d.firstChild;
    box.querySelector('h2').textContent = T.h; box.querySelectorAll('p')[0].textContent = T.p;
    var a = box.querySelector('a'); a.textContent = T.a; a.href = T.href;
    var ok = box.querySelector('button'); ok.textContent = T.b;
    // страница под окном недоступна: размытие, запрет прокрутки и работы с клавиатуры
    Array.prototype.forEach.call(document.body.children, function (n) { if (n.tagName !== 'SCRIPT' && n.tagName !== 'STYLE') { locked.push(n); n.setAttribute('inert', ''); } });
    document.documentElement.style.overflow = 'hidden';
    document.body.appendChild(d);
    ok.addEventListener('click', function () {
      grant(); d.parentNode.removeChild(d);
      locked.forEach(function (n) { n.removeAttribute('inert'); });
      document.documentElement.style.overflow = '';
    });
    d.addEventListener('keydown', function (e) { if (e.key === 'Tab') { e.preventDefault(); ok.focus(); } });
    setTimeout(function () { try { ok.focus(); } catch (e) {} }, 50);
  }
  if (document.body) show(); else document.addEventListener('DOMContentLoaded', show);
})();
