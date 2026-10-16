import re

from django import template
from django.utils.html import format_html, format_html_join
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def corps_article(texte):
    """Met en forme le texte d'un article (échappé, sans HTML libre).

    Blocs séparés par une ligne vide :
    « !! » chapô, « ## » sous-titre, « > » citation (la ligne « — Nom » suivante est la signature),
    lignes « - » liste de points, sinon paragraphe.
    """
    html = []
    for bloc in re.split(r'\n\s*\n', (texte or '').strip()):
        lignes = [ligne.strip() for ligne in bloc.splitlines() if ligne.strip()]
        if not lignes:
            continue
        premiere = lignes[0]
        if premiere.startswith('!! '):
            html.append(format_html('<p class="art-chapo">{}</p>', premiere[3:]))
        elif premiere.startswith('## '):
            html.append(format_html('<h2>{}</h2>', premiere[3:]))
        elif premiere.startswith('>'):
            citation = ' '.join(ligne.lstrip('> ').strip() for ligne in lignes if ligne.startswith('>'))
            signature = next((ligne for ligne in lignes if ligne.startswith('—')), '')
            html.append(format_html(
                '<blockquote class="art-citation"><p>{}</p>{}</blockquote>', citation,
                format_html('<cite>{}</cite>', signature) if signature else '',
            ))
        elif premiere.startswith('- '):
            points = format_html_join('', '<li>{}</li>', ((ligne[2:],) for ligne in lignes if ligne.startswith('- ')))
            html.append(format_html('<ul class="art-points">{}</ul>', points))
        else:
            html.append(format_html('<p>{}</p>', ' '.join(lignes)))
    return mark_safe('\n'.join(html))
