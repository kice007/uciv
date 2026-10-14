# Contribuer à UCIV

Merci de suivre ces règles, que le code soit écrit à la main ou avec un agent IA.

## Branches

- `main` est toujours dans un état qui fonctionne : on n'y pousse pas directement.
- Une branche par sujet : `feature/<sujet>`, `fix/<sujet>`, `docs/<sujet>`.

## Commits

- Message en français, à l'impératif, première ligne de 72 caractères maximum :
  `Ajoute la page Qui sommes-nous`.
- Une idée par commit. Corps du message si le « pourquoi » n'est pas évident.
- Ne jamais réécrire l'historique d'une branche partagée (pas de `--force` sur `main`).

## Avant d'ouvrir une demande de fusion

1. `cd src && python manage.py check`
2. `python manage.py test app` : tous les tests passent.
3. La page concernée a été vérifiée dans le navigateur.
4. `docs/ARCHITECTURE.md` est à jour si la structure a changé.

## Relecture

- Une personne autre que l'auteur relit chaque demande de fusion.
- Le code produit par un agent IA est relu comme n'importe quel autre.
- Les changements de dépendances (`requirements.txt`) demandent l'accord de l'équipe.

## Conventions du code

Voir [ARCHITECTURE.md](docs/ARCHITECTURE.md) et [CLAUDE.md](CLAUDE.md).
