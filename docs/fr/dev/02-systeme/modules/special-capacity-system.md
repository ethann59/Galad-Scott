---
i18n:
  en: "Special Ability System"
  fr: "Systeme de capacites speciales"
---

# Systeme de capacites speciales

Les capacites speciales sont modelisees par des composants `Spe*` et mises a jour par `CapacitiesSpecialesProcessor`.

## Composants

Fichiers dans [src/components/special](https://github.com/ethann59/Galad-Scott/tree/main/src/components/special) :

- `SpeScout` : invincibilite temporaire
- `SpeMaraudeur` : reduction de degats
- `SpeLeviathan` : seconde salve
- `SpeDruid` : lierre immobilisant
- `SpeArchitect` : boost de rechargement en zone
- `SpeKamikazeComponent` : boost de vitesse
- `isVinedComponent` + `VineComponent` : effet lierre

## Mise a jour

Le processeur [src/processeurs/CapacitiesSpecialesProcessor.py](https://github.com/ethann59/Galad-Scott/blob/main/src/processeurs/CapacitiesSpecialesProcessor.py) :

- Appelle `update(dt)` sur chaque composant `Spe*`.
- Met a jour les effets (ex: lierre via `VineProcessor`).
- Applique les reductions de cooldown via `SpeArchitect` sur les `RadiusComponent`.

## Integration

- Les unites sont creees dans [src/factory/unitFactory.py](https://github.com/ethann59/Galad-Scott/blob/main/src/factory/unitFactory.py).
- Les capacites speciales sont ajoutees au moment de la creation d'entites.

## Bonnes pratiques

- Garder l'API des `Spe*` coherente (`update`, timers, flags d'etat).
- Concentrer la logique dans les processeurs plutot que dans les composants.