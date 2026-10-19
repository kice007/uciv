/* Administration UCIV : ouverture et fermeture de la barre latérale sur petits écrans. */
(function () {
  'use strict';

  function init() {
    var menu = document.getElementById('menu-admin');
    var burger = document.querySelector('[data-menu-ouvrir]');
    if (!menu || !burger) return;

    function basculer(ouvert) {
      menu.classList.toggle('est-ouvert', ouvert);
      document.body.classList.toggle('menu-ouvert', ouvert);
      burger.setAttribute('aria-expanded', ouvert ? 'true' : 'false');
    }

    burger.addEventListener('click', function () { basculer(true); });
    document.querySelectorAll('[data-menu-fermer]').forEach(function (el) {
      el.addEventListener('click', function () { basculer(false); });
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') basculer(false);
    });
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
