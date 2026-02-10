"""
Tests pour Galad Scott Rail Shooter
"""
import pytest
import pygame
import threading
import time
from unittest.mock import Mock, patch

class TestRailShooter:
    """Tests pour le moteur rail shooter"""
    
    def setup_method(self):
        """Configuration pour chaque test"""
        pygame.init()
        
    def test_rail_shooter_import(self):
        """Test d'importation du rail shooter"""
        from src.rail_shooter import RailShooterEngine, run_rail_shooter
        assert RailShooterEngine is not None
        assert run_rail_shooter is not None
        
    def test_rail_shooter_init(self):
        """Test d'initialisation du rail shooter"""
        from src.rail_shooter import RailShooterEngine
        
        # Mock window pour éviter l'ouverture d'une vraie fenêtre
        mock_surface = Mock()
        mock_surface.get_size.return_value = (800, 600)
        
        engine = RailShooterEngine(window=mock_surface)
        assert engine.window == mock_surface
        assert engine.running == True
        assert engine.score == 0
        assert engine.game_over == False
        
    @patch('pygame.display.set_mode')
    @patch('pygame.display.set_caption')
    def test_rail_shooter_creation_no_window(self, mock_caption, mock_set_mode):
        """Test création rail shooter sans fenêtre existante"""
        from src.rail_shooter import RailShooterEngine
        
        mock_surface = Mock()
        mock_surface.get_size.return_value = (1024, 768)
        mock_set_mode.return_value = mock_surface
        
        engine = RailShooterEngine()
        assert engine.created_local_window == False  # Pas encore initialisé
        
    def test_enemy_spawn_parameters(self):
        """Test des paramètres de spawn des ennemis"""
        from src.rail_shooter import RailShooterEngine
        
        mock_surface = Mock()
        mock_surface.get_size.return_value = (800, 600)
        
        engine = RailShooterEngine(window=mock_surface)
        assert engine.spawn_interval > 0
        assert engine.max_enemies > 0
        
    def test_name_input_variables(self):
        """Test des variables de saisie de nom arcade"""
        from src.rail_shooter import RailShooterEngine
        
        mock_surface = Mock()
        mock_surface.get_size.return_value = (800, 600)
        
        engine = RailShooterEngine(window=mock_surface)
        assert hasattr(engine, '_entering_name')
        assert hasattr(engine, '_name_input')
        assert hasattr(engine, '_available_chars')
        assert hasattr(engine, '_game_over_pause')
        
    def teardown_method(self):
        """Nettoyage après chaque test"""
        pygame.quit()


class TestArcadeMenus:
    """Tests pour les menus arcade"""
    
    def setup_method(self):
        """Configuration pour chaque test"""
        pygame.init()
        
    def test_arcade_menus_import(self):
        """Test d'importation des menus arcade"""
        from src.functions.arcade_menus import show_arcade_help, show_arcade_credits, show_arcade_scores
        assert show_arcade_help is not None
        assert show_arcade_credits is not None  
        assert show_arcade_scores is not None
        
    @patch('pygame.display.get_surface')
    def test_arcade_help_no_surface(self, mock_get_surface):
        """Test aide arcade sans surface d'affichage"""
        from src.functions.arcade_menus import show_arcade_help
        
        mock_get_surface.return_value = None
        
        # Ne doit pas lever d'exception
        show_arcade_help()
        
    @patch('pygame.display.get_surface')
    def test_arcade_credits_no_surface(self, mock_get_surface):
        """Test crédits arcade sans surface d'affichage"""
        from src.functions.arcade_menus import show_arcade_credits
        
        mock_get_surface.return_value = None
        
        # Ne doit pas lever d'exception
        show_arcade_credits()
        
    def test_arcade_scores_empty_list(self):
        """Test scores arcade avec liste vide"""
        from src.functions.arcade_menus import show_arcade_scores
        
        with patch('pygame.display.get_surface') as mock_get_surface:
            mock_get_surface.return_value = None
            
            # Ne doit pas lever d'exception avec liste vide
            show_arcade_scores([])
            show_arcade_scores(["Player1    1000", "Player2     500"])
        
    def teardown_method(self):
        """Nettoyage après chaque test"""
        pygame.quit()


class TestArcadeError:
    """Tests pour le système d'erreur arcade"""
    
    def test_arcade_error_import(self):
        """Test d'importation du système d'erreur arcade"""
        from src.ui.arcade_error import ArcadeErrorScreen, show_error_screen
        assert ArcadeErrorScreen is not None
        assert show_error_screen is not None
        
    def test_arcade_error_screen_creation(self):
        """Test création écran d'erreur arcade"""
        from src.ui.arcade_error import ArcadeErrorScreen
        
        # Test avec paramètres par défaut
        screen = ArcadeErrorScreen("Test error", 1.0, "0x12345")
        assert screen.message == "Test error"
        assert screen.auto_exit_time == 1.0
        assert screen.error_code == "0x12345"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])