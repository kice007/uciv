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
    return reverse('app:engagement') + (f'?choix={choix}' if choix else '')


URL_ENGAGEMENT = lazy(_engagement, str)()
URL_VOLONTAIRE = lazy(_engagement, str)('volontaire')
URL_COMPETENCES = lazy(_engagement, str)('competences')

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
        'url': URL_ENGAGEMENT,
        'enfants': [
            {'label': 'Devenir volontaire', 'url': URL_VOLONTAIRE},
            {'label': 'Rejoindre UCIV Leadership', 'url': URL_LEADERSHIP},
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
            {'label': 'Experience Lab', 'url': URL_EXPERIENCE},
        ],
    },
    {
        'titre': 'Nous connaître',
        'liens': [
            {'label': 'Qui sommes-nous ?', 'url': URL_QUI},
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
        'url': URL_VOLONTAIRE,
    },
    {
        'couleur': 'jaune',
        'titre': 'Rejoindre UCIV Leadership',
        'texte': 'Intègre un réseau sélectif de jeunes leaders et futurs leaders.',
        'url': URL_LEADERSHIP,
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

# --- Page Équipe ------------------------------------------------------------

EQUIPE = {
    'hero_titre': 'Les femmes et les hommes',
    'hero_suite': 'derrière UCIV.',
    'hero_chapo': "UCIV est porté par une équipe de personnes engagées qui mettent "
                  "leurs compétences, leur temps et leur énergie au service de la "
                  "mission de l'organisation.",
    'president_role': "Président et fondateur d'Une Côte d'Ivoire Volontaire.",
    'president_bio': "[Courte biographie à transmettre : parcours, engagement et "
                     "vision pour la jeunesse ivoirienne.]",
    # `photo` : chemin statique du portrait, découpé dans l'affiche bureau-executif.jpg
    # comme dans la maquette (basse résolution : à remplacer par des photos HD).
    # Sans photo, la carte affiche les initiales.
    'bureau': [
        {'nom': 'Aïssata Ouattara', 'initiales': 'AO', 'couleur': 'orange',
         'role': 'Secrétaire Générale', 'photo': 'app/assets/img/bureau-aissata-ouattara.jpg'},
        {'nom': 'Dr Angèle Zang', 'initiales': 'AZ', 'couleur': 'vert',
         'role': 'Trésorière Générale', 'photo': 'app/assets/img/bureau-angele-zang.jpg'},
        {'nom': 'Roxane Atchia', 'initiales': 'RA', 'couleur': 'jaune',
         'role': 'Commissaire aux comptes', 'photo': 'app/assets/img/bureau-roxane-atchia.jpg'},
        {'nom': 'Martine Boa', 'initiales': 'MB', 'couleur': 'profond',
         'role': 'Responsable Générale des projets', 'photo': 'app/assets/img/bureau-martine-boa.jpg'},
    ],
    'medias_intro': "Les biographies, photos et domaines d'expertise de chaque "
                    "responsable seront ajoutés dès leur transmission.",
    'medias': [
        {'nom': 'Emmanuel Fieni Kouassi', 'initiales': 'EF', 'couleur': 'orange',
         'role': 'Responsable Communication & mobilisation'},
        {'nom': 'Djamira Kamagaté', 'initiales': 'DK', 'couleur': 'vert',
         'role': 'Commissaire aux comptes adjointe et créatrice de contenu'},
        {'nom': 'Mieimmo Kouassi', 'initiales': 'MK', 'couleur': 'jaune',
         'role': 'Chargée de Marketing'},
        {'nom': 'Ago Maria Konan', 'initiales': 'AM', 'couleur': 'profond',
         'role': 'Secrétaire Générale adjointe et créatrice de contenu'},
    ],
}

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
         'url': URL_LEADERSHIP},
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
         'couleur': 'orange', 'icone': 'graduation-cap'},
        {'nom': 'PAIPRO-JEUNES', 'apport': "Accompagnement vers l'emploi",
         'couleur': 'vert', 'icone': 'briefcase'},
        {'nom': 'ONG Light for All CI', 'apport': 'Logistique de terrain',
         'couleur': 'profond', 'icone': 'truck'},
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

# --- Pages alimentées par la base : Opportunités, Actualités, Notre impact, Ressources ------------
# Les formes décoratives des bandeaux sont exprimées en pixels sur la maquette de 1440 px ;
# `creux` est le « rayon intérieur » (en %) : 0 = disque plein, 72 = anneau.

_ACCUEIL = {'label': 'Accueil', 'url': URL_HOME}
_ORANGE, _JAUNE, _VERT = 'var(--orange)', 'var(--jaune)', 'var(--vert)'
_CREME, _BLANC_8 = 'var(--creme)', 'rgba(255, 255, 255, .08)'

OPPORTUNITES_PAGE = {
    'hero': {
        'fond': 'vert-profond', 'hauteur': 580, 'taille': 62, 'taille_mobile': 40, 'largeur_texte': 760, 'largeur_chapo': 560,
        'fil': [_ACCUEIL, {'label': 'Opportunités'}],
        'surtitre': 'Opportunités',
        'titre': 'Les opportunités qui peuvent', 'suite': 'faire grandir votre parcours.',
        'chapo': "Retrouvez sur cette page les opportunités proposées par UCIV et son réseau de "
                 "partenaires, mises à jour au fil de l'eau.",
        'formes': [
            {'x': 1020, 'y': 90, 'w': 520, 'c': _ORANGE, 'creux': 72},
            {'x': 1120, 'y': 190, 'w': 320, 'c': _JAUNE, 'creux': 0},
            {'x': 880, 'y': -150, 'w': 280, 'c': _BLANC_8, 'creux': 70},
        ],
        'note': {'texte': 'saisis ta chance !', 'x': 1000, 'y': 438, 'taille': 44, 'rot': -7, 'c': 'var(--blanc)'},
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
        'formes': [
            {'x': 1080, 'y': -140, 'w': 520, 'c': _JAUNE, 'creux': 78},
            {'x': 930, 'y': 250, 'w': 380, 'c': _ORANGE, 'creux': 0},
            {'x': 1210, 'y': 330, 'w': 300, 'c': _VERT, 'creux': 70},
        ],
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
        'formes': [
            {'x': 1050, 'y': -120, 'w': 540, 'c': _CREME, 'creux': 80},
            {'x': 960, 'y': 270, 'w': 330, 'c': _JAUNE, 'creux': 0},
            {'x': 1200, 'y': 300, 'w': 300, 'c': _ORANGE, 'creux': 70},
        ],
        'note': {'texte': 'des preuves, pas des promesses', 'x': 890, 'y': 406, 'taille': 38, 'rot': -5,
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
        'formes': [
            {'x': 1070, 'y': -130, 'w': 520, 'c': _CREME, 'creux': 80},
            {'x': 980, 'y': 260, 'w': 320, 'c': _JAUNE, 'creux': 0},
            {'x': 1220, 'y': 300, 'w': 300, 'c': _VERT, 'creux': 70},
        ],
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

ARTICLE_PAGE = {
    'formes': [
        {'x': 1090, 'y': -160, 'w': 520, 'c': _ORANGE, 'creux': 78},
        {'x': -160, 'y': 300, 'w': 320, 'c': _JAUNE, 'creux': 74},
    ],
}
