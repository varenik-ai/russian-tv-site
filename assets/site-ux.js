/* Mobile channel switcher for channel pages: the left sidebar is hidden on screens <=1024px,
   so we build a compact category tabs + horizontally scrollable channel strip from the sidebar markup. */
(function () {
  var list = document.getElementById('ch-list');
  if (!list) return;
  var EN = (document.documentElement.lang || '').toLowerCase().indexOf('en') === 0;
  var st = document.createElement('style');
  st.textContent = '.m-switch{display:none;background:var(--card,#12121f);border:1px solid var(--border,#1e1e32);border-radius:12px;padding:10px 0 8px;min-height:112px}' +
    '@media(max-width:1024px){.m-switch{display:block}}' +
    '.m-switch h2{font-size:12px;font-weight:700;letter-spacing:.5px;text-transform:uppercase;color:var(--muted,#8b8ba0);margin:0 12px 8px}' +
    '.m-tabs,.m-row{display:flex;gap:8px;overflow-x:auto;padding:0 12px;scrollbar-width:none;-webkit-overflow-scrolling:touch}' +
    '.m-tabs::-webkit-scrollbar,.m-row::-webkit-scrollbar{display:none}' +
    '.m-tab{flex:0 0 auto;border:1px solid var(--border2,#2a2a40);background:transparent;color:var(--text,#e2e2f0);border-radius:16px;padding:5px 12px;font:600 12px inherit;cursor:pointer}' +
    '.m-tab[aria-selected=true]{background:var(--accent,#1a5fd9);border-color:var(--accent,#1a5fd9);color:#fff}' +
    '.m-row{margin-top:8px}' +
    '.m-ch{flex:0 0 auto;display:flex;align-items:center;gap:8px;border:1px solid var(--border,#1e1e32);background:var(--bg3,#151525);border-radius:10px;padding:6px 10px;color:var(--text,#e2e2f0);text-decoration:none;font-size:12px;font-weight:600;white-space:nowrap}' +
    '.m-ch.active{border-color:var(--accent,#1a5fd9);background:rgba(26,95,217,.18)}' +
    '.m-ch i{width:26px;height:26px;border-radius:6px;display:flex;align-items:center;justify-content:center;font-style:normal;font-size:9px;font-weight:900;flex:0 0 auto;overflow:hidden}' +
    '.m-ch i img{width:100%;height:100%;object-fit:contain;padding:2px;box-sizing:border-box}';
  document.head.appendChild(st);

  var cats = [], cur = null;
  Array.prototype.forEach.call(list.children, function (el) {
    if (el.classList.contains('cat-label-s')) { cur = { name: el.textContent.trim(), items: [] }; cats.push(cur); }
    else if (cur && el.classList.contains('ch-item-s')) cur.items.push(el);
  });
  if (!cats.length) return;
  var activeCat = 0;
  cats.forEach(function (c, i) { c.items.forEach(function (it) { if (it.classList.contains('active')) activeCat = i; }); });

  var wrap = document.createElement('nav');
  wrap.className = 'm-switch';
  wrap.setAttribute('aria-label', EN ? 'Switch channel' : 'Сменить канал');
  var h = document.createElement('h2'); h.textContent = EN ? 'Switch channel' : 'Другие каналы';
  var tabs = document.createElement('div'); tabs.className = 'm-tabs'; tabs.setAttribute('role', 'tablist');
  var row = document.createElement('div'); row.className = 'm-row';
  wrap.appendChild(h); wrap.appendChild(tabs); wrap.appendChild(row);

  function render(idx) {
    Array.prototype.forEach.call(tabs.children, function (t, i) { t.setAttribute('aria-selected', i === idx ? 'true' : 'false'); });
    row.innerHTML = '';
    cats[idx].items.forEach(function (it) {
      var a = document.createElement('a'); a.href = it.getAttribute('href'); a.className = 'm-ch' + (it.classList.contains('active') ? ' active' : '');
      var ic = it.querySelector('.ch-icon-s'); var i = document.createElement('i');
      if (ic) { i.setAttribute('style', ic.getAttribute('style') || ''); var im = ic.querySelector('img'); if (im) { var c = document.createElement('img'); c.src = im.src; c.alt = ''; c.width = 22; c.height = 22; c.loading = 'lazy'; i.appendChild(c); } else i.textContent = ic.textContent; }
      var s = document.createElement('span'); s.textContent = it.getAttribute('data-name') || it.textContent.trim();
      a.appendChild(i); a.appendChild(s); row.appendChild(a);
    });
    var act = row.querySelector('.active'); if (act && row.scrollTo) row.scrollTo({ left: Math.max(0, act.offsetLeft - 12), behavior: 'auto' });
  }
  cats.forEach(function (c, i) {
    var b = document.createElement('button'); b.type = 'button'; b.className = 'm-tab'; b.setAttribute('role', 'tab');
    b.textContent = c.name.replace(/^[^A-Za-zА-Яа-я]+/, '');
    b.addEventListener('click', function () { render(i); });
    tabs.appendChild(b);
  });
  render(activeCat);
  var anchor = document.getElementById('status') || document.getElementById('player-wrap');
  if (anchor && anchor.parentNode) anchor.parentNode.insertBefore(wrap, anchor.nextSibling);
})();
