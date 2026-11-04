/* Monetag OnClick (Popunder), зона 12194084 «Perfect tag»: тест один раз за сессию на всех страницах.
   Браузер открывает новое окно только в ответ на действие пользователя, поэтому скрипт грузится через 5 с,
   а реклама откроется при первом клике после его загрузки. Сессия: одна вкладка (sessionStorage).
   Отметка ставится при этом первом клике, и следующие страницы вкладки скрипт уже не загружают.
   Тег кладёт поверх страницы невидимые слои, и первый клик достаётся им, а не кнопке («запуск» плеера, ссылка).
   Поэтому, когда слой исчезает, клик передаётся элементу сайта в той же точке.
   Отключить: POP_ENABLED = false или ?noads=1 в адресе. */
(function () {
  var POP_ENABLED = true;
  var ZONE = '12194084';
  var SRC = 'https://al5sm.com/tag.min.js';
  var DELAY_MS = 5000;
  var KEY = 'rtv_pop_done';
  var RETRY_MS = [30, 80, 150, 300, 600];
  if (!POP_ENABLED || /[?&]noads=1/.test(location.search)) return;
  // Без sessionStorage нельзя гарантировать один показ, поэтому рекламу не загружаем.
  try { if (sessionStorage.getItem(KEY)) return; } catch (e) { return; }
  var ready = false, known = null;
  function forward(t, x, y, i) {
    var el = document.elementFromPoint(x, y);
    if (el && el !== t && !(t.contains && t.contains(el))) {
      if (el.click) el.click();
      return;
    }
    if (i < RETRY_MS.length) setTimeout(function () { forward(t, x, y, i + 1); }, RETRY_MS[i]);
  }
  function onClick(e) {
    if (!ready || !e.isTrusted) return;
    window.removeEventListener('click', onClick, true);
    try { sessionStorage.setItem(KEY, '1'); } catch (err) {}
    // Элемент появился после загрузки тега: это его слой, а не сайт.
    if (known && !known.has(e.target)) forward(e.target, e.clientX, e.clientY, 0);
    known = null;
  }
  function load() {
    try {
      known = new WeakSet();
      document.querySelectorAll('*').forEach(function (n) { known.add(n); });
      window.addEventListener('click', onClick, true);
      var s = document.createElement('script');
      s.async = true;
      s.dataset.zone = ZONE;
      s.src = SRC;
      s.onload = function () { ready = true; };
      (document.body || document.documentElement).appendChild(s);
    } catch (e) {}
  }
  function arm() { setTimeout(load, DELAY_MS); }
  if (document.readyState === 'complete') arm(); else window.addEventListener('load', arm);
})();
