---
i18n:
  en: "Maintenance"
  fr: "Maintenance"
---

# Maintenance

## Nettoyage

```bash
find . -name "__pycache__" -type d -exec rm -rf {} +
find . -name "*.pyc" -delete
```

## Tests

```bash
python -m pytest tests/
```

## Configuration

Sauvegarde de `galad_config.json` :

```bash
cp galad_config.json galad_config_backup.json
```