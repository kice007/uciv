"""
Contenus du site, issus du cahier de contenu éditorial (UCIV/info/uciv.md).

Pour l'instant les contenus sont écrits ici, en Python. Les éléments qui
devront être modifiables par l'équipe (articles, chiffres d'impact,
partenaires, opportunités) passeront plus tard en base de données, via des
modèles Django et l'interface d'administration.

Les liens marqués '#' pointent vers des pages qui n'existent pas encore.
"""

from django.urls import reverse, reverse_lazy
from django.utils.functional import lazy

URL_LEADERSHIP = reverse_lazy('app:uciv_leadership')
URL_QUI = reverse_lazy('app:qui_sommes_nous')
URL_PROGRAMMES = reverse_lazy('app:nos_programmes')
URL_HOME = reverse_lazy('app:home')
URL_OPPORTUNITES = reverse_lazy('app:opportunites')
URL_ACTUALITES = reverse_lazy('app:actualites')
URL_IMPACT = reverse_lazy('app:impact')
URL_RESSOURCES = reverse_lazy('app:ressources')
URL_PARTENAIRES = reverse_lazy('app:partenaires')
URL_CONTACT = reverse_lazy('app:contact')

def _engagement(choix=''):
    return reverse('app:engagement') + (f'?choix={choix}#formulaire' if choix else '')


URL_ENGAGEMENT = lazy(_engagement, str)()
URL_VOLONTAIRE = lazy(_engagement, str)('volontaire')
URL_COMPETENCES = lazy(_engagement, str)('competences')
URL_REJOINDRE_LEADERSHIP = lazy(_engagement, str)('leadership')

URL_GO = reverse_lazy('app:go_du_digital')
URL_EXPERIENCE = reverse_lazy('app:experience_lab')
URL_VISION_ACTION = reverse_lazy('app:vision_action')
URL_RH_PAROLE = reverse_lazy('app:rh_parole')
URL_INSCRIPTION_PROGRAMME = lazy(lambda: reverse('app:contact') + '?objet=Programme#ecrire', str)()

# --- Éléments communs à toutes les pages ----------------------------------

ANNONCE = {
    'date': '24 octobre 2026',
    'texte': "Lancement d'UCIV Leadership : conférence au format TEDx à l'American Corner.",
    'texte_court': "Lancement d'UCIV Leadership",
    'lien_label': 'Rejoindre UCIV Leadership',
    'url': URL_REJOINDRE_LEADERSHIP,
}

NAVIGATION = [
    {'label': 'Qui sommes-nous ?', 'url': URL_QUI, 'enfants': []},
    {
        'label': 'Nos programmes',
        'url': URL_PROGRAMMES,
        'enfants': [
            {'label': 'Les Go du Digital', 'url': URL_GO},
            {'label': 'UCIV Leadership', 'url': URL_LEADERSHIP},
            {'label': "De la vision à l'action", 'url': URL_VISION_ACTION, 'niveau': 2},
            {'label': 'Les RH ont la parole', 'url': URL_RH_PAROLE, 'niveau': 2},
            {'label': 'Experience Lab', 'url': URL_EXPERIENCE},
        ],
    },
    {
        'label': "S'engager",
        'url': URL_ENGAGEMENT,
        'enfants': [
            {'label': 'Devenir volontaire', 'url': URL_VOLONTAIRE},
            {'label': 'Rejoindre UCIV Leadership', 'url': URL_REJOINDRE_LEADERSHIP},
            {'label': 'Proposer mes compétences', 'url': URL_COMPETENCES},
        ],
    },
    {'label': 'Opportunités', 'url': URL_OPPORTUNITES, 'enfants': []},
    {'label': 'Notre impact', 'url': URL_IMPACT, 'enfants': []},
    {'label': 'Actualités', 'url': URL_ACTUALITES, 'enfants': []},
]

PIED_COLONNES = [
    {
        'titre': "S'engager",
        'liens': [
            {'label': "Je veux m'engager", 'url': URL_ENGAGEMENT},
            {'label': 'Devenir volontaire', 'url': URL_VOLONTAIRE},
            {'label': 'Proposer mes compétences', 'url': URL_COMPETENCES},
            {'label': 'Opportunités', 'url': URL_OPPORTUNITES},
        ],
    },
    {
        'titre': 'Nos programmes',
        'liens': [
            {'label': 'Les Go du Digital', 'url': URL_GO},
            {'label': 'UCIV Leadership', 'url': URL_LEADERSHIP},
            {'label': "De la vision à l'action", 'url': URL_VISION_ACTION},
            {'label': 'Les RH ont la parole', 'url': URL_RH_PAROLE},
            {'label': 'Experience Lab', 'url': URL_EXPERIENCE},
        ],
    },
    {
        'titre': 'Nous connaître',
        'liens': [
            {'label': 'Qui sommes-nous ?', 'url': URL_QUI},
            {'label': 'Équipe', 'url': reverse_lazy('app:equipe')},
            {'label': 'Notre impact', 'url': URL_IMPACT},
            {'label': 'Nos partenaires', 'url': URL_PARTENAIRES},
            {'label': 'Actualités', 'url': URL_ACTUALITES},
            {'label': 'Ressources', 'url': URL_RESSOURCES},
            {'label': 'Contact', 'url': URL_CONTACT},
        ],
    },
]

COORDONNEES = {
    'telephones': [
        {'label': '+225 07 87 56 17 66', 'href': 'tel:+2250787561766'},
        {'label': '07 07 722 078', 'href': 'tel:+2250707722078'},
    ],
    'email': 'organisationuciv@gmail.com',
    'adresse': '04 BP 2087 Abidjan',
}

RESEAUX = [
    {'label': 'Facebook', 'url': 'https://facebook.com/share/19XHRdY6AS'},
    {'label': 'TikTok · @uneciv', 'url': 'https://www.tiktok.com/@uneciv'},
    {'label': 'LinkedIn', 'url': 'https://www.linkedin.com/company/une-côte-d-ivoire-volontaire'},
]

URL_MENTIONS = reverse_lazy('app:mentions_legales')
URL_CONFIDENTIALITE = reverse_lazy('app:confidentialite')
URL_CONDITIONS = reverse_lazy('app:conditions')

MENTIONS = [
    {'label': 'Mentions légales', 'url': URL_MENTIONS},
    {'label': 'Politique de confidentialité', 'url': URL_CONFIDENTIALITE},
    {'label': "Conditions d'utilisation", 'url': URL_CONDITIONS},
]

# --- Page d'accueil --------------------------------------------------------

PARCOURS = ['Formation', 'Projet', 'Expérience', 'Impact']

PREUVES = [
    {
        'titre': 'Une mission de terrain',
        'texte': "Agir, sur place, au service d'une action concrète.",
    },
    {
        'titre': 'Un projet mené en équipe',
        'texte': 'Prendre des responsabilités et apprendre du collectif.',
    },
    {
        'titre': "Une formation suivie jusqu'au bout",
        'texte': 'Produire, tester, se tromper et recommencer.',
    },
]

DOMAINES = [
    {
        'icone': 'heart',
        'couleur': 'orange',
        'titre': 'Engagement citoyen',
        'texte': "Encourager les jeunes à participer activement à la vie de leur "
                 "communauté et à s'impliquer dans des causes d'intérêt collectif.",
    },
    {
        'icone': 'tool',
        'couleur': 'vert',
        'titre': 'Développement des compétences',
        'texte': "Créer des espaces d'apprentissage pratique où l'on produit, "
                 "teste, se trompe et recommence.",
    },
    {
        'icone': 'flag',
        'couleur': 'orange',
        'titre': 'Leadership',
        'texte': "Accompagner les jeunes dans la construction de leur capacité "
                 "d'initiative et de leur sens des responsabilités.",
    },
    {
        'icone': 'briefcase',
        'couleur': 'vert',
        'titre': 'Employabilité',
        'texte': "Aider chaque jeune à transformer ce qu'il a vécu à travers UCIV "
                 "en un véritable atout face à un employeur, un client ou un partenaire.",
    },
]

PROGRAMMES = [
    {
        'theme': 'orange',
        'titre': 'Les Go du Digital',
        'etiquette': '6 samedis · Jeunes femmes',
        'texte': "Six semaines autour du personal branding, de la sécurité numérique, "
                 "de la stratégie de contenu et des techniques de tournage.",
        'lien_label': 'Découvrir le programme',
        'url': URL_GO,
        'image': 'app/assets/img/go-du-digital-couverture.webp',
        'image_alt': "Deux participantes des Go du Digital travaillent sur leur téléphone.",
        'detouree': False,
    },
    {
        'theme': 'jaune',
        'titre': 'UCIV Leadership',
        'etiquette': 'Réseau sélectif · 30 à 50 membres',
        'texte': "Formations par des spécialistes, mentorat, conférences et un réseau "
                 "d'opportunités partagées entre membres.",
        'lien_label': 'Rejoindre UCIV Leadership',
        'url': URL_REJOINDRE_LEADERSHIP,
        'image': 'app/assets/img/leadership-couverture.webp',
        'image_alt': 'Quatre membres du réseau UCIV Leadership, bras croisés, en tenue professionnelle.',
        'detouree': True,
    },
    {
        'theme': 'creme',
        'titre': 'Experience Lab',
        'etiquette': 'Personal branding · Pitch',
        'texte': "Un espace pour mieux se connaître avant de chercher à se présenter. "
                 "« Know yourself before showing yourself. »",
        'lien_label': 'Découvrir Experience Lab',
        'url': URL_EXPERIENCE,
        'image': 'app/assets/img/experience-lab-couverture.webp',
        'image_alt': "Les participants d'Experience Lab réunis dans un jardin.",
        'detouree': False,
    },
]

# Chiffres transmis par UCIV (octobre 2026). Ils servent tant que la base ne contient aucun
# indicateur publié ; sinon ce sont ceux de l'administration (« Chiffres d'impact ») qui s'affichent.
INDICATEURS = [
    {'valeur': '+1 800', 'label': 'Jeunes mobilisés'},
    {'valeur': '40', 'label': 'Volontaires'},
    {'valeur': '5', 'label': 'Programmes réalisés'},
    {'valeur': '50', 'label': 'Participants formés'},
    {'valeur': '4', 'label': 'Partenaires'},
    {'valeur': '5', 'label': 'Projets réalisés'},
]

FACONS_DE_S_ENGAGER = [
    {
        'couleur': 'orange',
        'titre': 'Devenir volontaire',
        'texte': "Participe aux activités et aux projets d'UCIV, sur le terrain.",
        'url': URL_VOLONTAIRE,
    },
    {
        'couleur': 'jaune',
        'titre': 'Rejoindre UCIV Leadership',
        'texte': 'Intègre un réseau sélectif de jeunes leaders et futurs leaders.',
        'url': URL_REJOINDRE_LEADERSHIP,
    },
    {
        'couleur': 'vert',
        'titre': 'Proposer mes compétences',
        'texte': 'Communication, graphisme, audiovisuel, formation, numérique…',
        'url': URL_COMPETENCES,
    },
]

# Articles provisoires : titres rédigés à partir du cahier de contenu,
# à remplacer par les vrais articles (futur modèle `Article`).
ARTICLE_A_LA_UNE = {
    'categorie': 'Nos partenariats',
    'theme': 'orange',
    'meta': 'Insertion professionnelle',
    'titre': "UCIV et PAIPRO-JEUNES s'associent pour l'insertion des jeunes",
    'chapo': "À la fin des Go du Digital, les participantes sans emploi qui le "
             "souhaitent bénéficient d'un suivi vers l'insertion professionnelle.",
    'image': 'app/assets/img/partenariat-paipro.webp',
    'image_alt': "Poignée de main lors de la signature entre UCIV et PAIPRO-JEUNES.",
    'position': 'center 22%',
    'url': '#',
}

AUTRES_ARTICLES = [
    {
        'categorie': 'Leadership',
        'theme': 'jaune',
        'meta': '24 octobre 2026',
        'titre': 'UCIV Leadership : la conférence de lancement au format TEDx',
        'image': 'app/assets/img/affiche-leadership-jaune.webp',
        'image_alt': "Affiche d'UCIV Leadership : une jeune femme lève les poings.",
        'position': 'center 40%',
        'detouree': False,
        'url': '#',
    },
    {
        'categorie': 'Nos activités',
        'theme': 'vert',
        'meta': 'Rencontre',
        'titre': 'Des rencontres pour construire de nouvelles collaborations',
        'image': 'app/assets/img/rencontre-galerie.webp',
        'image_alt': 'Deux hommes posent devant un tableau dans une galerie.',
        'position': 'center 28%',
        'detouree': False,
        'url': '#',
    },
    {
        'categorie': 'Nos programmes',
        'theme': 'orange',
        'meta': 'Inscriptions',
        'titre': 'Les Go du Digital : la prochaine édition se prépare',
        'image': 'app/assets/img/groupe-nb.webp',
        'image_alt': 'Quatre jeunes souriants, en tenue professionnelle.',
        'position': 'center top',
        'detouree': True,
        'url': '#',
    },
]

