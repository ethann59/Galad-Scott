"""
Constants de gameplay - Valeurs numériques du jeu Galad Islands.
Centralise all constantes magiques pour faciliter la maintenance et l'équilibrage.
"""
# =============================================================================
# CONSTANTES DE PERFORMANCE ET Rendering
# =============================================================================

# Framerate
TARGET_FPS = 60
FRAME_TIME_MS = 1000.0  # pour les calculs de deltatime

# Interface utilisateur
HEALTH_BAR_HEIGHT = 6
HEALTH_BAR_OFFSET = 10  # pixels au-dessus du sprite
DEBUG_FONT_SIZE = 36

# Constantes pour les modales
MODAL_MARGIN = 20
MODAL_PADDING = 15
MODAL_SCROLL_SPEED = 30
MODAL_HEADER_HEIGHT = 50
MODAL_FOOTER_HEIGHT = 70
MODAL_BUTTON_WIDTH = 120
MODAL_BUTTON_HEIGHT = 40
MODAL_SCROLLBAR_WIDTH = 15
MODAL_ERROR_SURFACE_WIDTH = 200
MODAL_ERROR_SURFACE_HEIGHT = 100
MODAL_DEFAULT_MAX_WIDTH = 620
MODAL_DEFAULT_GIF_DURATION = 100  # millisecondes

# Tailles de police pour les modales
MODAL_FONT_SIZE_SMALL = 20
MODAL_FONT_SIZE_NORMAL = 22
MODAL_FONT_SIZE_MEDIUM = 26
MODAL_FONT_SIZE_LARGE = 30
MODAL_FONT_SIZE_XLARGE = 36
MODAL_TEXT_LINE_SPACING = 8
MODAL_MEDIA_SPACING = 10

# =============================================================================
# EVENEMENTS / TEMPO
# =============================================================================
# Delay (s) before global events (kraken/storms/bandits) start appearing after game start
INITIAL_EVENT_DELAY = 15.0
# Seuils de couleur pour les barres de vie
HEALTH_HIGH_THRESHOLD = 0.6  # Vert si > 60%
HEALTH_MEDIUM_THRESHOLD = 0.3   # Orange si > 30%, Rouge si < 30%
HEALTH_LOW_THRESHOLD = 0.3   # Rouge si < 30%, Orange entre les deux

# =============================================================================
# COULEURS (RGB)
# =============================================================================

# Couleurs de l'interface
COLOR_OCEAN_BLUE = (0, 50, 100)
COLOR_HEALTH_BACKGROUND = (100, 0, 0)
COLOR_HEALTH_HIGH = (0, 200, 0)      # Vert
COLOR_HEALTH_MEDIUM = (255, 165, 0)  # Orange
COLOR_HEALTH_LOW = (200, 0, 0)       # Rouge

# Couleurs pour les modales et interfaces
COLOR_WHITE = (255, 255, 255)
COLOR_GOLD = (255, 215, 0)
COLOR_GRAY = (128, 128, 128)
COLOR_DARK_GRAY = (64, 64, 64)
COLOR_LIGHT_GRAY = (192, 192, 192)
COLOR_ERROR_GRAY = (100, 100, 100)

# Couleurs communes pour les boutiques
COLOR_BLACK = (0, 0, 0)
COLOR_GREEN_SUCCESS = (80, 200, 80)
COLOR_RED_ERROR = (200, 80, 80)

# Couleurs de placeholder pour icônes
COLOR_PLACEHOLDER_UNIT = (100, 150, 200)
COLOR_PLACEHOLDER_BUILDING = (150, 120, 80)
COLOR_PLACEHOLDER_UPGRADE = (200, 150, 100)

# =============================================================================
# CONSTANTES DE MOUVEMENT ET PHYSICS
# =============================================================================

