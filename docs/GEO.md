# GEO : être cité par les moteurs de réponse IA

GEO (Generative Engine Optimization) : faire en sorte que ChatGPT, Claude, Perplexity et les AI Overviews de Google
trouvent, comprennent et citent le site UCIV. Analyse faite d'après le skill `seo-geo` (février 2026) sur le code du site
(il n'est pas encore en ligne : les scores sont des estimations, à refaire sur le site publié).

## Score estimé

| Critère (poids) | Avant | Après | Ce qui a changé |
|---|---|---|---|
| Citabilité (25 %) | 40 | 70 | Réponses directes et autonomes sur chaque page, chiffres et noms exacts |
| Lisibilité structurelle (20 %) | 55 | 85 | Titres en forme de question (H2 puis H3), réponses courtes, listes déjà nombreuses |
| Multimodal (15 %) | 45 | 45 | Images avec texte alternatif déjà en place ; pas de vidéo |
| Autorité et marque (20 %) | 40 | 55 | Fondateur, équipe et réseaux dans les données structurées ; dates sur les articles |
| Accessibilité technique (20 %) | 75 | 92 | Robots IA nommés et autorisés, `llms.txt` complet |
| **Score GEO** | **≈ 51 / 100** | **≈ 71 / 100** | |

Le multimodal et l'autorité hors du site sont les deux critères qui plafonnent le score : voir « Ce que le code ne peut pas faire ».

## Ce qui est en place

### Accessibilité technique
- **Rendu côté serveur** : tout le texte est dans le HTML initial (Django). Les robots IA n'exécutent pas le JavaScript : c'est le point le plus important, et il est acquis.
- **`/robots.txt`** : `GPTBot`, `OAI-SearchBot`, `ChatGPT-User`, `ClaudeBot` et `PerplexityBot` sont nommés et autorisés. L'administration n'y figure pas : une ligne `Disallow` révélerait son adresse secrète (ses pages portent déjà `noindex`). Les robots d'entraînement (`CCBot`, `Bytespider`, `anthropic-ai`, `cohere-ai`) ne sont pas listés : ils suivent donc la règle générale (autorisés). Pour les bloquer, ajouter un groupe `User-agent: …` suivi de `Disallow: /`.
- **`/llms.txt`** : présentation du site, **faits clés** (fondateur, siège, contact, programmes, date de lancement, partenaires), les 14 pages avec leur description, les **5 dernières actualités** (mises à jour automatiquement) et les réseaux.
- **`/sitemap.xml`** et URL canoniques : voir `docs/AVANCEMENT.md` (section SEO).

### Citabilité et structure : section « Questions fréquentes »
- Visible en bas de chacune des 14 pages (`app/includes/_faq.html`, contenu dans `content.FAQ`).
- Chaque entrée est un titre de niveau 3 en forme de question, suivi d'une réponse **autonome** : elle se comprend sans le reste de la page, avec le nom complet « Une Côte d'Ivoire Volontaire (UCIV) », les chiffres et les noms exacts.
- Aucune information inventée : les dates, tarifs et lieux encore inconnus sont annoncés « à confirmer » ; les chiffres d'impact absents sont expliqués.
- **Pas de balisage `FAQPage`** : Google le réserve aux sites publics et de santé, UCIV ne peut pas en bénéficier. Le contenu reste visible dans le HTML, ce qui suffit aux moteurs de réponse.

### Autorité
- **Organisation** (`NGO`) avec fondateur (`Person`), réseaux (`sameAs`), adresse et contact : page d'accueil.
- **Équipe** : les 9 personnes de la page Équipe sont déclarées (`Person`, poste, `worksFor`).
- **Articles** : `Article` avec dates de publication et de modification, auteur, éditeur ; les dates sont dans des balises `<time>`.
- **Pages alimentées par la base** : `dateModified` déduit de la dernière modification.

## Règles pour les rédacteurs (articles, pages)

Les moteurs de réponse citent des **passages** : écrivez pour qu'un paragraphe soit utile seul.

1. **Réponse d'abord** : la phrase d'ouverture d'une section répond directement (40 à 60 mots), puis détaille.
2. **Définition claire** : « UCIV est… », « Les Go du Digital est… », avec le nom complet la première fois.
3. **Passages de 134 à 167 mots** pour les explications importantes (à l'idéal pour la citation) ; une FAQ plus courte reste utile.
4. **Chiffres sourcés** : « 30 à 50 membres », « 6 samedis », « 90 % de pratique » plutôt que des formules vagues.
5. **Titres en questions** (« Comment intégrer UCIV Leadership ? ») et paragraphes de 2 à 4 phrases.
6. **Dates** sur tout contenu daté (le champ « date de publication » d'un article est affiché et déclaré).
7. **Auteur identifié** : remplacer « l'équipe UCIV » par un nom et un rôle dès que possible (crédibilité).

### Passages à réécrire en priorité
- **Accueil, « Pourquoi UCIV ? »** : deux paragraphes de 40 à 50 mots ; en faire un bloc de 134 à 167 mots qui définit UCIV, dit à qui elle s'adresse et ce qu'elle apporte.
- **Qui sommes-nous, « Notre ambition »** : même traitement.
- **Pages programmes** : ajouter une définition en une phrase au début de la première section (« Les Go du Digital est un programme… »).

## Ce que le code ne peut pas faire (actions hors du site)

Les études citées par le skill montrent que les mentions de la marque pèsent environ 3 fois plus que les liens entrants dans les citations IA. Pour progresser, UCIV doit exister ailleurs :

| Action | Pourquoi |
|---|---|
| **Chaîne YouTube** avec des vidéos des programmes (Go du Digital, lancement TEDx) | Signal le plus corrélé aux citations IA |
| **Page LinkedIn** complète et active | Signal d'autorité, déjà déclarée dans `sameAs` |
| **Page Facebook** avec l'adresse réelle (le lien actuel est un lien de partage) | Cohérence des profils |
| **Wikidata**, puis Wikipédia si la notoriété le permet | ChatGPT cite beaucoup ces sources |
| **Presse et blogs** qui parlent d'UCIV et de ses programmes | Mentions externes |
| **Discussions** (Reddit, forums de jeunes ivoiriens) quand elles sont naturelles | Perplexity s'y appuie fortement |
| **Google Search Console** et **Bing Webmaster Tools** (puis IndexNow) | Google AI Overviews cite surtout des pages bien classées ; Copilot s'appuie sur l'index Bing |

Autres pistes à plus long terme : une courte **vidéo** sur chaque programme (le contenu multimodal est davantage cité), une **étude originale** (par exemple un bilan chiffré des promotions), et la licence **RSL 1.0** si UCIV veut préciser les conditions d'usage de ses contenus par les IA.

## Vérifier après la mise en ligne

1. Ouvrir `https://uciv.org/robots.txt` et `https://uciv.org/llms.txt` : les adresses doivent commencer par `https://uciv.org` (variable `SITE_URL`).
2. Poser quelques questions précises à ChatGPT, Perplexity et Google (« Qu'est-ce qu'UCIV en Côte d'Ivoire ? », « Quand est le lancement d'UCIV Leadership ? ») et noter si le site est cité.
3. Refaire cette analyse (`/seo geo https://uciv.org`) un à deux mois après, pour mesurer l'effet.
