---
i18n:
  en: "Managers"
  fr: "Gestionnaires (Managers)"
---

# Gestionnaires (Managers)

Les gestionnaires encapsulent des services transverses (affichage, audio, cache, sprites). Ils sont utilises par le menu et les modes de jeu.

## Liste principale

| Gestionnaire | Role | Fichier |
| --- | --- | --- |
| `DisplayManager` | Fenetrage, fullscreen, resolution | [src/managers/display.py](https://github.com/ethann59/Galad-Scott/blob/main/src/managers/display.py) |
| `LayoutManager` | Layout UI adaptatif | [src/managers/display.py](https://github.com/ethann59/Galad-Scott/blob/main/src/managers/display.py) |
| `AudioManager` | Musiques et effets sonores | [src/managers/audio.py](https://github.com/ethann59/Galad-Scott/blob/main/src/managers/audio.py) |
| `VolumeWatcher` | Suivi des volumes (config) | [src/managers/audio.py](https://github.com/ethann59/Galad-Scott/blob/main/src/managers/audio.py) |
| `GamepadManager` | Detection et input manette | [src/managers/gamepad_manager.py](https://github.com/ethann59/Galad-Scott/blob/main/src/managers/gamepad_manager.py) |
| `SpriteManager` | Registre + cache d'images | [src/managers/sprite_manager.py](https://github.com/ethann59/Galad-Scott/blob/main/src/managers/sprite_manager.py) |
| `SurfaceCache` | Cache de surfaces et textures | [src/managers/surface_cache.py](https://github.com/ethann59/Galad-Scott/blob/main/src/managers/surface_cache.py) |
| `FontCache` | Cache de polices | [src/managers/font_cache.py](https://github.com/ethann59/Galad-Scott/blob/main/src/managers/font_cache.py) |
| `IslandResourceManager` | Gestion ressources d'iles | [src/managers/island_resource_manager.py](https://github.com/ethann59/Galad-Scott/blob/main/src/managers/island_resource_manager.py) |
| `TutorialManager` | Astuces et tutoriels | [src/managers/tutorial_manager.py](https://github.com/ethann59/Galad-Scott/blob/main/src/managers/tutorial_manager.py) |

## Usage type

- Le menu utilise `DisplayManager`, `AudioManager`, `GamepadManager`.
- Le jeu utilise `SpriteManager` pour charger et mettre en cache les images.
- `SurfaceCache` fournit des surfaces scalees et des overlays pour le rendu.

## Bonnes pratiques

- Eviter la logique metier dans les gestionnaires (mettre dans les processeurs).
- Preferer des interfaces simples et stables (API courte).
- Documenter les dependances (ex: config, Pygame init).