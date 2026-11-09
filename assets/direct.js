/* Меньше запросов к воркерам: hls.js обновляет плейлист прямо у источника, а не через воркер (/playlist?url=...).
   Только для источников, которые отдают плейлисты с открытым CORS. Главный плейлист и сегменты не меняются.
   v3: при ошибке или зависании такого запроса источник отключается для этой вкладки только на 2 минуты, потом снова
   пробуем напрямую (в v2 отключение действовало до закрытия вкладки). Пока источник отключён, запросы идут через
   воркер с меткой &fb=1: по ней в логах воркера отличаются повторы после сбоя от вкладок без этого скрипта.
   Встроенный плеер (AirPlay) сюда не попадает: у него нет hls.js. */
(function () {
  if (!window.Hls || !Hls.DefaultConfig) return;
  var HOSTS = /^https:\/\/(stream\.smotrim\.ru|streaming\.thestream\.cyou|tvc-hls\.cdnvideo\.ru|live-vgtrksmotrim\.cdnvideo\.ru)\//;
  var TIMEOUT_MS = 8000, RETRY_MS = 120000, KEY = 'rtv_direct_off', off = {};
  try { off = JSON.parse(sessionStorage.getItem(KEY) || '{}') || {}; } catch (e) {}
  // В v2 в хранилище лежала единица: она считается просроченной, прямой путь пробуем снова.
  function blocked(host) { var t = off[host]; return t > 1 && Date.now() - t < RETRY_MS; }
  function disable(host) { off[host] = Date.now(); try { sessionStorage.setItem(KEY, JSON.stringify(off)); } catch (e) {} }
  Hls.DefaultConfig.xhrSetup = function (xhr, url) {
    var m = /\/playlist\?url=([^&]+)$/.exec(url);
    if (!m) return;
    var target = decodeURIComponent(m[1]), hit = HOSTS.exec(target);
    if (!hit) return;
    if (blocked(hit[1])) { xhr.open('GET', url + '&fb=1', true); return; }
    xhr.open('GET', target, true);
    var timer = setTimeout(function () { disable(hit[1]); }, TIMEOUT_MS);
    xhr.addEventListener('loadend', function () { clearTimeout(timer); });
    xhr.addEventListener('error', function () { disable(hit[1]); });
    xhr.addEventListener('load', function () { if (xhr.status < 200 || xhr.status >= 300) disable(hit[1]); });
  };
})();