# Vitesses By default
DEFAULT_UNIT_SPEED = 3.5
DEFAULT_REVERSE_SPEED = -0.6
SPEED_ACCELERATION = 0.2
SPEED_DECELERATION = 0.1
BOUNDARY_MARGIN = 32  # pixels pour les bordures collision

# =============================================================================
# CONSTANTES DE COMBAT
# =============================================================================

# Projectiles
PROJECTILE_SPEED = 10.0
PROJECTILE_DAMAGE = 10
PROJECTILE_HEALTH = 1
PROJECTILE_WIDTH = 20
PROJECTILE_HEIGHT = 10
EXPLOSION_SIZE_WIDTH = 20
EXPLOSION_SIZE_HEIGHT = 10

# Vitesses des units (par type)
UNIT_SPEED_SCOUT = 5.0
UNIT_SPEED_MARAUDEUR = 3.5
UNIT_SPEED_LEVIATHAN = 2.0
UNIT_SPEED_DRUID = 3.5
UNIT_SPEED_KAMIKAZE = 6.0    # Très rapide
UNIT_SPEED_ARCHITECT = 3.5

# Vitesses de recul des units (par type)
UNIT_REVERSE_SPEED_SCOUT = -1.0
UNIT_REVERSE_SPEED_MARAUDEUR = -0.6
UNIT_REVERSE_SPEED_LEVIATHAN = -0.2
UNIT_REVERSE_SPEED_DRUID = -0.6
UNIT_REVERSE_SPEED_KAMIKAZE = -1.0
UNIT_REVERSE_SPEED_ARCHITECT = -0.6

# Attaques des units (par type)
UNIT_ATTACK_SCOUT = 10
UNIT_ATTACK_MARAUDEUR = 20
UNIT_ATTACK_LEVIATHAN = 30
UNIT_ATTACK_DRUID = 20
UNIT_ATTACK_KAMIKAZE = 150   # Dégâts collision importants
UNIT_ATTACK_ARCHITECT = 20

# Cooldowns d'attaque des units (en secondes)
UNIT_COOLDOWN_SCOUT = 2
UNIT_COOLDOWN_MARAUDEUR = 4
UNIT_COOLDOWN_LEVIATHAN = 1.5  # 1.5 secondes entre chaque attaque
UNIT_COOLDOWN_DRUID = 4
UNIT_COOLDOWN_KAMIKAZE = 0.5 # Cooldown très court, car il meurt after l'attaque
UNIT_COOLDOWN_ARCHITECT = 4

# Capacités spéciales

SPECIAL_ABILITY_COOLDOWN = 15.0 # Cooldown générique pour les capacités spéciales

# Zasper : Invincibilité
ZASPER_INVINCIBILITY_DURATION = 3.0 # Durée d'invincibilité de Zasper


# =============================================================================
# CONSTANTES DE RESSOURCES
# =============================================================================

# Coffres volants
FLYING_CHEST_SPAWN_INTERVAL = 15.0      # Intervalle d'apparition des coffres volants
FLYING_CHEST_MAX_COUNT = 5              # Nombre maximum de coffres volants actifs
FLYING_CHEST_GOLD_MIN = 60              # Gain minimal en or lors de la collecte
FLYING_CHEST_GOLD_MAX = 150             # Gain maximal en or lors de la collecte
FLYING_CHEST_LIFETIME = 25.0            # Durée before la chute automatique in l'océan
FLYING_CHEST_SINK_DURATION = 3.0        # Durée de l'animation de chute before disparition


# =============================================================================
# CONSTANTES DE VISION ET BROUILLARD DE GUERRE
# =============================================================================

# Portées de vision par type d'unit (en units de grille)
UNIT_VISION_SCOUT = 6.0
UNIT_VISION_MARAUDEUR = 5.0
UNIT_VISION_LEVIATHAN = 5.0  # Augmenté de 4.0 à 5.0 pour meilleure visibilité
UNIT_VISION_DRUID = 5.0
UNIT_VISION_ARCHITECT = 4.0