# Photos de partenariat (UCIV n'a pas encore transmis les logos) : `position` garde les visages dans le cadre.
PARTENAIRES = [
    {'nom': 'BonixUp', 'apport': 'Formation', 'photo': 'app/assets/img/partenaire-bonixup.webp',
     'photo_alt': "Signature du partenariat entre UCIV et BonixUp.", 'position': 'center 30%'},
    {'nom': 'PAIPRO-JEUNES', 'apport': 'Insertion professionnelle', 'photo': 'app/assets/img/partenariat-paipro.webp',
     'photo_alt': "Poignée de main lors de la signature entre UCIV et PAIPRO-JEUNES.", 'position': 'center 18%'},
    {'nom': 'ONG Light for All CI', 'apport': 'Logistique de terrain',
     'photo': 'app/assets/img/partenaire-light-for-all.webp',
     'photo_alt': "Rencontre entre UCIV et l'ONG Light for All CI.", 'position': 'center 32%'},
]


# --- Page UCIV Leadership ---------------------------------------------------

LEADERSHIP = {
    'url_rejoindre': URL_REJOINDRE_LEADERSHIP,
    'chapo': "UCIV Leadership est le réseau des leaders et futurs leaders d'Une Côte "
             "d'Ivoire Volontaire : un cadre où des jeunes triés sur le volet se "
             "forment, se connectent et passent à l'action ensemble.",
    'reperes': [
        {'label': 'Cohorte pionnière', 'valeur': '30 à 50 membres'},
        {'label': 'Sélection', 'valeur': 'Pitch vidéo, puis entretien collectif'},
        {'label': 'Lancement', 'valeur': '24 octobre 2026 · American Corner'},
    ],
    'vision': "Faire émerger une génération de jeunes capables de prendre des "
              "initiatives, d'assumer des responsabilités",
    'vision_suite': "et de contribuer à la transformation de leur communauté et de "
                    "leur pays.",
    'mission_intro': "Créer un environnement où les jeunes développent leur "
                     "leadership à travers :",
    'mission': [
        'la formation par des spécialistes de plusieurs domaines',
        'le mentorat, notamment en format « shadowing »',
        "les échanges et le partage d'expériences",
        'les projets à fort impact portés dans les universités',
        "l'engagement citoyen",
        "l'action collective",
    ],
    'reseau_intro': "Le réseau est mixte, sélectif et exigeant. Un système de points "
                    "d'engagement suit la contribution de chaque membre et conditionne "
                    "son maintien.",
    'etapes': [
        {'titre': 'Pitch vidéo',
         'texte': "Les candidats sont d'abord recrutés sur pitch vidéo."},
        {'titre': 'Entretien collectif',
         'texte': 'Deuxième étape de la sélection, en groupe.'},
        {'titre': 'Membre Aspirant',
         'texte': "Les nouveaux arrivants passent d'abord par une période d'essai."},
        {'titre': 'Membre du réseau',
         'texte': "Les points d'engagement conditionnent le maintien dans le réseau."},
    ],
    'pourquoi_titre': "Le leadership ne commence pas nécessairement avec un titre.",
    'pourquoi_suite': "Il commence avec la capacité à prendre des initiatives, servir, "
                      "proposer des solutions et agir.",
    'pourquoi_texte': "Rejoindre UCIV Leadership, c'est intégrer un réseau sélectif où "
                      "chaque membre apporte sa contribution, et où les bonnes "
                      "opportunités circulent en priorité entre membres.",
    'avantages': ['Emploi', 'Financement', 'Formations'],
    'principes': [
        {'titre': 'Leadership',
         'texte': 'Développer sa capacité à influencer positivement et à prendre des '
                  'responsabilités.'},
        {'titre': 'Responsabilité',
         'texte': 'Assumer son rôle et respecter ses engagements envers le groupe.'},
        {'titre': 'Volontariat',
         'texte': "Mettre ses compétences et son énergie au service d'une cause."},
        {'titre': 'Innovation',
         'texte': 'Oser proposer de nouvelles solutions, y compris à travers des '
                  'hackathons sociaux inter-universités.'},
        {'titre': 'Impact social',
         'texte': 'Transformer les idées en actions utiles et mesurables.'},
    ],
    'image': 'app/assets/img/leadership-couverture.webp',
    'image_alt': 'Quatre membres du réseau UCIV Leadership, bras croisés, en tenue professionnelle.',
    'programmes_intro': "Au sein du réseau, UCIV Leadership organise des programmes pour clarifier son "
                        "ambition et se rapprocher du monde professionnel.",
    'programmes': [
        {'nom': "De la vision à l'action", 'etiquette': 'Ambition · Leadership',
         'accroche': 'Transformer ses ambitions en actions concrètes.',
         'texte': "Un programme pour clarifier sa vision, développer un état d'esprit orienté vers l'action "
                  "et construire son plan d'action.",
         'image': 'app/assets/img/vision-action-groupe.webp',
         'image_alt': "Les participants du programme « De la vision à l'action » en photo de groupe.",
         'url': URL_VISION_ACTION},
        {'nom': 'Les RH ont la parole', 'etiquette': 'Employabilité · Recrutement',
         'accroche': 'Comprendre les attentes des recruteurs pour mieux préparer son avenir professionnel.',
         'texte': "Des panels et des échanges directs avec des spécialistes des ressources humaines : "
                  "recrutement, CV, entretiens.",
         'image': 'app/assets/img/rh-parole-groupe.webp',
         'image_alt': "Les participants de « Les RH ont la parole » réunis dans un jardin.",
         'url': URL_RH_PAROLE},
    ],
    'temoignages': {
        'titre': 'Ils en parlent', 'suite': 'le mieux.',
        'intro': 'Paroles de membres du réseau UCIV Leadership.',
        'liste': [],
    },
    'theme': "« S'engager aujourd'hui",
    'theme_suite': 'pour transformer demain. »',
    'lancement_infos': ['24 octobre 2026', 'American Corner', 'Heure à confirmer'],
}

# --- Page Qui sommes-nous ? -------------------------------------------------

QUI_SOMMES_NOUS = {
    'hero_titre': "Une jeunesse qui ne se contente pas d'attendre.",
    'hero_suite': 'Une jeunesse qui agit.',
    'hero_chapo': "UCIV est une initiative citoyenne qui mobilise la jeunesse autour "
                  "du volontariat, du bénévolat et de l'engagement citoyen.",
    'ambition': "Faire du volontariat un véritable espace de développement personnel, "
                "professionnel et citoyen :",
    'ambition_suite': "un lieu où l'on apprend en agissant, pas seulement en écoutant.",
    'ambition_texte': "À travers ses programmes, ses projets et ses activités, UCIV "
                      "crée des espaces permettant aux jeunes de s'engager, "
                      "d'apprendre, de développer leurs compétences, de prendre des "
                      "responsabilités et de contribuer à des actions concrètes.",
    'ambition_mots': ['Volontariat', 'Bénévolat', 'Engagement citoyen'],
    'vision': 'Former une génération de jeunes engagés, responsables',
    'vision_suite': 'et acteurs du changement.',
    'vision_texte': "Nous croyons qu'une jeunesse qui développe ses compétences, prend "
                    "des initiatives et s'engage dans sa communauté est mieux préparée "
                    "à contribuer au développement de la Côte d'Ivoire.",
    'mission': "Mobiliser les jeunes autour du volontariat et de l'engagement pour "
               "développer leurs compétences et contribuer à leur employabilité.",
    'mission_liste': [
        'le volontariat et le bénévolat',
        'les formations',
        'les programmes de développement des compétences',
        'le leadership',
        'les projets citoyens',
        'la mobilisation communautaire',
        "les initiatives en faveur de l'employabilité",
    ],
    'valeurs_intro': "Six repères qui guident nos programmes, nos projets et la "
                     "manière dont nous travaillons ensemble.",
    'valeurs': [
        {'titre': 'Engagement',
         'texte': "Nous encourageons chacun à passer de l'intention à l'action."},
        {'titre': 'Responsabilité',
         'texte': "S'engager, c'est accepter de prendre sa part dans les actions "
                  "auxquelles on participe, jusqu'au bout."},
        {'titre': 'Solidarité',
         'texte': "Nous croyons à la force du collectif et à la capacité des "
                  "individus à agir ensemble."},
        {'titre': 'Apprentissage',
         'texte': "Chaque expérience, réussie ou ratée, est une occasion de "
                  "développer une nouvelle compétence."},
        {'titre': 'Innovation',
         'texte': "Nous encourageons les idées nouvelles et les initiatives "
                  "capables de répondre aux défis réels de notre société."},
        {'titre': 'Impact',
         'texte': "Notre engagement doit se traduire par des actions utiles et des "
                  "changements concrets."},
    ],
    'citation': 'Chaque engagement peut devenir une expérience.',
    'citation_suite': 'Chaque expérience peut devenir une compétence.',
}

# --- Page Nos programmes ----------------------------------------------------

NOS_PROGRAMMES = {
    'hero_titre': 'Des programmes pour apprendre,',
    'hero_suite': "s'engager et agir.",
    'hero_chapo': "UCIV développe des programmes conçus pour répondre à des besoins "
                  "précis des jeunes ivoiriens : compétences numériques, leadership, "
                  "personal branding, employabilité.",
    'methode_intro': "De la formation courte et pratique jusqu'à la mise en situation "
                     "réelle, avec un accompagnement qui ne s'arrête pas à la dernière "
                     "séance.",
    'methode': [
        {'couleur': 'orange', 'titre': 'Une formation courte et pratique'},
        {'couleur': 'jaune', 'titre': 'Une mise en situation réelle'},
        {'couleur': 'vert', 'titre': 'Un accompagnement après la dernière séance'},
    ],
    'programmes': [
        {
            'theme': 'orange',
            'bouton': 'orange',
            'etiquette': '6 samedis · Jeunes femmes',
            'titre': 'Les Go du Digital',
            'accroche': "Le digital comme outil d'autonomie, d'expression et "
                        "d'opportunité.",
            'texte': "Un programme pratique à 90 %, organisé autour de quatre volets : "
                     "Personal Branding, Sécurité Numérique, Stratégie de Contenu et "
                     "Techniques de Tournage. Chaque édition se conclut par la "
                     "compétition « La Reine du Digital ».",
            'lien_label': 'Découvrir le programme',
            'url': URL_GO,
            'image': 'app/assets/img/go-du-digital-couverture.webp',
            'image_alt': 'Deux participantes des Go du Digital travaillent sur leur téléphone.',
            'detouree': False,
        },
        {
            'theme': 'jaune',
            'bouton': 'encre',
            'etiquette': 'Réseau sélectif · 30 à 50 membres',
            'titre': 'UCIV Leadership',
            'accroche': 'Un réseau. Un engagement. Un impact.',
            'texte': "Le réseau des jeunes leaders et futurs leaders d'UCIV : "
                     "formations par des spécialistes, mentorat, conférences avec des "
                     "personnalités qui ont réussi, et un réseau d'opportunités "
                     "partagées entre membres.",
            'lien_label': 'Rejoindre UCIV Leadership',
            'url': URL_REJOINDRE_LEADERSHIP,
            'image': 'app/assets/img/groupe-nb.webp',
            'image_alt': 'Quatre jeunes leaders souriants, en tenue professionnelle.',
            'detouree': True,
            'sous_programmes': [
                {'label': "De la vision à l'action", 'url': URL_VISION_ACTION},
                {'label': 'Les RH ont la parole', 'url': URL_RH_PAROLE},
            ],
        },
        {
            'theme': 'vert',
            'bouton': 'vert',
            'etiquette': 'Personal branding · Pitch',
            'titre': 'Experience Lab',
            'accroche': '« Know yourself before showing yourself. »',
            'texte': "Un espace consacré au personal branding et au pitch "
                     "professionnel, pour mieux se connaître avant de chercher à se "
                     "présenter.",
            'lien_label': 'Découvrir Experience Lab',
            'url': URL_EXPERIENCE,
            'image': 'app/assets/img/experience-lab-couverture.webp',
            'image_alt': "Les participants d'Experience Lab réunis dans un jardin.",
            'detouree': False,
        },
    ],
}

# --- Page Les Go du Digital -------------------------------------------------

