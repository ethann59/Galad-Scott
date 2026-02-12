---
i18n:
  en: "Debug / Developer Mode"
  fr: "Mode debug"
---

# Mode debug

Le mode debug est controle par `dev_mode` dans `galad_config.json`. Il est utilise principalement pour activer des logs plus verbeux.

## Activation

```json
{
  "dev_mode": true
}
```

## Effets

- Niveau de logging plus verbeux au demarrage (voir [main.py](https://github.com/ethann59/Galad-Scott/blob/main/main.py)).
- Certains processeurs loguent des informations de debug si necessaire.