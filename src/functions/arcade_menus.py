"""
Menus simplifiés pour borne d'arcade - Version sécurisée.
"""

import pygame
import os
from typing import Optional, List


def show_arcade_help() -> None:
    """Affiche l'aide adaptée pour borne d'arcade."""
    try:
        surface = pygame.display.get_surface()
        if surface is None:
            print("Pas de surface d'affichage - Aide ignorée")
            return
        
        # Contenu d'aide simplifié pour l'arcade
        help_content = [
            "═══════════════════════════════════════",
            "           GALAD ISLANDS", 
            "          RAIL SHOOTER",
            "═══════════════════════════════════════",
            "",
            "CONTRÔLES:",
            "",
            "🎮 DÉPLACEMENT:",
            "  ↑ ou Z      : Monter",
            "  ↓ ou S      : Descendre", 
            "  ← ou Q      : Aller à gauche",
            "  → ou D      : Aller à droite",
            "",
            "🔫 COMBAT:",
            "  ESPACE      : Tirer", 
            "  CLIC SOURIS : Tirer",
            "",
            "📋 MENU:",
            "  ÉCHAP       : Quitter le jeu",
            "  ENTRÉE      : Valider",
            "",
            "🎯 OBJECTIF:",
            "  Survivez le plus longtemps possible !",
            "  Chaque ennemi rapporte 10 points.",
            "",
            "🚀 ENNEMIS:",
            "  Scout     : Rapide, zigzague",
            "  Maraudeur : Tire en rafales", 
            "  Kamikaze  : Charge vers vous",
            "",
            "═══════════════════════════════════════",
        ]
        
        _show_arcade_text_screen("AIDE", help_content, surface)
        
    except Exception as e:
        print(f"Erreur affichage aide: {e}")


def show_arcade_credits() -> None:
    """Affiche les crédits adaptés pour borne d'arcade."""
    try:
        surface = pygame.display.get_surface()
        if surface is None:
            print("Pas de surface d'affichage - Crédits ignorés")
            return
        
        credits_content = [
            "═══════════════════════════════════════",
            "           GALAD SCOTT", 
            "═══════════════════════════════════════",
            "",
            "🎮 DÉVELOPPEMENT:",
            "  Cailliau Ethann",
            ""
            " D'APRÈS GALAD ISLANDS, CRÉÉ PAR:",
            "  Alluin Edouard",
            "  Behani Julien",
            "  Cailliau Ethann",
            "  Damman Alexandre",
            "  Fournier Enzo",
            "  Lambert Romain",
            "",
            "🎨 GRAPHISMES:", 
            "  Sprites et animations originaux",
            "",
            "🎵 AUDIO:",
            "  Musique et effets sonores",
            "",
            "🔧 TECHNOLOGIES:",
            "  Python + Pygame",
            "  Architecture ECS Esper",
            "",
            "🏆 REMERCIEMENTS:",
            "  À tous les testeurs",
            "  À la communauté Pygame",
            "",
            "📧 CONTACT:",
            "  Voir documentation du projet",
            "",
            "═══════════════════════════════════════",
            "",
            "    Merci de jouer !",
        ]
        
        _show_arcade_text_screen("CRÉDITS", credits_content, surface)
        
    except Exception as e:
        print(f"Erreur affichage crédits: {e}")


def show_arcade_scores(score_lines: List[str]) -> None:
    """Affiche les scores adaptés pour borne d'arcade."""
    try:
        surface = pygame.display.get_surface()
        if surface is None:
            print("Pas de surface d'affichage - Scores ignorés")
            return
        
        scores_content = [
            "═══════════════════════════════════════",
            "         MEILLEURS SCORES",
            "═══════════════════════════════════════",
            "",
        ]
        
        if score_lines:
            for i, line in enumerate(score_lines, 1):
                if line.strip():
                    scores_content.append(f"{i:2d}. {line}")
        else:
            scores_content.extend([
                "      Aucun score enregistré",
                "",
                "    Jouez pour être le premier !",
            ])
        
        scores_content.extend([
            "",
            "═══════════════════════════════════════",
        ])
        
        _show_arcade_text_screen("SCORES", scores_content, surface)
        
    except Exception as e:
        print(f"Erreur affichage scores: {e}")


def _show_arcade_text_screen(title: str, content: List[str], surface: pygame.Surface) -> None:
    """Affiche un écran de texte simple avec navigation clavier."""
    try:
        # Fonts
        try:
            font_title = pygame.font.Font(None, 48)
            font_text = pygame.font.Font(None, 24)
            font_small = pygame.font.Font(None, 20)
        except Exception:
            font_title = pygame.font.SysFont("Arial", 48, bold=True)
            font_text = pygame.font.SysFont("Arial", 24)
            font_small = pygame.font.SysFont("Arial", 20)
        
        width, height = surface.get_size()
        running = True
        scroll_offset = 0
        max_visible_lines = (height - 200) // 30  # Lignes visibles
        clock = pygame.time.Clock()
        
        while running:
            # Événements
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        running = False
                    elif event.key in (pygame.K_UP, pygame.K_w):
                        scroll_offset = max(0, scroll_offset - 1)
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        max_scroll = max(0, len(content) - max_visible_lines)
                        scroll_offset = min(max_scroll, scroll_offset + 1)
            
            # Rendu
            surface.fill((20, 20, 40))
            
            # Titre
            title_surface = font_title.render(title, True, (255, 215, 0))
            title_rect = title_surface.get_rect(center=(width // 2, 50))
            surface.blit(title_surface, title_rect)
            
            # Contenu avec scroll
            y_start = 120
            visible_content = content[scroll_offset:scroll_offset + max_visible_lines]
            
            for i, line in enumerate(visible_content):
                color = (255, 255, 255)
                if line.startswith("═"):
                    color = (255, 215, 0)
                elif line.startswith("🎮") or line.startswith("🎨") or line.startswith("🎵") or line.startswith("🔧") or line.startswith("🏆"):
                    color = (150, 255, 150)
                
                text_surface = font_text.render(line, True, color)
                surface.blit(text_surface, (50, y_start + i * 30))
            
            # Indicateurs de scroll
            if scroll_offset > 0:
                scroll_up = font_small.render("▲ ↑ Plus haut", True, (200, 200, 200))
                surface.blit(scroll_up, (width - 150, 120))
            
            if scroll_offset + max_visible_lines < len(content):
                scroll_down = font_small.render("▼ ↓ Plus bas", True, (200, 200, 200))
                surface.blit(scroll_down, (width - 150, height - 150))
            
            # Instructions
            instructions = [
                "↑↓: Défiler  Entrée/Espace: Fermer  Échap: Retour menu"
            ]
            
            for i, instruction in enumerate(instructions):
                text_surface = font_small.render(instruction, True, (180, 180, 180))
                text_rect = text_surface.get_rect(center=(width // 2, height - 40 + i * 25))
                surface.blit(text_surface, text_rect)
            
            pygame.display.flip()
            clock.tick(60)
            
    except Exception as e:
        print(f"Erreur affichage écran: {e}")