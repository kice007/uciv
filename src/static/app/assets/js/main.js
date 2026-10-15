/*
 * UCIV — interactions du site (JavaScript sans dépendance).
 * 1. Apparition des blocs au défilement
 * 2. Ombre de l'en-tête quand la page a défilé
 * 3. Menu mobile
 * 4. Points des carrousels à défilement horizontal
 * 5. Formulaires pas encore branchés
 * 6. Pastilles « Objet » du formulaire de contact
 */
(function () {
  'use strict';

  var mouvementReduit = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* 1. Apparition au défilement ------------------------------------------- */
  var blocs = document.querySelectorAll('[data-reveal]');

  function reveler(el) {
    el.classList.add('est-visible');
  }

  if (!('IntersectionObserver' in window)) {
    blocs.forEach(reveler);
  } else {
    var observateur = new IntersectionObserver(function (entrees) {
      entrees.forEach(function (entree) {
        if (!entree.isIntersecting) return;
        var el = entree.target;
        reveler(el);
        observateur.unobserve(el);

        // Dans un carrousel horizontal, les cartes hors écran ne croiseraient jamais
        // la fenêtre : on les révèle en même temps que la première.
        var carrousel = el.parentElement && el.parentElement.closest('[data-defilement]');
        if (carrousel) {
          carrousel.querySelectorAll('[data-reveal]').forEach(function (voisin) {
            reveler(voisin);
            observateur.unobserve(voisin);
          });
        }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -8% 0px' });

    blocs.forEach(function (el) { observateur.observe(el); });
  }

  /* 2. En-tête ------------------------------------------------------------ */
  var entete = document.querySelector('[data-entete]');
  if (entete) {
    var majEntete = function () {
      entete.classList.toggle('est-defile', window.scrollY > 48);
    };
    window.addEventListener('scroll', majEntete, { passive: true });
    majEntete();
  }

  /* 3. Menu mobile -------------------------------------------------------- */
  var menu = document.querySelector('[data-menu]');
  var boutonOuvrir = document.querySelector('[data-menu-ouvrir]');

  if (menu && boutonOuvrir) {
    var panneau = menu.querySelector('.menu-mobile__panneau');
    var boutonFermer = panneau.querySelector('[data-menu-fermer]');

    var ouvrirMenu = function () {
      menu.classList.remove('sans-animation');
      menu.hidden = false;
      // Lecture d'une propriété de mise en page : force le navigateur à prendre en compte
      // l'état de départ avant d'ajouter la classe, sinon la transition ne joue pas.
      void panneau.offsetWidth;
      menu.classList.add('est-ouvert');
      document.body.classList.add('menu-ouvert');
      boutonOuvrir.setAttribute('aria-expanded', 'true');
      boutonFermer.focus({ preventScroll: true });
    };

    var fermerMenu = function (immediat) {
      if (menu.hidden) return;
      menu.classList.toggle('sans-animation', Boolean(immediat));
      menu.classList.remove('est-ouvert');
      document.body.classList.remove('menu-ouvert');
      boutonOuvrir.setAttribute('aria-expanded', 'false');
      boutonOuvrir.focus({ preventScroll: true });

      if (immediat || mouvementReduit) {
        menu.hidden = true;
        return;
      }
      var terminer = function (evenement) {
        if (evenement.target !== panneau || evenement.propertyName !== 'transform') return;
        panneau.removeEventListener('transitionend', terminer);
        // Le menu a pu être rouvert pendant la fermeture.
        if (!menu.classList.contains('est-ouvert')) menu.hidden = true;
      };
      panneau.addEventListener('transitionend', terminer);
    };

    boutonOuvrir.addEventListener('click', ouvrirMenu);
    menu.querySelectorAll('[data-menu-fermer]').forEach(function (el) {
      el.addEventListener('click', function () { fermerMenu(false); });
    });
    menu.querySelectorAll('a').forEach(function (lien) {
      lien.addEventListener('click', function () { fermerMenu(true); });
    });
    document.addEventListener('keydown', function (evenement) {
      // Action au clavier : fermeture immédiate, sans animation.
      if (evenement.key === 'Escape') fermerMenu(true);
    });
    // Si la fenêtre passe en largeur ordinateur, le menu mobile n'a plus lieu d'être.
    window.matchMedia('(min-width: 1280px)').addEventListener('change', function (mq) {
      if (mq.matches) fermerMenu(true);
    });
  }

  /* 4. Carrousels --------------------------------------------------------- */
  document.querySelectorAll('[data-defilement]').forEach(function (piste) {
    var nom = piste.getAttribute('data-defilement');
    var indicateur = document.querySelector('[data-defilement-points="' + nom + '"]');
    if (!indicateur) return;
    var points = indicateur.querySelectorAll('.defilement-indicateur__points span');
    var enAttente = false;

    var maj = function () {
      enAttente = false;
      var cartes = piste.children;
      if (!cartes.length) return;
      var pas = cartes.length > 1 ? cartes[1].offsetLeft - cartes[0].offsetLeft : cartes[0].offsetWidth;
      var finAtteinte = piste.scrollLeft + piste.clientWidth >= piste.scrollWidth - 4;
      var index = finAtteinte ? cartes.length - 1 : Math.round(piste.scrollLeft / pas);
      points.forEach(function (point, i) {
        point.classList.toggle('est-actif', i === index);
      });
    };

    piste.addEventListener('scroll', function () {
      if (enAttente) return;
      enAttente = true;
      window.requestAnimationFrame(maj);
    }, { passive: true });
  });

  /* 5. Formulaires provisoires -------------------------------------------- */
  document.querySelectorAll('[data-form-provisoire]').forEach(function (formulaire) {
    formulaire.addEventListener('submit', function (evenement) {
      evenement.preventDefault();
      var note = formulaire.parentElement.querySelector('p');
      if (note) note.textContent = "L'inscription à la lettre d'information sera bientôt disponible.";
    });
  });
  /* 6. Pastilles « Objet » : elles pilotent la liste déroulante du formulaire de contact. */
  document.querySelectorAll('[data-objet]').forEach(function (liste) {
    var pastilles = document.querySelectorAll('[data-objet-valeur]');
    function synchroniser() {
      pastilles.forEach(function (pastille) {
        pastille.classList.toggle('est-actif', pastille.getAttribute('data-objet-valeur') === liste.value);
      });
    }
    pastilles.forEach(function (pastille) {
      pastille.addEventListener('click', function () {
        liste.value = pastille.getAttribute('data-objet-valeur');
        synchroniser();
      });
    });
    liste.addEventListener('change', synchroniser);
    synchroniser();
  });
})();