# Témoignages des pages programme : une entrée par personne, affichée en carte
# {'nom': 'Prénom Nom', 'programme': 'Participante — Les Go du Digital', 'citation': '…',
#  'photo': 'app/assets/img/…webp' (facultatif : sans photo, une silhouette s'affiche)}.
# La section n'apparaît que si au moins un témoignage est renseigné.

GO_DU_DIGITAL = {
    'image': 'app/assets/img/go-du-digital-couverture.webp',
    'image_alt': 'Deux participantes des Go du Digital travaillent sur leur téléphone.',
    'url_inscription': URL_INSCRIPTION_PROGRAMME,
    'hero_surtitre': 'Programme · Jeunes femmes · 6 samedis',
    'hero_chapo': "Le digital comme outil d'autonomie, d'expression et d'opportunité.",
    'hero_note': 'elles créent, elles osent !',
    'reperes': [
        {'label': 'Durée', 'valeur': '6 samedis'},
        {'label': 'Approche', 'valeur': '90 % pratique'},
        {'label': 'Lieu', 'valeur': 'Variable selon les éditions'},
        {'label': 'Prochaine édition', 'valeur': 'Date à confirmer'},
    ],
    'volets_intro': "Permettre aux participantes de développer des compétences "
                    "concrètes dans l'utilisation du numérique et des réseaux "
                    "sociaux, tout en les sensibilisant à un usage responsable et "
                    "professionnel de ces outils.",
    'volets': [
        {'couleur': 'orange', 'icone': 'user', 'titre': 'Personal Branding'},
        {'couleur': 'vert', 'icone': 'shield', 'titre': 'Sécurité Numérique'},
        {'couleur': 'jaune', 'icone': 'pen-line', 'titre': 'Stratégie de Contenu'},
        {'couleur': 'profond', 'icone': 'video', 'titre': 'Techniques de Tournage'},
    ],
    'apprentissages': [
        {'titre': 'Développer leur personal branding',
         'texte': "Comprendre leur identité, leurs forces, et construire une "
                  "présence cohérente sur le digital."},
        {'titre': 'Créer du contenu',
         'texte': "Découvrir les principes de création de contenus adaptés à chaque "
                  "plateforme, du cadrage au montage."},
        {'titre': 'Vendre en ligne',
         'texte': "Comprendre comment utiliser les outils numériques et les réseaux "
                  "sociaux pour présenter et commercialiser une activité ou une "
                  "offre."},
        {'titre': "Se protéger dans l'environnement numérique",
         'texte': "Adopter de bonnes pratiques de sécurité et de protection de ses "
                  "informations personnelles."},
        {'titre': 'Utiliser les réseaux sociaux de manière responsable',
         'texte': "Comprendre les opportunités et les responsabilités qui viennent "
                  "avec une présence en ligne."},
    ],
    'pedagogie_texte': "Le programme privilégie les exercices, les mises en "
                       "situation, les échanges entre participantes et la "
                       "production de contenus réels.",
    'reine_texte': "Chaque édition se conclut par une compétition qui valorise les "
                   "meilleures productions des participantes devant un jury et le "
                   "public.",
    'public': [
        'Jeunes femmes',
        'Étudiantes',
        'Jeunes professionnelles',
        'Femmes souhaitant développer une activité grâce au digital',
        'Personnes souhaitant améliorer leurs compétences numériques',
    ],
    'suivi_titre': "Un suivi vers l'insertion professionnelle",
    'suivi_texte': "À la fin du programme, les participantes sans emploi qui "
                   "souhaitent un accompagnement bénéficient d'un suivi vers "
                   "l'insertion professionnelle, en partenariat avec PAIPRO-JEUNES.",
    'partenaires': ['BonixUp', 'PAIPRO-JEUNES', 'ONG Light for All CI'],
    'inscriptions': [
        {'label': 'Ouverture des inscriptions', 'valeur': 'À confirmer'},
        {'label': 'Tarif', 'valeur': 'À confirmer'},
        {'label': 'Modalités', 'valeur': 'À confirmer'},
    ],
    'temoignages': {
        'titre': 'Elles en parlent', 'suite': 'le mieux.',
        'intro': 'Paroles de participantes, à la fin de leurs six samedis de formation.',
        'laureate': {
            'nom': 'Leticia BOSSON', 'programme': 'Lauréate — Les Go du Digital',
            'badge': 'Lauréate · Reine du Digital',
            'photo': 'app/assets/img/leticia-bosson.webp',
            'photo_alt': 'Leticia BOSSON, couronnée Reine du Digital.',
            'citation': "Ces six semaines de formation m'ont beaucoup appris. Nous avons été sérieusement "
                        "formées à la création de contenu, avec beaucoup de pratique et d'exercices, ce qui "
                        "m'a permis de monter très vite en compétence. Je sors de cette formation très "
                        "heureuse, d'autant plus que j'ai été couronnée Reine. Je recommande à 100 % le "
                        "programme Les Go du Digital.",
        },
        'liste': [],
    },
    'galerie': {
        'titre': 'Six samedis', 'suite': 'de pratique.',
        'intro': "Interventions, ateliers de création de contenu et remise des attestations de la dernière "
                 "édition.",
        # `taille` : place de la photo dans la mosaïque (maquette : 3 photos en haut, 4 en bas).
        'photos': [
            {'image': 'app/assets/img/gdd-18.webp', 'alt': 'Un intervenant présente un atelier aux participantes.', 'taille': 'haut-1'},
            {'image': 'app/assets/img/gdd-img1355.webp', 'alt': 'Les participantes montrent leurs attestations de fin de formation.', 'taille': 'haut-2'},
            {'image': 'app/assets/img/gdd-dsc00150.webp', 'alt': 'Une participante filme avec son téléphone.', 'taille': 'haut-3'},
            {'image': 'app/assets/img/gdd-32.webp', 'alt': 'Des participantes concentrées sur leur téléphone.', 'taille': 'bas'},
            {'image': 'app/assets/img/gdd-dsc00060.webp', 'alt': 'Une participante réfléchit pendant un atelier.', 'taille': 'bas'},
            {'image': 'app/assets/img/gdd-42.webp', 'alt': 'La salle de formation pendant une intervention.', 'taille': 'bas'},
            {'image': 'app/assets/img/gdd-img8842.webp', 'alt': "L'équipe et les participantes en tee-shirt UCIV.", 'taille': 'bas'},
        ],
    },
}

# --- Page Experience Lab ----------------------------------------------------

EXPERIENCE_LAB = {
    'image': 'app/assets/img/experience-lab-couverture.webp',
    'image_alt': "Les participants d'Experience Lab réunis dans un jardin.",
    'url_inscription': URL_INSCRIPTION_PROGRAMME,
    'hero_surtitre': 'Programme · Personal branding et pitch',
    'hero_chapo': "Apprendre à mieux se connaître, mieux se présenter et mieux "
                  "valoriser son expérience.",
    'hero_note': "connais-toi d'abord !",
    'approche_titre': '« Know yourself',
    'approche_suite': 'before showing yourself. »',
    'approche_intro': "Avant de chercher à être visible, il faut comprendre…",
    'questions': [
        {'couleur': 'orange', 'texte': "qui l'on est"},
        {'couleur': 'vert', 'texte': "ce que l'on sait faire"},
        {'couleur': 'orange', 'texte': "ce que l'on peut apporter"},
        {'couleur': 'profond', 'texte': "comment on souhaite être perçu"},
    ],
    'objectifs_intro': "Experience Lab est un espace d'apprentissage et de partage "
                       "destiné à accompagner les jeunes dans leur développement "
                       "personnel et professionnel.",
    'objectifs': [
        'Mieux comprendre leur identité et leurs forces',
        'Définir leur positionnement',
        'Apprendre à valoriser leurs compétences',
        'Construire une présentation personnelle cohérente',
        'Améliorer leur capacité à présenter leur parcours',
        'Développer leur confiance dans les situations professionnelles',
    ],
    'inscriptions': [
        {'label': 'Format', 'valeur': 'À confirmer'},
        {'label': 'Dates', 'valeur': 'À confirmer'},
        {'label': 'Modalités', 'valeur': 'À confirmer'},
    ],
    'temoignages': {
        'titre': 'Ils en parlent', 'suite': 'le mieux.',
        'intro': "Ce que les participants retiennent de leur passage à l'Experience Lab.",
        'liste': [],
    },
}

# --- Page Équipe ------------------------------------------------------------

EQUIPE = {
    'hero_titre': 'Les femmes et les hommes',
    'hero_suite': 'derrière UCIV.',
    'hero_chapo': "UCIV est porté par une équipe de personnes engagées qui mettent "
                  "leurs compétences, leur temps et leur énergie au service de la "
                  "mission de l'organisation.",
    'president_photo': 'app/assets/img/equipe-marshall-kouame.webp',
    'president_role': "Entrepreneur du numérique, spécialiste en communication visuelle et audiovisuelle, "
                      "fondateur-président d'Une Côte d'Ivoire Volontaire.",
    'president_bio': [
        "Titulaire d'un diplôme en Art et Image Numérique, Marshall Kouamé met ses compétences créatives et "
        "son expérience en communication au service de projets à impact social. Convaincu que l'engagement "
        "citoyen est un puissant levier de développement, il s'investit dans la mobilisation, la formation "
        "et l'accompagnement des jeunes à travers des initiatives qui favorisent le volontariat, "
        "l'employabilité et le leadership.",
        "À travers UCIV, il porte une vision : faire du volontariat une véritable école d'expérience, de "
        "compétences et de leadership pour la jeunesse ivoirienne. Son ambition est de contribuer à "
        "l'émergence d'une génération de jeunes responsables, compétents et engagés, capables de prendre "
        "des initiatives et de participer activement au développement de la Côte d'Ivoire.",
    ],
    'president_citation': "« Chaque jeune a un potentiel à révéler et un rôle à jouer dans la "
                          "transformation de son pays. »",
    # Portraits transmis par UCIV (octobre 2026), dossier « L'ÉQUIPE » : (nom, rôle, fichier).
    # La couleur du liseré sous chaque photo est attribuée à la suite (voir plus bas).
    'groupes': [
        {
            'cle': 'bureau', 'surtitre': 'Bureau exécutif', 'titre': "L'équipe",
            'suite': 'qui fait avancer UCIV.',
            'membres': [
                ('Aïssata Ouattara', 'Secrétaire Générale', 'aissata-ouattara'),
                ('Ago Maria Konan', 'Secrétaire Générale adjointe', 'ago-maria-konan'),
                ('Dr Angèle Zang', 'Trésorière Générale', 'angele-zang'),
                ('Roxane Atchia', 'Commissaire aux comptes', 'roxane-atchia'),
                ('Djamira Kamagaté', 'Commissaire aux comptes adjointe', 'djamira-kamagate'),
            ],
        },
        {
            'cle': 'responsables', 'surtitre': 'Les responsables', 'titre': 'Celles et ceux',
            'suite': 'qui portent les projets.',
            'membres': [
                ('Christelle Boidi', 'Responsable Générale des Ressources Humaines', 'christelle-boidi'),
                ('Martine Boa', 'Responsable Générale des projets', 'martine-boa'),
                ('Roxane Tchimou', 'Responsable Générale des Ambassadeurs', 'roxane-tchimou'),
                ('Abissiri Coulibaly', 'Responsable de la logistique', 'abissiri-coulibaly'),
                ('Danielle Bohoussou', 'Responsable Environnement & Écocitoyenneté', 'danielle-bohoussou'),
                ('Goho Auxane', 'Responsable Communication', 'auxane-goho'),
                ('Martial Coulibaly', 'Responsable Formations « Objectif Métiers »', 'martial-coulibaly'),
                ('Nelly Atchia', 'Responsable Formations & Ateliers', 'nelly-atchia'),
                ('Naomi Lahore Yao', "Responsable de l'Expérience Talent & Engagement", 'naomi-lahore-yao'),
                ('Mieimmo Kouassi', 'Chargée de Marketing', 'mieimmo-kouassi'),
            ],
        },
        {
            'cle': 'ambassadrices', 'surtitre': 'Nos ambassadrices', 'titre': "La voix d'UCIV",
            'suite': 'sur le terrain.',
            'intro': "Elles portent les valeurs d'UCIV et relaient ses programmes auprès des jeunes.",
            'membres': [
                ('Désirée Okpekon', 'Ambassadrice', 'desiree-okpekon'),
                ('Samira Kouassi', 'Ambassadrice', 'samira-kouassi'),
            ],
        },
    ],
}

_COULEURS_EQUIPE = ['orange', 'vert', 'jaune', 'profond', 'orange-fonce']
for _groupe in EQUIPE['groupes']:
    _groupe['membres'] = [
        {'nom': nom, 'role': role, 'photo': f'app/assets/img/equipe-{fichier}.webp',
         'couleur': _COULEURS_EQUIPE[n % len(_COULEURS_EQUIPE)]}
        for n, (nom, role, fichier) in enumerate(_groupe['membres'])
    ]

