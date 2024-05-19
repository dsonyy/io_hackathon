"""
Starting Template

Once you have learned how to use classes, you can begin your program with this
template.

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.starting_template
"""
import arcade

from hackathon.game.level.minigame.mathgame.math_logic import MathLevel
from .game import State
from .game.level import Level
from .game.player import Player
from .game.level.menu import Menu
from .game.level.world import World
from .game.level.electronics import Electronics


SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
SCREEN_TITLE = "Starting Template"

LEVELS: dict[State, type[Level]] = {
    State.Menu: Menu,
    State.World: World,
    State.MinigameElectro: Electronics,
    State.MinigameMath: MathLevel
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

    def __init__(self, width, height, title):
        super().__init__(width, height, title, fullscreen=True)

        arcade.set_background_color(arcade.color.AMAZON)
        
        # TODO: this is a workaround to pass and control window stuff from the game states
        self.window = self
        
        self.levels = dict()
        # If you have sprite lists, you should create them here,
        # and set them to None

    def switch_to_level(self, state: State) -> None:
        if state not in self.levels:
            level = LEVELS[state](self)
            level.setup()
            self.levels[state] = level

        self.state = state
        self.level = level

    def setup(self):
        """ Set up the game variables. Call to re-start the game. """
        # Create your sprites and sprite lists here

        self.switch_to_level(State.MinigameMath)

        # Reset all loaded levels
        for level in self.levels.values():
            level.setup()

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
