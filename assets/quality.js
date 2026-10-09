/* Quality selector for hls.js players. Usage: rtvQuality.attach(hls, videoEl)
   Shows a "gear" button in the player when the stream offers more than one quality level.
   Choice ("auto", a height like "720", or a bitrate tier like "b2500") is remembered in localStorage ("rtv_quality"). */
(function () {
  var KEY = 'rtv_quality';
  var EN = (document.documentElement.lang || '').toLowerCase().indexOf('en') === 0;
  var T = EN ? { quality: 'Quality', auto: 'Auto', autoHint: 'recommended', mbps: 'Mbit/s' }
             : { quality: 'Качество', auto: 'Авто', autoHint: 'рекомендуется', mbps: 'Мбит/с' };
  function get() { try { return localStorage.getItem(KEY) || 'auto'; } catch (e) { return 'auto'; } }
  function set(v) { try { localStorage.setItem(KEY, v); } catch (e) {} }

  var css = document.createElement('style');
  css.textContent =
    '.rtvq-btn{position:absolute;bottom:10px;right:54px;z-index:51;background:rgba(0,0,0,.65);color:#fff;border:none;border-radius:5px;height:34px;padding:0 10px;font:600 12px/34px -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;cursor:pointer;display:none;white-space:nowrap}' +
    '.rtvq-btn:hover{background:rgba(0,0,0,.9)}' +
    '.player-wrap:hover .rtvq-btn,.rtvq-btn.rtvq-open{display:block}' +
    '@media(hover:none),(pointer:coarse){.rtvq-btn{display:block}}' +
    '.rtvq-menu{position:absolute;bottom:50px;right:10px;z-index:52;background:#12121f;border:1px solid #2a2a40;border-radius:10px;padding:6px;min-width:190px;box-shadow:0 8px 28px rgba(0,0,0,.55);font:13px/1.3 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;color:#e2e2f0}' +
    '.rtvq-menu h4{margin:4px 8px 6px;font-size:11px;font-weight:700;letter-spacing:.5px;text-transform:uppercase;color:#8b8ba0}' +
    '.rtvq-item{display:flex;justify-content:space-between;gap:12px;width:100%;background:none;border:0;color:inherit;text-align:left;padding:8px 10px;border-radius:7px;cursor:pointer;font:inherit}' +
    '.rtvq-item:hover{background:#1c1c32}.rtvq-item[aria-checked=true]{background:#1a3a7a;font-weight:700}' +
    '.rtvq-item small{color:#9a9ab5;font-weight:400}';
  document.head.appendChild(css);

  function tierLabel(level) {
    var h = level.height, mb = level.bitrate ? (level.bitrate / 1e6) : 0;
    var mbTxt = mb ? (mb >= 10 ? mb.toFixed(0) : mb.toFixed(1)) + ' ' + T.mbps : '';
    return { main: h ? h + 'p' : mbTxt, sub: h ? mbTxt : '' };
  }

  function attach(hls, video) {
    if (!hls || !video) return;
    var wrap = video.closest ? video.closest('.player-wrap, #player-screen, body') : null;
    var host = wrap || video.parentNode;
    // убрать прошлые экземпляры (пересоздание hls при реконнекте)
    Array.prototype.forEach.call(host.querySelectorAll('.rtvq-btn,.rtvq-menu'), function (n) { n.parentNode.removeChild(n); });
    var btn = null, menu = null;

    function close() { if (menu) { menu.parentNode.removeChild(menu); menu = null; } if (btn) btn.classList.remove('rtvq-open'); }
    function currentLabel() {
      var pref = get();
      if (pref === 'auto') {
        var lv = hls.levels && hls.levels[hls.currentLevel >= 0 ? hls.currentLevel : 0];
        var hh = (lv && lv.height) || video.videoHeight || 0;
        return T.auto + (hh ? ' (' + hh + 'p)' : '');
      }
      var cl = hls.levels && hls.levels[hls.currentLevel];
      if (cl) { var t = tierLabel(cl); return t.main; }
      return pref.charAt(0) === 'b' ? (parseInt(pref.slice(1), 10) / 1000).toFixed(1) + ' ' + T.mbps : pref + 'p';
    }
    function refreshBtn() { if (btn) btn.textContent = '⚙ ' + currentLabel(); }

    function applyPref() {
      var pref = get(), levels = hls.levels || [];
      if (pref === 'auto' || !levels.length) { hls.currentLevel = -1; return; }
      if (pref.charAt(0) === 'b') { // по битрейту (когда у уровней нет RESOLUTION)
        var wantB = parseInt(pref.slice(1), 10) * 1000, idx = -1, diff = 1e12;
        levels.forEach(function (l, i) { var d = Math.abs((l.bitrate || 0) - wantB); if (d < diff) { diff = d; idx = i; } });
        hls.currentLevel = idx >= 0 ? idx : -1; return;
      }
      var want = parseInt(pref, 10), best = -1, bestH = -1;
      levels.forEach(function (l, i) {
        var h = l.height || 0;
        if (h <= want && h > bestH) { best = i; bestH = h; }
      });
      hls.currentLevel = best >= 0 ? best : -1;   // нет подходящей высоты — оставляем авто
    }

    function build() {
      var levels = hls.levels || [];
      if (levels.length < 2) return;
      btn = document.createElement('button'); btn.type = 'button'; btn.className = 'rtvq-btn'; btn.setAttribute('aria-haspopup', 'true'); btn.setAttribute('aria-label', T.quality);
      host.appendChild(btn);
      applyPref(); refreshBtn();
      btn.addEventListener('click', function (e) {
        e.stopPropagation();
        if (menu) { close(); return; }
        menu = document.createElement('div'); menu.className = 'rtvq-menu'; menu.setAttribute('role', 'menu');
        var h = document.createElement('h4'); h.textContent = T.quality; menu.appendChild(h);
        function item(label, sub, value, checked) {
          var b = document.createElement('button'); b.type = 'button'; b.className = 'rtvq-item'; b.setAttribute('role', 'menuitemradio'); b.setAttribute('aria-checked', checked ? 'true' : 'false');
          b.innerHTML = '<span></span><small></small>'; b.firstChild.textContent = label; b.lastChild.textContent = sub || '';
          b.addEventListener('click', function (ev) { ev.stopPropagation(); set(value); applyPref(); refreshBtn(); close(); });
          menu.appendChild(b);
        }
        var pref = get();
        item(T.auto, T.autoHint, 'auto', pref === 'auto');
        levels.map(function (l, i) { return { l: l, i: i }; }).sort(function (a, b) { return (b.l.bitrate || 0) - (a.l.bitrate || 0); }).forEach(function (x) {
          var t = tierLabel(x.l), val = x.l.height ? String(x.l.height) : 'b' + Math.round((x.l.bitrate || 0) / 1000);
          item(t.main, t.sub, val, pref === val);
        });
        host.appendChild(menu); btn.classList.add('rtvq-open');
      });
      document.addEventListener('click', function (e) { if (menu && !menu.contains(e.target) && e.target !== btn) close(); });
    }

    if (hls.levels && hls.levels.length) build();
    else hls.once(Hls.Events.MANIFEST_PARSED, build);
    hls.on(Hls.Events.LEVEL_SWITCHED, refreshBtn);
    video.addEventListener('resize', refreshBtn);
    video.addEventListener('loadedmetadata', refreshBtn);
  }
  window.rtvQuality = { attach: attach };
})();
