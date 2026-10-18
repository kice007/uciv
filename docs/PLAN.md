# Plan de réalisation du site UCIV

Source : `maquette/design_uciv.pen` (16 écrans desktop à 1440 px et 15 écrans mobiles à 390 px). Ce plan liste ce
qu'il faut construire pour passer de la page d'accueil actuelle au site complet.

## 1. Résumé

| | État |
|---|---|
| Page d'accueil | Faite (`app/layout/index.html`), à comparer à la maquette |
| Pages restantes | 14 pages + 1 modèle d'article |
| Composants partagés | En-tête, pied de page, bandeau : faits ; fil d'Ariane, hero de page, formulaires : à faire |
| Données | Tout est en dur dans `app/content.py` ; modèles Django à créer pour le contenu modifiable |
| Formulaires | 4 à créer (engagement, partenariat, contact, newsletter) |
| Responsive | Mobile : écrans « … — Mobile » de la maquette (fait, section 23 de `main.css`) ; tablette à définir |

## 2. Direction artistique (écran « Fondations »)

À reporter dans `static/app/assets/css/main.css` (vérifier qu'ils y sont déjà).

| Rôle | Valeur |
|---|---|
| Orange | `#E17F1C` (foncé `#B45F0D`) |
| Jaune | `#F7C548` |
| Vert | `#1B7A43` (profond `#0C3322`) |
| Fonds | crème `#FBF5EA`, sable `#F1E6D3`, blanc `#FFFFFF` |
| Textes | encre `#17120C`, texte `#5C5247` |
| Titres | Bricolage Grotesque |
| Accent éditorial | Instrument Serif (italique) |
| Corps | Plus Jakarta Sans |
| Manuscrit | Caveat |

## 3. Pages à réaliser

Toutes les pages partagent : bandeau d'annonce, en-tête, hero, pied de page.

| # | Page | URL proposée | Sections | Spécificités |
|---|---|---|---|---|
| 1 | Accueil | `/` | Hero, Manifeste, Engagement en expérience, Domaines d'action, Programmes, Vision & chiffres, Rejoindre UCIV, Fondateur, Actualités, Partenaires | Existe : auditer l'écart avec la maquette |
| 2 | Qui sommes-nous ? | `/qui-sommes-nous/` | Hero, Ambition, Vision & mission, Valeurs (6), Citation, Fondateur | Contenu statique |
| 3 | Équipe | `/qui-sommes-nous/equipe/` | Hero, Président, Bureau exécutif (4), Médias & communication (4), Appel | Données : `MembreEquipe`. Bios « à transmettre » |
| 4 | Nos programmes | `/programmes/` | Hero, Méthode (3 étapes), Les programmes (3 cartes + « à venir »), Appel | Cartes alimentées par le modèle `Programme` |
| 5 | Les Go du Digital | `/programmes/go-du-digital/` | Hero, Repères, Volets (4), Apprentissages (5), Pédagogie, Public & suivi, Partenaires du programme, Inscriptions | Gabarit « page programme » |
| 6 | UCIV Leadership | `/programmes/uciv-leadership/` | Hero, Repères, Vision & mission, Intégrer le réseau (4 étapes), Pourquoi rejoindre, Principes (5), Thème, Lancement | Gabarit « page programme » |
| 7 | Experience Lab | `/programmes/experience-lab/` | Hero, Approche, Objectifs (6), Inscriptions | Gabarit « page programme » |
| 8 | Je veux m'engager | `/engagement/` | Hero, Trois façons, Formulaire d'engagement | Formulaire 1 |
| 9 | Partenaires | `/partenaires/` | Hero, Ils nous accompagnent (3), Formes de collaboration (10), Proposer un partenariat | Formulaire 2 |
| 10 | Opportunités | `/opportunites/` | Hero, Catégories (5), Opportunités du moment (filtrables), Appel | Modèle `Opportunite`, filtre par catégorie |
| 11 | Actualités | `/actualites/` | Hero, Fil d'actualités (filtres 10 catégories, article à la une) | Modèle `Article` |
| 12 | Article | `/actualites/<slug>/` | Hero article, Corps, À lire aussi (3), Appel | Gabarit unique pour tous les articles |
| 13 | Notre impact | `/impact/` | Hero, UCIV en chiffres (6), Nos histoires (3), Citation | Modèle `Indicateur` ; valeurs `000` à remplacer |
| 14 | Ressources | `/ressources/` | Hero, Bibliothèque (filtres Type × Thème), Appel | Modèle `Ressource` |
| 15 | Contact | `/contact/` | Hero, Formulaire & coordonnées | Formulaire 3 |

Fiches à prévoir en plus (liens « Voir le détail » / « Consulter ») : détail d'une
opportunité et d'une ressource. Non dessinées dans la maquette : à décider.

## 4. Composants partagés

| Composant | Où | État |
|---|---|---|
| Bandeau d'annonce | haut de toutes les pages | Fait (`_header.html`) |
| En-tête + navigation (7 entrées + CTA « Je veux m'engager ») | toutes | Fait ; ajouter l'état « page active » |
| Pied de page (4 colonnes + newsletter + réseaux) | toutes | Fait ; brancher la newsletter |
| Hero de page intérieure | toutes sauf accueil | À faire : fil d'Ariane, surtitre, titre, chapo, CTA, mot manuscrit |
| Bloc « Appel » (titre + bouton) | 5 pages | À faire |
| Bloc « Citation » | Qui sommes-nous, Impact | À faire |
| Bloc « Fondateur » | Accueil, Qui sommes-nous | Fait sur l'accueil : à extraire en include |
| Bandeau de repères (3-4 chiffres clés) | pages programme | À faire |
| Liste numérotée (01, 02…) | valeurs, principes, étapes | À faire |
| Carte article / carte opportunité / carte ressource | listes | À faire |
| Filtres (pastilles) | Opportunités, Actualités, Ressources | À faire (JS léger) |
| Champs de formulaire (texte, e-mail, tél., liste, cases, zone de texte) | 3 formulaires | À faire |

Recommandation : un gabarit `app/base/page.html` (hero + contenu + appel + pied) et
un include par composant dans `templates/app/includes/`.

## 5. Modèles de données

Tous héritent de `Convention` (`created_at`, `update_at`, `publish`).

| Modèle | Champs principaux |
|---|---|
| `Programme` | titre, slug, étiquette, accroche, texte, image, repères, ordre |
| `Article` | titre, slug, catégorie, extrait, corps, image, légende, auteur, date, temps de lecture, à la une |
| `Opportunite` | catégorie (5), intitulé, source (UCIV/partenaire), structure, lieu, date limite, description, lien |
| `Ressource` | type (6), thème (4), titre, méta (pages/durée), fichier ou lien |
| `MembreEquipe` | nom, rôle, groupe (président / bureau / médias), bio, photo, ordre |
| `Partenaire` | nom, rôle, logo, programme(s) |
| `Indicateur` | libellé, valeur, ordre |
| `SoumissionEngagement` | nom, e-mail, téléphone, choix, compétences, message |
| `SoumissionPartenariat` | nom, organisation, e-mail, téléphone, type, message |
| `SoumissionContact` | nom, e-mail, téléphone, organisation, objet, message |
| `Abonne` | e-mail, date |

Attention : `ImageField` exige Pillow, retiré des dépendances. Soit réinstaller
Pillow, soit utiliser des chemins d'image statiques / `FileField`.

## 6. Formulaires

| Formulaire | Champs | Traitement |
|---|---|---|
| Engagement | Nom, e-mail, téléphone, « Je souhaite » (3 choix), domaines de compétences (10 cases, facultatif), message | Enregistrer + e-mail à l'équipe + accusé de réception |
| Partenariat | Nom, organisation, e-mail, téléphone, type de collaboration (10), présentation | Idem |
| Contact | Nom, e-mail, téléphone, organisation (facultatif), objet (7), message | Idem |
| Newsletter | E-mail | Enregistrer, désinscription à prévoir |

Communs : protection CSRF, anti-spam (champ piège), messages de succès/erreur,
mention « Tes données servent uniquement à te recontacter » et lien vers une
**politique de confidentialité à rédiger** (page absente de la maquette).

## 7. Étapes de réalisation

1. **Socle** : gabarit de page intérieure, fil d'Ariane, état actif de la navigation, includes (appel, citation, repères, liste numérotée).
2. **Pages statiques** : Qui sommes-nous, Nos programmes, les 3 pages programme.
3. **Contenu dynamique** : modèles `Article`, `Opportunite`, `Ressource`, `MembreEquipe`, `Indicateur`, administration Django, migration de `content.py`.
4. **Listes et filtres** : Actualités, Article, Opportunités, Ressources, Équipe, Impact.
5. **Formulaires** : Engagement, Partenariat, Contact, Newsletter, e-mails.
6. **Finitions** : responsive mobile/tablette, accessibilité, SEO (titres, métadonnées, `sitemap.xml`), performances des images, page 404.
7. **Mise en ligne** : réglages de production (`DEBUG=False`, `ALLOWED_HOSTS`, `SECRET_KEY`), `collectstatic`, hébergement.

## 8. Points à clarifier

- **Textes provisoires** dans la maquette : dates, tarifs, modalités et lieux « à confirmer » ; chiffres d'impact `000` ; bios de l'équipe « à transmettre » ; crédits photo ; modèle d'article avec crochets `[...]`.
- **Responsive** : les écrans mobiles existent (390 px) ; la tablette n'est pas dessinée.
- **Pages manquantes** : politique de confidentialité, mentions légales, 404, détail d'une opportunité / d'une ressource.
- **Newsletter** : service d'envoi (le projet est limité à Django) ou simple collecte d'adresses ?
- **Images** : photos à fournir pour chaque hero (Qui sommes-nous, programmes, article…) ; le site actuel en a 10.
- **Réseaux sociaux** : URLs réelles de Facebook, TikTok (`@uneciv`), LinkedIn.
- **Hébergement** et nom de domaine.
