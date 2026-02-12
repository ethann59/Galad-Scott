---
i18n:
  en: "Tower System Implementation"
  fr: "Implementation du systeme de tours"
---

# Implementation du systeme de tours

Ce systeme n'est pas encore implemente dans le code actuel. La page est conservee pour une implementation future.

## Composants

- [src/components/core/towerComponent.py](https://github.com/ethann59/Galad-Scott/blob/main/src/components/core/towerComponent.py)
- [src/components/core/defenseTowerComponent.py](https://github.com/ethann59/Galad-Scott/blob/main/src/components/core/defenseTowerComponent.py)
- [src/components/core/healTowerComponent.py](https://github.com/ethann59/Galad-Scott/blob/main/src/components/core/healTowerComponent.py)

`TowerComponent` est la source de verite pour :

- `tower_type` (`DEFENSE` ou `HEAL`)
- `range`, `attack_speed`
- `damage` ou `heal_amount`
- cooldown interne

## Factory

Les tours sont creees via :

- `create_defense_tower`
- `create_heal_tower`

Fichier : [src/factory/buildingFactory.py](https://github.com/ethann59/Galad-Scott/blob/main/src/factory/buildingFactory.py)

Les sprites sont choisis par equipe via `SpriteID.ALLY_DEFENCE_TOWER` / `SpriteID.ENEMY_DEFENCE_TOWER` et `SpriteID.ALLY_HEAL_TOWER` / `SpriteID.ENEMY_HEAL_TOWER`.

## Processeur

Le comportement est gere par `TowerProcessor` :

- Mise a jour du cooldown interne
- Choix d'une cible selon l'equipe et le type de tour
- Creation de projectiles pour les tours de defense
- Application de soins pour les tours de soin

Fichier : [src/processeurs/towerProcessor.py](https://github.com/ethann59/Galad-Scott/blob/main/src/processeurs/towerProcessor.py)