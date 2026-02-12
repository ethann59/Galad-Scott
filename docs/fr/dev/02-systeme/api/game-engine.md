---
i18n:
  en: "API - Game Engine"
  fr: "API - Moteur de jeu"
---

# API - Moteur de jeu

Le mode principal actuel est le **rail shooter**. Le moteur est encapsule dans `RailShooterEngine`.

## RailShooterEngine

Fichier : [src/rail_shooter.py](https://github.com/ethann59/Galad-Scott/blob/main/src/rail_shooter.py)

Responsabilites :

- Initialisation Pygame et ressources
- Boucle de jeu
- ECS minimal (collisions, lifetime)
- Saisie de score arcade

### Methodes principales

- `initialize()` : init Pygame, assets, ECS.
- `run()` : boucle principale.
- `_handle_events()` : input et actions.
- `_update(dt)` : logique de jeu.
- `_render()` : rendu.

## Entree application

Le menu principal est defini dans [main.py](https://github.com/ethann59/Galad-Scott/blob/main/main.py) et lance le rail shooter via `run_rail_shooter()`.