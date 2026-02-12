---
i18n:
  en: "Processors"
  fr: "Processeurs ECS"
---

# Processeurs ECS

Les processeurs contiennent la logique metier. Ils parcourent des ensembles d'entites et de composants via `esper`.

## Processeurs principaux

| Processeur | Role | Fichier |
| --- | --- | --- |
| `CollisionProcessor` | Collisions entites/terrain | [src/processeurs/collisionProcessor.py](https://github.com/ethann59/Galad-Scott/blob/main/src/processeurs/collisionProcessor.py) |
| `MovementProcessor` | Deplacement + limites de carte | [src/processeurs/movementProcessor.py](https://github.com/ethann59/Galad-Scott/blob/main/src/processeurs/movementProcessor.py) |
| `PlayerControlProcessor` | Entrees joueur + capacites | [src/processeurs/playerControlProcessor.py](https://github.com/ethann59/Galad-Scott/blob/main/src/processeurs/playerControlProcessor.py) |
| `LifetimeProcessor` | Nettoyage des entites temporaires | [src/processeurs/lifetimeProcessor.py](https://github.com/ethann59/Galad-Scott/blob/main/src/processeurs/lifetimeProcessor.py) |
| `CapacitiesSpecialesProcessor` | Timers des capacites | [src/processeurs/CapacitiesSpecialesProcessor.py](https://github.com/ethann59/Galad-Scott/blob/main/src/processeurs/CapacitiesSpecialesProcessor.py) |
| `TowerProcessor` | Logique des tours | [src/processeurs/towerProcessor.py](https://github.com/ethann59/Galad-Scott/blob/main/src/processeurs/towerProcessor.py) |

## Processeurs d'evenements

| Processeur | Role | Fichier |
| --- | --- | --- |
| `StormProcessor` | Tempetes | [src/processeurs/stormProcessor.py](https://github.com/ethann59/Galad-Scott/blob/main/src/processeurs/stormProcessor.py) |
| `FlyingChestProcessor` | Coffres volants | [src/processeurs/flyingChestProcessor.py](https://github.com/ethann59/Galad-Scott/blob/main/src/processeurs/flyingChestProcessor.py) |
| `KrakenProcessor` | Evenement Kraken | [src/processeurs/events/krakenProcessor.py](https://github.com/ethann59/Galad-Scott/blob/main/src/processeurs/events/krakenProcessor.py) |
| `BanditsProcessor` | Evenement Bandits | [src/processeurs/events/banditsProcessor.py](https://github.com/ethann59/Galad-Scott/blob/main/src/processeurs/events/banditsProcessor.py) |
| `EventProcessor` | Routage d'evenements | [src/processeurs/eventProcessor.py](https://github.com/ethann59/Galad-Scott/blob/main/src/processeurs/eventProcessor.py) |

## Autres processeurs

| Processeur | Role | Fichier |
| --- | --- | --- |
| `CombatRewardProcessor` | Recompenses de combat | [src/processeurs/combatRewardProcessor.py](https://github.com/ethann59/Galad-Scott/blob/main/src/processeurs/combatRewardProcessor.py) |
| `ExplosionSoundProcessor` | Sons d'explosion | [src/processeurs/explosionSoundProcessor.py](https://github.com/ethann59/Galad-Scott/blob/main/src/processeurs/explosionSoundProcessor.py) |
| `KnownBaseProcessor` | Registre de bases ennemies | [src/processeurs/KnownBaseProcessor.py](https://github.com/ethann59/Galad-Scott/blob/main/src/processeurs/KnownBaseProcessor.py) |
| `PassiveIncomeProcessor` | Or passif de secours | [src/processeurs/economy/passiveIncomeProcessor.py](https://github.com/ethann59/Galad-Scott/blob/main/src/processeurs/economy/passiveIncomeProcessor.py) |
| `VineProcessor` | Effet lierre | [src/processeurs/ability/VineProcessor.py](https://github.com/ethann59/Galad-Scott/blob/main/src/processeurs/ability/VineProcessor.py) |

## Integration dans la boucle

Dans `RailShooterEngine`, seuls les processeurs necessaires au mode arcade sont ajoutes (ex: collisions et lifetime). Les autres sont utilises dans les modes plus complets.