# --- Programmes d'UCIV Leadership (une page par programme, même gabarit) ------------
# Textes transmis par UCIV (octobre 2026). Clé = slug de l'URL /programmes/uciv-leadership/<slug>/.

PROGRAMMES_LEADERSHIP = {
    'de-la-vision-a-l-action': {
        'nom': "De la vision à l'action", 'fond': 'profond', 'formes_cle': 'vision_action',
        'titre': 'De la vision', 'suite': "à l'action.",
        'chapo': 'Transformer ses ambitions en actions concrètes.',
        'note': "passe à l'action !",
        'image': 'app/assets/img/vision-action-couverture.webp',
        'image_alt': "Un intervenant sourit pendant un échange du programme « De la vision à l'action ».",
        'a_propos_titre': 'Avoir une vision', 'a_propos_suite': 'est un premier pas.',
        'a_propos': [
            "« De la vision à l'action » est un programme porté par Une Côte d'Ivoire Volontaire (UCIV). Il vise "
            "à encourager les jeunes à clarifier leurs ambitions, à développer leur potentiel et à passer "
            "concrètement à l'action pour construire leur avenir.",
            "Avoir une vision est un premier pas, mais la concrétiser demande de la préparation, du courage, de "
            "la discipline et de la persévérance. Ce programme invite les jeunes à dépasser leurs hésitations, "
            "à mieux comprendre leur potentiel et à transformer leurs aspirations en initiatives concrètes.",
            "À travers des échanges, des réflexions et des expériences inspirantes, les participants sont "
            "encouragés à adopter une posture proactive face aux défis de leur parcours personnel, "
            "professionnel et citoyen.",
        ],
        'objectifs_intro': "Cinq objectifs pour passer de l'intention à l'initiative.",
        'objectifs': [
            ('Clarifier sa vision', "Aider les jeunes à mieux définir leurs aspirations, leurs objectifs et la "
                                    "direction qu'ils souhaitent donner à leur vie."),
            ("Développer un état d'esprit orienté vers l'action",
             "Encourager l'initiative, la responsabilité personnelle et la confiance en ses capacités."),
            ('Surmonter les obstacles', "Apprendre à faire face à la peur, aux doutes et aux difficultés qui "
                                        "freinent le passage à l'action."),
            ("Construire un plan d'action", "Traduire ses ambitions en objectifs concrets, réalistes et "
                                            "progressifs."),
            ('Encourager le leadership', "Former une jeunesse capable de prendre des initiatives et de "
                                         "contribuer positivement au développement de sa communauté."),
        ],
        'approche_titre': 'Échanger, réfléchir,', 'approche_suite': 'agir.',
        'approche': [
            "Le programme privilégie une approche participative, fondée sur le partage d'expériences, la "
            "réflexion personnelle, les échanges et l'identification de pistes d'action concrètes.",
            "L'objectif n'est pas seulement d'inspirer les participants, mais de les amener à repartir avec une "
            "vision plus claire de leurs ambitions et une meilleure compréhension des étapes à franchir pour les "
            "réaliser.",
        ],
        'public_titre': 'Pour les jeunes', 'public_suite': 'qui veulent agir.',
        'public': "« De la vision à l'action » s'adresse principalement aux jeunes désireux de mieux orienter "
                  "leur avenir, de développer leur leadership et de concrétiser leurs projets personnels, "
                  "professionnels ou citoyens.",
        'conviction': "Chez Une Côte d'Ivoire Volontaire, nous croyons que la jeunesse ne doit pas seulement "
                      "rêver d'un avenir meilleur : elle doit pouvoir prendre part à sa construction.",
        'conviction_titre': "Une vision donne une direction. L'action ouvre le chemin.",
        'conviction_suite': "La persévérance permet d'avancer.",
        'conviction_fin': "Avec « De la vision à l'action », UCIV encourage chaque jeune à devenir acteur de son "
                          "avenir et contributeur du changement dans sa communauté.",
        'inscriptions_titre': 'Transforme ton ambition', 'inscriptions_suite': "en plan d'action.",
    },
    'les-rh-ont-la-parole': {
        'nom': 'Les RH ont la parole', 'fond': 'orange', 'formes_cle': 'rh_parole',
        'titre': 'Les RH ont', 'suite': 'la parole.',
        'chapo': 'Comprendre les attentes des recruteurs pour mieux préparer son avenir professionnel.',
        'note': 'prépare ton avenir !',
        'image': 'app/assets/img/rh-parole-groupe.webp',
        'image_alt': "Les participants de « Les RH ont la parole » réunis dans un jardin.",
        'a_propos_titre': 'Se rapprocher', 'a_propos_suite': 'du monde professionnel.',
        'a_propos': [
            "« Les RH ont la parole » est une initiative portée par Une Côte d'Ivoire Volontaire (UCIV). Elle "
            "vise à rapprocher les jeunes du monde professionnel en leur donnant l'occasion d'échanger "
            "directement avec des spécialistes des ressources humaines.",
            "L'accès au premier emploi représente un défi pour de nombreux jeunes diplômés. Il devient donc "
            "essentiel de mieux comprendre les attentes des entreprises, les critères de recrutement et les "
            "compétences recherchées sur le marché du travail.",
            "À travers des panels, des échanges interactifs et des témoignages de professionnels, cette "
            "initiative permet aux participants de mieux comprendre les réalités du recrutement et de "
            "bénéficier de conseils pratiques pour préparer leur insertion professionnelle.",
        ],
        'objectifs_intro': 'Cinq objectifs pour mieux comprendre le recrutement et préparer son insertion.',
        'objectifs': [
            ('Comprendre le recrutement', "Permettre aux jeunes de mieux connaître les attentes des recruteurs "
                                          "et les étapes du processus de sélection."),
            ('Renforcer son employabilité', "Aider les participants à identifier les compétences techniques et "
                                            "comportementales recherchées par les employeurs."),
            ('Mieux valoriser son profil', "Donner des conseils pratiques pour améliorer son CV, préparer ses "
                                           "entretiens et présenter ses expériences."),
            ('Créer un pont entre les jeunes et les entreprises',
             'Favoriser le dialogue entre les professionnels RH et la nouvelle génération de talents.'),
            ('Encourager le développement professionnel',
             "Sensibiliser les jeunes à l'importance de la formation continue, du volontariat et de "
             "l'acquisition d'expériences concrètes."),
        ],
        'approche_titre': 'Rencontrer, questionner,', 'approche_suite': 'comprendre.',
        'approche': [
            "Le programme repose sur des rencontres et des échanges directs avec des professionnels des "
            "ressources humaines. Il privilégie le partage d'expériences, les questions-réponses et les conseils "
            "pratiques pour mieux préparer l'entrée dans le monde du travail.",
            "Au-delà de la transmission d'informations, « Les RH ont la parole » favorise une meilleure "
            "compréhension mutuelle entre les attentes des jeunes candidats et les exigences du marché de "
            "l'emploi.",
        ],
        'public_titre': 'Pour les étudiants', 'public_suite': 'et jeunes diplômés.',
        'public': "Cette initiative s'adresse principalement aux étudiants, aux jeunes diplômés, aux personnes "
                  "en recherche d'emploi et à tous les jeunes désireux de mieux préparer leur parcours "
                  "professionnel.",
        'conviction': "Chez Une Côte d'Ivoire Volontaire, nous sommes convaincus que l'employabilité des jeunes "
                      "se construit grâce à l'acquisition de compétences, à l'expérience, à l'engagement et à "
                      "une meilleure connaissance du monde professionnel.",
        'conviction_titre': 'Donner la parole aux RH,',
        'conviction_suite': "c'est donner aux jeunes des clés.",
        'conviction_fin': 'Des clés pour mieux comprendre le recrutement et construire leur avenir professionnel.',
        'inscriptions_titre': 'Prépare ton entrée', 'inscriptions_suite': 'dans le monde du travail.',
    },
}
for _slug, _programme in PROGRAMMES_LEADERSHIP.items():
    _programme.update(
        slug=_slug,
        url_inscription=URL_INSCRIPTION_PROGRAMME,
        inscriptions=[
            {'label': 'Format', 'valeur': 'À confirmer'},
            {'label': 'Dates', 'valeur': 'À confirmer'},
            {'label': 'Modalités', 'valeur': 'À confirmer'},
        ],
        temoignages={'titre': 'Ils en parlent', 'suite': 'le mieux.',
                     'intro': f"Ce que les participants retiennent du programme « {_programme['nom']} ».",
                     'liste': []},
    )

# --- Page Je veux m'engager -------------------------------------------------

ENGAGEMENT = {
    'hero_titre': 'Ton engagement peut',
    'hero_suite': 'commencer ici.',
    'hero_chapo': "UCIV rassemble des jeunes qui souhaitent apprendre, contribuer et "
                  "agir. Tu peux nous rejoindre de différentes manières, selon ce que "
                  "tu as envie d'apporter et le temps que tu peux y consacrer.",
    'hero_note': 'il y a une place pour toi !',
    'facons': [
        {'couleur': 'blanc', 'bouton': 'vert', 'titre': 'Devenir volontaire',
         'texte': "Participe aux activités et aux projets d'UCIV et mets tes "
                  "compétences au service d'actions concrètes, sur le terrain.",
         'url': URL_VOLONTAIRE},
        {'couleur': 'jaune', 'bouton': 'encre', 'titre': 'Rejoindre UCIV Leadership',
         'texte': "Intègre un réseau sélectif de jeunes leaders et futurs leaders "
                  "qui souhaitent développer leurs capacités et agir ensemble.",
         'url': URL_REJOINDRE_LEADERSHIP},
        {'couleur': 'profond', 'bouton': 'blanc', 'titre': 'Proposer mes compétences',
         'texte': "Tu as une compétence ou une expertise à mettre au service d'UCIV ? "
                  "Nous pouvons avoir besoin de profils dans différents domaines :",
         'puces': ['Communication', 'Graphisme', 'Audiovisuel', 'Photographie',
                   'Formation', 'Événementiel', 'Ressources humaines',
                   'Gestion de projet', 'Numérique', 'Développement web'],
         'url': URL_COMPETENCES},
    ],
    'formulaire_texte': "Il existe une place pour ton engagement au sein d'UCIV. "
                        "L'équipe revient vers toi pour la suite.",
    'merci': "Merci ! Ta demande a bien été envoyée. L'équipe revient vers toi pour "
             "la suite.",
}

# --- Page Partenaires -------------------------------------------------------

PAGE_PARTENAIRES = {
    'hero_titre': "Ensemble, créons plus d'opportunités",
    'hero_suite': 'pour la jeunesse.',
    'hero_chapo': "Les défis liés à la jeunesse ne se résolvent pas par une seule "
                  "organisation agissant seule. UCIV développe des collaborations "
                  "avec toute organisation partageant la volonté de contribuer au "
                  "développement de la jeunesse ivoirienne.",
    'accompagnent_intro': "Des collaborations comme celles menées avec BonixUp, "
                          "PAIPRO-JEUNES et Light for All CI montrent ce qu'un "
                          "partenariat peut apporter aux jeunes.",
    'partenaires': [
        {'nom': 'BonixUp', 'apport': 'Accès à des formateurs',
         'couleur': 'orange', 'icone': 'graduation-cap', 'photo': PARTENAIRES[0]['photo'],
         'photo_alt': PARTENAIRES[0]['photo_alt'], 'position': PARTENAIRES[0]['position']},
        {'nom': 'PAIPRO-JEUNES', 'apport': "Accompagnement vers l'emploi",
         'couleur': 'vert', 'icone': 'briefcase', 'photo': PARTENAIRES[1]['photo'],
         'photo_alt': PARTENAIRES[1]['photo_alt'], 'position': PARTENAIRES[1]['position']},
        {'nom': 'ONG Light for All CI', 'apport': 'Logistique de terrain',
         'couleur': 'profond', 'icone': 'truck', 'photo': PARTENAIRES[2]['photo'],
         'photo_alt': PARTENAIRES[2]['photo_alt'], 'position': PARTENAIRES[2]['position']},
    ],
    'formes_intro': "Institutions, entreprises, associations, ONG, établissements de "
                    "formation : plusieurs manières de construire ensemble.",
    'formes': [
        'Partenariats institutionnels', 'Partenariats techniques',
        'Partenariats financiers', 'Sponsoring', 'Mécénat',
        'Collaborations sur des programmes', 'Formations',
        'Opportunités de stage', 'Opportunités professionnelles', 'Projets communs',
    ],
    'formulaire_texte': "Présentez-nous votre organisation et expliquez-nous comment "
                        "nous pourrions construire une collaboration utile aux jeunes "
                        "que nous accompagnons.",
    'merci': "Merci ! Votre proposition a bien été envoyée. L'équipe vous recontacte "
             "rapidement.",
}


