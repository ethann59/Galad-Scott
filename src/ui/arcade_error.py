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
            
        # Surface d'écran - forcer le plein écran
        try:
            self.surface = pygame.display.get_surface()
            if self.surface is None:
                # Obtenir la résolution native de l'écran
                pygame.display.init()
                info = pygame.display.Info()
                screen_width = info.current_w
                screen_height = info.current_h
                
                # Créer une surface en plein écran
                self.surface = pygame.display.set_mode(
                    (screen_width, screen_height), 
                    pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF
                )
        except Exception:
            try:
                # Fallback sur une grande fenêtre si le plein écran échoue
                self.surface = pygame.display.set_mode((1920, 1080))
            except Exception:
                # Dernier recours
                self.surface = pygame.display.set_mode((800, 600))
                
        if self.surface is None:
            # Si impossible d'initialiser pygame, sortie immédiate
            print(f"ERREUR CRITIQUE: {error_message}")
            sys.exit(1)
            
        # Polices style système adaptées à la taille d'écran
        width, height = self.surface.get_size() if self.surface else (800, 600)
        
        # Adapter la taille des polices selon la résolution
        base_scale = min(width / 1920, height / 1080)  # Scale basé sur 1920x1080
        title_size = max(24, int(48 * base_scale))
        normal_size = max(16, int(28 * base_scale))
        small_size = max(12, int(20 * base_scale))
        
        try:
            self.font_title = pygame.font.SysFont("Courier", title_size, bold=True)
            self.font_normal = pygame.font.SysFont("Courier", normal_size)
            self.font_small = pygame.font.SysFont("Courier", small_size)
        except Exception:
            try:
                self.font_title = pygame.font.Font(None, title_size)
                self.font_normal = pygame.font.Font(None, normal_size)
                self.font_small = pygame.font.Font(None, small_size)
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
        
        # Adapter les marges et espacements à la taille d'écran
        margin_x = max(50, width // 20)  # Marge adaptative
        margin_y = max(50, height // 15)
        line_spacing = max(25, height // 35)
        
        # Si les polices ne sont pas disponibles, affichage basique
        if not all([self.font_title, self.font_normal, self.font_small]):
            pygame.draw.rect(self.surface, (255, 255, 255), 
                           (margin_x, height//2 - 50, width - 2*margin_x, 100))
            return
        
        y_pos = margin_y
        
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
                # Centrer le texte pour les titres principaux
                text_rect = text.get_rect(center=(width // 2, y_pos + text.get_height() // 2))
                self.surface.blit(text, text_rect)
            y_pos += line_spacing * 1.5  # Espacement plus grand pour les titres
        
        y_pos += line_spacing
        
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
                self.surface.blit(text, (margin_x, y_pos))
            y_pos += line_spacing
        
        # Informations de debug
        y_pos += line_spacing
        debug_lines = [
            "Informations de debug pour les techniciens:",
            f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}",
            "Stack trace disponible dans les logs système.",
        ]
        
        for line in debug_lines:
            text = self.font_small.render(line, True, (200, 200, 200))
            self.surface.blit(text, (margin_x, y_pos))
            y_pos += line_spacing * 0.8
        
        # Compteur de fermeture - centré en bas
        countdown_text = f"Fermeture automatique dans {int(remaining_time) + 1} secondes..."
        countdown = self.font_normal.render(countdown_text, True, (255, 255, 0))
        countdown_rect = countdown.get_rect(center=(width // 2, height - margin_y * 2))
        self.surface.blit(countdown, countdown_rect)
        
        # Instructions - centrées tout en bas
        instructions = "Appuyez sur n'importe quelle touche pour fermer"
        inst_text = self.font_small.render(instructions, True, (255, 255, 255))
        inst_rect = inst_text.get_rect(center=(width // 2, height - margin_y))
        self.surface.blit(inst_text, inst_rect)
    
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
    # Logs détaillés dans la console
    print("=" * 80)
    print("ERREUR CRITIQUE SYSTÈME - GALAD ISLANDS RAIL SHOOTER")
    print("=" * 80)
    print(f"Message: {message}")
    print(f"Code d'erreur: {code}")
    print(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Fermeture automatique dans: {auto_exit} secondes")
    print("-" * 80)
    print("Affichage de l'écran d'erreur utilisateur...")
    print("=" * 80)
    
    try:
        error_screen = ArcadeErrorScreen(message, auto_exit, code)
        error_screen.show()
    except Exception as e:
        # Fallback ultime si même l'écran d'erreur plante
        print(f"ERREUR CRITIQUE LORS DE L'AFFICHAGE: {e}")
        print(f"MESSAGE ORIGINAL: {message}")
        print(f"CODE ORIGINAL: {code}")
        print("Le jeu va se fermer...")
        time.sleep(2)
        sys.exit(1)


# Fonction pour gérer les erreurs globales
def handle_critical_error(error: Exception, context: str = "Inconnu") -> None:
    """Gère une erreur critique avec écran bleu."""
    error_msg = f"{type(error).__name__}: {str(error)}"
    error_code = f"0x{hash(str(error)) & 0xFFFFFF:08X}"
    
    # Logs détaillés dans la console
    print("\n" + "=" * 80)
    print(f"ERREUR CRITIQUE dans {context.upper()}")
    print("=" * 80)
    print(f"Type: {type(error).__name__}")
    print(f"Message: {str(error)}")
    print(f"Contexte: {context}")
    print(f"Code généré: {error_code}")
    print(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Stack trace si disponible
    try:
        import traceback
        print("-" * 40)
        print("STACK TRACE:")
        traceback.print_exc()
        print("-" * 40)
    except Exception:
        print("Stack trace non disponible")
    
    print("Lancement de l'écran d'erreur utilisateur...")
    print("=" * 80 + "\n")
    
    show_error_screen(
        message=f"Erreur dans {context}",
        code=error_code,
        auto_exit=5.0
    )