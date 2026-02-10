"""
Système d'erreur style borne d'arcade pour Galad Islands.
Écran bleu temporisé qui ferme automatiquement le jeu.
"""

import pygame
import sys
import time
from typing import List, Optional


class ArcadeErrorScreen:
    """Écran d'erreur style borne d'arcade avec fermeture automatique."""
    
    def __init__(self, error_message: str = "ERREUR SYSTÈME", 
                 auto_exit_delay: float = 5.0, 
                 error_code: str = "0x00000001"):
        self.error_message = error_message
        self.auto_exit_delay = auto_exit_delay
        self.error_code = error_code
        self.start_time = time.time()
        
        # Initialisation minimale de pygame si nécessaire
        try:
            if not pygame.get_init():
                pygame.init()
            if not pygame.display.get_init():
                pygame.display.init()
            if not pygame.font.get_init():
                pygame.font.init()
        except Exception:
            pass
            
        # Surface d'écran
        try:
            self.surface = pygame.display.get_surface()
            if self.surface is None:
                self.surface = pygame.display.set_mode((800, 600))
        except Exception:
            # Si impossible d'initialiser pygame, sortie immédiate
            print(f"ERREUR CRITIQUE: {error_message}")
            sys.exit(1)
            
        # Polices style système
        try:
            self.font_title = pygame.font.SysFont("Courier", 32, bold=True)
            self.font_normal = pygame.font.SysFont("Courier", 20)
            self.font_small = pygame.font.SysFont("Courier", 16)
        except Exception:
            try:
                self.font_title = pygame.font.Font(None, 32)
                self.font_normal = pygame.font.Font(None, 20)
                self.font_small = pygame.font.Font(None, 16)
            except Exception:
                # Fallback extrême
                self.font_title = None
                self.font_normal = None
                self.font_small = None
    
    def show(self) -> None:
        """Affiche l'écran d'erreur et ferme automatiquement."""
        clock = pygame.time.Clock()
        
        while True:
            # Calculer le temps restant
            elapsed = time.time() - self.start_time
            remaining = max(0, self.auto_exit_delay - elapsed)
            
            # Si le temps est écoulé, fermer
            if remaining <= 0:
                self._force_exit()
                
            # Gérer les événements
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._force_exit()
                elif event.type == pygame.KEYDOWN:
                    # N'importe quelle touche ferme l'écran (borne d'arcade)
                    self._force_exit()
                elif event.type == pygame.JOYBUTTONDOWN:
                    # Support des boutons de joystick/borne
                    self._force_exit()
            
            # Rendu de l'écran bleu
            self._render_blue_screen(remaining)
            
            pygame.display.flip()
            clock.tick(30)
    
    def _render_blue_screen(self, remaining_time: float) -> None:
        """Rendu de l'écran bleu style Windows."""
        if not self.surface:
            return
            
        # Fond bleu classique
        self.surface.fill((0, 0, 139))  # Bleu foncé
        
        width, height = self.surface.get_size()
        
        # Si les polices ne sont pas disponibles, affichage basique
        if not all([self.font_title, self.font_normal, self.font_small]):
            pygame.draw.rect(self.surface, (255, 255, 255), 
                           (50, height//2 - 50, width - 100, 100))
            return
        
        y_pos = 80
        
        # Titre d'erreur
        title_lines = [
            "*** ARRÊT : GALAD ISLANDS ***",
            "",
            "Une erreur système s'est produite et le jeu doit être fermé",
            "pour éviter tout dommage à votre système."
        ]
        
        for line in title_lines:
            if line:
                text = self.font_title.render(line, True, (255, 255, 255))
                self.surface.blit(text, (50, y_pos))
            y_pos += 40
        
        y_pos += 20
        
        # Message d'erreur principal
        error_lines = [
            f"ERREUR: {self.error_message}",
            "",
            "Informations techniques:",
            f"*** Code d'erreur: {self.error_code}",
            "*** Module: Galad Islands Rail Shooter",
            "*** Version: 2026.02.10",
            "",
            "Si c'est la première fois que vous voyez cet écran d'erreur,",
            "redémarrez le jeu. Si cet écran apparaît de nouveau,",
            "contactez l'administrateur de la borne."
        ]
        
        for line in error_lines:
            if line:
                text = self.font_normal.render(line, True, (255, 255, 255))
                self.surface.blit(text, (50, y_pos))
            y_pos += 25
        
        # Informations de debug
        y_pos += 30
        debug_lines = [
            "Informations de debug pour les techniciens:",
            f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}",
            "Stack trace disponible dans les logs système.",
        ]
        
        for line in debug_lines:
            text = self.font_small.render(line, True, (200, 200, 200))
            self.surface.blit(text, (50, y_pos))
            y_pos += 20
        
        # Compteur de fermeture
        y_pos = height - 80
        countdown_text = f"Fermeture automatique dans {int(remaining_time) + 1} secondes..."
        countdown = self.font_normal.render(countdown_text, True, (255, 255, 0))
        self.surface.blit(countdown, (50, y_pos))
        
        # Instructions
        instructions = "Appuyez sur n'importe quelle touche pour fermer"
        inst_text = self.font_small.render(instructions, True, (255, 255, 255))
        self.surface.blit(inst_text, (50, height - 40))
    
    def _force_exit(self) -> None:
        """Force la fermeture du jeu."""
        try:
            pygame.quit()
        except Exception:
            pass
        sys.exit(1)


def show_error_screen(message: str = "Erreur inconnue", 
                     code: str = "0x00000001",
                     auto_exit: float = 5.0) -> None:
    """Affiche un écran d'erreur style borne et ferme le jeu."""
    try:
        error_screen = ArcadeErrorScreen(message, auto_exit, code)
        error_screen.show()
    except Exception:
        # Fallback ultime si même l'écran d'erreur plante
        print(f"ERREUR CRITIQUE: {message}")
        print(f"CODE: {code}")
        print("Le jeu va se fermer...")
        time.sleep(2)
        sys.exit(1)


# Fonction pour gérer les erreurs globales
def handle_critical_error(error: Exception, context: str = "Inconnu") -> None:
    """Gère une erreur critique avec écran bleu."""
    error_msg = f"{type(error).__name__}: {str(error)}"
    error_code = f"0x{hash(str(error)) & 0xFFFFFF:08X}"
    
    print(f"ERREUR CRITIQUE dans {context}: {error_msg}")
    
    show_error_screen(
        message=f"Erreur dans {context}",
        code=error_code,
        auto_exit=5.0
    )