import arcade
from abc import ABC, abstractmethod

from ..player.player import Player

class State(ABC):
    '''
    An individual level's state representation.
    Extend this as an enum to represent and handle level's logic.
    '''

class Level(ABC):
    '''
    An abstract base class to represent game level.
    Define all minigames, worldmap and main menu extending this.
    '''

    sprites: arcade.SpriteList
    player: Player
    state: State

    @abstractmethod
    def setup(self) -> None:
        pass

    @abstractmethod
    def draw(self) -> None:
        pass

    @property
    @abstractmethod
    def finished(self) -> bool:
        pass

    @abstractmethod
    def on_update(self, delta_time: int) -> bool:
        pass

    @abstractmethod
    def on_key_pressed(self, key: int, modifiers: int) -> bool:
        pass

    @abstractmethod
    def on_key_released(self, key: int, modifiers: int) -> bool:
        pass

    @abstractmethod
    def on_mouse_motion(self, x: int, y: int, delta_x: int, delta_y: int):
        """
        Called whenever the mouse moves.
        """
        pass

    @abstractmethod
    def on_mouse_press(self, x: int, y: int, button: int, key_modifiers: int):
        """
        Called when the user presses a mouse button.
        """
        pass

    @abstractmethod
    def on_mouse_release(self, x: int, y: int, button: int, key_modifiers: int):
        """
        Called when a user releases a mouse button.
        """
        pass
