# Main menu in Pygame avec gestion d'erreur style borne d'arcade

import pygame
import sys
import os
import logging
import traceback

# Gestion globale des erreurs pour borne d'arcade
def setup_global_error_handling():
    """Configure la gestion d'erreur globale avec écran bleu."""
    def handle_exception(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
            
        # Erreur critique - écran bleu
        error_msg = f"{exc_type.__name__}: {str(exc_value)}"
        
        # Log dans la console
        print("\n" + "=" * 80)
        print("ERREUR GLOBALE NON GÉRÉE - GALAD ISLANDS")
        print("=" * 80)
        print(f"Type: {exc_type.__name__}")
        print(f"Message: {str(exc_value)}")
        print(f"Fichier: {exc_traceback.tb_frame.f_code.co_filename}")
        print(f"Ligne: {exc_traceback.tb_lineno}")
        print(f"Timestamp: {__import__('time').strftime('%Y-%m-%d %H:%M:%S')}")
        print("-" * 40)
        print("STACK TRACE COMPLÈTE:")
        traceback.print_exc()
        print("=" * 80)
        
        try:
            from src.ui.arcade_error import show_error_screen
            show_error_screen(
                message=error_msg,
                code=f"0x{hash(str(exc_value)) & 0xFFFFFF:08X}",
                auto_exit=8.0
            )
        except Exception:
            # Fallback si même l'écran d'erreur plante
            print("IMPOSSIBLE D'AFFICHER L'ÉCRAN D'ERREUR!")
            print(f"ERREUR FINALE: {error_msg}")
            print("Le jeu va se fermer automatiquement...")
            pygame.time.wait(3000)
            sys.exit(1)
    
    sys.excepthook = handle_exception

# Initialiser la gestion d'erreur dès le début
setup_global_error_handling()

# Ancien système de crash remplacé par arcade_error
from src.managers.display import LayoutManager, get_display_manager
from src.managers.audio import AudioManager, VolumeWatcher
from src.menu.state import MenuState
from src.ui.ui_component import Button
from src.constants.assets import MUSIC_MAIN_THEME, MUSIC_IN_GAME
import src.settings.settings as settings
from src.rail_shooter import run_rail_shooter
from src.functions.optionsWindow import show_options_window
from src.settings.localization import t
from src.functions.resource_path import get_resource_path
from src.settings.settings import get_project_version, is_dev_mode_enabled



# Configure logging level: DEBUG in dev mode, WARNING otherwise (to improve runtime fluidity)
logging.basicConfig(level=logging.DEBUG if is_dev_mode_enabled() else logging.WARNING)

class MainMenu:
    """Main menu class."""

    def __init__(self, surface=None):
        # Logo pygame
        logo_path = get_resource_path(os.path.join("assets", "logo.png"))
        print(logo_path)  # verification

        if os.path.isfile(logo_path):
            logo = pygame.image.load(logo_path)
            pygame.display.set_icon(logo)

        # Pygame initialization
        pygame.init()

        # Managers
        # Use shared display manager singleton
        self.display_manager = get_display_manager()
        self.audio_manager = AudioManager()
        self.volume_watcher = VolumeWatcher(self.audio_manager)

        # Initialize gamepad support
        try:
            from src.managers.gamepad_manager import get_gamepad_manager
            self.gamepad_manager = get_gamepad_manager()
            logging.info("Gamepad support initialized")
        except Exception as e:
            logging.warning(f"Failed to initialize gamepad support: {e}")
            self.gamepad_manager = None

        # Menu state
        self.state = MenuState()

        # Display surface
        self.surface = self.display_manager.initialize(surface)
        self.created_local_window = (surface is None)

        # Assets
        self.bg_original = self._load_background()
        self.bg_scaled = None

        # UI Components
        self.buttons = []
        self.particles = None
        
        # Navigation clavier
        self.selected_button_index = 0

        # Fonts
        self.menu_font = None

        # Layout initialization
        self._initialize_ui()



    def _load_background(self):
        """Loads the background image."""
        bg_path = get_resource_path(os.path.join("assets", "image", "galad_islands_bg2.png"))
        return pygame.image.load(bg_path)

    def _initialize_ui(self):
        """Initializes all UI components."""
        width, height = self.display_manager.get_size()
        pygame.display.set_caption(t("system.main_window_title"))

        # Particles disabled for rail shooter mode
        self.particles = None

        # Buttons
        self._create_buttons()

        # Layout update
        self._update_layout()

    def _create_buttons(self):
        """Creates menu buttons with their callbacks."""
        labels = [
            t("menu.play"),
            t("menu.options"),
            t("menu.quit")
        ]

        callbacks = [
            self._on_play,
            self._on_options,
            self._on_quit
        ]

        select_sound = self.audio_manager.get_select_sound()

        # Create buttons with temporary positions
        self.buttons = [
            Button(label, 0, 0, 100, 50, callback, select_sound)
            for label, callback in zip(labels, callbacks)
        ]

    def _update_layout(self):
        """Updates the layout of all components."""
        width, height = self.display_manager.get_size()

        # Recalculate button layout
        layout = LayoutManager.calculate_button_layout(width, height, len(self.buttons))

        for i, button in enumerate(self.buttons):
            x = layout['btn_x']
            y = layout['start_y'] + i * (layout['btn_h'] + layout['btn_gap'])
            button.update_position(x, y, layout['btn_w'], layout['btn_h'])

        # Update fonts
        self.menu_font = pygame.font.SysFont("Arial", layout['font_size'], bold=True)

        # Resize background
        self.bg_scaled = pygame.transform.scale(self.bg_original, (width, height))

        self.state.clear_layout_dirty()

    def _update_button_labels(self):
        """Updates button labels with current translations."""
        labels = [
            t("menu.play"),
            t("menu.options"),
            t("menu.credits"),
            t("menu.help"),
            t("menu.scores"),
            t("menu.quit")
        ]
        for button, label in zip(self.buttons, labels):
            button.text = label

    # ========== Button callbacks ==========

    def _on_play(self):
        """Starts the game."""
        # Launch the rail shooter directly.
        self.audio_manager.play_music(MUSIC_IN_GAME)
        run_rail_shooter(window=self.surface, audio_manager=self.audio_manager)
        # Restore the main menu theme when the game ends.
        self.audio_manager.play_music(MUSIC_MAIN_THEME)



    def _on_options(self):
        """Shows the options window with crash protection."""
        try:
            show_options_window()
        except Exception as e:
            # Si les options plantent, afficher l'écran bleu
            try:
                from src.ui.arcade_error import show_error_screen
                show_error_screen(
                    message="Erreur dans les options système",
                    code="0x000OPT99",
                    auto_exit=5.0
                )
            except Exception:
                # Fallback ultime - message simple
                print("ERREUR: Les options ne sont pas disponibles")
                print("Continuez à jouer normalement...")

    def _on_quit(self):
        """Quits the application."""
        self.state.running = False

    # ========== Event handling ==========

    def _handle_events(self):
        """Handles all Pygame events."""
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            # Handle gamepad connection/disconnection events
            if self.gamepad_manager:
                try:
                    if self.gamepad_manager.handle_connection_events(event):
                        continue
                except Exception:
                    pass

            if event.type == pygame.QUIT:
                self.state.running = False

            elif event.type == pygame.KEYDOWN:
                self._handle_keydown(event)

            elif event.type == pygame.JOYBUTTONDOWN:
                self._handle_gamepad_button(event)

            elif event.type == pygame.VIDEORESIZE:
                self._handle_resize(event)

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self._handle_mouse_down(mouse_pos)

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self._handle_mouse_up(mouse_pos)

    def _handle_gamepad_button(self, event):
        """Handles gamepad button events."""
        try:
            from src.managers.gamepad_manager import GamepadButtons

            # A button (Cross on PS) - Select/Confirm
            if event.button == GamepadButtons.A:
                # Simulate mouse click on the first button if available
                if self.buttons:
                    self.buttons[0].callback()

            # B button (Circle on PS) - Back/Cancel
            elif event.button == GamepadButtons.B:
                if self.display_manager.is_fullscreen:
                    self.display_manager.toggle_fullscreen()
                else:
                    self.state.running = False

            # Start button - Play game
            elif event.button == GamepadButtons.START:
                self._on_play()

        except ImportError:
            pass

    def _handle_keydown(self, event):
        """Handles keyboard events with menu navigation."""
        if event.key == pygame.K_ESCAPE:
            if self.display_manager.is_fullscreen:
                self.display_manager.toggle_fullscreen()
            else:
                self.state.running = False

        elif event.key == pygame.K_F11:
            self.display_manager.toggle_fullscreen()
            
        # Navigation clavier dans le menu
        elif event.key in (pygame.K_UP, pygame.K_w):
            if self.buttons:
                self.selected_button_index = (self.selected_button_index - 1) % len(self.buttons)
                
        elif event.key in (pygame.K_DOWN, pygame.K_s):
            if self.buttons:
                self.selected_button_index = (self.selected_button_index + 1) % len(self.buttons)
                
        elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
            if self.buttons and self.selected_button_index < len(self.buttons):
                selected_button = self.buttons[self.selected_button_index]
                selected_button.callback()  # Appeler directement le callback

    def _handle_resize(self, event):
        """Handles window resizing."""
        if self.display_manager.handle_resize(event.w, event.h):
            self.state.schedule_resize(event.w, event.h)
            self.state.mark_layout_dirty()
            if self.particles is not None:
                self.particles.resize(event.w, event.h)

    def _handle_mouse_down(self, mouse_pos):
        """Handles mouse click."""
        for button in self.buttons:
            if button.rect.collidepoint(mouse_pos):
                self.state.handle_button_press(button)
                break

    def _handle_mouse_up(self, mouse_pos):
        """Handles mouse button release."""
        pressed = self.state.button_animator.pressed_button
        self.state.handle_button_release(pressed, mouse_pos, t("menu.quit"))

    # ========== Rendering ==========

    def _render(self, dt: float):
        """Performs complete menu rendering."""
        mouse_pos = pygame.mouse.get_pos()

        # Background
        self.surface.blit(self.bg_scaled, (0, 0))

        # Particles disabled

        # Buttons avec surbrillance pour navigation clavier
        for i, button in enumerate(self.buttons):
            is_pressed = self.state.button_animator.is_pressed(button)
            
            # Surbrillance pour le bouton sélectionné au clavier
            if i == self.selected_button_index:
                highlight_rect = pygame.Rect(
                    button.rect.x - 8, button.rect.y - 8,
                    button.rect.width + 16, button.rect.height + 16
                )
                pygame.draw.rect(self.surface, (255, 215, 0, 100), highlight_rect, 4, border_radius=8)
            
            button.draw(self.surface, mouse_pos, pressed=is_pressed, font=self.menu_font)

        # Version and dev mode indicator
        self._render_version_info()
        
        pygame.display.update()



    def _render_version_info(self):
        """Displays version and dev mode indicator in the bottom right corner."""
        width, height = self.display_manager.get_size()

        # Get version and dev mode status
        version = get_project_version()
        dev_mode = is_dev_mode_enabled()

        # Version text
        version_text = f"v{version}"
        if dev_mode:
            version_text += " [DEV]"

        # Use smaller font for version display
        version_font = pygame.font.SysFont("Arial", 12, bold=False)
        
        # Shadow for version text
        shadow_color = (40, 40, 40) if not dev_mode else (100, 0, 0)  # Dark red shadow for dev mode
        shadow = version_font.render(version_text, True, shadow_color)
        shadow_rect = shadow.get_rect(bottomright=(width - 8, height - 8))
        self.surface.blit(shadow, shadow_rect)

        # Main version text
        text_color = (200, 200, 150) if not dev_mode else (255, 100, 100)  # Light red for dev mode
        version_surf = version_font.render(version_text, True, text_color)
        version_rect = version_surf.get_rect(bottomright=(width - 6, height - 6))
        self.surface.blit(version_surf, version_rect)

    # ========== Main loop ==========

    def run(self):
        """Main menu loop."""
        clock = pygame.time.Clock()

        try:
            while self.state.running:
                # Delta time
                dt = clock.tick(60) / 1000.0

                # State update
                resize_result = self.state.update(dt)
                if resize_result:
                    try:
                        settings.apply_resolution(resize_result[0], resize_result[1])
                        print(f"💾 Resolution saved: {resize_result[0]}x{resize_result[1]}")
                    except Exception as e:
                        print(f"⚠️ Resolution save error: {e}")

                # Sync with configuration
                if self.display_manager.update_from_config():
                    self.state.mark_layout_dirty()

                # Check for volume changes
                self.volume_watcher.check_for_changes()
                
                # Apply display changes
                if self.display_manager.dirty:
                    self.surface = self.display_manager.apply_changes()
                    self.state.mark_layout_dirty()

                # Check if the language changed earlier during state.update()
                # (MenuState sets language_changed so we only refresh once here.)
                if getattr(self.state, 'language_changed', False):
                    self._update_button_labels()
                    pygame.display.set_caption(t("system.main_window_title"))
                    # reset the signal so subsequent loops don't re-run this
                    self.state.language_changed = False

                # Recalculate layout if needed
                current_size = self.surface.get_size()
                display_size = self.display_manager.get_size()
                if current_size != display_size or self.state.layout_dirty:
                    self.display_manager.width, self.display_manager.height = current_size
                    self._update_layout()

                # Event handling
                self._handle_events()

                # Rendering
                if self.state.running:
                    self._render(dt)

        finally:
            if self.created_local_window:
                self.audio_manager.stop_music()
                pygame.quit()
                sys.exit()


def main_menu(win=None):
    """
    Main menu entry point.

    Args:
        win: Existing Pygame surface (optional)
    """
    menu = MainMenu(win)
    menu.run()


# Program entry point
if __name__ == "__main__":
    # Launch menu
    try:
        main_menu()
    except Exception as e:
        import traceback
        traceback.print_exc()
        # Utiliser l'écran bleu au lieu du crash popup
        try:
            from src.ui.arcade_error import show_error_screen
            show_error_screen(
                message="Erreur critique du système", 
                code="0x00000000",
                auto_exit=10.0
            )
        except Exception:
            print(f"ERREUR FATALE: {e}")
            sys.exit(1)
