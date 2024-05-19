"""
Starting Template

Once you have learned how to use classes, you can begin your program with this
template.

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.starting_template
"""
from typing import Literal
import arcade

from hackathon.game.level.minigame.mathgame.mathgame import MathLevel
from .game import State
from .game.level import Level
from .game.player import Player
from .game.level.menu import Menu
from .game.level.world import World
from .game.level.electronics import Electronics
from .game.level.menu.endscreen import EndScreen


SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
SCREEN_TITLE = "Starting Template"

LEVELS: dict[State, type[Level]] = {
    State.Menu: Menu,
    State.World: World,
    State.MinigameElectro: Electronics,
    State.MinigameMath: MathLevel,
    State.EndScreen: EndScreen
}


class MyGame(arcade.Window):
    """
    Main application class.

    NOTE: Go ahead and delete the methods you don't need.
    If you do need a method, delete the 'pass' and replace it
    with your own code. Don't leave 'pass' in this program.
    """

    state: State  # game state, corresponds to level
    level: Level  # Level control object

    levels: dict[State, Level]

    plot: dict[Literal['ects'], int]
    classes_completed: dict[State, bool]

    names: list[str]

    def __init__(self, width, height, title):
        super().__init__(width, height, title, fullscreen=True)

        arcade.set_background_color(arcade.color.ALMOND)

        self.window = self
        self.levels = dict()

        self.plot = {}
        self.classes_completed = {}

        self.names = []

    def add_ects(self) -> None:
        self.plot['ects'] += 1

    def switch_to_level(self, state: State) -> None:
        level = self.levels.get(state, None)

        if level is None:
            level = LEVELS[state](self)
            level.setup()

        self.state = state
        self.level = level

        self.update(1)

    def setup(self):
        """ Set up the game variables. Call to re-start the game. """
        # Create your sprites and sprite lists here

        self.plot = {
            'ects': 0
        }

        self.classes_completed = {
            State.MinigameAlgo: False,
            State.MinigameElectro: False,
            State.MinigameMath: False
        }

        self.switch_to_level(State.Menu)

        # Reset all loaded levels
        for level in self.levels.values():
            level.setup()

    def on_resize(self, width: float, height: float) -> None:
        if hasattr(self.level, 'on_resize'):
            self.level.on_resize(width, height)

    def on_draw(self):
        """
        Render the screen.
        """

        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        self.clear()
        self.level.draw()

        # Call draw() on all your sprite lists below

    def on_update(self, delta_time: int):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        self.level.on_update(delta_time)

    def on_key_press(self, key: int, key_modifiers: int):
        """
        Called whenever a key on the keyboard is pressed.

        For a full list of keys, see:
        https://api.arcade.academy/en/latest/arcade.key.html
        """
        self.level.on_key_press(key, key_modifiers)

    def on_key_release(self, key: int, key_modifiers: int):
        """
        Called whenever the user lets off a previously pressed key.
        """
        self.level.on_key_release(key, key_modifiers)

    def on_mouse_motion(self, x: int, y: int, delta_x: int, delta_y: int):
        """
        Called whenever the mouse moves.
        """
        self.level.on_mouse_motion(x, y, delta_x, delta_y)

    def on_mouse_press(self, x: int, y: int, button: int, key_modifiers: int):
        """
        Called when the user presses a mouse button.
        """
        self.level.on_mouse_press(x, y, button, key_modifiers)

    def on_mouse_release(self, x: int, y: int, button: int, key_modifiers: int):
        """
        Called when a user releases a mouse button.
        """
        self.level.on_mouse_release(x, y, button, key_modifiers)


def main():
    """ Main function """
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
