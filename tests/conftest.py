#!/usr/bin/env python3
"""
Configuration commune pour les tests pytest du rail shooter Galad Scott
"""

import pytest
import pygame
import sys
import os

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


@pytest.fixture(scope="session", autouse=True)
def pygame_init():
    """Initialize pygame pour tous les tests nécessitant l'affichage."""
    pygame.init()
    # Mode headless minimal pour les tests
    pygame.display.set_mode((1, 1), pygame.HIDDEN)
    yield
    pygame.quit()


@pytest.fixture
def test_surface():
    """Crée une surface de test pour les tests de rendu."""
    return pygame.Surface((800, 600))


@pytest.fixture  
def mock_config():
    """Configuration de test simulée."""
    return {
        'window_width': 800,
        'window_height': 600,
        'fullscreen': False,
        'language': 'fr',
        'volume': 0.5,
        'vsync': False
    }


@pytest.fixture
def mock_clock():
    """Clock pygame pour les tests de timing."""
    return pygame.time.Clock()


@pytest.fixture
def sample_events():
    """Événements pygame typiques pour les tests."""
    return [
        pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_SPACE}),
        pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_ESCAPE}),
        pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'button': 1, 'pos': (400, 300)})
    ]