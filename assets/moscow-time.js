/* Конвертер «московское время → местное» (страницы США, Великобритании, Канады и страницы каналов для зрителей из этих стран).
   Работает через Intl.DateTimeFormat с часовыми поясами IANA, поэтому сам учитывает переход на летнее время и дату.
   Разметка: <div class="rtv-conv" data-lang="en|ru" data-zones='[["New York","America/New_York"], ...]' data-default="21:00"></div>
   Без JavaScript остаётся статичная таблица на странице (стандартное время). Ничего не отправляется на сервер. */
(function () {
  'use strict';
  var MSK = 'Europe/Moscow';
  function parts(date, tz) {
    var f = new Intl.DateTimeFormat('en-CA', { timeZone: tz, year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit', hourCycle: 'h23' });
    var o = {}; f.formatToParts(date).forEach(function (p) { o[p.type] = p.value; }); return o;
  }
  function fmt(date, tz, lang) {
    var us = lang === 'en' && /^America\//.test(tz);
    return new Intl.DateTimeFormat(lang === 'ru' ? 'ru-RU' : (us ? 'en-US' : 'en-GB'), { timeZone: tz, hour: 'numeric', minute: '2-digit', hour12: us }).format(date);
  }
  function build(el) {
    var lang = el.getAttribute('data-lang') === 'ru' ? 'ru' : 'en', zones = [];
    try { zones = JSON.parse(el.getAttribute('data-zones') || '[]'); } catch (e) {}
    if (!zones.length) return;
    var T = lang === 'ru'
      ? { l: 'Время в Москве', now: 'Сейчас в Москве', prev: 'накануне', next: 'на следующий день', note: 'Расчёт по вашей текущей дате и с учётом летнего времени.', city: 'Город' }
      : { l: 'Moscow time', now: 'Now in Moscow', prev: 'previous day', next: 'next day', note: 'Calculated for today\'s date, including daylight saving time.', city: 'City' };
    var id = 'mt' + Math.random().toString(36).slice(2, 7);
    el.innerHTML = '<div style="display:flex;flex-wrap:wrap;gap:8px 14px;align-items:center;margin:6px 0 4px"><label for="' + id + '" style="color:var(--text);font-weight:600">' + T.l + '</label>' +
      '<input id="' + id + '" type="time" step="300" style="background:var(--bg3,#1b1b30);color:var(--text,#fff);border:1px solid var(--border2,#33334d);border-radius:8px;padding:6px 10px;font:inherit">' +
      '<span class="mt-now" style="color:var(--muted);font-size:13px"></span></div><div class="mt-out" style="overflow-x:auto"></div><p style="color:var(--muted);font-size:12px;margin:6px 0 0">' + T.note + '</p>';
    var input = el.querySelector('input'), out = el.querySelector('.mt-out'), now = el.querySelector('.mt-now');
    input.value = el.getAttribute('data-default') || '21:00';
    function render() {
      var v = (input.value || '21:00').split(':'), h = +v[0], m = +v[1] || 0;
      var nowD = new Date(), p = parts(nowD, MSK);
      var utc = Date.UTC(+p.year, +p.month - 1, +p.day, h - 3, m);   // Москва UTC+3 круглый год
      var d = new Date(utc), mskDay = p.year + p.month + p.day;
      now.textContent = T.now + ': ' + fmt(nowD, MSK, 'ru'.length ? 'ru' : lang).replace(/\s?[AP]M$/i, '');
      var rows = '';
      zones.forEach(function (z) {
        var q = parts(d, z[1]), day = q.year + q.month + q.day, tag = day < mskDay ? ' <span style="color:var(--muted);font-size:12px">(' + T.prev + ')</span>' : day > mskDay ? ' <span style="color:var(--muted);font-size:12px">(' + T.next + ')</span>' : '';
        rows += '<tr style="border-bottom:1px solid var(--border)"><td style="padding:8px 10px;color:var(--text);font-weight:600">' + z[0] + '</td><td style="padding:8px 10px;color:var(--muted)"><strong style="color:var(--text)">' + fmt(d, z[1], lang) + '</strong>' + tag + '</td></tr>';
      });
      out.innerHTML = '<table style="width:100%;border-collapse:collapse;font-size:14px;margin-top:6px"><thead><tr style="border-bottom:2px solid var(--border2)"><th style="text-align:left;padding:8px 10px;color:var(--text)">' + T.city + '</th><th style="text-align:left;padding:8px 10px;color:var(--text)">' + T.l + ' ' + (input.value || '21:00') + ' =</th></tr></thead><tbody>' + rows + '</tbody></table>';
    }
    input.addEventListener('input', render); render();
  }
  function init() { Array.prototype.forEach.call(document.querySelectorAll('.rtv-conv'), function (e) { try { build(e); } catch (x) {} }); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
