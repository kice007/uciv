/* Loader de la page UCIV Leadership : le logo du réseau s'assemble sur fond blanc (voir templates/app/includes/_loader_leadership.html).
   Le logo est découpé en pièces (point, corps, « UCIV. », dix lettres, slogan) qui entrent l'une après l'autre.
   La sortie attend la fin de l'animation ET le chargement de la page, puis joue la sortie du loader du site (sans le rideau orange). Même contrat que le loader du site :
   html.uciv-loading pendant l'attente, événement « uciv:loaded » à la fin. */
(function () {
  'use strict';

  var root = document.getElementById('uciv-loader');
  if (!root) return;
  var logo = root.querySelector('.ull');
  var docEl = document.documentElement;
  var reduit = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  var min = reduit ? 400 : +root.getAttribute('data-min') || 0;
  var max = +root.getAttribute('data-max') || 15000;
  var t0 = performance.now();
  var pret = false, parti = false, fini = false;
  var pieces = {};

  docEl.classList.add('uciv-loading');
  root.classList.add('is-js');

  function sortir() {
    if (parti) return;
    parti = true;
    root.classList.add('is-leaving');
    setTimeout(function () {
      if (root.parentNode) root.parentNode.removeChild(root);
      docEl.classList.remove('uciv-loading');
      window.dispatchEvent(new CustomEvent('uciv:loaded'));
    }, reduit ? 380 : 1320);   // durée de la sortie (logo qui s'élève, puis panneau qui monte)
  }

  // Sort quand la page est chargée et que l'animation a eu le temps de se jouer.
  function planifier() {
    if (fini) return;
    fini = true;
    setTimeout(sortir, Math.max(0, min - (performance.now() - t0)));
  }
  function pageChargee() { pret = true; if (pieces.corps || pieces.erreur) planifier(); }

  if (document.readyState === 'complete') pageChargee(); else window.addEventListener('load', pageChargee);
  setTimeout(function () { pret = true; planifier(); }, max);

  /* Repère du dessin : 2576 px de large, hauteur déduite des proportions réelles du logo. */
  var REF_W = 2576;
  function piece(img, ref, x1, y1, x2, y2) {
    var el = img.cloneNode();
    el.className = 'ull__piece';
    var h = ref.h;
    el.style.clipPath = 'inset(' + [y1 / h * 100, (REF_W - x2) / REF_W * 100, (h - y2) / h * 100, x1 / REF_W * 100]
      .map(function (v) { return v.toFixed(3) + '%'; }).join(' ') + ')';
    el._inset = [y1 / h * 100, (REF_W - x2) / REF_W * 100, (h - y2) / h * 100, x1 / REF_W * 100];
    logo.appendChild(el);
    return el;
  }

  function construire(img) {
    var ref = { h: REF_W * img.naturalHeight / img.naturalWidth };
    logo.style.aspectRatio = img.naturalWidth + ' / ' + img.naturalHeight;
    var xs = [800, 962, 1117, 1322, 1533, 1697, 1903, 2092, 2313, 2375, 2580];
    pieces.point = piece(img, ref, 520, 0, 730, 185);
    pieces.corps = piece(img, ref, 0, 185, 760, 990);
    pieces.uciv = piece(img, ref, 790, 165, 1650, 495);
    pieces.lettres = xs.slice(0, -1).map(function (x, i) { return piece(img, ref, x, 540, xs[i + 1], 840); });
    pieces.slogan = piece(img, ref, 800, 865, 2440, 990);
  }

  function jouer() {
    var o = function (duree, delai, courbe) {
      return { duration: duree, delay: delai, fill: 'both', easing: courbe || 'cubic-bezier(.2,.8,.2,1)' };
    };
    pieces.corps.style.transformOrigin = '30% 90%';
    pieces.corps.animate([{ transform: 'scale(.15) rotate(-30deg)', opacity: 0 }, { transform: 'scale(1) rotate(0)', opacity: 1 }],
      o(1000, 0, 'cubic-bezier(.2,.9,.3,1.25)'));
    pieces.point.animate([{ transform: 'translateY(-90%)', opacity: 0 }, { transform: 'translateY(0)', opacity: 1, offset: 0.55 },
      { transform: 'translateY(-6%)', offset: 0.75 }, { transform: 'translateY(0)', opacity: 1 }], o(1100, 500, 'ease-in'));
    pieces.point.animate([{ transform: 'translateY(0)' }, { transform: 'translateY(-2.5%)' }],
      { duration: 1600, delay: 1800, direction: 'alternate', iterations: Infinity, easing: 'ease-in-out' });
    pieces.uciv.animate([{ transform: 'translateX(-10%)', opacity: 0 }, { transform: 'translateX(0)', opacity: 1 }], o(800, 800));
    pieces.lettres.forEach(function (el, i) {
      el.animate([{ transform: 'translateY(14%)', opacity: 0 }, { transform: 'translateY(0)', opacity: 1 }], o(650, 1400 + i * 80));
    });
    var c = pieces.slogan._inset;
    pieces.slogan.animate([
      { clipPath: 'inset(' + c[0] + '% 100% ' + c[2] + '% ' + c[3] + '%)' },
      { clipPath: 'inset(' + c[0] + '% ' + c[1] + '% ' + c[2] + '% ' + c[3] + '%)' }
    ], o(900, 2500, 'ease-out'));
  }

  // L'animation démarre quand le logo est disponible ; la durée minimale se compte à partir de là.
  var img = new Image();
  img.alt = '';
  img.onload = function () {
    construire(img);
    t0 = performance.now();
    if (!reduit && root.animate !== undefined && pieces.corps.animate) jouer();
    if (pret) planifier();
  };
  img.onerror = function () { pieces.erreur = true; if (pret) planifier(); };
  img.src = root.getAttribute('data-src');
})();
