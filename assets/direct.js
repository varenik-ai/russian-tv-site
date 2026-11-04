/* Меньше запросов к воркерам: hls.js обновляет плейлист прямо у источника, а не через воркер (/playlist?url=...).
   Только для источников, которые отдают плейлисты с открытым CORS. Главный плейлист и сегменты не меняются.
   При ошибке или зависании такого запроса источник отключается для этой вкладки, и повтор hls.js идёт через воркер, как раньше.
   Встроенный плеер (AirPlay) сюда не попадает: у него нет hls.js. */
(function () {
  if (!window.Hls || !Hls.DefaultConfig) return;
  var HOSTS = /^https:\/\/(stream\.smotrim\.ru|streaming\.thestream\.cyou|tvc-hls\.cdnvideo\.ru|live-vgtrksmotrim\.cdnvideo\.ru)\//;
  var TIMEOUT_MS = 8000, KEY = 'rtv_direct_off', off = {};
  try { off = JSON.parse(sessionStorage.getItem(KEY) || '{}') || {}; } catch (e) {}
  function disable(host) { off[host] = 1; try { sessionStorage.setItem(KEY, JSON.stringify(off)); } catch (e) {} }
  Hls.DefaultConfig.xhrSetup = function (xhr, url) {
    var m = /\/playlist\?url=([^&]+)$/.exec(url);
    if (!m) return;
    var target = decodeURIComponent(m[1]), hit = HOSTS.exec(target);
    if (!hit || off[hit[1]]) return;
    xhr.open('GET', target, true);
    var timer = setTimeout(function () { disable(hit[1]); }, TIMEOUT_MS);
    xhr.addEventListener('loadend', function () { clearTimeout(timer); });
    xhr.addEventListener('error', function () { disable(hit[1]); });
    xhr.addEventListener('load', function () { if (xhr.status < 200 || xhr.status >= 300) disable(hit[1]); });
  };
})();