# --- Page Contact -----------------------------------------------------------

CONTACT = {
    'hero_titre': 'Parlons-',
    'hero_suite': 'nous.',
    'hero_chapo': "Une question ? Une proposition de partenariat ? Une envie de "
                  "rejoindre UCIV ? Une idée de projet ? Notre équipe est disponible "
                  "pour échanger avec vous.",
    'hero_note': 'on vous répond !',
    'telephones': [
        {'label': '+225 07 87 56 17 66', 'href': 'tel:+2250787561766'},
        {'label': '+225 07 07 722 078', 'href': 'tel:+2250707722078'},
    ],
    'merci': "Merci ! Votre message a bien été envoyé. Nous vous répondons dès que "
             "possible.",
}

# --- Forme UCIV des bandeaux (heros) ----------------------------------------------------------------
# La forme du logo remplace les cercles décoratifs (maquette, octobre 2026). Valeurs relevées dans la maquette,
# en pixels, par rapport au coin haut gauche du hero : (x, y, largeur, hauteur, rotation, couleur).
# Rotation en degrés dans le sens inverse des aiguilles d'une montre, autour du coin haut gauche (comme Pencil).
# `desktop` : maquette de 1440 px ; `mobile` : maquette de 390 px (gabarit app/includes/_formes_uciv.html).

_F_CREME, _F_JAUNE, _F_VERT, _F_ORANGE = 'var(--creme)', 'var(--jaune)', 'var(--vert)', 'var(--orange)'
_F_BLANC = 'var(--blanc)'
_F_MOBILE = [(280, -110, 181, 240, 0, 'rgba(255, 255, 255, .15)')]
_F_HAUT_DROITE = (1184, -180, 331, 440, 0, _F_JAUNE)    # Experience Lab et programmes d'UCIV Leadership

FORMES_HEROS = {
    'home': {'desktop': [(1595.9, 355, 603, 901, 262, _F_CREME), (-90, 580, 226, 300, 0, _F_VERT)]},
    'qui_sommes_nous': {'desktop': [(1561.7, 202.3, 591, 784, 269.2, _F_CREME), (1234, -200, 331, 440, 0, _F_JAUNE)]},
    'nos_programmes': {'desktop': [(1486.5, 312.7, 286, 380, 293.7, _F_JAUNE),
                                   (889, -14.7, 420, 457, 44.7, 'rgba(255, 255, 255, .08)')]},
    'go_du_digital': {'desktop': [(1594.7, 289.4, 582, 792, -91.6, _F_CREME)]},
    'uciv_leadership': {'desktop': [(817, -216, 734, 894, 0, _F_BLANC), (-146, 470, 271, 360, 0, _F_VERT)],
                        'mobile': [(264, -56, 181, 240, 0, 'rgba(255, 255, 255, .15)')]},
    'experience_lab': {'desktop': [_F_HAUT_DROITE, (1493.3, 396, 460, 610, 272.7, _F_CREME)]},
    'vision_action': {'desktop': [_F_HAUT_DROITE, (1425.9, 182, 460, 610, 293.9, _F_CREME)]},
    'rh_parole': {'desktop': [_F_HAUT_DROITE, (1501.1, 260, 460, 610, 276.5, _F_CREME)]},
    'engagement': {'desktop': [(1042.1, -41, 484, 521, 11.8, _F_ORANGE)]},
    'partenaires': {'desktop': [(1347.4, -127, 751, 808, -40.7, _F_CREME), (-128, 470, 256, 340, 0, _F_VERT)]},
    'opportunites': {'desktop': [(1234, 110, 461, 461, -22.6, 'rgba(255, 255, 255, .08)')]},
    'actualites': {'desktop': [(1144, -140, 392, 520, 0, _F_JAUNE), (1301.9, 521.4, 429, 470, 223.8, _F_ORANGE)]},
    'article': {'desktop': [(-121, 300, 241, 320, 0, _F_JAUNE)]},
    'impact': {'desktop': [(1117, -120, 407, 540, 0, _F_CREME)]},
    'ressources': {'desktop': [(1134, -130, 392, 520, 0, _F_CREME)]},
    'equipe': {'desktop': [(1144, -140, 392, 520, 0, _F_JAUNE)]},
    'contact': {'desktop': [(1134, -130, 392, 520, 0, _F_CREME), (-170.4, 402.5, 256, 340, 16.2, _F_JAUNE)]},
    'legal': {'desktop': [(1122, -170, 377, 500, 0, 'rgba(255, 255, 255, .1)')]},
    'recherche': {'desktop': [(1134, -130, 392, 520, 0, 'rgba(255, 255, 255, .08)')]},
}
for _formes in FORMES_HEROS.values():
    _formes.setdefault('mobile', _F_MOBILE)

# --- Pages alimentées par la base : Opportunités, Actualités, Notre impact, Ressources ------------
# Les formes décoratives des bandeaux : voir FORMES_HEROS (`formes_cle`).

_ACCUEIL = {'label': 'Accueil', 'url': URL_HOME}

OPPORTUNITES_PAGE = {
    'hero': {
        'fond': 'vert-profond', 'hauteur': 580, 'taille': 62, 'taille_mobile': 40, 'largeur_texte': 760, 'largeur_chapo': 560,
        'fil': [_ACCUEIL, {'label': 'Opportunités'}],
        'surtitre': 'Opportunités',
        'titre': 'Les opportunités qui peuvent', 'suite': 'faire grandir votre parcours.',
        'chapo': "Retrouvez sur cette page les opportunités proposées par UCIV et son réseau de "
                 "partenaires, mises à jour au fil de l'eau.",
        'formes_cle': 'opportunites',
        'note': {'texte': 'saisis ta chance !', 'x': 1000, 'y': 470, 'taille': 44, 'rot': -7, 'c': 'var(--blanc)'},
    },
    'categories': [
        ('Volontariat', "Des missions permettant de s'engager et de développer son expérience."),
        ('Formations', 'Des formations et ateliers pour développer ses compétences.'),
        ('Stages', 'Des opportunités de mise en pratique professionnelle.'),
        ('Emploi', 'Des opportunités professionnelles communiquées par les partenaires.'),
        ('Appels à candidatures',
         'Des programmes, concours et initiatives auxquels les jeunes peuvent participer.'),
    ],
    'note_modele': "Les fiches ci-dessous sont des emplacements : elles seront alimentées depuis "
                   "l'espace d'administration du site.",
}

ACTUALITES_PAGE = {
    'hero': {
        'fond': 'vert-profond', 'hauteur': 500, 'taille': 88, 'taille_mobile': 48, 'largeur_texte': 700, 'largeur_chapo': 560,
        'fil': [_ACCUEIL, {'label': 'Actualités'}],
        'surtitre': 'Actualités',
        'titre': "L'actualité", 'suite': "d'UCIV.",
        'chapo': "Découvrez les activités, projets, événements, partenariats et initiatives qui "
                 "font vivre Une Côte d'Ivoire Volontaire.",
        'formes_cle': 'actualites',
    },
    'par_page': 6,
}

IMPACT_PAGE = {
    'hero': {
        'fond': 'vert', 'hauteur': 520, 'taille': 66, 'taille_mobile': 40, 'largeur_texte': 760, 'largeur_chapo': 560,
        'fil': [_ACCUEIL, {'label': 'Notre impact'}],
        'surtitre': 'Notre impact',
        'titre': 'Des actions. Des expériences.', 'suite': "De l'impact.",
        'chapo': "Nous voulons pouvoir mesurer notre engagement à travers des résultats concrets.",
        'formes_cle': 'impact',
        'note': {'texte': 'des preuves, pas des promesses', 'x': 890, 'y': 440, 'taille': 38, 'rot': -5,
                 'c': 'var(--blanc)'},
    },
    'chiffres_intro': "Une recherche est en cours pour établir des chiffres fiables. Les valeurs "
                      "seront mises à jour depuis l'espace d'administration dès qu'elles seront "
                      "disponibles.",
    'histoires_intro': "Des jeunes qui ont participé à une activité, des volontaires qui ont "
                       "développé de nouvelles compétences, des participants qui ont transformé "
                       "leur expérience en opportunité.",
    # Couleurs des cartes d'indicateurs, dans l'ordre de la maquette.
    'couleurs': ['orange', 'vert', 'jaune', 'profond', 'sable', 'brun'],
}

RESSOURCES_PAGE = {
    'hero': {
        'fond': 'orange', 'hauteur': 500, 'taille': 76, 'taille_mobile': 44, 'largeur_texte': 760, 'largeur_chapo': 600,
        'fil': [_ACCUEIL, {'label': 'Ressources'}],
        'surtitre': 'Ressources',
        'titre': "Apprendre. S'informer.", 'suite': 'Progresser.',
        'chapo': "Retrouvez les ressources produites ou recommandées par UCIV pour accompagner les "
                 "jeunes dans leur développement personnel, professionnel et citoyen.",
        'formes_cle': 'ressources',
    },
    'note_modele': "Les fiches ci-dessus sont des emplacements : elles seront alimentées depuis "
                   "l'espace d'administration du site.",
    # Icône et couleur du picto de chaque type, d'après la maquette.
    'types': {
        'guide': {'icone': 'book-open', 'couleur': 'orange'},
        'manuel': {'icone': 'notebook-text', 'couleur': 'brun'},
        'support': {'icone': 'presentation', 'couleur': 'vert'},
        'article': {'icone': 'newspaper', 'couleur': 'jaune'},
        'video': {'icone': 'play', 'couleur': 'profond'},
        'podcast': {'icone': 'mic', 'couleur': 'jaune'},
    },
}

RECHERCHE_PAGE = {
    'hero': {
        'fond': 'vert-profond', 'hauteur': 420, 'taille': 72, 'taille_mobile': 40, 'largeur_texte': 760,
        'largeur_chapo': 560, 'formes_cle': 'recherche',
        'fil': [_ACCUEIL, {'label': 'Rechercher'}],
        'surtitre': 'Rechercher',
        'titre': 'Que cherchez-vous', 'suite': 'sur le site ?',
        'chapo': "Programmes, actualités, opportunités, ressources : tapez un ou plusieurs mots.",
    },
    'exemples': ['Go du Digital', 'Leadership', 'volontaire', 'partenariat', 'recrutement'],
}

ARTICLE_PAGE = {
    'formes_cle': 'article',
}

# --- Référencement (SEO) ----------------------------------------------------
# Titre : 50-60 caractères ; description : 120-160 caractères ; une entrée par URL nommée de l'application.
# `fil` : fil d'Ariane des données structurées (libellé, nom d'URL ; None = page courante).
# `type` : type de page pour le balisage schema.org (voir app/seo.py).

LANCEMENT_LEADERSHIP = {'date': '2026-10-24', 'lieu': 'American Corner', 'ville': 'Abidjan'}
IMAGE_PAR_DEFAUT = 'app/assets/img/og-defaut.jpg'

_ACC = ('Accueil', 'home')

