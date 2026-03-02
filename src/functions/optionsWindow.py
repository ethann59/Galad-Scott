"""
Options ultra-simples pour borne d'arcade - Version sécurisée.
"""

import pygame
import sys


def _apply_settings(music_vol: int, effects_vol: int) -> None:
    """Applique les réglages choisis."""
    try:
        # Conversion des pourcentages en valeurs pygame (0.0 à 1.0)
        music_level = music_vol / 100.0
        effects_level = effects_vol / 100.0
        
        # Application du volume musique
        pygame.mixer.music.set_volume(music_level)
        
        # Sauvegarde dans la configuration si possible
        try:
            from src.settings.settings import config_manager
            config_manager.set("music_volume", music_level)
            config_manager.set("effects_volume", effects_level)
            config_manager.set("language", "fr")
            config_manager.save()
            print(f"✅ Options appliquées: Musique={music_vol}%, Effets={effects_vol}%")
        except Exception:
            print(f"⚠️ Options appliquées temporairement: Musique={music_vol}%, Effets={effects_vol}%")
            
    except Exception as e:
        print(f"❌ Erreur application options: {e}")


def show_options_window() -> None:
    """Affiche un panneau d'options ultra-simplifié et sécurisé."""
    try:
        # Vérifications de sécurité
        surface = pygame.display.get_surface()
        if surface is None:
            print("Pas de surface d'affichage - Options ignorées")
            return
            
        # Font de base
        try:
            font_big = pygame.font.Font(None, 48)
            font_med = pygame.font.Font(None, 32)
        except Exception:
            font_big = pygame.font.SysFont("Arial", 48)
            font_med = pygame.font.SysFont("Arial", 32)
        
        # Variables d'état simples
        music_vol = 50  # Pourcentage affiché
        effects_vol = 70
        selected = 0
        options_count = 3
        running = True
        
        clock = pygame.time.Clock()
        
        while running:
            # Gestion des événements
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_f:  # Bouton F pour retour/annuler
                        running = False
                    elif event.key in (pygame.K_UP, pygame.K_w):
                        selected = (selected - 1) % options_count
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        selected = (selected + 1) % options_count
                    elif event.key == pygame.K_r:  # Bouton R pour valider
                        if selected == 2:  # Appliquer et fermer
                            _apply_settings(music_vol, effects_vol)
                            running = False
                    elif event.key in (pygame.K_LEFT,):
                        if selected == 0:  # Musique
                            music_vol = max(0, music_vol - 10)
                        elif selected == 1:  # Effets
                            effects_vol = max(0, effects_vol - 10)
                    elif event.key in (pygame.K_RIGHT,):
                        if selected == 0:  # Musique
                            music_vol = min(100, music_vol + 10)
                        elif selected == 1:  # Effets
                            effects_vol = min(100, effects_vol + 10)
            
            # Rendu simple
            surface.fill((20, 20, 40))
            
            # Titre
            title = font_big.render("OPTIONS", True, (255, 255, 255))
            surface.blit(title, (50, 50))
            
            # Options
            y = 150
            spacing = 60
            
            options_text = [
                f"Musique: {music_vol}%",
                f"Effets: {effects_vol}%", 
                "Appliquer et fermer"
            ]
            
            for i, text in enumerate(options_text):
                color = (255, 215, 0) if i == selected else (200, 200, 200)
                rendered = font_med.render(text, True, color)
                surface.blit(rendered, (100, y + i * spacing))
                
                # Indicateur de sélection
                if i == selected:
                    pygame.draw.rect(surface, (255, 215, 0), 
                                   (80, y + i * spacing - 5, 300, 40), 2)
            
            pygame.display.flip()
            clock.tick(60)
    
    except Exception as e:
        # En cas d'erreur, utiliser l'écran bleu
        try:
            from src.ui.arcade_error import show_error_screen
            show_error_screen(
                message="Erreur dans les options",
                code="0x000OPT01", 
                auto_exit=3.0
            )
        except Exception:
            # Fallback ultime
            print(f"ERREUR OPTIONS: {e}")
            sys.exit(1)