---
i18n:
  en: "Project Configuration"
  fr: "Configuration du projet"
---

# Configuration du projet

Le jeu utilise `galad_config.json` pour stocker les preferences utilisateur. Le fichier est gere par [src/settings/settings.py](https://github.com/ethann59/Galad-Scott/blob/main/src/settings/settings.py).

Galad Scott limite l'utilisateur au minimum de configurations pour simplifier l'experience. Les options disponibles sont :
- volume sonore (master, musique, effets)

## Exemple de configuration

```json
{
  "screen_width": 1280,
  "screen_height": 1024,
  "window_mode": "fullscreen",
  "volume_master": 0.8,
  "volume_music": 0.5,
  "volume_effects": 0.7,
  "vsync": true,
  "performance_mode": "high",
  "max_fps": 75,
  "show_fps": false,
  "dev_mode": false,
  "language": "fr",
  "key_bindings": {
    "unit_move_forward": ["up"],
    "unit_move_backward": ["down"],
    "unit_turn_left": ["left"],
    "unit_turn_right": ["right"],
    "unit_shoot": ["f"]
  }
}
```

## Acces via ConfigManager

```python
from src.settings.settings import config_manager

width, height = config_manager.get_resolution()
config_manager.set("volume_music", 0.6)
config_manager.save_config()
```