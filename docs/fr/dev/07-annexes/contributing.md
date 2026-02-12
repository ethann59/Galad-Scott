---
i18n:
  en: "Contribution Guide"
  fr: "Guide de contribution"
---

# Guide de contribution

## Workflow

1. Creer une branche depuis `main`.
2. Appliquer des commits courts et descriptifs.
3. Ouvrir une PR vers `main`.

## Conventions de commit

Utiliser Conventional Commits : https://www.conventionalcommits.org/

Exemples :

- `feat(rail): add new enemy wave`
- `fix(score): clamp name length`
- `docs(dev): update systems overview`

## Tests

```bash
python -m pytest tests/
```