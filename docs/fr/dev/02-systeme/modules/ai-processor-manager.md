---
i18n:
  en: "AI Processor Manager"
  fr: "Gestionnaire de processeurs IA"
---

# Gestionnaire de processeurs IA

Il n'existe pas de gestionnaire dynamique de processeurs IA dans le code actuel. Les processeurs sont ajoutes explicitement lors de l'initialisation ECS.

Si un gestionnaire est reintroduit, il devra :

- Activer/desactiver les processeurs selon la presence d'entites pertinentes.
- Eviter les scans inutiles (priorites et short-circuit).