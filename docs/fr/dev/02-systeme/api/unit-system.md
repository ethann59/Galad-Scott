---
i18n:
  en: "API - Unit System"
  fr: "API - Systeme d'unites"
---

# API - Systeme d'unites

Les unites sont creees via la factory et composees de composants ECS standard.

## Creation

Fichier : [src/factory/unitFactory.py](https://github.com/ethann59/Galad-Scott/blob/main/src/factory/unitFactory.py)

Signature :

```python
def UnitFactory(unit: UnitKey, enemy: bool, pos: PositionComponent, enable_ai: bool = None, self_play_mode: bool = False, active_team_id: int = 1):
    ...
```

La factory ajoute :

- `PositionComponent`, `VelocityComponent`
- `TeamComponent`, `HealthComponent`, `AttackComponent`
- `RadiusComponent`, `CanCollideComponent`
- `VisionComponent`
- `SpriteComponent` via `SpriteManager`
- Composants `Spe*` selon l'unite

## Capacites speciales

Voir [Systeme de capacites speciales](../modules/special-capacity-system.md).

## Collisions et degats

- Les collisions sont gerees par [src/processeurs/collisionProcessor.py](https://github.com/ethann59/Galad-Scott/blob/main/src/processeurs/collisionProcessor.py).
- Les degats sont appliques par `functions.handleHealth` (handler `entities_hit`).

## Statistiques

Les stats (PV, degats, cooldowns, vision) sont definies dans [src/constants/gameplay.py](https://github.com/ethann59/Galad-Scott/blob/main/src/constants/gameplay.py).