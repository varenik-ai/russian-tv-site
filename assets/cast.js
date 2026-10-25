/* Трансляция на телевизор для плеера russian-tv.com (главные и страницы каналов, RU/EN).
   - Chromium-браузеры (Chrome, Edge, Opera, Яндекс.Браузер; ПК и Android): Google Cast. Телевизор сам берёт поток
     по ссылке воркера (/stream?channel=ID), телефон/компьютер остаётся свободным.
   - Safari (iPhone, iPad, Mac): AirPlay — только когда видео играет нативным плеером (не через MSE/blob).
   - Остальные браузеры: кнопки нет.
   Скрипт Google Cast (gstatic.com) подгружается лениво и только в Chromium. Требует player-ui.js (панель .rtvp-bar). */
(function () {
  var EN = (document.documentElement.lang || '').toLowerCase().indexOf('en') === 0;
  var T = EN
    ? { cast: 'Cast to TV', air: 'AirPlay', on: 'Casting to', stop: 'Stop casting', fail: 'Could not send this channel to the TV. Try again or pick another channel.', tv: 'TV' }
    : { cast: 'Трансляция на ТВ', air: 'AirPlay', on: 'Транслируется на', stop: 'Остановить трансляцию', fail: 'Не удалось отправить канал на ТВ. Попробуйте ещё раз или выберите другой канал.', tv: 'телевизор' };
  var UA = navigator.userAgent || '';
  var isIOS = /iPhone|iPad|iPod/.test(UA) || (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1);
  var chromium = !!window.chrome && !isIOS && !/Firefox|FxiOS/.test(UA);
  var ICON_CAST = '<svg viewBox="0 0 24 24"><path d="M1 18v3h3c0-1.66-1.34-3-3-3zm0-4v2c2.76 0 5 2.24 5 5h2c0-3.87-3.13-7-7-7zm0-4v2c4.97 0 9 4.03 9 9h2c0-6.08-4.93-11-11-11zm20-7H3c-1.1 0-2 .9-2 2v3h2V5h18v14h-7v2h7c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2z"/></svg>';
  var ICON_AIR = '<svg viewBox="0 0 24 24"><path d="M6 22h12l-6-6-6 6zM21 3H3c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h4v-2H3V5h18v12h-4v2h4c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2z"/></svg>';

  var video = null, wrap = null, bar = null, btn = null, overlay = null, casting = false, lastId = null, origPlay = null, wasPlaying = false;

  function chId() {
    try { if (typeof currentCh !== 'undefined' && currentCh) return currentCh.id; } catch (e) {}
    try { if (typeof CH_ID !== 'undefined') return CH_ID; } catch (e) {}
    return null;
  }
  function chName() {
    try { if (typeof currentCh !== 'undefined' && currentCh) return (EN && currentCh.nameEn) ? currentCh.nameEn : currentCh.name; } catch (e) {}
    var h = document.querySelector('h1'); return h ? h.textContent.replace(/\s*(смотреть|watch|live).*$/i, '').trim() : document.title;
  }
  function chImage() {
    var slug = null;
    try { if (typeof currentCh !== 'undefined' && currentCh && currentCh.slug) slug = currentCh.slug; } catch (e) {}
    if (!slug) { var m = location.pathname.match(/\/([a-z0-9-]+-live)\/?$/); if (m) slug = m[1]; }
    return location.origin + (slug ? '/assets/og/' + slug + '.jpg' : '/og-image.jpg');
  }
  function proxy() { try { if (typeof _currentProxy === 'function') return _currentProxy(); } catch (e) {} return 'https://stream.russian-tv.com'; }

  function css() {
    var s = document.createElement('style');
    s.textContent = '.rtvc-over{position:absolute;inset:0;z-index:37;display:none;flex-direction:column;align-items:center;justify-content:center;gap:14px;padding:20px;text-align:center;background:#0b0b14;color:#fff;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}' +
      '.rtvc-over.rtvc-show{display:flex}.rtvc-over svg{width:44px;height:44px;fill:#7db4ff}.rtvc-over b{font-size:17px}.rtvc-over span{font-size:13px;color:#a8a8c4;max-width:420px}' +
      '.rtvc-over button{border:1px solid rgba(255,255,255,.25);background:rgba(255,255,255,.1);color:#fff;border-radius:18px;padding:9px 18px;font:700 13px/1 inherit;cursor:pointer}' +
      '.rtvc-over button:hover{background:rgba(255,255,255,.2)}';
    document.head.appendChild(s);
  }
  function makeBtn(label, icon) {
    var b = document.createElement('button'); b.type = 'button'; b.className = 'rtvp-btn'; b.innerHTML = icon; b.setAttribute('aria-label', label); b.title = label; b.style.display = 'none'; return b;
  }
  function mount(b) {
    var cin = bar.querySelector('.rtvp-cinema-btn');
    bar.insertBefore(b, cin && cin.parentNode === bar ? cin : null);
  }
  function ensureOverlay() {
    if (overlay) return overlay;
    overlay = document.createElement('div'); overlay.className = 'rtvc-over'; overlay.setAttribute('role', 'status');
    wrap.appendChild(overlay); return overlay;
  }
  function showOverlay(device, err) {
    var o = ensureOverlay(); o.innerHTML = '';
    o.insertAdjacentHTML('beforeend', ICON_CAST);
    var b = document.createElement('b'); b.textContent = T.on + ' ' + (device || T.tv); o.appendChild(b);
    var s = document.createElement('span'); s.textContent = err ? T.fail : chName(); o.appendChild(s);
    var stop = document.createElement('button'); stop.type = 'button'; stop.textContent = T.stop;
    stop.addEventListener('click', function () { try { cast.framework.CastContext.getInstance().endCurrentSession(true); } catch (e) {} });
    o.appendChild(stop); o.classList.add('rtvc-show');
  }

  // ---------------------------------------------------------------- Google Cast
  function initCast() {
    var ctx = cast.framework.CastContext.getInstance();
    ctx.setOptions({ receiverApplicationId: chrome.cast.media.DEFAULT_MEDIA_RECEIVER_APP_ID, autoJoinPolicy: chrome.cast.AutoJoinPolicy.ORIGIN_SCOPED });
    btn = makeBtn(T.cast, ICON_CAST); mount(btn);
    btn.addEventListener('click', function () { if (casting) return; try { ctx.requestSession().catch(function () {}); } catch (e) {} });
    function vis() { var st = ctx.getCastState(); btn.style.display = (st && st !== 'NO_DEVICES_AVAILABLE') ? 'inline-flex' : 'none'; btn.classList.toggle('on', st === 'CONNECTED'); }
    ctx.addEventListener(cast.framework.CastContextEventType.CAST_STATE_CHANGED, vis); vis();
    ctx.addEventListener(cast.framework.CastContextEventType.SESSION_STATE_CHANGED, function (e) {
      var S = cast.framework.SessionState;
      if (e.sessionState === S.SESSION_STARTED || e.sessionState === S.SESSION_RESUMED) start();
      else if (e.sessionState === S.SESSION_ENDED) stop();
      vis();
    });
    if (ctx.getCurrentSession()) start();
    if (/[?&]castdebug=1/.test(location.search)) debugBadge(ctx, vis);
  }
  // диагностика: ?castdebug=1 показывает состояние Cast и Remote Playback и принудительно выводит кнопку
  function debugBadge(ctx, vis) {
    var d = document.createElement('div');
    d.style.cssText = 'position:absolute;left:8px;top:8px;z-index:70;background:rgba(0,0,0,.8);color:#fff;font:12px/1.4 monospace;padding:6px 8px;border-radius:6px;pointer-events:none;max-width:90%';
    wrap.appendChild(d);
    var remote = 'n/a';
    try { var probe = document.createElement('video'); probe.src = proxy() + '/stream?channel=' + (chId() || 'tnt'); probe.style.display = 'none'; document.body.appendChild(probe); probe.remote.watchAvailability(function (a) { remote = String(a); }).catch(function (e) { remote = 'err ' + (e && e.name); }); } catch (e) { remote = 'unsupported'; }
    setInterval(function () { d.textContent = 'Cast: ' + ctx.getCastState() + ' | Remote Playback: ' + remote + ' | Chrome ' + ((UA.match(/Chrome\/(\d+)/) || [])[1] || '?'); btn.style.display = 'inline-flex'; }, 1000);
  }
  function deviceName() { try { return cast.framework.CastContext.getInstance().getCurrentSession().getCastDevice().friendlyName; } catch (e) { return null; } }
  function sendMedia() {
    var ctx = cast.framework.CastContext.getInstance(), s = ctx.getCurrentSession(), id = chId();
    if (!s || !id) return;
    lastId = id;
    var url = proxy() + '/stream?channel=' + encodeURIComponent(id);
    var mi = new chrome.cast.media.MediaInfo(url, 'application/x-mpegURL');
    mi.streamType = chrome.cast.media.StreamType.LIVE;
    var md = new chrome.cast.media.GenericMediaMetadata(); md.title = chName(); md.images = [new chrome.cast.Image(chImage())]; mi.metadata = md;
    var req = new chrome.cast.media.LoadRequest(mi); req.autoplay = true;
    showOverlay(deviceName(), false);
    s.loadMedia(req).catch(function () { showOverlay(deviceName(), true); });
  }
  function start() {
    if (!casting) {
      casting = true; wasPlaying = !video.paused;
      origPlay = video.play; video.play = function () { return Promise.resolve(); };   // страница не должна запускать локальное воспроизведение, пока идёт трансляция
      try { video.pause(); } catch (e) {}
      wrap.classList.add('rtvc-active');
    }
    sendMedia();
  }
  function stop() {
    if (!casting) return;
    casting = false;
    if (origPlay) { video.play = origPlay; origPlay = null; }
    if (overlay) overlay.classList.remove('rtvc-show');
    wrap.classList.remove('rtvc-active');
    if (wasPlaying) { try { var p = video.play(); if (p && p.catch) p.catch(function () {}); } catch (e) {} }
  }
  function loadCastSdk() {
    window.__onGCastApiAvailable = function (ok) { if (ok) { try { initCast(); } catch (e) {} } };
    var s = document.createElement('script'); s.async = true; s.src = 'https://www.gstatic.com/cv/js/sender/v1/cast_sender.js?loadCastFramework=1';
    document.head.appendChild(s);
  }

  // ---------------------------------------------------------------- AirPlay (Safari)
  function initAirPlay() {
    btn = makeBtn(T.air, ICON_AIR); mount(btn);
    try { video.setAttribute('x-webkit-airplay', 'allow'); video.disableRemotePlayback = false; } catch (e) {}
    var available = false, forced = false;
    var isBlob = function () { return /^blob:/.test(video.currentSrc || ''); };
    // iPhone/iPad: hls.js играет через MSE (blob), а AirPlay-видео возможно только с нативным HLS.
    // Поэтому кнопка видна всегда, а первое нажатие на blob-канале переключает его на нативный плеер, второе открывает выбор устройства.
    function vis() { btn.style.display = chId() ? 'inline-flex' : 'none'; btn.classList.toggle('rtvc-ready', !isBlob()); }
    video.addEventListener('webkitplaybacktargetavailabilitychanged', function (e) { available = e.availability === 'available'; vis(); });
    video.addEventListener('loadstart', vis);
    video.addEventListener('playing', vis);
    btn.addEventListener('click', function () {
      if (isBlob()) {
        forced = true;
        try { if (typeof hls !== 'undefined' && hls && hls.destroy) { hls.destroy(); hls = null; } } catch (e) {}
        video.src = proxy() + '/stream?channel=' + encodeURIComponent(chId()) + '&native=1';
        try { var pp = video.play(); if (pp && pp.catch) pp.catch(function () {}); } catch (e) {}
        btn.title = T.air + ' ▶';
        return;
      }
      try { video.webkitShowPlaybackTargetPicker(); } catch (e) {}
    });
  }

  // ---------------------------------------------------------------- запуск
  function boot() {
    video = document.querySelector('.player-wrap video');
    wrap = video && video.closest('.player-wrap');
    bar = wrap && wrap.querySelector('.rtvp-bar');
    if (!bar) return false;
    css();
    if (window.WebKitPlaybackTargetAvailabilityEvent) { initAirPlay(); return true; }
    if (chromium) {
      // смена канала на главной во время трансляции: отправляем новый канал на ТВ, локальное видео остаётся на паузе
      video.addEventListener('loadstart', function () {
        if (!casting) return;
        try { video.pause(); } catch (e) {}
        if (chId() !== lastId) sendMedia();
      });
      if (/[?&]casttest=1/.test(location.search)) { window.__rtvCastInit = initCast; return true; }   // тестовый режим без загрузки SDK Google
      var go = function () { setTimeout(loadCastSdk, 1500); };
      if (document.readyState === 'complete') go(); else window.addEventListener('load', go);
      return true;
    }
    return true;
  }
  var tries = 0;
  (function wait() { if (boot() || ++tries > 40) return; setTimeout(wait, 250); })();
})();
