"""
Options ultra-simples pour borne d'arcade - Version sécurisée.
"""

import pygame
import sys


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
        lang = "FR"
        selected = 0
        options_count = 4
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
                    elif event.key in (pygame.K_UP, pygame.K_w):
                        selected = (selected - 1) % options_count
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        selected = (selected + 1) % options_count
                    elif event.key in (pygame.K_LEFT, pygame.K_a):
                        if selected == 0:  # Musique
                            music_vol = max(0, music_vol - 10)
                        elif selected == 1:  # Effets
                            effects_vol = max(0, effects_vol - 10)
                        elif selected == 2:  # Langue
                            lang = "EN" if lang == "FR" else "FR"
                    elif event.key in (pygame.K_RIGHT, pygame.K_d):
                        if selected == 0:  # Musique
                            music_vol = min(100, music_vol + 10)
                        elif selected == 1:  # Effets
                            effects_vol = min(100, effects_vol + 10)
                        elif selected == 2:  # Langue
                            lang = "EN" if lang == "FR" else "FR"
                    elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        if selected == 3:  # Fermer
                            running = False
            
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
                f"Langue: {lang}",
                "Fermer"
            ]
            
            for i, text in enumerate(options_text):
                color = (255, 215, 0) if i == selected else (200, 200, 200)
                rendered = font_med.render(text, True, color)
                surface.blit(rendered, (100, y + i * spacing))
                
                # Indicateur de sélection
                if i == selected:
                    pygame.draw.rect(surface, (255, 215, 0), 
                                   (80, y + i * spacing - 5, 300, 40), 2)
            
            # Instructions
            instructions = [
                "↑↓: Naviguer  ←→: Ajuster",
                "Entrée: Sélectionner  Échap: Fermer"
            ]
            
            inst_y = surface.get_height() - 100
            for instruction in instructions:
                inst_text = pygame.font.Font(None, 24).render(instruction, True, (150, 150, 150))
                surface.blit(inst_text, (50, inst_y))
                inst_y += 30
            
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