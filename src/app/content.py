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
URL_PROGRAMMES = reverse_lazy('app:nos_programmes')
URL_GO = reverse_lazy('app:go_du_digital')
URL_EXPERIENCE = reverse_lazy('app:experience_lab')

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
        'url': URL_PROGRAMMES,
        'enfants': [
            {'label': 'Les Go du Digital', 'url': URL_GO},
            {'label': 'UCIV Leadership', 'url': URL_LEADERSHIP},
            {'label': 'Experience Lab', 'url': URL_EXPERIENCE},
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
            {'label': 'Les Go du Digital', 'url': URL_GO},
            {'label': 'UCIV Leadership', 'url': URL_LEADERSHIP},
            {'label': 'Experience Lab', 'url': URL_EXPERIENCE},
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
        'url': URL_GO,
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
        'url': URL_EXPERIENCE,
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
            'image': 'app/assets/img/go-du-digital.jpg',
            'image_alt': 'Une jeune femme se filme avec son téléphone pendant un atelier.',
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
            'url': URL_LEADERSHIP,
            'image': 'app/assets/img/groupe-nb.png',
            'image_alt': 'Quatre jeunes leaders souriants, en tenue professionnelle.',
            'detouree': True,
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
            'image': 'app/assets/img/experience-lab.jpg',
            'image_alt': 'Un jeune homme présente son parcours devant un petit groupe.',
            'detouree': False,
        },
    ],
}

# --- Page Les Go du Digital -------------------------------------------------

GO_DU_DIGITAL = {
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
}

# --- Page Experience Lab ----------------------------------------------------

EXPERIENCE_LAB = {
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
}
