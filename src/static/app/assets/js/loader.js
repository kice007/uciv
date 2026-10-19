/* Loader UCIV : pilote la sortie du loader (voir templates/app/includes/_loader.html pour les options).
   Événement émis à la fin : window.addEventListener('uciv:loaded', ...). API : UCIVLoader.done() et UCIVLoader.replay(). */
(function () {
  var T = {loop:2100,step:2000,settle:1620,intro:1750}; // ms — must match the CSS timeline
  var KEY = 'uciv-loader-seen';
  var docEl = document.documentElement;
  var template = null;

  function init(root, opts) {
    opts = opts || {};
    var once = opts.once || root.getAttribute('data-once') || 'always';
    try { if (once === 'session' && sessionStorage.getItem(KEY)) { root.parentNode.removeChild(root); return; } } catch (e) {}

    var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
    var min = opts.min != null ? opts.min : +root.getAttribute('data-min') || 0;
    var max = +root.getAttribute('data-max') || 15000;
    var manual = root.getAttribute('data-wait') === 'manual';
    var t0 = performance.now();
    var ready = false, scheduled = false;

    docEl.classList.add('uciv-loading');
    root.classList.add('is-js');

    function finishLoading() {
      if (ready) return;
      ready = true; schedule();
    }
    if (!manual) {
      if (document.readyState === 'complete') finishLoading(); else window.addEventListener('load', finishLoading);
    }
    setTimeout(finishLoading, max);
    root._ucivDone = finishLoading;

    // time spent in the ronde loop, read from the running CSS animation when possible
    function loopTime() {
      var el = root.querySelector('.ul-b0');
      if (el && el.getAnimations) {
        var list = el.getAnimations();
        for (var i = 0; i < list.length; i++) {
          if (list[i].animationName && list[i].animationName.indexOf('ul-r-') === 0 && list[i].currentTime != null) return list[i].currentTime - T.loop;
        }
      }
      return performance.now() - t0 - T.loop;
    }

    function schedule() {
      if (scheduled) return;
      scheduled = true;
      var elapsed = performance.now() - t0;
      var wait = reduce ? 0 : Math.max(0, Math.max(min, T.intro) - elapsed);
      if (!reduce) {
        // inside the loop, leave only once the circle has landed and the lines are redrawn
        var lt = loopTime() + wait + 220;
        if (lt > 0) { var into = lt % T.step; if (into < T.settle) wait += T.settle - into; }
      }
      setTimeout(leave, wait + 220);
    }

    function leave() {
      root.classList.add('is-leaving');
      try { sessionStorage.setItem(KEY, '1'); } catch (e) {}
      setTimeout(function () {
        if (root.parentNode) root.parentNode.removeChild(root);
        docEl.classList.remove('uciv-loading');
        window.dispatchEvent(new CustomEvent('uciv:loaded'));
      }, reduce ? 380 : 1320);
    }
  }

  var first = document.getElementById('uciv-loader');
  if (!first) return;
  template = first.outerHTML;
  init(first);

  window.UCIVLoader = {
    // Single-page apps: set data-wait="manual" on #uciv-loader and call UCIVLoader.done() when ready.
    done: function () { var r = document.getElementById('uciv-loader'); if (r && r._ucivDone) r._ucivDone(); },
    // Replays the full animation (handy for demos). opts.min = minimum display in ms.
    replay: function (opts) {
      var old = document.getElementById('uciv-loader');
      if (old) old.parentNode.removeChild(old);
      var tmp = document.createElement('div');
      tmp.innerHTML = template;
      var root = tmp.firstChild;
      document.body.insertBefore(root, document.body.firstChild);
      init(root, { once: 'always', min: opts && opts.min });
    }
  };
})();
