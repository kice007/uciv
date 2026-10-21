"""Stockage des fichiers statiques avec empreinte dans l'adresse.

Nginx garde les fichiers statiques 30 jours dans le navigateur. Comme `main.css` garde le même nom après chaque mise en
ligne, un visiteur déjà venu recevait le nouveau HTML avec l'ancien CSS (formes absentes, style incomplet). Chaque adresse
statique reçoit donc `?v=<empreinte du contenu>` : elle change dès que le fichier change, et le navigateur recharge.
"""
import hashlib
import os

from django.contrib.staticfiles import finders
from django.contrib.staticfiles.storage import StaticFilesStorage


class StatiqueAvecEmpreinte(StaticFilesStorage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._empreintes = {}   # chemin -> (mtime, taille, empreinte)

    def _chemin_source(self, nom):
        copie = self.path(nom)
        return copie if os.path.exists(copie) else finders.find(nom)

    def _empreinte(self, nom):
        chemin = self._chemin_source(nom)
        if not chemin or not os.path.isfile(chemin):
            return ''
        info = os.stat(chemin)
        connue = self._empreintes.get(chemin)
        if connue and connue[:2] == (info.st_mtime_ns, info.st_size):
            return connue[2]
        with open(chemin, 'rb') as fichier:
            empreinte = hashlib.md5(fichier.read(), usedforsecurity=False).hexdigest()[:10]
        self._empreintes[chemin] = (info.st_mtime_ns, info.st_size, empreinte)
        return empreinte

    def url(self, name):
        adresse = super().url(name)
        empreinte = self._empreinte(name) if name else ''
        return f'{adresse}?v={empreinte}' if empreinte else adresse
