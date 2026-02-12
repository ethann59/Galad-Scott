---
i18n:
  en: "Technical Overview"
  fr: "Documentation technique"
---

# Documentation technique

Galad Scott est un jeu Python base sur Pygame, avec une architecture ECS (via `esper`). Le mode principal actuel est un rail shooter.

## Demarrage rapide

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
python main.py
```

## Points d'entree

- Menu principal : [main.py](https://github.com/ethann59/Galad-Scott/blob/main/main.py)
- Moteur rail shooter : [src/rail_shooter.py](https://github.com/ethann59/Galad-Scott/blob/main/src/rail_shooter.py)

## Structure du projet

```
src/
  components/    # Composants ECS
  processeurs/   # Processeurs ECS
  managers/      # Services transverses (audio, affichage, sprites)
  factory/       # Creation d'entites
  ui/            # Composants UI
  menu/          # Etat et logique du menu
docs/            # Documentation
assets/          # Images, sons, locales
```

## Tests

```bash
python -m pytest tests/
```