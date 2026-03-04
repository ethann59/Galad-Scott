import math
import random
from typing import Dict, Optional, Set

import esper as es
import pygame

from src.components.core.canCollideComponent import CanCollideComponent
from src.components.core.healthComponent import HealthComponent
from src.components.core.positionComponent import PositionComponent
from src.components.core.projectileComponent import ProjectileComponent
from src.components.core.spriteComponent import SpriteComponent
from src.components.core.teamComponent import TeamComponent
from src.components.core.velocityComponent import VelocityComponent
from src.components.core.immunityComponent import ImmunityComponent
from src.constants.assets import MUSIC_IN_GAME
from src.constants.gameplay import SPECIAL_ABILITY_COOLDOWN, ZASPER_INVINCIBILITY_DURATION
from src.constants.team import Team
from src.functions.projectileCreator import create_projectile
from src.managers.sprite_manager import SpriteID, sprite_manager
from src.processeurs.collisionProcessor import CollisionProcessor
from src.processeurs.lifetimeProcessor import LifetimeProcessor
from src.settings.settings import config_manager


class RailShooterEngine:
    """Minimal rail shooter loop built on existing ECS components."""

    def __init__(self, window: Optional[pygame.Surface] = None, audio_manager=None):
        self.window = window
        self.audio_manager = audio_manager
        self.running = True
        self.created_local_window = False

        self.clock: Optional[pygame.time.Clock] = None
        self.player_id: Optional[int] = None
        self.player_fire_cooldown = 0.0
        self.player_fire_interval = 0.18  # Anti-spam: ~5.5 tirs/sec max
        self._last_player_health = 0  # Tracker pour détecter les dégâts
        self.enemy_fire_cooldowns: Dict[int, float] = {}
        self.enemy_states: Dict[int, Dict[str, float]] = {}
        self.enemy_score_values: Dict[int, int] = {}
        self.enemy_entities: Set[int] = set()
        self.despawned_enemies: Set[int] = set()
        self._boss_wave = 0

        self.spawn_timer = 0.0
        self.spawn_interval = 1.1
        self.max_enemies = 8

        self.score = 0
        self.game_over = False
        self.game_over_timer = 0.0
        self._last_dt = 0.0
        self._background_speed = 80.0
        self._projectile_speed_multiplier = 2.5
        self._player_projectile_speed_multiplier = 35.0  # Projectiles alliés nettement plus rapides
        self._score_saved = False
        
        # Variables pour la saisie de nom style borne d'arcade
        self._entering_name = False
        self._name_input = ""
        self._name_confirmed = False
        self._letter_index = 0  # Index de la lettre actuelle
        self._char_position = 0  # Position dans le nom
        self._available_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 "
        self._game_over_pause = 0.0  # Pause avant saisie pour éviter validation accidentelle

        self.collision_processor: Optional[CollisionProcessor] = None
        self.lifetime_processor: Optional[LifetimeProcessor] = None

        self._background_tile = None
        self._background_scroll = 0.0
        self._background_stretched = None
        self._background_stretched_size = (0, 0)

        self._hud_font = None
        self._hud_big_font = None
        self._name_font = None
        self._name_big_font = None

        self._player_immunity_timer = 0.0
        self._player_immunity_duration = 2.0  # 2 secondes d'immunité
        self._player_special_duration = float(ZASPER_INVINCIBILITY_DURATION)
        self._player_special_cooldown = float(SPECIAL_ABILITY_COOLDOWN)
        self._player_special_cooldown_timer = 0.0
        self._player_blink_rate = 0.1  # Clignotement 10x par seconde
        self._player_visible = True

        self._hud_cache_key = None
        self._hud_cache_surface = None
        self._game_over_surface = None
        self._name_title_surface = None
        self._name_instructions_surfaces = []

    def run(self) -> None:
        self.initialize()
        if self.clock is None:
            raise RuntimeError("Clock not initialized")

        while self.running:
            dt = self.clock.tick(int(config_manager.get("max_fps", 60))) / 1000.0
            self._last_dt = dt
            self._handle_events()
            self._update(dt)
            self._render()

        self._cleanup()

    def initialize(self) -> None:
        pygame.init()

        if self.window is None:
            width, height = config_manager.get_resolution()
            flags = pygame.RESIZABLE | pygame.DOUBLEBUF
            if config_manager.get("window_mode") == "fullscreen":
                flags |= pygame.FULLSCREEN
            self.window = pygame.display.set_mode((width, height), flags)
            self.created_local_window = True

        pygame.display.set_caption("Galad Islands - Rail Shooter")
        self.clock = pygame.time.Clock()

        if self.audio_manager is not None:
            try:
                self.audio_manager.play_music(MUSIC_IN_GAME)
            except Exception:
                pass

        self._preload_assets()
        self._init_ui_cache()
        self._init_ecs()
        self._create_player()
        self._init_background()

    def _init_ui_cache(self) -> None:
        self._hud_font = pygame.font.SysFont("Arial", 20, bold=True)
        self._hud_big_font = pygame.font.SysFont("Arial", 48, bold=True)
        self._name_font = pygame.font.SysFont("Arial", 24, bold=True)
        self._name_big_font = pygame.font.SysFont("Arial", 32, bold=True)

        self._game_over_surface = self._hud_big_font.render("GAME OVER", True, (255, 200, 200))
        self._name_title_surface = self._name_big_font.render("ENTREZ VOTRE NOM:", True, (255, 255, 100))
        self._name_instructions_surfaces = [
            self._name_font.render("↑↓: Changer lettre  →: Valider", True, (150, 150, 150)),
            self._name_font.render("←: Retour  R: Valider nom  F: Effacer", True, (150, 150, 150)),
        ]

    def _preload_assets(self) -> None:
        sprite_manager.preload_sprites(
            [
                SpriteID.ALLY_SCOUT,
                SpriteID.ENEMY_SCOUT,
                SpriteID.ENEMY_MARAUDEUR,
                SpriteID.ENEMY_KAMIKAZE,
                SpriteID.ENEMY_LEVIATHAN,
                SpriteID.PROJECTILE_BULLET,
                SpriteID.PROJECTILE_FIREBALL,
                SpriteID.TERRAIN_SEA,
            ]
        )

    def _init_ecs(self) -> None:
        es.clear_database()
        es._processors.clear()
        
        # Initialize ECS properly without setting _world
        self.collision_processor = CollisionProcessor(graph=None)
        self.lifetime_processor = LifetimeProcessor()
        es.add_processor(self.collision_processor, priority=0)
        es.add_processor(self.lifetime_processor, priority=1)

        es.set_handler("attack_event", create_projectile)

    def _create_player(self) -> None:
        if self.window is None:
            return

        width, height = self.window.get_size()
        player = es.create_entity()
        es.add_component(player, PositionComponent(width * 0.2, height * 0.5, 180.0))
        es.add_component(player, VelocityComponent(0.0, 0.0, 0.0, 1.0))
        es.add_component(player, TeamComponent(Team.ALLY))
        es.add_component(player, HealthComponent(3, 3))
        es.add_component(player, CanCollideComponent())

        sprite = sprite_manager.create_sprite_component(SpriteID.ALLY_SCOUT, 64, 80)
        if sprite is not None:
            self._flip_sprite_horizontal(sprite)
            es.add_component(player, sprite)

        self.player_id = player
        self._last_player_health = 3  # Initialiser au HP max

    def _init_background(self) -> None:
        if self.window is None:
            return
        tile = sprite_manager.get_scaled_sprite(SpriteID.TERRAIN_SEA, (64, 64))
        if tile is not None:
            self._background_tile = tile

    def _handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return
            if self._entering_name and event.type == pygame.KEYDOWN and self._game_over_pause <= 0:
                self._handle_name_input_arcade(event)
                continue
            # Combinaison pause: boutons R+F (système pause sur borne arcade)
            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_r] and keys[pygame.K_f]:
                    self.running = False
                    return
            # Bouton R pour tirer (contrôle borne d'arcade)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r and not self._entering_name:
                self._try_player_fire()
            # Bouton T pour capacité spéciale Scott (invincibilité temporaire)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_t and not self._entering_name and not self.game_over:
                self._activate_scott_special()
            # Support clic souris pour test
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self._try_player_fire()

    def _update(self, dt: float) -> None:
        if self.window is None:
            return

        if self.game_over:
            if self._entering_name:
                # Gestion de la pause avant saisie
                if self._game_over_pause > 0:
                    self._game_over_pause -= dt
                # Sinon, la saisie est gérée dans _handle_events
            elif self._name_confirmed:
                self.game_over_timer -= dt
                if self.game_over_timer <= 0:
                    self.running = False
            else:
                # Démarrer la saisie de nom après un délai
                self.game_over_timer -= dt
                if self.game_over_timer <= 0:
                    self._start_name_entry()
            return

        self._update_player(dt)
        self._spawn_enemies(dt)
        self._update_enemies(dt)
        self._move_projectiles(dt)

        es.process(dt=dt)
        self._cleanup_entities()
        self._check_player_damage()  # V\u00e9rifier les d\u00e9g\u00e2ts du joueur et appliquer l'immunit\u00e9
        self._check_game_over()

    def _update_player(self, dt: float) -> None:
        if self.player_id is None or not es.entity_exists(self.player_id):
            return

        if self._player_special_cooldown_timer > 0:
            self._player_special_cooldown_timer = max(0.0, self._player_special_cooldown_timer - dt)

        # Gérer l'immunité et le clignotement
        if self._player_immunity_timer > 0:
            self._player_immunity_timer -= dt
            self._player_visible = int(self._player_immunity_timer * (1.0 / self._player_blink_rate)) % 2 == 0
        else:
            self._player_visible = True
            # Retirer le composant d'immunité quand l'immunité expire
            if es.has_component(self.player_id, ImmunityComponent):
                es.remove_component(self.player_id, ImmunityComponent)

        speed = 260.0
        dx = 0.0
        dy = 0.0

        keys = pygame.key.get_pressed()

        # Contrôles borne d'arcade: ←→↑↓
        if keys[pygame.K_LEFT]:
            dx = -speed * dt
        if keys[pygame.K_RIGHT]:
            dx += speed * dt
        if keys[pygame.K_UP]:
            dy = -speed * dt
        if keys[pygame.K_DOWN]:
            dy += speed * dt

        pos = es.component_for_entity(self.player_id, PositionComponent)
        pos.x += dx
        pos.y += dy

        if self.window is not None:
            width, height = self.window.get_size()
            margin = 32
            pos.x = max(margin, min(width - margin, pos.x))
            pos.y = max(margin, min(height - margin, pos.y))

        if self.player_fire_cooldown > 0:
            self.player_fire_cooldown -= dt

        # Tir automatique continu pour borne d'arcade - Bouton R
        if keys[pygame.K_r]:
            self._try_player_fire()

    def _activate_scott_special(self) -> None:
        if self.player_id is None or not es.entity_exists(self.player_id):
            return
        if self._player_special_cooldown_timer > 0:
            return

        self._player_immunity_timer = max(self._player_immunity_timer, self._player_special_duration)
        self._player_special_cooldown_timer = self._player_special_cooldown

        if not es.has_component(self.player_id, ImmunityComponent):
            es.add_component(self.player_id, ImmunityComponent())

    def _spawn_enemies(self, dt: float) -> None:
        if self.window is None:
            return

        self.spawn_timer -= dt
        if self.spawn_timer > 0:
            return

        self.spawn_timer = self.spawn_interval

        width, height = self.window.get_size()
        margin = 40
        spawn_y = random.uniform(margin, height - margin)
        spawn_x = width + 80

        if self._should_spawn_leviathan_boss() and len(self.enemy_entities) < (self.max_enemies + 1):
            self._spawn_enemy(
                kind="leviathan",
                sprite_id=SpriteID.ENEMY_LEVIATHAN,
                sprite_w=180,
                sprite_h=220,
                hp=25,
                speed=85.0,
                spawn_x=spawn_x,
                spawn_y=spawn_y,
                score_value=250,
            )
            self._boss_wave += 1
            return

        if len(self.enemy_entities) >= self.max_enemies:
            return

        # Progression des ennemis basée sur le score
        enemy_types = []
        
        # Scouts: toujours disponibles (plus fréquents au début)
        scout_weight = 70 if self.score < 100 else (50 if self.score < 300 else 30)
        enemy_types.extend([("scout", SpriteID.ENEMY_SCOUT, 80, 100, 2, 140.0, 10)] * scout_weight)
        
        # Maraudeurs: apparaissent après 50 points, deviennent fréquents
        if self.score >= 50:
            maraudeur_weight = 20 if self.score < 200 else (50 if self.score < 500 else 60)
            enemy_types.extend([("maraudeur", SpriteID.ENEMY_MARAUDEUR, 110, 120, 4, 120.0, 20)] * maraudeur_weight)
        
        # Kamikazes: rares, apparaissent après 150 points, oneshot mais dangereux
        if self.score >= 150:
            kamikaze_weight = 5 if self.score < 400 else 10
            enemy_types.extend([("kamikaze", SpriteID.ENEMY_KAMIKAZE, 110, 90, 1, 200.0, 25)] * kamikaze_weight)
        
        enemy_type = random.choice(enemy_types)
        kind, sprite_id, sprite_w, sprite_h, hp, speed, score_value = enemy_type

        self._spawn_enemy(
            kind=kind,
            sprite_id=sprite_id,
            sprite_w=sprite_w,
            sprite_h=sprite_h,
            hp=hp,
            speed=speed,
            spawn_x=spawn_x,
            spawn_y=spawn_y,
            score_value=score_value,
        )

    def _spawn_enemy(
        self,
        kind: str,
        sprite_id: SpriteID,
        sprite_w: int,
        sprite_h: int,
        hp: int,
        speed: float,
        spawn_x: float,
        spawn_y: float,
        score_value: int,
    ) -> None:
        enemy = es.create_entity()
        es.add_component(enemy, PositionComponent(spawn_x, spawn_y, 0.0))
        es.add_component(enemy, VelocityComponent(speed, speed, -speed, 1.0))
        es.add_component(enemy, TeamComponent(Team.ENEMY))
        es.add_component(enemy, HealthComponent(hp, hp))
        es.add_component(enemy, CanCollideComponent())

        sprite = sprite_manager.create_sprite_component(sprite_id, sprite_w, sprite_h)
        if sprite is not None:
            es.add_component(enemy, sprite)

        self.enemy_entities.add(enemy)
        self.enemy_score_values[enemy] = int(score_value)
        self.enemy_fire_cooldowns[enemy] = random.uniform(0.8, 1.6)
        self.enemy_states[enemy] = {
            "kind": 0.0,
            "speed": speed,
            "fire_cooldown": random.uniform(0.6, 1.4),
            "burst_timer": 0.0,
            "burst_shots": 0.0,
            "zigzag_phase": random.uniform(0.0, math.tau),
            "base_y": spawn_y,
        }
        if kind == "scout":
            self.enemy_states[enemy]["kind"] = 0.0
        elif kind == "maraudeur":
            self.enemy_states[enemy]["kind"] = 1.0
        elif kind == "kamikaze":
            self.enemy_states[enemy]["kind"] = 2.0
        else:
            self.enemy_states[enemy]["kind"] = 3.0

    def _has_active_leviathan(self) -> bool:
        for enemy_id in self.enemy_entities:
            state = self.enemy_states.get(enemy_id)
            if state and int(state.get("kind", -1.0)) == 3 and es.entity_exists(enemy_id):
                return True
        return False

    def _should_spawn_leviathan_boss(self) -> bool:
        # Un boss toutes les 250 points, un seul actif à la fois
        target_wave = self.score // 250
        if target_wave <= self._boss_wave:
            return False
        return not self._has_active_leviathan()

    def _update_enemies(self, dt: float) -> None:
        player_pos = None
        if self.player_id is not None and es.entity_exists(self.player_id):
            player_pos = es.component_for_entity(self.player_id, PositionComponent)

        for enemy_id in list(self.enemy_entities):
            if not es.entity_exists(enemy_id):
                self.enemy_entities.discard(enemy_id)
                self.enemy_fire_cooldowns.pop(enemy_id, None)
                self.enemy_states.pop(enemy_id, None)
                continue

            pos = es.component_for_entity(enemy_id, PositionComponent)
            state = self.enemy_states.get(enemy_id)
            if not state:
                continue

            kind = int(state.get("kind", 0.0))
            speed = state.get("speed", 120.0)

            start_x = pos.x
            if kind == 0:
                self._update_scout_enemy(enemy_id, pos, state, dt, player_pos)
            elif kind == 1:
                self._update_maraudeur_enemy(enemy_id, pos, state, dt, player_pos)
            elif kind == 2:
                self._update_kamikaze_enemy(enemy_id, pos, state, dt, player_pos)
            else:
                self._update_leviathan_enemy(enemy_id, pos, state, dt, player_pos)
            if pos.x > start_x:
                pos.x = start_x

    def _update_scout_enemy(self, enemy_id: int, pos: PositionComponent, state: Dict[str, float], dt: float, player_pos: Optional[PositionComponent]) -> None:
        speed = state.get("speed", 140.0)
        state["zigzag_phase"] += dt * 2.2
        base_y = state.get("base_y", pos.y)
        pos.y = base_y + math.sin(state["zigzag_phase"]) * 45.0
        pos.x -= speed * dt

        state["fire_cooldown"] -= dt
        if player_pos is not None and state["fire_cooldown"] <= 0:
            # Avec la formule de déplacement actuelle (-cos/-sin), 0° part vers la gauche
            self._fire_with_direction(enemy_id, pos, 0.0)
            state["fire_cooldown"] = random.uniform(0.6, 1.1)

    def _update_maraudeur_enemy(self, enemy_id: int, pos: PositionComponent, state: Dict[str, float], dt: float, player_pos: Optional[PositionComponent]) -> None:
        speed = state.get("speed", 110.0)
        pos.x -= speed * dt

        if player_pos is not None:
            dy = player_pos.y - pos.y
            pos.y += max(-1.0, min(1.0, dy / 80.0)) * 90.0 * dt

        if state.get("burst_shots", 0.0) > 0:
            state["burst_timer"] -= dt
            if state["burst_timer"] <= 0:
                # Avec la formule de déplacement actuelle (-cos/-sin), 0° part vers la gauche
                angle = 0.0 + random.uniform(-10.0, 10.0)
                self._fire_with_direction(enemy_id, pos, angle)
                state["burst_shots"] -= 1
                state["burst_timer"] = 0.12
            return

        state["fire_cooldown"] -= dt
        if player_pos is not None and state["fire_cooldown"] <= 0:
            state["burst_shots"] = 3.0
            state["burst_timer"] = 0.0
            state["fire_cooldown"] = random.uniform(1.4, 2.2)

    def _update_kamikaze_enemy(self, enemy_id: int, pos: PositionComponent, state: Dict[str, float], dt: float, player_pos: Optional[PositionComponent]) -> None:
        speed = state.get("speed", 170.0)
        if player_pos is None:
            pos.x -= speed * dt
            return

        dx = player_pos.x - pos.x
        dy = player_pos.y - pos.y
        dist = max(1.0, math.hypot(dx, dy))
        boost = 1.6 if dist < 220.0 else 1.0
        pos.x += (dx / dist) * speed * boost * dt
        pos.y += (dy / dist) * speed * boost * dt

        # Kamikaze = mort instantanée au contact du joueur
        hit_radius = 52.0
        if dist <= hit_radius and self.player_id is not None and es.entity_exists(self.player_id):
            if es.has_component(self.player_id, HealthComponent):
                player_health = es.component_for_entity(self.player_id, HealthComponent)
                player_health.currentHealth = 0

            if self.collision_processor is not None:
                try:
                    self.collision_processor._create_explosion_at_position(pos.x, pos.y)
                except Exception:
                    pass

            if es.entity_exists(enemy_id):
                es.delete_entity(enemy_id)

    def _update_leviathan_enemy(self, enemy_id: int, pos: PositionComponent, state: Dict[str, float], dt: float, player_pos: Optional[PositionComponent]) -> None:
        speed = state.get("speed", 85.0)
        pos.x -= speed * dt

        if player_pos is not None:
            dy = player_pos.y - pos.y
            pos.y += max(-1.0, min(1.0, dy / 120.0)) * 55.0 * dt

        state["fire_cooldown"] -= dt
        if player_pos is not None and state["fire_cooldown"] <= 0:
            # Salve large pour accentuer le côté boss
            self._fire_at_target(enemy_id, pos, player_pos, spread=16.0)
            self._fire_at_target(enemy_id, pos, player_pos, spread=0.0)
            self._fire_at_target(enemy_id, pos, player_pos, spread=-16.0)
            state["fire_cooldown"] = random.uniform(1.6, 2.4)

    def _move_projectiles(self, dt: float) -> None:
        for ent, (pos, vel, _) in es.get_components(PositionComponent, VelocityComponent, ProjectileComponent):
            if vel.currentSpeed == 0:
                continue
            direction_rad = math.radians(pos.direction)
            
            # Différencier vitesse projectiles joueur vs ennemis
            team = es.component_for_entity(ent, TeamComponent) if es.has_component(ent, TeamComponent) else None
            if team and team.team_id == Team.ALLY:
                speed = vel.currentSpeed * self._player_projectile_speed_multiplier
            else:
                speed = vel.currentSpeed * self._projectile_speed_multiplier
                
            pos.x += -math.cos(direction_rad) * speed * dt
            pos.y += -math.sin(direction_rad) * speed * dt

    def _try_player_fire(self) -> None:
        if self.player_id is None or not es.entity_exists(self.player_id):
            return
        if self.player_fire_cooldown > 0:
            return
        es.dispatch_event("attack_event", self.player_id, "bullet")
        self.player_fire_cooldown = self.player_fire_interval

    def _fire_at_target(self, enemy_id: int, pos: PositionComponent, target: Optional[PositionComponent], spread: float = 0.0) -> None:
        if target is None:
            return
        dx = target.x - pos.x
        dy = target.y - pos.y
        angle = math.degrees(math.atan2(-dy, -dx))
        if spread:
            angle += random.uniform(-spread, spread)
        self._fire_with_direction(enemy_id, pos, angle)

    def _fire_with_direction(self, enemy_id: int, pos: PositionComponent, direction: float) -> None:
        original_direction = pos.direction
        pos.direction = direction
        es.dispatch_event("attack_event", enemy_id, "bullet")
        pos.direction = original_direction

    def _flip_sprite_horizontal(self, sprite: SpriteComponent) -> None:
        surface = sprite.surface or sprite.image
        if surface is None:
            return
        flipped = pygame.transform.flip(surface, True, False)
        sprite.surface = flipped
        if sprite.image is not None:
            sprite.image = pygame.transform.flip(sprite.image, True, False)

    def _cleanup_entities(self) -> None:
        if self.window is None:
            return

        width, height = self.window.get_size()
        margin = 120

        for ent, pos in es.get_component(PositionComponent):
            if es.has_component(ent, ProjectileComponent):
                # Laisser une marge avant de supprimer les projectiles
                if pos.x < -50 or pos.x > width + 50 or pos.y < -50 or pos.y > height + 50:
                    if es.entity_exists(ent):
                        es.delete_entity(ent)
                    continue
            if pos.x < -margin or pos.x > width + margin or pos.y < -margin or pos.y > height + margin:
                if ent in self.enemy_entities:
                    self.despawned_enemies.add(ent)
                    self.enemy_entities.discard(ent)
                    self.enemy_fire_cooldowns.pop(ent, None)
                    self.enemy_states.pop(ent, None)
                    self.enemy_score_values.pop(ent, None)
                if ent == self.player_id:
                    continue
                if es.entity_exists(ent):
                    es.delete_entity(ent)

        for enemy_id in list(self.enemy_entities):
            if not es.entity_exists(enemy_id):
                if enemy_id not in self.despawned_enemies:
                    self.score += self.enemy_score_values.get(enemy_id, 10)
                self.enemy_entities.discard(enemy_id)
                self.enemy_fire_cooldowns.pop(enemy_id, None)
                self.enemy_states.pop(enemy_id, None)
                self.enemy_score_values.pop(enemy_id, None)

        self.despawned_enemies.clear()

    def _check_player_damage(self) -> None:
        """V\u00e9rifier si le joueur a pris des d\u00e9g\u00e2ts et activer l'immunit\u00e9."""
        if self.player_id is None or not es.entity_exists(self.player_id):
            return

        health = es.component_for_entity(self.player_id, HealthComponent)
        current_health = health.currentHealth

        if current_health < self._last_player_health:
            # Le joueur a pris des d\u00e9g\u00e2ts - activer l'immunit\u00e9
            self._player_immunity_timer = self._player_immunity_duration            # Ajouter le composant d'immunité au joueur
            if not es.has_component(self.player_id, ImmunityComponent):
                es.add_component(self.player_id, ImmunityComponent())
        self._last_player_health = current_health

    def _check_game_over(self) -> None:
        if self.player_id is None:
            return

        if not es.entity_exists(self.player_id):
            self.game_over = True
            self.game_over_timer = 1.5  # Délai avant de commencer la saisie
            return

        health = es.component_for_entity(self.player_id, HealthComponent)
        if health.currentHealth <= 0:
            self.game_over = True
            self.game_over_timer = 1.5  # Délai avant de commencer la saisie

    def _render(self) -> None:
        if self.window is None:
            return

        self._render_background()
        self._render_sprites()
        self._render_hud()

        pygame.display.flip()

    def _render_background(self) -> None:
        if self.window is None:
            return

        if self._background_tile is None:
            self.window.fill((0, 50, 100))
            return

        width, height = self.window.get_size()

        if (
            self._background_stretched is None
            or self._background_stretched_size != (width, height)
        ):
            self._background_stretched = pygame.transform.smoothscale(
                self._background_tile,
                (width, height),
            )
            self._background_stretched_size = (width, height)

        self.window.blit(self._background_stretched, (0, 0))

    def _render_sprites(self) -> None:
        if self.window is None:
            return

        width, height = self.window.get_size()
        margin = 100
        is_player_immune = self._player_immunity_timer > 0
            
        for ent, (pos, sprite) in es.get_components(PositionComponent, SpriteComponent):
            # Passer le joueur si imune et en train de clignoter invisiblement
            if ent == self.player_id and is_player_immune and not self._player_visible:
                continue

            surface = sprite.surface or sprite.image
            if surface is None:
                continue
            if pos.x < -margin or pos.x > width + margin or pos.y < -margin or pos.y > height + margin:
                continue
            rect = surface.get_rect(center=(int(pos.x), int(pos.y)))
            self.window.blit(surface, rect)

    def _render_hud(self) -> None:
        if self.window is None:
            return

        health_value = 0
        if self.player_id is not None and es.entity_exists(self.player_id):
            health = es.component_for_entity(self.player_id, HealthComponent)
            health_value = int(health.currentHealth)

        special_cd = max(0.0, float(self._player_special_cooldown_timer))
        special_state = "READY" if special_cd <= 0 else f"{special_cd:.1f}s"

        hud_key = (health_value, self.score, special_state)
        if self._hud_cache_key != hud_key:
            text = f"HP {health_value}  Score {self.score}  SP {special_state}"
            if self._hud_font is not None:
                self._hud_cache_surface = self._hud_font.render(text, True, (255, 255, 255))
            self._hud_cache_key = hud_key

        if self._hud_cache_surface is not None:
            self.window.blit(self._hud_cache_surface, (16, 12))

        if self.game_over:
            # Afficher "GAME OVER" en haut
            if self._game_over_surface is not None:
                rect = self._game_over_surface.get_rect(center=(self.window.get_width() // 2, 80))
                self.window.blit(self._game_over_surface, rect)

            # Afficher la saisie du nom ou le compte à rebours
            if self._entering_name and not self._name_confirmed:
                if self._game_over_pause <= 0:
                    self._render_name_prompt()
                else:
                    # Affichage du délai restant
                    pause_text = f"Saisie dans {self._game_over_pause:.1f}s..."
                    if self._name_font is not None:
                        pause_surface = self._name_font.render(pause_text, True, (255, 255, 100))
                        pause_rect = pause_surface.get_rect(center=(self.window.get_width() // 2, self.window.get_height() // 2))
                        self.window.blit(pause_surface, pause_rect)

    def _cleanup(self) -> None:
        if self.created_local_window:
            pygame.display.set_mode(config_manager.get_resolution(), pygame.RESIZABLE)

    def _save_score_once(self) -> None:
        if self._score_saved:
            return
        try:
            # Sauvegarde au format JSON classique
            from src.utils.score_manager import add_score
            name = self._name_input.strip() or "UNK"
            add_score(self.score, name)
            
        except Exception as e:
            print(f"❌ Erreur sauvegarde score: {e}")
        self._score_saved = True

    def _start_name_entry(self) -> None:
        if not self._entering_name:
            self._entering_name = True
            self._name_input = ""
            self._name_confirmed = False
            self._letter_index = 0  # Reset index lettre
            self._char_position = 0  # Reset position dans nom
            self._game_over_pause = 2.0  # 2 secondes de pause avant saisie



    def _handle_name_input_arcade(self, event: pygame.event.Event) -> None:
        """Interface de saisie style borne d'arcade - utilise les touches R/F et flèches."""
        # R pour valider le nom
        if event.key == pygame.K_r:
            self._name_confirmed = True
            self._entering_name = False
            self.game_over_timer = 1.5
            self._save_score_once()
            return
        
        # Flèches UP/DOWN pour changer la lettre
        elif event.key == pygame.K_UP:
            self._letter_index = (self._letter_index - 1) % len(self._available_chars)
            
        elif event.key == pygame.K_DOWN:
            self._letter_index = (self._letter_index + 1) % len(self._available_chars)
        
        # Flèche RIGHT pour confirmer la lettre et aller à la suivante
        elif event.key == pygame.K_RIGHT:
            if self._char_position < len(self._name_input):
                # Modifier lettre existante
                name_list = list(self._name_input)
                name_list[self._char_position] = self._available_chars[self._letter_index]
                self._name_input = ''.join(name_list)
            else:
                # Ajouter nouvelle lettre
                if len(self._name_input) < 3:  # Limité à 3 caractères pour borne
                    self._name_input += self._available_chars[self._letter_index]
            
            # Passer au caractère suivant
            if self._char_position < 2:  # Max 3 caractères (0-2)
                self._char_position += 1
                self._letter_index = 0  # Reset sur 'A'
        
        # Flèche LEFT pour revenir au caractère précédent
        elif event.key == pygame.K_LEFT:
            if self._char_position > 0:
                self._char_position -= 1
                # Charger la lettre actuelle à cette position
                if self._char_position < len(self._name_input):
                    current_char = self._name_input[self._char_position]
                    try:
                        self._letter_index = self._available_chars.index(current_char)
                    except ValueError:
                        self._letter_index = 0
        
        # F pour effacer le caractère actuel
        elif event.key == pygame.K_f:
            if self._name_input and self._char_position > 0:
                self._char_position -= 1
                self._name_input = self._name_input[:self._char_position] + self._name_input[self._char_position + 1:]
        
        # S'assurer que _name_input ne dépasse pas la position
        if len(self._name_input) < self._char_position:
            self._char_position = len(self._name_input)

    def _render_name_prompt(self) -> None:
        """Affiche l'interface de saisie de nom style arcade."""
        if self.window is None:
            return
        
        # Position centrale
        width, height = self.window.get_size()
        center_x = width // 2
        center_y = height // 2 + 80
        
        # Titre
        if self._name_title_surface is not None:
            title_rect = self._name_title_surface.get_rect(center=(center_x, center_y - 60))
            self.window.blit(self._name_title_surface, title_rect)
        
        # Nom actuel avec curseur
        name_display = self._name_input + "_" * (3 - len(self._name_input))
        name_chars = list(name_display)
        
        # Affichage caractère par caractère
        char_width = 30
        start_x = center_x - (len(name_chars) * char_width) // 2
        
        for i, char in enumerate(name_chars):
            color = (255, 255, 255)
            if i == self._char_position:
                # Caractère sélectionné
                if i < len(self._name_input):
                    char = self._available_chars[self._letter_index]  # Montre la lettre sélectionnée
                else:
                    char = self._available_chars[self._letter_index]  # Nouvelle lettre
                color = (255, 255, 0)  # Jaune pour sélection
                
                # Fond de sélection
                pygame.draw.rect(self.window, (80, 80, 150), 
                               (start_x + i * char_width - 5, center_y - 20, char_width - 10, 40))
            
            if self._name_font is not None:
                char_surface = self._name_font.render(char, True, color)
                char_rect = char_surface.get_rect(center=(start_x + i * char_width, center_y))
                self.window.blit(char_surface, char_rect)

        y_offset = center_y + 80
        for i, inst_surface in enumerate(self._name_instructions_surfaces):
            inst_rect = inst_surface.get_rect(center=(center_x, y_offset + i * 30))
            self.window.blit(inst_surface, inst_rect)


def run_rail_shooter(window: Optional[pygame.Surface] = None, audio_manager=None) -> None:
    engine = RailShooterEngine(window=window, audio_manager=audio_manager)
    engine.run()
