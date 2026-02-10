# Tests pour Galad Scott Rail Shooter

Ce dossier contient les tests unitaires et d'intégration pour Galad Scott.

## Structure des Tests

- `test_rail_shooter.py` - Tests principaux du moteur rail shooter
- `test_audio_manager.py` - Tests du gestionnaire audio
- `test_components.py` - Tests des composants ECS
- `test_display_manager.py` - Tests du gestionnaire d'affichage
- `test_localization.py` - Tests du système de traduction
- `test_performance.py` - Tests de performance
- `test_utils.py` - Tests des utilitaires
- `conftest.py` - Configuration commune des tests

## Lancement des Tests

```bash
# Tous les tests
python -m pytest tests/ -v

# Tests spécifiques
python -m pytest tests/test_rail_shooter.py -v

# Tests avec rapport de couverture
python -m pytest tests/ --cov=src --cov-report=html
```

## Tests Requis

Les tests suivants doivent passer pour valider le rail shooter :

- ✅ Importation et initialisation du moteur rail shooter
- ✅ Fonctionnement des menus arcade 
- ✅ Système d'erreur arcade
- ✅ Gestion audio de base
- ✅ Système de traduction simplifié

## Configuration

Les tests utilisent pygame en mode headless quand possible pour éviter l'ouverture de fenêtres pendant l'exécution automatisée.