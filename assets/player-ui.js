/* Unified player UI for russian-tv.com (home + channel pages, RU/EN).
   Adds to every .player-wrap with a <video>:
   - a glass control bar (sound + volume, LIVE, quality slot, picture-in-picture, fullscreen) that auto-hides while playing
   - a prominent "Turn on sound" call-to-action whenever the video plays muted
   - a buffering spinner, keyboard shortcuts (M — sound, F — fullscreen)
   Existing page logic stays in charge of playback; legacy fullscreen/unmute buttons are hidden and driven through .click(). */
(function () {
  var EN = (document.documentElement.lang || '').toLowerCase().indexOf('en') === 0;
  var T = EN ? { sound: 'Turn on sound', soundOn: 'Sound on', mute: 'Mute', unmute: 'Unmute', volume: 'Volume', fs: 'Fullscreen', pip: 'Picture-in-picture', live: 'LIVE', cta: 'Turn on sound', ctaSub: 'Tap here', key: 'M — sound · F — fullscreen' }
               : { sound: 'Включить звук', soundOn: 'Звук включён', mute: 'Выключить звук', unmute: 'Включить звук', volume: 'Громкость', fs: 'Полный экран', pip: 'Картинка в картинке', live: 'В ЭФИРЕ', cta: 'Включить звук', ctaSub: 'Нажмите здесь', key: 'M — звук · F — полный экран' };

  var css = document.createElement('style');
  css.textContent = [
    '.rtvp-bar{position:absolute;left:0;right:0;bottom:0;z-index:40;display:flex;align-items:center;gap:8px;padding:28px 12px 10px;background:linear-gradient(to top,rgba(0,0,0,.78),rgba(0,0,0,0));opacity:1;transition:opacity .3s ease;pointer-events:none}',
    '.rtvp-bar>*{pointer-events:auto}',
    '.rtvp.rtvp-idle .rtvp-bar{opacity:0;pointer-events:none}.rtvp.rtvp-idle .rtvp-bar>*{pointer-events:none}',
    '.rtvp-btn{width:40px;height:40px;border-radius:50%;border:1px solid rgba(255,255,255,.18);background:rgba(20,20,34,.62);-webkit-backdrop-filter:blur(10px);backdrop-filter:blur(10px);color:#fff;display:inline-flex;align-items:center;justify-content:center;cursor:pointer;padding:0;transition:background .2s,transform .15s}',
    '.rtvp-btn:hover{background:rgba(70,90,160,.75)}.rtvp-btn:active{transform:scale(.94)}',
    '.rtvp-btn:focus-visible,.rtvp-cta:focus-visible,.rtvq-btn:focus-visible{outline:2px solid #7db4ff;outline-offset:2px}',
    '.rtvp-btn svg{width:20px;height:20px;fill:currentColor}',
    '.rtvp-vol{width:0;opacity:0;transition:width .2s,opacity .2s;accent-color:#4a8bff;height:4px;cursor:pointer}',
    '.rtvp-soundgrp:hover .rtvp-vol,.rtvp-vol:focus{width:84px;opacity:1}',
    '@media(hover:none){.rtvp-vol{display:none}}',
    '.rtvp-soundgrp{display:flex;align-items:center;gap:8px}',
    '.rtvp-live{display:inline-flex;align-items:center;gap:6px;font:800 11px/1 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;letter-spacing:1px;color:#fff;background:rgba(204,0,0,.9);padding:6px 10px;border-radius:14px}',
    '.rtvp-live i{width:6px;height:6px;border-radius:50%;background:#fff;display:inline-block;animation:rtvp-pulse 1.2s infinite}',
    '@keyframes rtvp-pulse{0%,100%{opacity:1}50%{opacity:.35}}',
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
    '.rtvp-hint{position:absolute;right:14px;top:14px;z-index:41;font:600 11px/1 -apple-system,BlinkMacSystemFont,sans-serif;color:rgba(255,255,255,.75);background:rgba(0,0,0,.45);padding:6px 9px;border-radius:8px;opacity:0;transition:opacity .25s;pointer-events:none}',
    '.rtvp.rtvp-showhint .rtvp-hint{opacity:1}',
    /* прячем старые элементы — теперь всё в единой панели */
    '.rtvp .fs-btn,.rtvp #fullscreen-btn,.rtvp .unmute-banner,.rtvp #unmute-btn{display:none!important}',
    '.rtvp.grid-mode .rtvp-bar,.rtvp.grid-mode .rtvp-cta,.rtvp.grid-mode .rtvp-spin,.rtvp.rtvp-inactive .rtvp-bar,.rtvp.rtvp-inactive .rtvp-cta{display:none!important}',
    '@media(max-width:560px){.rtvp-bar{gap:6px;padding:24px 8px 8px}.rtvp-btn{width:38px;height:38px}.rtvp-cta{padding:8px 16px 8px 10px}.rtvp-cta b{font-size:14px}.rtvq-btn.rtvq-in-bar{padding:0 10px;height:38px}}'
  ].join('\n');
  document.head.appendChild(css);

  var ICON = {
    vol: '<svg viewBox="0 0 24 24"><path d="M3 9v6h4l5 5V4L7 9H3zm13.5 3A4.5 4.5 0 0 0 14 7.97v8.05A4.5 4.5 0 0 0 16.5 12zM14 3.23v2.06c2.89.86 5 3.54 5 6.71s-2.11 5.85-5 6.71v2.06c4.01-.91 7-4.49 7-8.77s-2.99-7.86-7-8.77z"/></svg>',
    mute: '<svg viewBox="0 0 24 24"><path d="M16.5 12A4.5 4.5 0 0 0 14 7.97v2.21l2.45 2.45c.03-.2.05-.41.05-.63zm2.5 0c0 .94-.2 1.82-.54 2.64l1.51 1.51A8.8 8.8 0 0 0 21 12c0-4.28-2.99-7.86-7-8.77v2.06c2.89.86 5 3.54 5 6.71zM4.27 3 3 4.27 7.73 9H3v6h4l5 5v-6.73l4.25 4.25c-.67.52-1.42.93-2.25 1.18v2.06a8.99 8.99 0 0 0 3.69-1.81L19.73 21 21 19.73l-9-9L4.27 3zM12 4 9.91 6.09 12 8.18V4z"/></svg>',
    pip: '<svg viewBox="0 0 24 24"><path d="M19 7h-8v6h8V7zm2-4H3a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h18a2 2 0 0 0 2-2V5a2 2 0 0 0-2-2zm0 16.01H3V4.98h18v14.03z"/></svg>',
    fs: '<svg viewBox="0 0 24 24"><path d="M7 14H5v5h5v-2H7v-3zm-2-4h2V7h3V5H5v5zm12 7h-3v2h5v-5h-2v3zM14 5v2h3v3h2V5h-5z"/></svg>'
  };
  function el(tag, cls, html) { var e = document.createElement(tag); if (cls) e.className = cls; if (html) e.innerHTML = html; return e; }
  function btn(label, icon, cls) { var b = el('button', 'rtvp-btn' + (cls ? ' ' + cls : ''), icon); b.type = 'button'; b.setAttribute('aria-label', label); b.title = label; return b; }

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
    var slot = el('div', 'rtvp-slot');
    var pip = null;
    if (document.pictureInPictureEnabled && video.requestPictureInPicture) {
      pip = btn(T.pip, ICON.pip);
      pip.addEventListener('click', function () {
        try { if (document.pictureInPictureElement) document.exitPictureInPicture(); else video.requestPictureInPicture(); } catch (e) {}
      });
    }
    var fs = btn(T.fs, ICON.fs);
    bar.appendChild(grp); bar.appendChild(live); bar.appendChild(el('span', 'rtvp-spacer')); bar.appendChild(slot);
    if (pip) bar.appendChild(pip);
    bar.appendChild(fs);

    var cta = el('button', 'rtvp-cta', '<span class="ico">' + ICON.mute + '</span><span><b>' + T.cta + '</b><small>' + T.ctaSub + '</small></span>');
    cta.type = 'button'; cta.setAttribute('aria-label', T.sound);
    var spin = el('div', 'rtvp-spin');
    var hint = el('div', 'rtvp-hint'); hint.textContent = T.key;
    wrap.appendChild(spin); wrap.appendChild(bar); wrap.appendChild(cta); wrap.appendChild(hint);

    function isMuted() { return video.muted || video.volume === 0; }
    function setMuted(m) {
      try {
        if (m) { video.muted = true; }
        else { video.muted = false; if (video.volume === 0) video.volume = 1; }
      } catch (e) {}
      try { if (typeof userUnmuted !== 'undefined') userUnmuted = !m; } catch (e) {}   // главная страница хранит своё состояние
      sync();
    }
    function sync() {
      var m = isMuted();
      sound.innerHTML = m ? ICON.mute : ICON.vol; sound.setAttribute('aria-label', m ? T.unmute : T.mute); sound.title = m ? T.unmute : T.mute;
      vol.value = m ? 0 : video.volume;
      var playing = !video.paused && !video.ended && video.readyState >= 2;
      cta.classList.toggle('rtvp-show', playing && m && video.videoWidth >= 0);
      wrap.classList.toggle('rtvp-inactive', !(video.currentSrc || video.src) || (!playing && video.readyState < 2));
    }
    sound.addEventListener('click', function () { setMuted(!isMuted()); });
    cta.addEventListener('click', function (e) { e.stopPropagation(); setMuted(false); });
    vol.addEventListener('input', function () { var v = parseFloat(vol.value); video.volume = v; video.muted = v === 0; sync(); });
    fs.addEventListener('click', function () {
      var legacy = wrap.querySelector('.fs-btn,#fullscreen-btn');
      if (legacy) { legacy.click(); return; }
      var d = document, active = d.fullscreenElement || d.webkitFullscreenElement;
      if (active) { (d.exitFullscreen || d.webkitExitFullscreen).call(d); }
      else if (wrap.requestFullscreen) wrap.requestFullscreen();
      else if (wrap.webkitRequestFullscreen) wrap.webkitRequestFullscreen();
      else if (video.webkitEnterFullscreen) video.webkitEnterFullscreen();
    });
    ['volumechange', 'playing', 'pause', 'loadedmetadata', 'emptied', 'loadstart', 'canplay'].forEach(function (ev) { video.addEventListener(ev, sync); });
    ['waiting', 'stalled', 'seeking'].forEach(function (ev) { video.addEventListener(ev, function () { spin.classList.add('rtvp-show'); }); });
    ['playing', 'canplay', 'pause', 'emptied'].forEach(function (ev) { video.addEventListener(ev, function () { spin.classList.remove('rtvp-show'); }); });

    // автоскрытие панели
    var idleTimer = null;
    function wake() {
      wrap.classList.remove('rtvp-idle'); clearTimeout(idleTimer);
      idleTimer = setTimeout(function () {
        var keep = video.paused || video.videoWidth === 0 || wrap.querySelector('.rtvq-menu') || bar.matches(':hover') || document.activeElement && bar.contains(document.activeElement) && document.activeElement.matches(':focus-visible');
        if (keep) { wake(); return; }
        wrap.classList.add('rtvp-idle');
      }, 3000);
    }
    ['mousemove', 'mousedown', 'touchstart', 'keydown', 'click'].forEach(function (ev) { wrap.addEventListener(ev, wake, { passive: true }); });
    video.addEventListener('playing', wake); video.addEventListener('pause', wake);
    wake(); sync();

    // клавиши: M — звук, F — полный экран (когда плеер виден и не вводится текст)
    document.addEventListener('keydown', function (e) {
      if (e.metaKey || e.ctrlKey || e.altKey) return;
      var t = e.target; if (t && (t.tagName === 'INPUT' && t.type !== 'range' || t.tagName === 'TEXTAREA' || t.isContentEditable)) return;
      if (wrap.classList.contains('rtvp-inactive') || wrap.classList.contains('grid-mode')) return;
      var r = wrap.getBoundingClientRect(); if (r.bottom < 0 || r.top > innerHeight) return;
      var k = (e.key || '').toLowerCase();
      if (k === 'm' || k === 'ь') { setMuted(!isMuted()); e.preventDefault(); wake(); }
      else if (k === 'f' || k === 'а') { fs.click(); e.preventDefault(); }
    });
    // подсказка про клавиши — один раз, на компьютере
    try { if (matchMedia('(hover:hover)').matches && !localStorage.getItem('rtv_kbhint')) { video.addEventListener('playing', function once() { video.removeEventListener('playing', once); wrap.classList.add('rtvp-showhint'); setTimeout(function () { wrap.classList.remove('rtvp-showhint'); }, 4500); try { localStorage.setItem('rtv_kbhint', '1'); } catch (e) {} }); } } catch (e) {}
  }

  window.rtvPlayerUI = { init: init };
  function boot() { Array.prototype.forEach.call(document.querySelectorAll('.player-wrap'), init); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot); else boot();
})();
