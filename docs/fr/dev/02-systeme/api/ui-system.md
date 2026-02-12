---
i18n:
  en: "API - UI System"
  fr: "API - Systeme UI"
---

# API - Systeme UI

Le projet utilise des composants UI simples pour le menu principal.

## Composants

Fichier : [src/ui/ui_component.py](https://github.com/ethann59/Galad-Scott/blob/main/src/ui/ui_component.py)

### Button

- Bouton principal avec hover et feedback visuel.
- Utilise un callback passe au constructeur.

### SmallButton

- Variante compacte pour actions secondaires.

### ParticleSystem

- Particules decoratives optionnelles.

## Utilisation

Le menu principal cree les boutons et les met a jour via [main.py](https://github.com/ethann59/Galad-Scott/blob/main/main.py) et [src/menu/state.py](https://github.com/ethann59/Galad-Scott/blob/main/src/menu/state.py).