SEO_PAGES = {
    'home': {
        'titre': "Une Côte d'Ivoire Volontaire (UCIV) — Agir pour le pays",
        'description': "UCIV mobilise la jeunesse ivoirienne par le volontariat et l'engagement citoyen : programmes, "
                       "réseau de leaders, formations et opportunités pour agir.",
        'type': 'accueil', 'fil': [],
    },
    'qui_sommes_nous': {
        'titre': 'Qui sommes-nous ? Vision, mission et valeurs | UCIV',
        'description': "Découvrez UCIV, initiative citoyenne qui mobilise la jeunesse : notre ambition, notre vision, "
                       "notre mission et les six valeurs qui guident nos programmes.",
        'type': 'a_propos', 'fil': [_ACC, ('Qui sommes-nous ?', None)],
    },
    'equipe': {
        'titre': "L'équipe d'UCIV — Bureau exécutif et communication",
        'description': "Rencontrez l'équipe d'UCIV : le président fondateur Marshall Kouamé, le bureau exécutif et la "
                       "direction des médias et de la communication.",
        'type': 'a_propos', 'fil': [_ACC, ('Qui sommes-nous ?', 'qui_sommes_nous'), ('Équipe', None)],
    },
    'nos_programmes': {
        'titre': 'Nos programmes — Go du Digital, Leadership, Experience Lab',
        'description': "Les Go du Digital, UCIV Leadership et Experience Lab : trois programmes pour apprendre en "
                       "agissant, avec formation pratique, mise en situation réelle et suivi.",
        'type': 'programmes', 'fil': [_ACC, ('Nos programmes', None)],
    },
    'go_du_digital': {
        'titre': 'Les Go du Digital — Programme digital pour jeunes femmes',
        'description': "Les Go du Digital : 6 samedis, 90 % de pratique, pour que les jeunes femmes fassent du digital "
                       "un outil d'autonomie, d'expression et d'opportunité.",
        'type': 'cours', 'fil': [_ACC, ('Nos programmes', 'nos_programmes'), ('Les Go du Digital', None)],
        'cours': {'nom': 'Les Go du Digital', 'public': 'Jeunes femmes'},
    },
    'uciv_leadership': {
        'titre': 'UCIV Leadership — Le réseau des futurs jeunes leaders',
        'description': "UCIV Leadership, le réseau sélectif des jeunes leaders : formations, mentorat et projets à fort "
                       "impact. Lancement le 24 octobre 2026 à l'American Corner.",
        'type': 'evenement', 'fil': [_ACC, ('Nos programmes', 'nos_programmes'), ('UCIV Leadership', None)],
        'image': 'app/assets/img/og-leadership.jpg',
    },
    'experience_lab': {
        'titre': 'Experience Lab — Personal branding et pitch | UCIV',
        'description': "Experience Lab : un espace pour apprendre à mieux se connaître, mieux se présenter et valoriser "
                       "son expérience grâce au personal branding et au pitch.",
        'type': 'cours', 'fil': [_ACC, ('Nos programmes', 'nos_programmes'), ('Experience Lab', None)],
        'cours': {'nom': 'Experience Lab', 'public': 'Jeunes'},
        'image': 'app/assets/img/og-experience-lab.jpg',
    },
    'vision_action': {
        'titre': "De la vision à l'action — Programme UCIV Leadership",
        'description': "De la vision à l'action, programme d'UCIV Leadership : clarifier son ambition, surmonter "
                       "ses doutes et construire un plan d'action concret.",
        'type': 'cours',
        'fil': [_ACC, ('Nos programmes', 'nos_programmes'), ('UCIV Leadership', 'uciv_leadership'),
                ("De la vision à l'action", None)],
        'cours': {'nom': "De la vision à l'action", 'public': 'Jeunes'},
        'image': 'app/assets/img/og-vision-action.jpg',
    },
    'rh_parole': {
        'titre': "Les RH ont la parole — Programme d'UCIV Leadership",
        'description': "Les RH ont la parole, programme d'UCIV Leadership : échanger avec des recruteurs pour "
                       "comprendre le recrutement et réussir son CV et ses entretiens.",
        'type': 'cours',
        'fil': [_ACC, ('Nos programmes', 'nos_programmes'), ('UCIV Leadership', 'uciv_leadership'),
                ('Les RH ont la parole', None)],
        'cours': {'nom': 'Les RH ont la parole', 'public': 'Étudiants, jeunes diplômés et chercheurs d\'emploi'},
        'image': 'app/assets/img/og-rh-parole.jpg',
    },
    'engagement': {
        'titre': "Je veux m'engager — Devenir volontaire avec UCIV",
        'description': "Il y a une place pour ton engagement : deviens volontaire, rejoins UCIV Leadership ou propose "
                       "tes compétences en communication, numérique ou formation.",
        'type': 'page', 'fil': [_ACC, ("Je veux m'engager", None)],
        'image': 'app/assets/img/og-engagement.jpg',
    },
    'partenaires': {
        'titre': "Devenir partenaire d'UCIV — Collaborer pour la jeunesse",
        'description': "Devenez partenaire d'UCIV : partenariats institutionnels, techniques ou financiers, sponsoring, "
                       "mécénat, formations et stages pour la jeunesse ivoirienne.",
        'type': 'page', 'fil': [_ACC, ('Partenaires', None)],
        'image': 'app/assets/img/og-partenaires.jpg',
    },
    'opportunites': {
        'titre': 'Opportunités pour les jeunes — Volontariat, stages, emploi',
        'description': "Volontariat, formations, stages, emploi, appels à candidatures : retrouvez les opportunités "
                       "proposées par UCIV et ses partenaires, mises à jour régulièrement.",
        'type': 'collection', 'fil': [_ACC, ('Opportunités', None)],
    },
    'actualites': {
        'titre': "Actualités — Activités, projets et événements d'UCIV",
        'description': "Activités, projets, événements, partenariats et témoignages : toute l'actualité d'Une Côte "
                       "d'Ivoire Volontaire, de l'engagement citoyen au leadership.",
        'type': 'collection', 'fil': [_ACC, ('Actualités', None)],
    },
    'impact': {
        'titre': 'Notre impact — Indicateurs et parcours de jeunes | UCIV',
        'description': "Des actions, des expériences, de l'impact : les indicateurs d'UCIV et des parcours de jeunes qui "
                       "ont transformé leur engagement en compétences.",
        'type': 'page', 'fil': [_ACC, ('Notre impact', None)],
    },
    'ressources': {
        'titre': 'Ressources — Guides, supports et vidéos pour les jeunes',
        'description': "Guides, manuels, supports de formation, articles, vidéos et podcasts produits ou recommandés par "
                       "UCIV pour accompagner les jeunes dans leur parcours.",
        'type': 'collection', 'fil': [_ACC, ('Ressources', None)],
    },
    'contact': {
        'titre': "Contact — Écrire à Une Côte d'Ivoire Volontaire",
        'description': "Une question, un partenariat, une envie de rejoindre UCIV ? Écrivez-nous ou appelez-nous : "
                       "coordonnées officielles d'Une Côte d'Ivoire Volontaire, à Abidjan.",
        'type': 'contact', 'fil': [_ACC, ('Contact', None)],
    },
}

# Pages listées dans le sitemap et dans llms.txt, dans l'ordre d'importance.
PAGES_INDEXABLES = ['home', 'qui_sommes_nous', 'equipe', 'nos_programmes', 'go_du_digital', 'uciv_leadership',
                    'vision_action', 'rh_parole', 'experience_lab', 'engagement', 'partenaires', 'opportunites', 'actualites', 'impact',
                    'ressources', 'contact']
# Paramètres d'URL qui ne changent que l'affichage : ces variantes ne sont pas indexées.
PARAMETRES_FILTRES = ('categorie', 'type', 'theme', 'choix', 'objet')

# --- GEO : réponses directes pour les moteurs de réponse IA ----------------------------------------------------
# Section « Questions fréquentes » visible sur chaque page : titres en forme de question, réponse autonome
# (extractible sans le reste de la page), chiffres et noms exacts. Les faits viennent des contenus du site ;
# ne rien y ajouter qui ne soit pas vérifié (dates, tarifs et lieux « à confirmer » restent annoncés comme tels).
# Pas de balisage FAQPage : réservé par Google aux sites publics et de santé (voir app/seo.py).

FAQ_TITRE = 'Questions fréquentes'

