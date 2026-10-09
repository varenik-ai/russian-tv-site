/* Unified player UI for russian-tv.com (home + channel pages, RU/EN).
   For every .player-wrap with a <video> it adds:
   - a glass control bar (sound + volume, LIVE / "back to live", quality slot, cinema mode, picture-in-picture, fullscreen) that auto-hides while playing
   - a prominent "Turn on sound" call-to-action when the video plays muted
   - click = play/pause (mouse), double click / double tap = fullscreen, big pause indicator
   - remembered volume, buffering spinner, clear error panel with retry + similar channels
   - "video lagging?" hint that offers a lower quality, keyboard shortcuts (M, F, Space, T)
   Existing page logic stays in charge of playback; legacy buttons are hidden and driven through .click(). */
(function () {
  var EN = (document.documentElement.lang || '').toLowerCase().indexOf('en') === 0;
  var T = EN ? {
    mute: 'Mute', unmute: 'Unmute', volume: 'Volume', fs: 'Fullscreen', pip: 'Picture-in-picture', live: 'LIVE', cinema: 'Cinema mode',
    cta: 'Turn on sound', ctaSub: 'Tap here', key: 'M — sound · F — fullscreen · Space — pause · T — cinema', goLive: 'Back to live',
    errTitle: 'Can’t load this channel', errText: 'The source is temporarily unavailable. We keep trying other servers — you can wait or pick another channel.',
    retry: 'Try again', other: 'Watch instead:', lagTitle: 'Video lagging?', lagText: 'Try a lower quality — it needs less internet speed.', lagBtn: 'Lower quality', paused: 'Paused'
  } : {
    mute: 'Выключить звук', unmute: 'Включить звук', volume: 'Громкость', fs: 'Полный экран', pip: 'Картинка в картинке', live: 'В ЭФИРЕ', cinema: 'Режим кинотеатра',
    cta: 'Включить звук', ctaSub: 'Нажмите здесь', key: 'M — звук · F — полный экран · Пробел — пауза · T — кинотеатр', goLive: 'К прямому эфиру',
    errTitle: 'Не удаётся загрузить канал', errText: 'Источник временно недоступен. Мы пробуем другие серверы — можно подождать или выбрать другой канал.',
    retry: 'Повторить', other: 'Смотреть вместо этого:', lagTitle: 'Видео тормозит?', lagText: 'Попробуйте качество ниже — оно требует меньше скорости интернета.', lagBtn: 'Снизить качество', paused: 'Пауза'
  };
  function ls(k, v) { try { if (v === undefined) return localStorage.getItem(k); if (v === null) localStorage.removeItem(k); else localStorage.setItem(k, v); } catch (e) {} return null; }

  var css = document.createElement('style');
  css.textContent = [
    '.rtvp-bar{position:absolute;left:0;right:0;bottom:0;z-index:40;display:flex;align-items:center;gap:8px;padding:28px 12px 10px;background:linear-gradient(to top,rgba(0,0,0,.78),rgba(0,0,0,0));opacity:1;transition:opacity .3s ease;pointer-events:none}',
    '.rtvp-bar>*{pointer-events:auto}',
    '.rtvp.rtvp-idle .rtvp-bar{opacity:0;pointer-events:none}.rtvp.rtvp-idle .rtvp-bar>*{pointer-events:none}',
    '.rtvp.rtvp-idle{cursor:none}',
    '.rtvp-btn{width:40px;height:40px;border-radius:50%;border:1px solid rgba(255,255,255,.18);background:rgba(20,20,34,.62);-webkit-backdrop-filter:blur(10px);backdrop-filter:blur(10px);color:#fff;display:inline-flex;align-items:center;justify-content:center;cursor:pointer;padding:0;transition:background .2s,transform .15s;flex:0 0 auto}',
    '.rtvp-btn:hover{background:rgba(70,90,160,.75)}.rtvp-btn:active{transform:scale(.94)}.rtvp-btn.on{background:rgba(26,95,217,.85)}',
    '.rtvp-btn:focus-visible,.rtvp-cta:focus-visible,.rtvq-btn:focus-visible,.rtvp-pill:focus-visible{outline:2px solid #7db4ff;outline-offset:2px}',
    '.rtvp-btn svg{width:20px;height:20px;fill:currentColor}',
    '.rtvp-vol{width:0;opacity:0;transition:width .2s,opacity .2s;accent-color:#4a8bff;height:4px;cursor:pointer}',
    '.rtvp-soundgrp:hover .rtvp-vol,.rtvp-vol:focus{width:84px;opacity:1}',
    '@media(hover:none){.rtvp-vol{display:none}}',
    '.rtvp-soundgrp{display:flex;align-items:center;gap:8px}',
    '.rtvp-live{display:inline-flex;align-items:center;gap:6px;font:800 11px/1 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;letter-spacing:1px;color:#fff;background:rgba(204,0,0,.9);padding:6px 10px;border-radius:14px;white-space:nowrap}',
    '.rtvp-live i{width:6px;height:6px;border-radius:50%;background:#fff;display:inline-block;animation:rtvp-pulse 1.2s infinite}',
    '.rtvp.rtvp-behind .rtvp-live{background:rgba(90,90,110,.9)}.rtvp.rtvp-behind .rtvp-live i{animation:none;opacity:.5}',
    '@keyframes rtvp-pulse{0%,100%{opacity:1}50%{opacity:.35}}',
    '.rtvp-pill{display:none;align-items:center;border:1px solid rgba(255,255,255,.2);background:rgba(26,95,217,.9);color:#fff;border-radius:18px;padding:0 14px;height:34px;font:700 12px/1 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;cursor:pointer;white-space:nowrap}',
    '.rtvp.rtvp-behind .rtvp-pill.golive{display:inline-flex}',
    '.rtvp-spacer{flex:1}',
    '.rtvp-slot{display:flex;align-items:center;gap:8px}',
    '.rtvq-btn.rtvq-in-bar{position:static;display:inline-flex;align-items:center;height:40px;border-radius:20px;padding:0 14px;border:1px solid rgba(255,255,255,.18);background:rgba(20,20,34,.62);-webkit-backdrop-filter:blur(10px);backdrop-filter:blur(10px);font:600 12px/1 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;opacity:1;z-index:auto}',
    '.rtvq-btn.rtvq-in-bar:hover{background:rgba(70,90,160,.75)}',
    '.rtvq-menu.rtvq-in-bar{top:auto;bottom:62px;right:12px}',
    '.rtvp-cta{position:absolute;top:14px;left:50%;transform:translateX(-50%);z-index:60;display:none;align-items:center;gap:12px;border:0;cursor:pointer;color:#fff;border-radius:32px;padding:10px 22px 10px 12px;background:linear-gradient(135deg,#1a5fd9,#19a8ff);box-shadow:0 8px 30px rgba(26,95,217,.55);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;text-align:left;animation:rtvp-glow 2s infinite}',
    '.rtvp-cta.rtvp-show{display:flex}',
    '.rtvp-cta .ico{width:38px;height:38px;border-radius:50%;background:rgba(255,255,255,.2);display:flex;align-items:center;justify-content:center;flex:0 0 auto}',
    '.rtvp-cta .ico svg{width:22px;height:22px;fill:#fff}',
    '.rtvp-cta b{display:block;font-size:16px;font-weight:800;line-height:1.15}.rtvp-cta small{display:block;font-size:12px;opacity:.85;font-weight:500;margin-top:1px}',
    '@keyframes rtvp-glow{0%,100%{box-shadow:0 8px 30px rgba(26,95,217,.5),0 0 0 0 rgba(25,168,255,.5)}50%{box-shadow:0 8px 30px rgba(26,95,217,.7),0 0 0 12px rgba(25,168,255,0)}}',
    '.rtvp-spin{position:absolute;left:50%;top:50%;width:46px;height:46px;margin:-23px 0 0 -23px;border:4px solid rgba(255,255,255,.25);border-top-color:#fff;border-radius:50%;z-index:35;display:none;animation:rtvp-rot .8s linear infinite;pointer-events:none}',
    '.rtvp-spin.rtvp-show{display:block}@keyframes rtvp-rot{to{transform:rotate(360deg)}}',
    '.rtvp-pausebig{position:absolute;left:50%;top:50%;width:76px;height:76px;margin:-38px 0 0 -38px;z-index:36;border-radius:50%;background:rgba(0,0,0,.55);-webkit-backdrop-filter:blur(8px);backdrop-filter:blur(8px);display:none;align-items:center;justify-content:center;pointer-events:none}',
    '.rtvp-pausebig svg{width:38px;height:38px;fill:#fff}.rtvp-pausebig.rtvp-show{display:flex}',
    '.rtvp-hint{position:absolute;right:14px;top:14px;z-index:41;max-width:80%;font:600 11px/1.3 -apple-system,BlinkMacSystemFont,sans-serif;color:rgba(255,255,255,.8);background:rgba(0,0,0,.5);padding:7px 10px;border-radius:8px;opacity:0;transition:opacity .25s;pointer-events:none}',
    '.rtvp.rtvp-showhint .rtvp-hint{opacity:1}',
    '.rtvp-err{position:absolute;inset:0;z-index:55;display:none;flex-direction:column;align-items:center;justify-content:center;gap:12px;padding:20px;text-align:center;background:rgba(8,8,16,.88);color:#e8e8f4;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}',
    '.rtvp-err.rtvp-show{display:flex}.rtvp-err h4{margin:0;font-size:18px;font-weight:800}.rtvp-err p{margin:0;max-width:440px;font-size:13px;line-height:1.5;color:#a8a8c4}',
    '.rtvp-err .row{display:flex;flex-wrap:wrap;gap:8px;justify-content:center;align-items:center}',
    '.rtvp-err .lbl{font-size:12px;color:#8888a8}',
    '.rtvp-err .rtvp-pill{display:inline-flex;text-decoration:none}.rtvp-err .rtvp-pill.alt{background:rgba(255,255,255,.1)}',
    '.rtvp-toast{position:absolute;left:50%;bottom:76px;transform:translateX(-50%);z-index:58;display:none;align-items:center;gap:12px;max-width:92%;padding:10px 12px 10px 16px;border-radius:14px;background:rgba(18,18,31,.95);border:1px solid #2a2a40;box-shadow:0 8px 28px rgba(0,0,0,.5);color:#e8e8f4;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}',
    '.rtvp-toast.rtvp-show{display:flex}.rtvp-toast b{display:block;font-size:13px}.rtvp-toast span{display:block;font-size:12px;color:#a8a8c4;margin-top:2px}',
    '.rtvp-toast .x{background:none;border:0;color:#a8a8c4;font-size:18px;cursor:pointer;padding:4px 8px}',
    /* прячем старые элементы — теперь всё в единой панели */
    '.rtvp .fs-btn,.rtvp #fullscreen-btn,.rtvp .unmute-banner,.rtvp #unmute-btn{display:none!important}',
    '.rtvp.grid-mode .rtvp-bar,.rtvp.grid-mode .rtvp-cta,.rtvp.grid-mode .rtvp-spin,.rtvp.grid-mode .rtvp-pausebig,.rtvp.rtvp-inactive .rtvp-bar,.rtvp.rtvp-inactive .rtvp-cta,.rtvp.rtvp-inactive .rtvp-pausebig{display:none!important}',
    /* режим кинотеатра (только компьютеры) */
    '@media(min-width:1025px){body.rtv-cinema .left-sidebar,body.rtv-cinema .sidebar-wrapper,body.rtv-cinema .right-sidebar,body.rtv-cinema .tg-col,body.rtv-cinema .side-col{display:none!important}',
    'body.rtv-cinema .page-wrap,body.rtv-cinema .main-wrap{grid-template-columns:1fr!important}body.rtv-cinema .main-col{max-width:1400px!important}body.rtv-cinema .player-col{grid-column:1!important}',
    'body.rtv-cinema .player-wrap:not(.grid-mode){width:min(100%,calc((100vh - 120px)*16/9));margin-left:auto;margin-right:auto}}',
    '.rtvp-cinema-btn{display:none}@media(min-width:1025px){.rtvp-cinema-btn{display:inline-flex}}',
    /* узкие экраны и горизонтальный телефон */
    '@media(max-width:560px){.rtvp-bar{gap:6px;padding:24px 8px 8px}.rtvp-btn{width:38px;height:38px}.rtvp-cta{padding:8px 16px 8px 10px;top:10px}.rtvp-cta b{font-size:14px}.rtvq-btn.rtvq-in-bar{padding:0 10px;height:38px}.rtvp-live{padding:6px 8px}.rtvp-pill{padding:0 10px}}',
    '@media(max-width:380px){.rtvp-live{display:none}.rtvq-btn.rtvq-in-bar{font-size:11px;padding:0 8px}}',
    '@media(max-height:480px) and (orientation:landscape){.rtvp-bar{padding:16px 10px 6px}.rtvp-btn{width:34px;height:34px}.rtvq-btn.rtvq-in-bar{height:34px}.rtvp-cta{top:8px;padding:6px 14px 6px 8px}.rtvp-cta .ico{width:30px;height:30px}.rtvp-cta b{font-size:13px}.rtvp-cta small{display:none}.rtvp-err h4{font-size:15px}.rtvp-err p{display:none}.rtvp-toast{bottom:56px}}'
  ].join('\n');
  document.head.appendChild(css);

  var ICON = {
    vol: '<svg viewBox="0 0 24 24"><path d="M3 9v6h4l5 5V4L7 9H3zm13.5 3A4.5 4.5 0 0 0 14 7.97v8.05A4.5 4.5 0 0 0 16.5 12zM14 3.23v2.06c2.89.86 5 3.54 5 6.71s-2.11 5.85-5 6.71v2.06c4.01-.91 7-4.49 7-8.77s-2.99-7.86-7-8.77z"/></svg>',
    mute: '<svg viewBox="0 0 24 24"><path d="M16.5 12A4.5 4.5 0 0 0 14 7.97v2.21l2.45 2.45c.03-.2.05-.41.05-.63zm2.5 0c0 .94-.2 1.82-.54 2.64l1.51 1.51A8.8 8.8 0 0 0 21 12c0-4.28-2.99-7.86-7-8.77v2.06c2.89.86 5 3.54 5 6.71zM4.27 3 3 4.27 7.73 9H3v6h4l5 5v-6.73l4.25 4.25c-.67.52-1.42.93-2.25 1.18v2.06a8.99 8.99 0 0 0 3.69-1.81L19.73 21 21 19.73l-9-9L4.27 3zM12 4 9.91 6.09 12 8.18V4z"/></svg>',
    pip: '<svg viewBox="0 0 24 24"><path d="M19 7h-8v6h8V7zm2-4H3a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h18a2 2 0 0 0 2-2V5a2 2 0 0 0-2-2zm0 16.01H3V4.98h18v14.03z"/></svg>',
    fs: '<svg viewBox="0 0 24 24"><path d="M7 14H5v5h5v-2H7v-3zm-2-4h2V7h3V5H5v5zm12 7h-3v2h5v-5h-2v3zM14 5v2h3v3h2V5h-5z"/></svg>',
    cin: '<svg viewBox="0 0 24 24"><path d="M19 6H5a2 2 0 0 0-2 2v8a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V8a2 2 0 0 0-2-2zm0 10H5V8h14v8z"/></svg>',
    play: '<svg viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg>'
  };
  function el(tag, cls, html) { var e = document.createElement(tag); if (cls) e.className = cls; if (html) e.innerHTML = html; return e; }
  function btn(label, icon, cls) { var b = el('button', 'rtvp-btn' + (cls ? ' ' + cls : ''), icon); b.type = 'button'; b.setAttribute('aria-label', label); b.title = label; return b; }
  function pill(text, cls) { var b = el('button', 'rtvp-pill' + (cls ? ' ' + cls : '')); b.type = 'button'; b.textContent = text; return b; }

  // ---- похожие каналы для панели ошибки ----
  function similarChannels() {
    var out = [];
    try {
      if (typeof CHANNEL_GROUPS !== 'undefined' && typeof currentCh !== 'undefined' && currentCh) {   // главная
        var grp = CHANNEL_GROUPS.filter(function (g) { return g.channels.some(function (c) { return c.id === currentCh.id; }); })[0];
        (grp ? grp.channels : []).filter(function (c) { return c.id !== currentCh.id; }).slice(0, 3).forEach(function (c) { out.push({ name: EN && c.nameEn ? c.nameEn : c.name, ch: c }); });
        return out;
      }
    } catch (e) {}
    var list = document.getElementById('ch-list');
    if (list) {   // страница канала: берём соседей из той же категории сайдбара
      var items = [], cur = null, started = false;
      Array.prototype.forEach.call(list.children, function (n) {
        if (n.classList.contains('cat-label-s')) { if (started) return; items = []; }
        else if (n.classList.contains('ch-item-s')) { items.push(n); if (n.classList.contains('active')) started = true; }
      });
      items.filter(function (n) { return !n.classList.contains('active'); }).slice(0, 3).forEach(function (n) { out.push({ name: n.getAttribute('data-name'), href: n.getAttribute('href') }); });
    }
    return out;
  }

  function init(wrap) {
    var video = wrap.querySelector('video');
    if (!video || wrap.getAttribute('data-rtvp')) return;
    wrap.setAttribute('data-rtvp', '1'); wrap.classList.add('rtvp');

    var bar = el('div', 'rtvp-bar');
    var grp = el('div', 'rtvp-soundgrp');
    var sound = btn(T.mute, ICON.vol);
    var vol = el('input', 'rtvp-vol'); vol.type = 'range'; vol.min = 0; vol.max = 1; vol.step = 0.05; vol.value = 1; vol.setAttribute('aria-label', T.volume);
    grp.appendChild(sound); grp.appendChild(vol);
    var live = el('span', 'rtvp-live', '<i></i>' + T.live);
    var golive = pill(T.goLive, 'golive');
    var slot = el('div', 'rtvp-slot');
    var cinema = btn(T.cinema, ICON.cin, 'rtvp-cinema-btn');
    var pip = null;
    if (document.pictureInPictureEnabled && video.requestPictureInPicture) {
      pip = btn(T.pip, ICON.pip);
      pip.addEventListener('click', function () { try { if (document.pictureInPictureElement) document.exitPictureInPicture(); else video.requestPictureInPicture(); } catch (e) {} });
    }
    var fs = btn(T.fs, ICON.fs);
    bar.appendChild(grp); bar.appendChild(live); bar.appendChild(golive); bar.appendChild(el('span', 'rtvp-spacer')); bar.appendChild(slot);
    bar.appendChild(cinema); if (pip) bar.appendChild(pip); bar.appendChild(fs);

    var cta = el('button', 'rtvp-cta', '<span class="ico">' + ICON.mute + '</span><span><b>' + T.cta + '</b><small>' + T.ctaSub + '</small></span>');
    cta.type = 'button'; cta.setAttribute('aria-label', T.cta);
    var spin = el('div', 'rtvp-spin');
    var pausebig = el('div', 'rtvp-pausebig', ICON.play); pausebig.setAttribute('aria-hidden', 'true');
    var hint = el('div', 'rtvp-hint'); hint.textContent = T.key;
    var err = el('div', 'rtvp-err'); err.setAttribute('role', 'alert');
    var toast = el('div', 'rtvp-toast'); toast.setAttribute('role', 'status');
    [spin, pausebig, bar, cta, hint, err, toast].forEach(function (n) { wrap.appendChild(n); });

    // ---- звук ----
    function savedVol() { var v = parseFloat(ls('rtv_vol')); return isFinite(v) && v > 0 ? Math.min(1, v) : 1; }
    function isMuted() { return video.muted || video.volume === 0; }
    function setMuted(m, remember) {
      try {
        if (m) { video.muted = true; }
        else { video.muted = false; if (video.volume === 0) video.volume = savedVol(); }
      } catch (e) {}
      try { if (typeof userUnmuted !== 'undefined') userUnmuted = !m; } catch (e) {}
      if (remember !== false) { ls('rtv_muted', m ? '1' : '0'); if (!m) ls('rtv_vol', String(video.volume || 1)); }
      sync();
    }
    var restored = false;
    function restorePrefs() {   // громкость и сознательное «без звука» переносим между каналами
      if (restored) return; restored = true;
      try {
        var v = savedVol(); if (Math.abs(video.volume - v) > 0.01 && ls('rtv_vol')) video.volume = v;
        if (ls('rtv_muted') === '1') video.muted = true;
      } catch (e) {}
    }
    function sync() {
      var m = isMuted();
      sound.innerHTML = m ? ICON.mute : ICON.vol; sound.setAttribute('aria-label', m ? T.unmute : T.mute); sound.title = m ? T.unmute : T.mute;
      vol.value = m ? 0 : video.volume;
      var playing = !video.paused && !video.ended && video.readyState >= 2;
      cta.classList.toggle('rtvp-show', playing && m && ls('rtv_muted') !== '1');
      pausebig.classList.toggle('rtvp-show', video.paused && video.readyState >= 2 && !!(video.currentSrc || video.src));
      wrap.classList.toggle('rtvp-inactive', !(video.currentSrc || video.src) || (!playing && video.readyState < 2 && !video.paused));
    }
    sound.addEventListener('click', function () { setMuted(!isMuted()); });
    cta.addEventListener('click', function (e) { e.stopPropagation(); setMuted(false); });
    vol.addEventListener('input', function () { var v = parseFloat(vol.value); video.volume = v; video.muted = v === 0; ls('rtv_vol', String(v || savedVol())); ls('rtv_muted', v === 0 ? '1' : '0'); sync(); });

    // ---- полный экран / кинотеатр ----
    function toggleFs() {
      var legacy = wrap.querySelector('.fs-btn,#fullscreen-btn');
      if (legacy) { legacy.click(); return; }
      var d = document, active = d.fullscreenElement || d.webkitFullscreenElement;
      if (active) { (d.exitFullscreen || d.webkitExitFullscreen).call(d); }
      else if (wrap.requestFullscreen) wrap.requestFullscreen();
      else if (wrap.webkitRequestFullscreen) wrap.webkitRequestFullscreen();
      else if (video.webkitEnterFullscreen) video.webkitEnterFullscreen();
    }
    fs.addEventListener('click', toggleFs);
    function setCinema(on, remember) { document.body.classList.toggle('rtv-cinema', on); cinema.classList.toggle('on', on); if (remember) ls('rtv_cinema', on ? '1' : '0'); }
    cinema.addEventListener('click', function () { setCinema(!document.body.classList.contains('rtv-cinema'), true); });
    if (ls('rtv_cinema') === '1') setCinema(true, false);

    // ---- пауза / эфир ----
    function togglePlay() { if (video.paused) { var p = video.play(); if (p && p.catch) p.catch(function () {}); } else video.pause(); }
    function liveEdge() { try { return video.seekable.length ? video.seekable.end(video.seekable.length - 1) : 0; } catch (e) { return 0; } }
    function behind() { var e = liveEdge(); return e ? e - video.currentTime : 0; }
    golive.addEventListener('click', function () { var e = liveEdge(); if (e) video.currentTime = Math.max(0, e - 3); var p = video.play(); if (p && p.catch) p.catch(function () {}); wake(); });
    setInterval(function () { wrap.classList.toggle('rtvp-behind', !wrap.classList.contains('rtvp-inactive') && behind() > 15); }, 1000);

    // клик по видео: мышь — пауза/пуск, двойной клик/касание — полный экран, касание — показать панель
    var clickTimer = null;
    wrap.addEventListener('click', function (e) {
      var t = e.target;
      if (t.closest && t.closest('.rtvp-bar,.rtvp-cta,.rtvp-err,.rtvp-toast,.rtvq-menu,.rtvq-btn,button,a,input,#overlay,.player-overlay,.tile-grid')) return;
      if (wrap.classList.contains('rtvp-inactive') || wrap.classList.contains('grid-mode')) return;
      var touch = (e.pointerType === 'touch') || (e.pointerType === undefined && matchMedia('(pointer:coarse)').matches);
      if (clickTimer) { clearTimeout(clickTimer); clickTimer = null; toggleFs(); return; }
      clickTimer = setTimeout(function () { clickTimer = null; if (!touch) togglePlay(); }, 260);
    });

    // ---- события видео ----
    ['volumechange', 'playing', 'pause', 'play', 'loadedmetadata', 'emptied', 'loadstart', 'canplay'].forEach(function (ev) { video.addEventListener(ev, sync); });
    video.addEventListener('playing', restorePrefs); video.addEventListener('emptied', function () { restored = false; });
    ['waiting', 'stalled', 'seeking'].forEach(function (ev) { video.addEventListener(ev, function () { spin.classList.add('rtvp-show'); }); });
    ['playing', 'canplay', 'pause', 'emptied'].forEach(function (ev) { video.addEventListener(ev, function () { spin.classList.remove('rtvp-show'); }); });

    // ---- панель ошибки ----
    var errTimer = null, errArmed = false;
    function hideErr() { err.classList.remove('rtvp-show'); }
    function disarmErr() { errArmed = false; clearTimeout(errTimer); }
    function armErr() {   // отсчёт с первой попытки: повторные перезапуски плеера таймер не сбрасывают
      if (errArmed) return; errArmed = true; clearTimeout(errTimer);
      errTimer = setTimeout(function () { errArmed = false; if (video.readyState < 3 && !wrap.classList.contains('grid-mode')) showErr(); }, 22000);
    }
    function retry() {
      hideErr(); disarmErr(); armErr();
      try { if (typeof loadStream === 'function' && typeof currentCh !== 'undefined' && currentCh) { loadStream(currentCh); return; } } catch (e) {}
      try { if (typeof createHls === 'function') { window._lastCreateHlsAt = 0; createHls(); return; } } catch (e) {}
      try { if (typeof startStream === 'function') { startStream(); return; } } catch (e) {}
      location.reload();
    }
    function showErr() {
      err.innerHTML = '';
      err.appendChild(el('h4', '', T.errTitle)); err.appendChild(el('p', '', T.errText));
      var r1 = el('div', 'row'); var rb = pill(T.retry); rb.style.display = 'inline-flex'; rb.addEventListener('click', retry); r1.appendChild(rb); err.appendChild(r1);
      var sim = similarChannels();
      if (sim.length) {
        var r2 = el('div', 'row'); r2.appendChild(el('span', 'lbl', T.other));
        sim.forEach(function (s) {
          if (s.href) { var a = el('a', 'rtvp-pill alt'); a.href = s.href; a.textContent = s.name; r2.appendChild(a); }
          else { var b = pill(s.name, 'alt'); b.style.display = 'inline-flex'; b.addEventListener('click', function () { hideErr(); try { openChannel(s.ch); } catch (e) {} }); r2.appendChild(b); }
        });
        err.appendChild(r2);
      }
      err.classList.add('rtvp-show'); spin.classList.remove('rtvp-show');
    }
    video.addEventListener('loadstart', armErr);
    video.addEventListener('playing', function () { disarmErr(); hideErr(); });
    video.addEventListener('error', function () { setTimeout(function () { if (video.readyState < 3) showErr(); }, 4000); });

    // ---- «тормозит?» ----
    var waits = [], toastShownAt = 0, toastTimer = null;
    function hideToast() { toast.classList.remove('rtvp-show'); }
    video.addEventListener('waiting', function () {
      var now = Date.now(); waits = waits.filter(function (t) { return now - t < 45000; }); waits.push(now);
      if (waits.length >= 3 && video.currentTime > 5 && now - toastShownAt > 180000 && window.rtvQuality && window.rtvQuality.lower) {
        toastShownAt = now; toast.innerHTML = '';
        var tx = el('div'); tx.appendChild(el('b', '', T.lagTitle)); tx.appendChild(el('span', '', T.lagText)); toast.appendChild(tx);
        var go = pill(T.lagBtn); go.style.display = 'inline-flex'; go.addEventListener('click', function () { try { window.rtvQuality.lower(); } catch (e) {} hideToast(); });
        var x = el('button', 'x', '✕'); x.type = 'button'; x.setAttribute('aria-label', 'Close'); x.addEventListener('click', hideToast);
        toast.appendChild(go); toast.appendChild(x); toast.classList.add('rtvp-show');
        clearTimeout(toastTimer); toastTimer = setTimeout(hideToast, 15000);
      }
    });

    // ---- автоскрытие панели ----
    var idleTimer = null;
    function wake() {
      wrap.classList.remove('rtvp-idle'); clearTimeout(idleTimer);
      idleTimer = setTimeout(function () {
        var keep = video.paused || video.videoWidth === 0 || wrap.querySelector('.rtvq-menu') || bar.matches(':hover') || (document.activeElement && bar.contains(document.activeElement) && document.activeElement.matches(':focus-visible'));
        if (keep) { wake(); return; }
        wrap.classList.add('rtvp-idle');
      }, 3000);
    }
    ['mousemove', 'mousedown', 'touchstart', 'keydown', 'click'].forEach(function (ev) { wrap.addEventListener(ev, wake, { passive: true }); });
    video.addEventListener('playing', wake); video.addEventListener('pause', wake);
    wake(); sync();

    // ---- клавиши ----
    document.addEventListener('keydown', function (e) {
      if (e.metaKey || e.ctrlKey || e.altKey) return;
      var t = e.target; if (t && ((t.tagName === 'INPUT' && t.type !== 'range') || t.tagName === 'TEXTAREA' || t.tagName === 'BUTTON' && (e.key === ' ') || t.isContentEditable)) return;
      if (wrap.classList.contains('rtvp-inactive') || wrap.classList.contains('grid-mode')) return;
      var r = wrap.getBoundingClientRect(); if (r.bottom < 0 || r.top > innerHeight) return;
      var k = (e.key || '').toLowerCase();
      if (k === 'm' || k === 'ь') { setMuted(!isMuted()); e.preventDefault(); wake(); }
      else if (k === 'f' || k === 'а') { toggleFs(); e.preventDefault(); }
      else if (k === 't' || k === 'е') { cinema.click(); e.preventDefault(); }
      else if (k === ' ' || k === 'k' || k === 'л') { togglePlay(); e.preventDefault(); wake(); }
    });
    try { if (matchMedia('(hover:hover)').matches && !ls('rtv_kbhint2')) { video.addEventListener('playing', function once() { video.removeEventListener('playing', once); wrap.classList.add('rtvp-showhint'); setTimeout(function () { wrap.classList.remove('rtvp-showhint'); }, 5000); ls('rtv_kbhint2', '1'); }); } } catch (e) {}
  }

  window.rtvPlayerUI = { init: init };
  function boot() { Array.prototype.forEach.call(document.querySelectorAll('.player-wrap'), init); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot); else boot();
})();
