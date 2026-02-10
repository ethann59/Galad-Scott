# -*- coding: utf-8 -*-
"""
Disabled tutorial manager - all tutorial functions are no-ops.
"""
from typing import Optional, Dict, List, Any


class TutorialManager:
    """
    Disabled tutorial manager - does nothing when called.
    This allows the game to run without tutorial/tips functionality.
    """

    def __init__(self, config_manager=None):
        """Initialize disabled tutorial manager."""
        self.config_manager = config_manager
        self.active_notification = None
        self.is_finished = True
        self.is_skipped = True
        self.show_tutorial = False
        self.current_tip_key = None
        self.steps = []
        self.read_tips = set()

    def get_tip_by_key(self, key: str) -> None:
        """Returns None - tips are disabled."""
        return None

    def show_tip(self, key: str) -> None:
        """Does nothing - tips are disabled."""
        pass

    def check_event_tutorial(self, event_name: str, **kwargs) -> None:
        """Does nothing - tutorials are disabled."""
        pass

    def advance_step(self) -> None:
        """Does nothing - tutorials are disabled."""
        pass

    def check_game_state(self, **context) -> None:
        """Does nothing - tutorials are disabled."""
        pass

    def skip_tutorial(self) -> None:
        """Does nothing - already skipped."""
        pass

    def finish_tutorial(self) -> None:
        """Does nothing - already finished."""
        pass

    def update(self, dt: float) -> None:
        """Does nothing - no updates needed."""
        pass

    def render(self, surface) -> None:
        """Does nothing - no rendering needed."""
        pass

    def handle_event(self, event) -> bool:
        """Does nothing - returns False."""
        return False

    def handle_notification_event(self, event, screen_width: int, screen_height: int) -> None:
        """Does nothing - no notifications to handle."""
        pass

    def draw(self, surface) -> None:
        """Does nothing - no drawing needed."""
        pass

    def is_active(self) -> bool:
        """Returns False - no tutorials active."""
        return False

    def reset(self) -> None:
        """Does nothing - nothing to reset."""
        pass