FAQ = {
    'home': [
        ("Qu'est-ce qu'Une Côte d'Ivoire Volontaire (UCIV) ?",
         "Une Côte d'Ivoire Volontaire (UCIV) est une initiative citoyenne qui mobilise la jeunesse ivoirienne "
         "autour du volontariat, du bénévolat et de l'engagement citoyen. Elle en fait un levier de compétences, "
         "de leadership et d'employabilité grâce à des missions de terrain, des projets menés en équipe et des "
         "formations suivies jusqu'au bout."),
        ("Quels programmes propose UCIV ?",
         "UCIV propose trois programmes : Les Go du Digital (6 samedis de formation, pratique à 90 %, pour les jeunes "
         "femmes), UCIV Leadership (un réseau sélectif de 30 à 50 membres pour la cohorte pionnière) et Experience "
         "Lab (un espace consacré au personal branding et au pitch professionnel)."),
        ("Comment s'engager avec UCIV ?",
         "Il existe trois façons de rejoindre UCIV : devenir volontaire, rejoindre le réseau UCIV Leadership ou "
         "proposer ses compétences (communication, graphisme, audiovisuel, photographie, formation, numérique…). "
         "Il suffit de remplir le formulaire d'engagement du site : l'équipe revient ensuite vers la personne."),
        ("Où se trouve UCIV et comment la contacter ?",
         "UCIV est basée à Abidjan (04 BP 2087 Abidjan, Côte d'Ivoire). On peut l'appeler au +225 07 87 56 17 66 ou "
         "au +225 07 07 722 078, ou écrire à organisationuciv@gmail.com."),
        ("Quelle est la prochaine grande date d'UCIV ?",
         "La prochaine grande date d'UCIV est le 24 octobre 2026 : le lancement du réseau UCIV Leadership, lors "
         "d'une conférence au format TEDx à l'American Corner d'Abidjan. L'heure sera confirmée sur le site."),
    ],
    'qui_sommes_nous': [
        ("Qu'est-ce qu'UCIV ?",
         "UCIV (Une Côte d'Ivoire Volontaire) est une initiative citoyenne qui mobilise la jeunesse autour du "
         "volontariat, du bénévolat et de l'engagement citoyen. Son ambition est de faire du volontariat un véritable "
         "espace de développement personnel, professionnel et citoyen : un lieu où l'on apprend en agissant, pas "
         "seulement en écoutant."),
        ("Quelle est la mission d'UCIV ?",
         "La mission d'UCIV est de mobiliser les jeunes autour du volontariat et de l'engagement pour développer "
         "leurs compétences et contribuer à leur employabilité. Elle agit à travers le volontariat et le bénévolat, "
         "les formations, les programmes de développement des compétences, le leadership, les projets citoyens, la "
         "mobilisation communautaire et les initiatives en faveur de l'employabilité."),
        ("Quelle est la vision d'UCIV ?",
         "UCIV veut former une génération de jeunes engagés, responsables et acteurs du changement. Elle croit "
         "qu'une jeunesse qui développe ses compétences, prend des initiatives et s'engage dans sa communauté est "
         "mieux préparée à contribuer au développement de la Côte d'Ivoire."),
        ("Quelles sont les valeurs d'UCIV ?",
         "UCIV s'appuie sur six valeurs : l'engagement, la responsabilité, la solidarité, l'apprentissage, "
         "l'innovation et l'impact. Elles guident ses programmes, ses projets et la manière dont l'équipe travaille "
         "ensemble."),
        ("Qui a fondé UCIV ?",
         "UCIV a été fondée par Marshall Kouamé, président et fondateur d'Une Côte d'Ivoire Volontaire."),
    ],
    'equipe': [
        ("Qui dirige UCIV ?",
         "UCIV est dirigée par son président et fondateur, Marshall Kouamé. Le bureau exécutif comprend Aïssata "
         "Ouattara (Secrétaire Générale), le Dr Angèle Zang (Trésorière Générale), Roxane Atchia (Commissaire aux "
         "comptes) et Martine Boa (Responsable Générale des projets)."),
        ("Qui assure la communication d'UCIV ?",
         "La direction des médias et de la communication réunit Emmanuel Fieni Kouassi (Responsable Communication & "
         "mobilisation), Djamira Kamagaté (Commissaire aux comptes adjointe et créatrice de contenu), Mieimmo Kouassi "
         "(Chargée de Marketing) et Ago Maria Konan (Secrétaire Générale adjointe et créatrice de contenu)."),
        ("Comment rejoindre l'équipe d'UCIV ?",
         "Toute personne qui souhaite mettre ses compétences au service d'UCIV peut proposer son aide depuis le "
         "formulaire d'engagement du site, en choisissant « Proposer mes compétences »."),
    ],
    'nos_programmes': [
        ("Quels sont les programmes d'UCIV ?",
         "UCIV développe trois programmes : Les Go du Digital (le digital comme outil d'autonomie, d'expression et "
         "d'opportunité), UCIV Leadership (le réseau des jeunes leaders et futurs leaders) et Experience Lab (le "
         "personal branding et le pitch professionnel). D'autres programmes seront annoncés."),
        ("Quelle est la méthode commune à tous les programmes ?",
         "Chaque programme suit la même logique en trois temps : une formation courte et pratique, une mise en "
         "situation réelle, puis un accompagnement qui ne s'arrête pas à la dernière séance."),
        ("À qui s'adressent les programmes d'UCIV ?",
         "Les programmes répondent à des besoins précis des jeunes ivoiriens : compétences numériques, leadership, "
         "personal branding et employabilité."),
    ],
    'go_du_digital': [
        ("Qu'est-ce que Les Go du Digital ?",
         "Les Go du Digital est un programme d'UCIV destiné aux jeunes femmes, qui fait du digital un outil "
         "d'autonomie, d'expression et d'opportunité. Il dure 6 samedis, avec 90 % de pratique, et s'organise "
         "autour de quatre volets : Personal Branding, Sécurité Numérique, Stratégie de Contenu et Techniques de "
         "Tournage."),
        ("Qui peut participer aux Go du Digital ?",
         "Le programme est pensé pour les jeunes femmes, les étudiantes, les jeunes professionnelles, les femmes "
         "souhaitant développer une activité grâce au digital et les personnes souhaitant améliorer leurs "
         "compétences numériques."),
        ("Qu'apprennent les participantes ?",
         "Les participantes apprennent à développer leur personal branding, à créer du contenu, à vendre en ligne, "
         "à se protéger dans l'environnement numérique et à utiliser les réseaux sociaux de manière responsable."),
        ("Qu'est-ce que « La Reine du Digital » ?",
         "« La Reine du Digital » est la compétition qui conclut chaque édition des Go du Digital. Elle valorise les "
         "meilleures productions des participantes devant un jury et le public."),
        ("Quand a lieu la prochaine édition et combien coûte-t-elle ?",
         "La date de la prochaine édition, le lieu, le tarif et les modalités d'inscription sont encore à confirmer. "
         "Ils seront publiés sur cette page dès qu'ils seront connus."),
    ],
    'uciv_leadership': [
        ("Qu'est-ce qu'UCIV Leadership ?",
         "UCIV Leadership est le réseau des leaders et futurs leaders d'Une Côte d'Ivoire Volontaire : un cadre où "
         "des jeunes triés sur le volet se forment, se connectent et passent à l'action ensemble, grâce à des "
         "formations par des spécialistes, du mentorat, des échanges et des projets à fort impact."),
        ("Comment intégrer le réseau UCIV Leadership ?",
         "La sélection se fait en deux étapes : un pitch vidéo, puis un entretien collectif. Les nouveaux arrivants "
         "sont d'abord membres aspirants, puis deviennent membres du réseau. Un système de points d'engagement suit "
         "la contribution de chaque membre et conditionne son maintien."),
        ("Quand a lieu le lancement d'UCIV Leadership ?",
         "Le lancement a lieu le 24 octobre 2026 à l'American Corner d'Abidjan, avec une conférence au format TEDx. "
         "L'heure reste à confirmer."),
        ("Combien de membres compte la cohorte pionnière ?",
         "La cohorte pionnière réunit entre 30 et 50 membres. Le réseau est mixte, sélectif et exigeant."),
        ("Qu'apporte UCIV Leadership à ses membres ?",
         "Le réseau fait circuler en priorité entre ses membres les bonnes opportunités, notamment en matière "
         "d'emploi, de financement et de formations."),
    ],
    'experience_lab': [
        ("Qu'est-ce qu'Experience Lab ?",
         "Experience Lab est le programme d'UCIV consacré au personal branding et au pitch professionnel. C'est un "
         "espace d'apprentissage et de partage qui aide les jeunes à mieux se connaître, mieux se présenter et "
         "mieux valoriser leur expérience."),
        ("Que signifie « Know yourself before showing yourself » ?",
         "Cette phrase résume l'approche d'Experience Lab : avant de chercher à être visible, il faut comprendre qui "
         "l'on est, ce que l'on sait faire, ce que l'on peut apporter et comment on souhaite être perçu."),
        ("Quels sont les objectifs d'Experience Lab ?",
         "Le programme permet aux participants de mieux comprendre leur identité et leurs forces, de définir leur "
         "positionnement, de valoriser leurs compétences, de construire une présentation personnelle cohérente, "
         "d'améliorer leur capacité à présenter leur parcours et de développer leur confiance dans les situations "
         "professionnelles."),
        ("Quel est le format et quelles sont les dates ?",
         "Le format, les dates et les modalités d'inscription d'Experience Lab sont encore à confirmer."),
    ],
    'vision_action': [
        ("Qu'est-ce que « De la vision à l'action » ?",
         "« De la vision à l'action » est un programme d'UCIV Leadership qui encourage les jeunes à clarifier leurs "
         "ambitions, à développer leur potentiel et à passer concrètement à l'action pour construire leur avenir."),
        ("Quels sont les objectifs de « De la vision à l'action » ?",
         "Le programme aide les jeunes à clarifier leur vision, à développer un état d'esprit orienté vers "
         "l'action, à surmonter les obstacles, à construire un plan d'action et à exercer leur leadership."),
        ("À qui s'adresse « De la vision à l'action » ?",
         "Il s'adresse principalement aux jeunes désireux de mieux orienter leur avenir, de développer leur "
         "leadership et de concrétiser leurs projets personnels, professionnels ou citoyens."),
        ("Quand a lieu « De la vision à l'action » ?",
         "Le format, les dates et les modalités d'inscription sont encore à confirmer."),
    ],
    'rh_parole': [
        ("Qu'est-ce que « Les RH ont la parole » ?",
         "« Les RH ont la parole » est une initiative d'UCIV Leadership qui permet aux jeunes d'échanger "
         "directement avec des spécialistes des ressources humaines, à travers des panels, des échanges "
         "interactifs et des témoignages de professionnels."),
        ("Qu'apprend-on pendant le programme ?",
         "Les participants comprennent mieux les attentes des recruteurs et les étapes du recrutement, "
         "identifient les compétences recherchées et reçoivent des conseils pratiques pour leur CV et leurs "
         "entretiens."),
        ("À qui s'adresse « Les RH ont la parole » ?",
         "Aux étudiants, aux jeunes diplômés, aux personnes en recherche d'emploi et à tous les jeunes désireux "
         "de mieux préparer leur parcours professionnel."),
        ("Quand a lieu « Les RH ont la parole » ?",
         "Le format, les dates et les modalités d'inscription sont encore à confirmer."),
    ],
    'engagement': [
        ("Comment devenir volontaire avec UCIV ?",
         "Pour devenir volontaire, il suffit de remplir le formulaire d'engagement en choisissant « Devenir "
         "volontaire ». Les volontaires participent aux activités et aux projets d'UCIV et mettent leurs compétences "
         "au service d'actions concrètes, sur le terrain."),
        ("Quelles compétences UCIV recherche-t-elle ?",
         "UCIV peut avoir besoin de profils en communication, graphisme, audiovisuel, photographie, formation, "
         "événementiel, ressources humaines, gestion de projet, numérique et développement web."),
        ("Que se passe-t-il après l'envoi du formulaire ?",
         "Après l'envoi du formulaire, l'équipe d'UCIV revient vers la personne pour la suite. Les données saisies "
         "servent uniquement à la recontacter."),
    ],
    'partenaires': [
        ("Qui sont les partenaires d'UCIV ?",
         "UCIV collabore notamment avec BonixUp (accès à des formateurs), PAIPRO-JEUNES (accompagnement vers "
         "l'emploi) et l'ONG Light for All CI (logistique de terrain)."),
        ("Quelles formes de collaboration UCIV propose-t-elle ?",
         "UCIV est ouverte aux partenariats institutionnels, techniques et financiers, au sponsoring, au mécénat, aux "
         "collaborations sur des programmes, aux formations, aux opportunités de stage et professionnelles, et aux "
         "projets communs."),
        ("Comment proposer un partenariat à UCIV ?",
         "Une organisation peut remplir le formulaire « Proposer un partenariat » de cette page en présentant sa "
         "structure et son idée de collaboration, ou écrire à organisationuciv@gmail.com."),
    ],
    'opportunites': [
        ("Quelles opportunités trouve-t-on sur le site d'UCIV ?",
         "Le site présente cinq catégories d'opportunités : le volontariat, les formations, les stages, l'emploi et "
         "les appels à candidatures. Chaque fiche indique la structure, le lieu et la date limite."),
        ("Qui propose ces opportunités ?",
         "Les opportunités sont proposées par UCIV et par son réseau de partenaires, et mises à jour au fil de l'eau."),
        ("Comment proposer une opportunité aux jeunes ?",
         "Une organisation qui souhaite publier une opportunité peut devenir partenaire d'UCIV depuis la page "
         "Partenaires."),
    ],
    'actualites': [
        ("Que trouve-t-on dans les actualités d'UCIV ?",
         "Les actualités présentent les activités, projets, événements, partenariats et initiatives qui font vivre "
         "Une Côte d'Ivoire Volontaire, ainsi que des témoignages et des portraits de jeunes."),
        ("Comment filtrer les actualités ?",
         "Les articles se filtrent par catégorie : nos activités, nos programmes, nos événements, nos partenariats, "
         "témoignages, portraits, employabilité, leadership et engagement citoyen."),
    ],
    'impact': [
        ("Comment UCIV mesure-t-elle son impact ?",
         "UCIV suit six indicateurs : le nombre de jeunes mobilisés, de volontaires, de programmes réalisés, de "
         "participants formés, de partenaires et de projets réalisés."),
        ("Pourquoi certains chiffres sont-ils affichés à 000 ?",
         "Une recherche est en cours pour établir des chiffres fiables. Les valeurs seront mises à jour dès qu'elles "
         "seront disponibles : UCIV préfère ne publier que des résultats vérifiés."),
        ("Où trouver des témoignages ?",
         "La section « Nos histoires » de cette page présente des parcours de jeunes qui ont participé à une "
         "activité, développé de nouvelles compétences ou transformé leur expérience en opportunité."),
    ],
    'ressources': [
        ("Quels types de ressources propose UCIV ?",
         "La bibliothèque réunit des guides, des manuels, des supports de formation, des articles, des vidéos et des "
         "podcasts."),
        ("Quels thèmes les ressources couvrent-elles ?",
         "Les ressources portent sur l'employabilité, le leadership, le numérique et le volontariat."),
        ("Qui produit les ressources ?",
         "Ce sont des ressources produites ou recommandées par UCIV pour accompagner les jeunes dans leur "
         "développement personnel, professionnel et citoyen."),
    ],
    'contact': [
        ("Comment contacter UCIV ?",
         "On peut contacter UCIV par téléphone au +225 07 87 56 17 66 ou au +225 07 07 722 078, par e-mail à "
         "organisationuciv@gmail.com, par courrier au 04 BP 2087 Abidjan, ou depuis le formulaire de cette page."),
        ("Sur quels réseaux sociaux suivre UCIV ?",
         "UCIV est présente sur Facebook, sur TikTok (compte @uneciv) et sur LinkedIn. Les liens vers ces pages "
         "figurent sur cette page et dans le pied de page de chaque page du site."),
        ("Pour quels sujets écrire à UCIV ?",
         "Le formulaire de contact couvre le volontariat, les programmes, UCIV Leadership, les partenariats, les "
         "propositions de compétences, la presse et les médias, ainsi que toute autre demande."),
    ],
}


# --- Pages légales ---------------------------------------------------------
# Une page par document, même gabarit (layout/legal.html). Les textes entre
# crochets sont à compléter ou valider par UCIV : ils s'affichent en orange.
# Blocs d'une section : {'p': texte}, {'fiche': [(libellé, valeur), …]},
# {'liste': [point, …]}, {'encadre': texte}.

LEGAL_MAJ = '[jj/mm/aaaa]'

LEGAL_DOCUMENTS = [
    {'cle': 'mentions', 'label': 'Mentions légales', 'url': URL_MENTIONS, 'icone': 'scale',
     'texte': 'Éditeur, hébergeur et propriété intellectuelle.'},
    {'cle': 'confidentialite', 'label': 'Politique de confidentialité', 'url': URL_CONFIDENTIALITE,
     'icone': 'shield-check', 'texte': 'Les données que nous collectons et vos droits.'},
    {'cle': 'conditions', 'label': "Conditions d'utilisation", 'url': URL_CONDITIONS,
     'icone': 'file-text', 'texte': "Les règles d'usage du site et des formulaires."},
]

def _legal_hero(label, titre, suite, chapo):
    return {
        'fond': 'vert-profond', 'hauteur': 480, 'taille': 72, 'taille_mobile': 40,
        'largeur_texte': 760, 'largeur_chapo': 580,
        'fil': [_ACCUEIL, {'label': label}],
        'surtitre': 'Informations légales',
        'titre': titre, 'suite': suite, 'chapo': chapo,
        'formes_cle': 'legal', 'maj': LEGAL_MAJ,
    }


