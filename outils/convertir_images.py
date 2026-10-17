"""Convertit les images sources en WebP léger pour le site, et fabrique les images de partage (Open Graph).

Usage, depuis la racine du dépôt (nécessite Pillow) :
    python outils/convertir_images.py

- Sources (originaux, non servis au public) : sources/images/
- Sortie WebP : src/static/app/assets/img/ (même nom, extension .webp)
- Images de partage : src/static/app/assets/img/og-*.jpg (1200 x 630, JPEG : lisible par tous les réseaux sociaux)

Pour ajouter une image : déposez l'original dans sources/images/ et relancez le script. La qualité baisse
par paliers, puis l'image est réduite, jusqu'à passer sous le poids cible.
"""
from pathlib import Path

from PIL import Image

RACINE = Path(__file__).resolve().parent.parent
SOURCES = RACINE / 'sources' / 'images'
CIBLE = RACINE / 'src' / 'static' / 'app' / 'assets' / 'img'

LARGEUR_MAX = 1400        # px : les plus grandes images du site s'affichent à moins de 820 px (x2 pour les écrans denses : 1400 px suffisent)
POIDS_CIBLE_KO = 200
QUALITES = (82, 78, 74, 70, 65, 60, 55)

# Réglages particuliers : (largeur maximale, poids cible en Ko)
EXCEPTIONS = {
    'logo-uciv-leadership.png': (900, 60),   # affiché à 300 px de large au maximum
}

# Images de partage : nom -> (source, centrage vertical de la découpe 0 = haut, 1 = bas, fond uni éventuel)
PARTAGE = {
    'og-defaut.jpg': ('groupe-couleur.png', None, '#E17F1C'),
    'og-leadership.jpg': ('affiche-leadership-jaune.jpg', 0.45, None),
    'og-experience-lab.jpg': ('experience-lab.jpg', 0.5, None),
    'og-engagement.jpg': ('volontaires-terrain.jpg', 0.35, None),
    'og-partenaires.jpg': ('partenariat-paipro.jpg', 0.4, None),
}
LARGEUR_OG, HAUTEUR_OG = 1200, 630


def ko(chemin):
    return chemin.stat().st_size / 1024


def convertir(source):
    largeur_max, cible_ko = EXCEPTIONS.get(source.name, (LARGEUR_MAX, POIDS_CIBLE_KO))
    image = Image.open(source)
    image.load()
    if image.mode not in ('RGB', 'RGBA'):
        image = image.convert('RGBA' if 'A' in image.getbands() or 'transparency' in image.info else 'RGB')
    if image.width > largeur_max:
        image = image.resize((largeur_max, round(image.height * largeur_max / image.width)), Image.LANCZOS)
    sortie = CIBLE / (source.stem + '.webp')
    while True:
        for qualite in QUALITES:
            image.save(sortie, 'WEBP', quality=qualite, method=6)
            if ko(sortie) <= cible_ko:
                return sortie, image.size, qualite
        image = image.resize((round(image.width * .9), round(image.height * .9)), Image.LANCZOS)


def fabriquer_partage(nom, source, centrage, fond):
    image = Image.open(SOURCES / source)
    image.load()
    if fond:                                   # photo détourée : posée en bas sur un fond de la couleur du site
        toile = Image.new('RGB', (LARGEUR_OG, HAUTEUR_OG), fond)
        image = image.convert('RGBA')
        hauteur = HAUTEUR_OG - 30
        image = image.resize((round(image.width * hauteur / image.height), hauteur), Image.LANCZOS)
        toile.paste(image, ((LARGEUR_OG - image.width) // 2, HAUTEUR_OG - hauteur), image)
    else:                                      # photo : découpe 1200 x 630
        image = image.convert('RGB')
        hauteur_decoupe = round(image.width * HAUTEUR_OG / LARGEUR_OG)
        if hauteur_decoupe > image.height:     # image trop large : on découpe sur la largeur
            largeur_decoupe = round(image.height * LARGEUR_OG / HAUTEUR_OG)
            x = (image.width - largeur_decoupe) // 2
            zone = (x, 0, x + largeur_decoupe, image.height)
        else:
            y = round((image.height - hauteur_decoupe) * centrage)
            zone = (0, y, image.width, y + hauteur_decoupe)
        toile = image.crop(zone).resize((LARGEUR_OG, HAUTEUR_OG), Image.LANCZOS)
    sortie = CIBLE / nom
    for qualite in (85, 80, 75, 70, 65, 60):
        toile.save(sortie, 'JPEG', quality=qualite, optimize=True, progressive=True)
        if ko(sortie) <= 150:
            break
    return sortie


def main():
    print(f"{'image':34} {'avant':>9} {'après':>9}  dimensions    qualité")
    for source in sorted(SOURCES.iterdir()):
        if source.suffix.lower() not in ('.jpg', '.jpeg', '.png'):
            continue
        sortie, taille, qualite = convertir(source)
        print(f'{source.name:34} {ko(source):7.0f} Ko {ko(sortie):7.0f} Ko  {taille[0]}x{taille[1]:<6} q={qualite}')
    print()
    for nom, (source, centrage, fond) in PARTAGE.items():
        sortie = fabriquer_partage(nom, source, centrage, fond)
        print(f'{nom:34} {"":9} {ko(sortie):7.0f} Ko  {LARGEUR_OG}x{HAUTEUR_OG}')


if __name__ == '__main__':
    main()
