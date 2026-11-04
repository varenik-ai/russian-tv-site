/* Monetag OnClick (Popunder), зона 12194084 «Perfect tag»: тест один раз за сессию на всех страницах.
   Браузер открывает новое окно только в ответ на действие пользователя, поэтому скрипт грузится через 5 с,
   а реклама откроется при первом клике после его загрузки. Сессия: одна вкладка (sessionStorage).
   Отметка ставится при этом первом клике, и следующие страницы вкладки скрипт уже не загружают.
   Отключить: POP_ENABLED = false или ?noads=1 в адресе. */
(function () {
  var POP_ENABLED = true;
  var ZONE = '12194084';
  var SRC = 'https://al5sm.com/tag.min.js';
  var DELAY_MS = 5000;
  var KEY = 'rtv_pop_done';
  if (!POP_ENABLED || /[?&]noads=1/.test(location.search)) return;
  // Без sessionStorage нельзя гарантировать один показ, поэтому рекламу не загружаем.
  try { if (sessionStorage.getItem(KEY)) return; } catch (e) { return; }
  function mark() {
    window.removeEventListener('click', mark, true);
    try { sessionStorage.setItem(KEY, '1'); } catch (e) {}
  }
  function load() {
    try {
      var s = document.createElement('script');
      s.async = true;
      s.dataset.zone = ZONE;
      s.src = SRC;
      s.onload = function () { window.addEventListener('click', mark, true); };
      (document.body || document.documentElement).appendChild(s);
    } catch (e) {}
  }
  function arm() { setTimeout(load, DELAY_MS); }
  if (document.readyState === 'complete') arm(); else window.addEventListener('load', arm);
})();
