window._playerReady = true;
window.dispatchEvent(new CustomEvent('playerReady', { detail: { autoplay: true } }));
