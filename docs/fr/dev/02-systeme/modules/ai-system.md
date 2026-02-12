---
i18n:
  en: "AI System"
  fr: "Systeme IA"
---

# Systeme IA

Le code actuel ne contient pas de systeme IA centralise. Les comportements automatiques sont principalement portes par des processeurs d'evenements et des composants specifiques aux unites.

## Etat actuel

- Comportements d'evenements dans [src/processeurs/events](https://github.com/ethann59/Galad-Scott/tree/main/src/processeurs/events).
- L'activation IA est gerable au niveau des unites via la factory (voir [src/factory/unitFactory.py](https://github.com/ethann59/Galad-Scott/blob/main/src/factory/unitFactory.py)).

## Recommandations

- Centraliser la logique IA dans un processeur dedie si besoin.
- Garder les decisions et le mouvement separes pour faciliter les tests.