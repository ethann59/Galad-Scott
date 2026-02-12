---
i18n:
  en: "Sprite Manager"
  fr: "Sprite Manager"
---

# Sprite Manager

Le Sprite Manager centralise les sprites via des IDs, gere le chargement, le cache et la creation de `SpriteComponent`.

## Fichiers cles

- [src/managers/sprite_manager.py](https://github.com/ethann59/Galad-Scott/blob/main/src/managers/sprite_manager.py)
- [src/utils/sprite_utils.py](https://github.com/ethann59/Galad-Scott/blob/main/src/utils/sprite_utils.py)
- [src/initialization/sprite_init.py](https://github.com/ethann59/Galad-Scott/blob/main/src/initialization/sprite_init.py)

## API principale

- `SpriteID` : enum des sprites disponibles.
- `SpriteManager.load_sprite(sprite_id)` : charge et met en cache.
- `SpriteManager.create_sprite_component(sprite_id, width, height)` : cree un `SpriteComponent` pret a l'emploi.
- `SpriteManager.preload_sprites([...])` : precharge.
- `SpriteManager.get_scaled_sprite(sprite_id, size)` : surface scalee en cache.

Exemple :

```python
from src.managers.sprite_manager import sprite_manager, SpriteID

sprite = sprite_manager.create_sprite_component(SpriteID.ALLY_SCOUT, 64, 80)
```

## Helpers

Le module [src/utils/sprite_utils.py](https://github.com/ethann59/Galad-Scott/blob/main/src/utils/sprite_utils.py) fournit des helpers pour creer des sprites d'unites, projectiles, evenements ou batiments.

## SpriteSystem (legacy)

Un utilitaire existe pour les composants basees sur `image_path` :

- [src/systems/sprite_system.py](https://github.com/ethann59/Galad-Scott/blob/main/src/systems/sprite_system.py)

Il charge et scale une image a partir du chemin stocke dans `SpriteComponent`. Le `SpriteManager` reste la voie principale pour les nouveaux sprites.