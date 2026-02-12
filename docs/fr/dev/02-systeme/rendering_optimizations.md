# Optimisations du rendu

Cette page decrit l'etat actuel des optimisations cote rendu.

## Etat actuel

- Le rendu utilise `pygame` directement.
- Les sprites sont caches via [src/managers/sprite_manager.py](https://github.com/ethann59/Galad-Scott/blob/main/src/managers/sprite_manager.py).
- Les surfaces scalees sont mises en cache via [src/managers/surface_cache.py](https://github.com/ethann59/Galad-Scott/blob/main/src/managers/surface_cache.py).

## Bonnes pratiques

- Precharger les sprites critiques au demarrage.
- Eviter les resizes d'images a chaque frame.
- Utiliser des surfaces deja scalees et reutilisables.
