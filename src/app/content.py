"""
Contenus du site, issus du cahier de contenu éditorial (UCIV/info/uciv.md).

Pour l'instant les contenus sont écrits ici, en Python. Les éléments qui
devront être modifiables par l'équipe (articles, chiffres d'impact,
partenaires, opportunités) passeront plus tard en base de données, via des
modèles Django et l'interface d'administration.

Les liens marqués '#' pointent vers des pages qui n'existent pas encore.
"""

from django.urls import reverse_lazy

URL_LEADERSHIP = reverse_lazy('app:uciv_leadership')
URL_QUI = reverse_lazy('app:qui_sommes_nous')

# --- Éléments communs à toutes les pages ----------------------------------

ANNONCE = {
    'date': 'Octobre 2026',
    'texte': "Lancement d'UCIV Leadership : conférence au format TEDx à l'American Corner.",
    'texte_court': "Lancement d'UCIV Leadership",
    'lien_label': 'Rejoindre UCIV Leadership',
    'url': URL_LEADERSHIP,
}

NAVIGATION = [
    {'label': 'Qui sommes-nous ?', 'url': URL_QUI, 'enfants': []},
    {
        'label': 'Nos programmes',
        'url': '#',
        'enfants': [
            {'label': 'Les Go du Digital', 'url': '#'},
            {'label': 'UCIV Leadership', 'url': URL_LEADERSHIP},
            {'label': 'Experience Lab', 'url': '#'},
        ],
    },
    {
        'label': "S'engager",
        'url': '#',
        'enfants': [
            {'label': 'Devenir volontaire', 'url': '#'},
            {'label': 'Rejoindre UCIV Leadership', 'url': URL_LEADERSHIP},
            {'label': 'Proposer mes compétences', 'url': '#'},
        ],
    },
    {'label': 'Opportunités', 'url': '#', 'enfants': []},
    {'label': 'Notre impact', 'url': '#', 'enfants': []},
    {'label': 'Actualités', 'url': '#', 'enfants': []},
]

PIED_COLONNES = [
    {
        'titre': "S'engager",
        'liens': [
            {'label': "Je veux m'engager", 'url': '#'},
            {'label': 'Devenir volontaire', 'url': '#'},
            {'label': 'Proposer mes compétences', 'url': '#'},
            {'label': 'Opportunités', 'url': '#'},
        ],
    },
    {
        'titre': 'Nos programmes',
        'liens': [
            {'label': 'Les Go du Digital', 'url': '#'},
            {'label': 'UCIV Leadership', 'url': URL_LEADERSHIP},
            {'label': 'Experience Lab', 'url': '#'},
        ],
    },
    {
        'titre': 'Nous connaître',
        'liens': [
            {'label': 'Qui sommes-nous ?', 'url': URL_QUI},
            {'label': 'Notre impact', 'url': '#'},
            {'label': 'Nos partenaires', 'url': '#'},
            {'label': 'Actualités', 'url': '#'},
            {'label': 'Ressources', 'url': '#'},
            {'label': 'Contact', 'url': '#'},
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

MENTIONS = [
    {'label': 'Mentions légales', 'url': '#'},
    {'label': 'Politique de confidentialité', 'url': '#'},
    {'label': "Conditions d'utilisation", 'url': '#'},
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
        'url': '#',
        'image': 'app/assets/img/go-du-digital.jpg',
        'image_alt': "Une jeune femme se filme avec son téléphone pendant un atelier.",
        'detouree': False,
    },
    {
        'theme': 'jaune',
        'titre': 'UCIV Leadership',
        'etiquette': 'Réseau sélectif · 30 à 50 membres',
        'texte': "Formations par des spécialistes, mentorat, conférences et un réseau "
                 "d'opportunités partagées entre membres.",
        'lien_label': 'Rejoindre UCIV Leadership',
        'url': URL_LEADERSHIP,
        'image': 'app/assets/img/groupe-nb.png',
        'image_alt': 'Quatre jeunes leaders souriants, en tenue professionnelle.',
        'detouree': True,
    },
    {
        'theme': 'creme',
        'titre': 'Experience Lab',
        'etiquette': 'Personal branding · Pitch',
        'texte': "Un espace pour mieux se connaître avant de chercher à se présenter. "
                 "« Know yourself before showing yourself. »",
        'lien_label': 'Découvrir Experience Lab',
        'url': '#',
        'image': 'app/assets/img/experience-lab.jpg',
        'image_alt': 'Un jeune homme présente son parcours devant un petit groupe.',
        'detouree': False,
    },
]

# Les chiffres réels ne sont pas encore fournis par UCIV : `valeur` reste à None
# et le gabarit affiche « à venir » à la place.
INDICATEURS = [
    {'valeur': None, 'label': 'Jeunes mobilisés'},
    {'valeur': None, 'label': 'Volontaires'},
    {'valeur': None, 'label': 'Programmes réalisés'},
    {'valeur': None, 'label': 'Participants formés'},
    {'valeur': None, 'label': 'Partenaires'},
    {'valeur': None, 'label': 'Projets réalisés'},
]

FACONS_DE_S_ENGAGER = [
    {
        'couleur': 'orange',
        'titre': 'Devenir volontaire',
        'texte': "Participe aux activités et aux projets d'UCIV, sur le terrain.",
        'url': '#',
    },
    {
        'couleur': 'jaune',
        'titre': 'Rejoindre UCIV Leadership',
        'texte': 'Intègre un réseau sélectif de jeunes leaders et futurs leaders.',
        'url': '#',
    },
    {
        'couleur': 'vert',
        'titre': 'Proposer mes compétences',
        'texte': 'Communication, graphisme, audiovisuel, formation, numérique…',
        'url': '#',
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
    'image': 'app/assets/img/partenariat-paipro.jpg',
    'image_alt': "Poignée de main lors de la signature entre UCIV et PAIPRO-JEUNES.",
    'position': 'center 22%',
    'url': '#',
}

AUTRES_ARTICLES = [
    {
        'categorie': 'Leadership',
        'theme': 'jaune',
        'meta': 'Octobre 2026',
        'titre': 'UCIV Leadership : la conférence de lancement au format TEDx',
        'image': 'app/assets/img/affiche-leadership-jaune.jpg',
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
        'image': 'app/assets/img/rencontre-galerie.jpg',
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
        'image': 'app/assets/img/groupe-nb.png',
        'image_alt': 'Quatre jeunes souriants, en tenue professionnelle.',
        'position': 'center top',
        'detouree': True,
        'url': '#',
    },
]

PARTENAIRES = [
    {'nom': 'BonixUp', 'apport': 'Formation'},
    {'nom': 'PAIPRO-JEUNES', 'apport': 'Insertion professionnelle'},
    {'nom': 'ONG Light for All CI', 'apport': 'Logistique de terrain'},
]


# --- Page UCIV Leadership ---------------------------------------------------

LEADERSHIP = {
    'chapo': "UCIV Leadership est le réseau des leaders et futurs leaders d'Une Côte "
             "d'Ivoire Volontaire : un cadre où des jeunes triés sur le volet se "
             "forment, se connectent et passent à l'action ensemble.",
    'reperes': [
        {'label': 'Cohorte pionnière', 'valeur': '30 à 50 membres'},
        {'label': 'Sélection', 'valeur': 'Pitch vidéo, puis entretien collectif'},
        {'label': 'Lancement', 'valeur': 'Octobre 2026 · American Corner'},
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
    'theme': "« S'engager aujourd'hui",
    'theme_suite': 'pour transformer demain. »',
    'lancement_infos': ['Octobre 2026', 'American Corner', 'Date et heure à confirmer'],
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