LEGAL = {
    'mentions': {
        'titre_page': 'Mentions légales',
        'description': "Éditeur, directeur de la publication, hébergeur et propriété intellectuelle "
                       "du site d'Une Côte d'Ivoire Volontaire.",
        'hero': _legal_hero(
            'Mentions légales', 'Mentions', 'légales.',
            "Qui édite ce site, qui l'héberge et à qui s'adresser : les informations "
            "obligatoires, en toute transparence."),
        'sections': [
            {'titre': 'Éditeur du site', 'blocs': [
                {'p': "Le site uciv.ci [adresse à confirmer] est édité par Une Côte d'Ivoire "
                      "Volontaire (UCIV), initiative citoyenne constituée en association de droit "
                      "ivoirien [forme juridique à confirmer]."},
                {'fiche': [
                    ('Dénomination', "Une Côte d'Ivoire Volontaire (UCIV)"),
                    ('Siège', "04 BP 2087 Abidjan, Côte d'Ivoire"),
                    ('Déclaration', '[N° de récépissé de déclaration]'),
                    ('Téléphone', '+225 07 87 56 17 66 / 07 07 722 078'),
                    ('E-mail', 'organisationuciv@gmail.com'),
                ]},
            ]},
            {'titre': 'Directeur de la publication', 'blocs': [
                {'p': "Marshall Kouamé, président et fondateur d'Une Côte d'Ivoire Volontaire."},
            ]},
            {'titre': 'Hébergement', 'blocs': [
                {'fiche': [
                    ('Hébergeur', "[Nom de l'hébergeur]"),
                    ('Adresse', "[Adresse postale de l'hébergeur]"),
                    ('Site web', '[www.hebergeur.com]'),
                ]},
            ]},
            {'titre': 'Conception et réalisation', 'blocs': [
                {'p': "Design et développement du site : [Nom du prestataire]. Le site est "
                      "construit avec Django, un logiciel libre."},
            ]},
            {'titre': 'Propriété intellectuelle', 'blocs': [
                {'p': "L'ensemble des contenus de ce site (textes, logos, photographies, visuels, "
                      "mise en page) est la propriété d'UCIV ou de ses partenaires, sauf mention "
                      "contraire. Toute reproduction, même partielle, est interdite sans "
                      "autorisation écrite préalable."},
                {'p': "Le logo UCIV et la marque « UCIV Leadership » ne peuvent être utilisés sans "
                      "l'accord d'UCIV."},
            ]},
            {'titre': 'Crédits photographiques', 'blocs': [
                {'p': "Photographies : UCIV et ses bénévoles, sauf mention contraire sous l'image. "
                      "[Autres crédits à compléter]."},
            ]},
            {'titre': 'Liens et responsabilité', 'blocs': [
                {'p': "UCIV s'efforce de publier des informations exactes et à jour, sans pouvoir "
                      "en garantir l'exhaustivité. Les liens vers des sites externes sont proposés "
                      "à titre informatif : UCIV n'est pas responsable de leur contenu."},
            ]},
            {'titre': 'Nous contacter', 'blocs': [
                {'p': "Pour toute question sur ces mentions ou pour signaler un contenu, "
                      "écrivez-nous via la page Contact ou à organisationuciv@gmail.com."},
            ]},
        ],
    },
    'confidentialite': {
        'titre_page': 'Politique de confidentialité',
        'description': "Données collectées par le site d'UCIV, finalités, durée de conservation "
                       "et exercice de vos droits.",
        'hero': _legal_hero(
            'Politique de confidentialité', 'Politique de', 'confidentialité.',
            "Quelles données nous collectons, pourquoi, combien de temps nous les gardons, et "
            "comment exercer vos droits."),
        'sections': [
            {'titre': 'Responsable du traitement', 'blocs': [
                {'p': "Le responsable du traitement des données collectées sur ce site est Une "
                      "Côte d'Ivoire Volontaire (UCIV), 04 BP 2087 Abidjan, représentée par son "
                      "président, Marshall Kouamé. Contact : organisationuciv@gmail.com."},
                {'p': "UCIV applique la loi n° 2013-450 du 19 juin 2013 relative à la protection "
                      "des données à caractère personnel en Côte d'Ivoire."},
            ]},
            {'titre': 'Données collectées', 'blocs': [
                {'p': "Nous collectons uniquement les données que vous nous transmettez "
                      "volontairement via nos formulaires :"},
                {'fiche': [
                    ("Je veux m'engager", "Nom, e-mail, téléphone, choix d'engagement, compétences, "
                                          "message"),
                    ('Partenariat', "Nom, organisation, e-mail, téléphone, type de collaboration, "
                                    "présentation"),
                    ('Contact', 'Nom, e-mail, téléphone, organisation (facultatif), objet, message'),
                    ("Lettre d'information", 'Adresse e-mail'),
                ]},
            ]},
            {'titre': 'Pourquoi nous les utilisons', 'blocs': [
                {'liste': [
                    "Vous recontacter au sujet de votre engagement, de votre proposition ou de "
                    "votre question",
                    'Organiser nos programmes, activités et événements',
                    "Vous envoyer notre lettre d'information, si vous vous y êtes inscrit",
                    'Établir des statistiques anonymes sur la participation',
                ]},
                {'encadre': 'Vos données ne sont jamais vendues ni utilisées à des fins publicitaires.'},
            ]},
            {'titre': 'Base légale', 'blocs': [
                {'p': "Le traitement repose sur votre consentement, exprimé lorsque vous envoyez un "
                      "formulaire ou vous inscrivez à la lettre d'information. Vous pouvez le "
                      "retirer à tout moment."},
            ]},
            {'titre': 'Destinataires', 'blocs': [
                {'p': "Seuls les membres de l'équipe UCIV chargés du suivi des demandes accèdent à "
                      "vos données. Elles peuvent être partagées avec un partenaire d'un programme "
                      "uniquement avec votre accord préalable. Notre hébergeur [Nom de "
                      "l'hébergeur] assure leur stockage technique."},
            ]},
            {'titre': 'Durée de conservation', 'blocs': [
                {'fiche': [
                    ('Demandes et candidatures', '[3 ans] après le dernier échange'),
                    ("Lettre d'information", "Jusqu'à votre désinscription"),
                    ('Données de connexion', '[12 mois] au maximum'),
                ]},
            ]},
            {'titre': 'Vos droits', 'blocs': [
                {'p': "Vous disposez d'un droit d'accès, de rectification, d'opposition et de "
                      "suppression de vos données. Pour l'exercer, écrivez à "
                      "organisationuciv@gmail.com en précisant votre demande : nous répondons "
                      "sous [30 jours]."},
                {'p': "Si vous estimez que vos droits ne sont pas respectés, vous pouvez saisir "
                      "l'Autorité de Régulation des Télécommunications/TIC de Côte d'Ivoire "
                      "(ARTCI)."},
            ]},
            {'titre': 'Sécurité', 'blocs': [
                {'p': "Le site est servi en connexion chiffrée (HTTPS). Les formulaires sont "
                      "protégés contre les envois automatisés et l'accès à l'espace "
                      "d'administration est réservé à l'équipe UCIV."},
            ]},
            {'titre': 'Cookies', 'blocs': [
                {'p': "Le site n'utilise aucun cookie publicitaire ni outil de mesure d'audience. "
                      "Seuls des cookies techniques, indispensables au fonctionnement des "
                      "formulaires (sécurité et session), sont déposés."},
            ]},
            {'titre': 'Modifications', 'blocs': [
                {'p': "Cette politique peut évoluer. La date de dernière mise à jour figure en haut "
                      "de la page."},
            ]},
        ],
    },
    'conditions': {
        'titre_page': "Conditions d'utilisation",
        'description': "Règles d'utilisation du site d'Une Côte d'Ivoire Volontaire, de ses "
                       "contenus et de ses formulaires.",
        'hero': _legal_hero(
            "Conditions d'utilisation", 'Conditions', "d'utilisation.",
            "Les règles qui encadrent l'usage du site, de ses contenus et de ses formulaires."),
        'sections': [
            {'titre': 'Objet', 'blocs': [
                {'p': "Les présentes conditions encadrent l'utilisation du site d'Une Côte "
                      "d'Ivoire Volontaire (UCIV). En naviguant sur le site, vous les acceptez."},
            ]},
            {'titre': 'Accès au site', 'blocs': [
                {'p': "Le site est accessible gratuitement, à tout moment, sauf interruption pour "
                      "maintenance ou cas de force majeure. UCIV peut faire évoluer ou suspendre "
                      "tout ou partie du site sans préavis."},
            ]},
            {'titre': 'Utilisation des formulaires', 'blocs': [
                {'p': "En utilisant nos formulaires (engagement, partenariat, contact, lettre "
                      "d'information), vous vous engagez à :"},
                {'liste': [
                    'Fournir des informations exactes et à jour',
                    "Ne pas usurper l'identité d'une autre personne ou organisation",
                    'Ne pas envoyer de contenu illicite, injurieux ou publicitaire',
                    'Ne pas tenter de perturber le fonctionnement du site',
                ]},
            ]},
            {'titre': 'Contenus et propriété intellectuelle', 'blocs': [
                {'p': "Les textes, photographies, logos et visuels du site appartiennent à UCIV ou "
                      "à ses partenaires. Vous pouvez partager un article en citant la source et "
                      "en renvoyant vers le site ; toute autre reproduction nécessite notre "
                      "accord écrit."},
            ]},
            {'titre': 'Opportunités et ressources', 'blocs': [
                {'p': "Les opportunités et ressources publiées le sont à titre informatif. "
                      "Lorsqu'elles proviennent d'un partenaire, celui-ci reste seul responsable "
                      "des conditions de l'offre et de la sélection des candidats."},
            ]},
            {'titre': 'Liens externes', 'blocs': [
                {'p': "Le site peut contenir des liens vers d'autres sites. UCIV n'exerce aucun "
                      "contrôle sur leur contenu et décline toute responsabilité à leur égard."},
            ]},
            {'titre': 'Responsabilité', 'blocs': [
                {'p': "UCIV met tout en œuvre pour publier des informations fiables, sans pouvoir "
                      "garantir l'absence d'erreur. UCIV ne saurait être tenue responsable d'un "
                      "dommage résultant de l'utilisation du site."},
            ]},
            {'titre': 'Droit applicable', 'blocs': [
                {'p': "Les présentes conditions sont soumises au droit ivoirien. En cas de litige, "
                      "et à défaut d'accord amiable, les tribunaux d'Abidjan sont seuls "
                      "compétents."},
            ]},
        ],
    },
}

# --- Page d'erreur 404 -------------------------------------------------------

PAGE_404 = {
    'titre': 'Cette page', 'suite': "s'est égarée.",
    'texte': "Le lien que vous avez suivi est peut-être incorrect, ou la page a été déplacée. "
             "Pas d'inquiétude : il y a toujours une place pour vous chez UCIV.",
    'note': "on s'est perdus ?",
    'liens': [
        {'label': 'Nos programmes', 'url': URL_PROGRAMMES},
        {'label': "Je veux m'engager", 'url': URL_ENGAGEMENT},
        {'label': 'Opportunités', 'url': URL_OPPORTUNITES},
        {'label': 'Actualités', 'url': URL_ACTUALITES},
    ],
}


# --- Lettre d'information ----------------------------------------------------
# Messages de la carte du pied de page après l'envoi du formulaire, et page de
# désinscription (deux étapes : confirmer, puis « C'est noté »).

NEWSLETTER = {
    'reussie': {'titre': "Merci, c'est noté !",
                'texte': 'Vous recevrez nos prochaines actualités à cette adresse.'},
    'deja': {'titre': 'Vous êtes déjà inscrit·e.',
             'texte': 'Merci de votre fidélité : rien à faire de plus.'},
    'invalide': 'Saisissez une adresse e-mail valide.',
}

DESINSCRIPTION = {
    'confirmer': {
        'titre': 'Vous nous', 'suite': 'quittez ?', 'note': 'on vous regrettera !', 'icone': 'mail-minus',
        'texte': "Vous êtes sur le point de désinscrire l'adresse {email} de la lettre d'information "
                 "d'UCIV. Vous ne recevrez plus nos actualités.",
        'bas': 'Vous pourrez vous réinscrire à tout moment depuis le pied de page.',
    },
    'fait': {
        'titre': "C'est noté.", 'suite': 'À bientôt !', 'note': "merci d'avoir été là !", 'icone': 'check',
        'texte': "L'adresse {email} ne recevra plus la lettre d'information d'UCIV. Merci d'avoir "
                 "suivi nos actualités.",
        'bas': "Vous avez changé d'avis ? Réinscrivez-vous depuis le pied de page.",
    },
}


# --- Trop de demandes (limiteur de débit, voir app/ratelimit.py) -------------------------------------------------------
PAGE_429 = {
    'titre': 'Doucement,', 'suite': 'trop de demandes.',
    'texte': "Plusieurs formulaires ont été envoyés depuis votre connexion en peu de temps. Par sécurité, "
             "patientez {duree} avant de réessayer. Si vous êtes une personne et non un robot, merci de votre compréhension !",
    'note': 'une petite pause ?', 'icone': 'clock',
}
