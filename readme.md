# Galad Scott

Un jeu de rail shooter d'arcade développé avec PyGame, inspiré de l'univers de Galad Islands. Optimisé pour bornes d'arcade avec des contrôles simples et une interface adaptée.

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/ethann59/Galad-Scott)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## Description

Galad Scott est un rail shooter d'arcade où les joueurs contrôlent un vaisseau et affrontent des vagues d'ennemis. Le jeu propose :

- **Gameplay Arcade** : Action rapide avec contrôles simples (clavier/manette)
- **Système de Score** : Tableau des scores avec saisie de nom style arcade
- **Interface Adaptée** : Menus simplifiés pour utilisation en borne d'arcade
- **Ennemis Variés** : Scouts, Maraudeurs et Kamikazes avec comportements distincts
- **Progression Équilibrée** : Difficulté croissante basée sur le score
- **Gestion d'Erreur** : Écrans d'erreur style arcade avec fermeture automatique

## Installation

### Installation Rapide

Clonez le dépôt et installez les dépendances :

```bash
git clone https://github.com/ethann59/Galad-Scott.git
cd Galad-Scott
pip install -r requirements.txt
```

### Environnement Virtuel (Recommandé)

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate.bat  # Windows
pip install -r requirements.txt
```

## Comment Jouer

Pour lancer le jeu :

```bash
python main.py
```

### Contrôles Borne d'Arcade

**Déplacement (Joystick) :**
- `↑` : Monter
- `↓` : Descendre  
- `←` : Aller à gauche
- `→` : Aller à droite

**Boutons :**
- `R` (bouton haut 1) : Tirer / Valider dans les menus
- `F` (bouton bas 1) : Retour dans les menus
- Boutons disponibles : F/G/H (bas) et R/T/Y (haut)

**Menu :**
- `↑↓` : Naviguer dans les menus
- `R` : Valider
- `F` : Retour
- `ÉCHAP` : Quitter (développement)

## Dépendances

### Dépendances Principales

- **[pygame](https://www.pygame.org/)** - Framework de jeu
- **[esper](https://esper.readthedocs.io/)** - Système Entity-Component-System
- **[Pillow](https://python-pillow.org/)** - Traitement d'images pour les sprites
- **[tomli](https://tomli.readthedocs.io/)** - Configuration TOML
- **[packaging](https://packaging.pypa.io/)** - Comparaison de versions

## Fonctionnalités

### Gameplay

- **Rail Shooter Classique** : Déplacement libre du vaisseau sur l'écran
- **Système de Tir** : Cadence de tir optimisée pour l'arcade
- **Ennemis Variés** :
  - **Scouts** : Rapides et agiles, zigzaguent
  - **Maraudeurs** : Tirent en rafales, résistants
  - **Kamikazes** : Chargent vers le joueur, oneshot mais dangereux
- **Progression Équilibrée** : Les ennemis apparaissent progressivement selon le score
- **Système de Score** : Chaque ennemi rapporte 10 points

### Interface Arcade

- **Navigation Clavier** : Tous les menus navigables au clavier/manette
- **Saisie de Nom Style Arcade** : Interface dédiée pour les high scores
- **Options Simplifiées** : Volume musique/effets, langue
- **Gestion d'Erreur Robuste** : Écrans d'erreur style borne avec auto-fermeture

## Configuration

Le jeu utilise `galad_config.json` pour la configuration :

```json
{
  "check_updates": true,
  "dev_mode": false,
  "language": "fr",
  "fullscreen": false,
  "resolution": "1920x1080",
  "music_volume": 0.4,
  "effects_volume": 0.56
}
```

## Développement

### Lancement des Tests

```bash
# Lancer tous les tests
python run_tests.py

# Tests avec couverture
pytest --cov=src --cov-report=html

# Tests spécifiques 
pytest tests/test_rail_shooter.py
```

### Structure du Projet (Simplifiée)

```text
Galad-Scott/
├── assets/                    # Ressources du jeu (sprites, sons, musique, fonts)
├── src/                       # Code source
│   ├── components/            # Composants ECS
│   │   └── core/             # Composants principaux (position, health, etc.)
│   ├── constants/             # Constantes du jeu
│   ├── functions/             # Fonctions utilitaires
│   │   └── arcade_menus.py   # Menus simplifiés pour arcade
│   ├── managers/              # Gestionnaires (audio, display, etc.)
│   ├── processeurs/           # Processeurs ECS (systèmes)
│   ├── settings/              # Configuration et paramètres
│   ├── ui/                    # Interface utilisateur
│   │   └── arcade_error.py   # Système d'erreur arcade
│   └── utils/                 # Modules utilitaires
├── main.py                    # Point d'entrée du jeu
├── rail_shooter.py            # Moteur principal du rail shooter
└── requirements.txt           # Dépendances de production
```

## Auteurs

### Galad Scott
- **Cailliau Ethann** - Développement et adaptation arcade

### Basé sur Galad Islands
Projet original créé par :
- **Alluin Edouard** - <edouard.alluin@etu.univ-littoral.fr>
- **Behani Julien** - <julien.behani@etu.univ-littoral.fr>
- **Cailliau Ethann** - <ethann.cailliau@etu.univ-littoral.fr>
- **Damman Alexandre** - <alexandre.damman@etu.univ-littoral.fr>
- **Fournier Enzo** - <enzo.fournier000@etu.univ-littoral.fr>
- **Lambert Romain** - <romain.lambert@etu.univ-littoral.fr>

## License

Ce projet est sous licence MIT - voir le fichier LICENSE pour plus de détails.

## Remerciements

Construit avec PyGame et le framework ECS Esper. Remerciements spéciaux à l'équipe originale de Galad Islands et à la communauté open-source.

### Adaptation Arcade

Galad Scott est une version simplifiée et optimisée pour borne d'arcade du projet original Galad Islands. Les fonctionnalités RTS complexes ont été remplacées par un gameplay rail shooter accessible.
