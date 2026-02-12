---
i18n:
  en: "Components"
  fr: "Composants ECS"
---

# Composants ECS

Les composants sont des structures de donnees simples. Ils ne contiennent pas de logique metier. Toute la logique est dans les processeurs.

## Organisation

```
src/components/
├── core/        # Donnees de base (position, sante, sprite, etc.)
├── special/     # Capacites speciales (Spe*)
├── events/      # Composants d'evenements (tempete, kraken, etc.)
├── globals/     # Camera, carte
└── properties/  # Composants utilitaires transverses
```

## Composants core (exemples)

| Composant | Role | Fichier |
| --- | --- | --- |
| `PositionComponent` | Position et direction | [src/components/core/positionComponent.py](https://github.com/ethann59/Galad-Scott/blob/main/src/components/core/positionComponent.py) |
| `VelocityComponent` | Vitesse et modificateurs | [src/components/core/velocityComponent.py](https://github.com/ethann59/Galad-Scott/blob/main/src/components/core/velocityComponent.py) |
| `HealthComponent` | Points de vie | [src/components/core/healthComponent.py](https://github.com/ethann59/Galad-Scott/blob/main/src/components/core/healthComponent.py) |
| `TeamComponent` | Equipe (allié/ennemi) | [src/components/core/teamComponent.py](https://github.com/ethann59/Galad-Scott/blob/main/src/components/core/teamComponent.py) |
| `SpriteComponent` | Donnees de rendu | [src/components/core/spriteComponent.py](https://github.com/ethann59/Galad-Scott/blob/main/src/components/core/spriteComponent.py) |
| `RadiusComponent` | Portee de tir + cooldowns | [src/components/core/radiusComponent.py](https://github.com/ethann59/Galad-Scott/blob/main/src/components/core/radiusComponent.py) |
| `AttackComponent` | Degats de base | [src/components/core/attackComponent.py](https://github.com/ethann59/Galad-Scott/blob/main/src/components/core/attackComponent.py) |
| `CanCollideComponent` | Marqueur de collision | [src/components/core/canCollideComponent.py](https://github.com/ethann59/Galad-Scott/blob/main/src/components/core/canCollideComponent.py) |
| `VisionComponent` | Portee de vision | [src/components/core/visionComponent.py](https://github.com/ethann59/Galad-Scott/blob/main/src/components/core/visionComponent.py) |

Exemple minimal :

```python
from dataclasses import dataclass as component

@component
class PositionComponent:
    def __init__(self, x=0.0, y=0.0, direction=0.0):
        self.x = x
        self.y = y
        self.direction = direction
```

## Composants special

Les capacites speciales sont portees par des composants `Spe*` :

- `SpeScout`, `SpeMaraudeur`, `SpeLeviathan`, `SpeDruid`, `SpeArchitect`, `SpeKamikazeComponent`
- Effets associes : `isVinedComponent`, `VineComponent`

Voir [Système de capacités spéciales](special-capacity-system.md).

## Composants events

Utilises pour les evenements du jeu (tempetes, coffres, kraken, bandits) :

- `stormComponent`, `flyChestComponent`, `krakenComponent`, `krakenTentacleComponent`, `banditsComponent`

## Composants globals

Composants de contexte global :

- `cameraComponent` : camera et conversion monde/ecran
- `mapComponent` : structure de carte et rendu associe

## Bonnes pratiques

- Garder les composants simples: donnees uniquement.
- Eviter la logique et les effets de bord dans les composants.
- Preferer des noms precis plutot que generiques.