"""
Module de configuration et paramètres du jeu Galad Islands.
Centralise la gestion des paramètres utilisateur et des constantes de jeu.
"""

import json
import os
from copy import deepcopy
from typing import Any, Dict, List, Tuple
from src.version import __version__

import math


# =============================================================================
# CONFIGURATION UTILISATEUR
# =============================================================================

CONFIG_FILE = "galad_config.json"

DEFAULT_CONFIG = {
    "screen_width": 1280,
    "screen_height": 1024,
    "window_mode": "fullscreen",  # "windowed", "fullscreen" -- Par défaut en fenêtré pour le développement
    "volume_master": 0.8,
    "volume_music": 0.5,
    "volume_effects": 0.7,
    "vsync": True,
    "performance_mode": "high",  # "auto", "high", "medium", "low"
    "max_fps": 75,  # Augmenté pour une meilleure expérience
    "show_fps": False,
    "dev_mode": False,  # Mode développement pour les actions debug
    "language": "fr",
    "key_bindings": {
        "unit_move_forward": ["up"],
        "unit_move_backward": ["down"],
        "unit_turn_left": ["left"],
        "unit_turn_right": ["right"],
        "unit_shoot": ["a"],
    }
}


class ConfigManager:
    """Gestionnaire centralisé de la configuration du jeu."""
    
    def __init__(self, config_path: str = CONFIG_FILE):
        self.path = config_path
        self.config = deepcopy(DEFAULT_CONFIG)
        self.load_config()

    def load_config(self) -> None:
        """Charge la configuration from le file JSON."""
        try:
            if os.path.exists(self.path):
                with open(self.path, 'r', encoding='utf-8') as f:
                    saved_config = json.load(f)
                    # Validation et fusion avec la config By default
                    for key, value in saved_config.items():
                        if key in self.config:
                            default_value = self.config[key]
                            if isinstance(default_value, dict) and isinstance(value, dict):
                                self.config[key] = self._merge_nested_dicts(default_value, value)
                            else:
                                self.config[key] = value
                print(f"Configuration chargée depuis {self.path}")
            else:
                # Create un file de config avec les valeurs By default
                self.save_config()
                print(f"Fichier de configuration non trouvé, création de {self.path} avec les valeurs par défaut")
        except Exception as e:
            print(f"Erreur lors du chargement de la configuration: {e}")
            print("Utilisation des valeurs par défaut")

    def save_config(self) -> bool:
        """Sauvegarde la configuration in le file JSON."""
        try:
            with open(self.path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
            print(f"Configuration sauvegardée dans {self.path}")
            return True
        except Exception as e:
            print(f"Erreur lors de la sauvegarde de la configuration: {e}")
            return False

    def get(self, key: str, default: Any = None) -> Any:
        """Récupère une valeur de configuration."""
        return self.config.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Définit une valeur de configuration."""
        if key in self.config:
            self.config[key] = value
        else:
            print(f"Avertissement: Clé de configuration inconnue: {key}")

    def reset_to_defaults(self) -> None:
        """Remet la configuration aux valeurs By default."""
        self.config = deepcopy(DEFAULT_CONFIG)

    # Méthodes spécifiques pour les paramètres fréquemment utilisés
    def get_resolution(self) -> Tuple[int, int]:
        """Retourne la résolution (largeur, hauteur)."""
        return (self.config["screen_width"], self.config["screen_height"])

    def set_resolution(self, width: int, height: int) -> None:
        """Définit la résolution d'écran."""
        self.config["screen_width"] = max(200, min(10000, int(width)))
        self.config["screen_height"] = max(200, min(10000, int(height)))

    def get_volumes(self) -> Dict[str, float]:
        """Retourne les volumes audio."""
        return {
            "master": self.config["volume_master"],
            "music": self.config["volume_music"],
            "effects": self.config["volume_effects"],
        }

    def set_volume(self, volume_type: str, value: float) -> None:
        """Définit un volume audio (0.0 à 1.0)."""
        key = f"volume_{volume_type}"
        if key in self.config:
            self.config[key] = max(0.0, min(1.0, float(value)))

    def get_performance_mode(self) -> str:
        """Retourne le mode de performance actuel."""
        return str(self.config.get("performance_mode", "auto"))

    def get_key_bindings(self) -> Dict[str, List[str]]:
        """Retourne une copie des associations de touches personnalisées."""
        key_bindings = self.config.get("key_bindings", {})
        return deepcopy(key_bindings) if isinstance(key_bindings, dict) else {}

    def set_key_binding(self, action: str, bindings: List[str]) -> None:
        """Met à jour les touches associées à une action spécifique."""
        if action:
            if "key_bindings" not in self.config or not isinstance(self.config["key_bindings"], dict):
                self.config["key_bindings"] = {}
            self.config["key_bindings"][action] = list(bindings)

    def _merge_nested_dicts(self, base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
        """Fusionne récursivement deux dictionnaires sans perdre les valeurs By default."""
        result = deepcopy(base)
        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_nested_dicts(result[key], value)
            else:
                result[key] = value
        return result


# Instance globale du gestionnaire de configuration
config_manager = ConfigManager()


def apply_resolution(width: int, height: int) -> bool:
    """
    Applique et sauvegarde une nouvelle résolution.
    Retourne True si la sauvegarde a réussi.
    """
    config_manager.set_resolution(width, height)
    return config_manager.save_config()

def set_window_mode(mode: str) -> bool:
    """Met à jour le mode d'affichage et sauvegarde la config."""
    if mode in ["windowed", "fullscreen"]:
        config_manager.set("window_mode", mode)
        return config_manager.save_config()
    return False

def set_audio_volume(volume_type: str, value: float) -> bool:
    """Met à jour un volume audio et sauvegarde."""
    if volume_type in ["master", "music", "effects"]:
        config_manager.set_volume(volume_type, value)
        return config_manager.save_config()
    return False

def reset_to_defaults() -> bool:
    """Réinitialise all paramètres aux valeurs By default et sauvegarde."""
    config_manager.reset_to_defaults()
    return config_manager.save_config()

def get_performance_mode() -> str:
    """Retourne le mode de performance actuel."""
    return config_manager.get_performance_mode()

def get_project_version() -> str:
    """
    Retourne la version actuelle du projet from le file version.py.
    """
    try:
        return __version__
    except Exception:
        return "unknown"


def is_dev_mode_enabled() -> bool:
    """
    Check if dev mode is enabled in the configuration.

    Returns:
        True if dev mode is enabled, False otherwise.
    """
    try:
        return config_manager.get('dev_mode', False)
    except Exception:
        return False


# =============================================================================
# CONSTANTES DE JEU
# =============================================================================

# Paramètres d'affichage
GAME_TITLE = "Galad Scott"
FPS = 60

# Dimensions de la carte de jeu
MAP_WIDTH = 45   # nombre de cases en largeur
MAP_HEIGHT = 45  # nombre de cases en hauteur

# Paramètres de génération de la carte
MINE_RATE = math.ceil(MAP_WIDTH * MAP_HEIGHT * 0.008)        # 0.8% de mines
GENERIC_ISLAND_RATE = math.ceil(MAP_WIDTH * MAP_HEIGHT * 0.007)  # 0.7% d'îles
CLOUD_RATE = math.ceil(MAP_WIDTH * MAP_HEIGHT * 0.03)       # 3% de nuages

# Paramètres de contrôle de la caméra
CAMERA_SPEED = 200  # pixels par seconde
ZOOM_MIN = 0.25
ZOOM_MAX = 2.5
ZOOM_SPEED = 0.1

# Contraintes d'affichage pour le calcul adaptatif des tuiles
MIN_VISIBLE_TILES_WIDTH = 15   # minimum de cases visibles en largeur
MIN_VISIBLE_TILES_HEIGHT = 10  # minimum de cases visibles en hauteur
MIN_TILE_SIZE = 16  # taille minimale d'une tuile en pixels
MAX_TILE_SIZE = 64  # taille maximale d'une tuile en pixels


# =============================================================================
# PROPRIÉTÉS DYNAMIQUES
# =============================================================================

def get_screen_dimensions() -> Tuple[int, int]:
    """Retourne les dimensions actuelles de l'écran."""
    return config_manager.get_resolution()

def get_screen_width() -> int:
    """Retourne la largeur actuelle de l'écran."""
    return config_manager.get("screen_width")

def get_screen_height() -> int:
    """Retourne la hauteur actuelle de l'écran."""
    return config_manager.get("screen_height")

def calculate_tile_size(screen_width: int = None, screen_height: int = None) -> int:
    """
    Calcule la taille optimale des tuiles selon la résolution d'écran.
    Assure qu'au moins MIN_VISIBLE_TILES_WIDTH x MIN_VISIBLE_TILES_HEIGHT cases sont visibles.
    """
    if screen_width is None or screen_height is None:
        screen_width, screen_height = get_screen_dimensions()
    
    # Calcul basé sur la contrainte la plus restrictive
    max_tile_width = screen_width // MIN_VISIBLE_TILES_WIDTH
    max_tile_height = screen_height // MIN_VISIBLE_TILES_HEIGHT
    
    # Prendre la plus petite valeur pour garantir la visibilité
    tile_size = min(max_tile_width, max_tile_height)
    
    # Appliquer les limites min/max
    return max(MIN_TILE_SIZE, min(MAX_TILE_SIZE, tile_size))

def get_tile_size() -> int:
    """Retourne la taille actuelle des tuiles."""
    return calculate_tile_size()


# =============================================================================
# COMPATIBILITÉ (constantes statiques)
# =============================================================================

# Propriétés pour la compatibilité avec l'ancien code
SCREEN_WIDTH = get_screen_width()
SCREEN_HEIGHT = get_screen_height()
TILE_SIZE = get_tile_size()
