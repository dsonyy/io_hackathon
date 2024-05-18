"""
Starting Template

Once you have learned how to use classes, you can begin your program with this
template.

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.starting_template
"""
import arcade


SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
SCREEN_TITLE = "Starting Template"


class MyGame(arcade.Window):
    """
    Main application class.

    NOTE: Go ahead and delete the methods you don't need.
    If you do need a method, delete the 'pass' and replace it
    with your own code. Don't leave 'pass' in this program.
    """

    def __init__(self, width, height, title, n_gates=4):
        super().__init__(width, height, title, fullscreen=True)

        self.all_sprites = arcade.SpriteList()
        self.blank_spaces = arcade.SpriteList()
        self.signs = arcade.SpriteList()
        self.held_blocks = None
        self.held_blocks_original_position = None
        self.number_of_gates = n_gates

        self.is_player_grabbed = False
        self.grabbed_sprite = None
        self.is_correct = False

        self.wires_group = [[0, 1, 0], [0, 0], [0, 1, 0], [0, 0], [0, 0, 0], [0, 0, 0]]

        # If you have sprite lists, you should create them here,
        # and set them to None


    def setup(self):
        """ Set up the game variables. Call to re-start the game. """

        arcade.set_background_color(arcade.color.AMAZON)

        # Create your sprites and sprite lists here

        # self.player = arcade.Sprite("../../assets/dirt.png", 3)
        # self.player.center_y = self.height / 2
        # self.player.left = 10
        # self.all_sprites.append(self.player)

        self.held_blocks = []  # kabelki maja priorytet
        # self.held_blocks_original_position = []

        # for i in range(self.number_of_gates):

        self.draw_gates()

        self.draw_blank_spaces()

        self.signs_draw()


        pass

    def on_draw(self):
        """
        Render the screen.
        """

        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        self.clear()

        # Call draw() on all your sprite lists below

        arcade.start_render()
        self.blank_spaces.draw()
        self.all_sprites.draw()
        self.signs.draw()
        self.draw_lamp()
        self.draw_wires()
        arcade.draw_rectangle_outline(760, 500, 1200, 600,
                                      arcade.color.BLACK, 5)


    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        self.all_sprites.update()
        # super().update(delta_time)
        pass

    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.

        For a full list of keys, see:
        https://api.arcade.academy/en/latest/arcade.key.html
        """
        # if key == 100:
        #     self.player.change_x = 10
        # if key == 97:
        #     self.player.change_x = -5
        pass

    def on_key_release(self, key, key_modifiers):
        """
        Called whenever the user lets off a previously pressed key.
        """
        pass

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        """
        Called whenever the mouse moves.
        """
        # if self.is_player_grabbed:
        #     self.player.center_x += delta_x
        #     self.player.center_y += delta_y

        if self.grabbed_sprite:
            self.grabbed_sprite.center_x += delta_x
            self.grabbed_sprite.center_y += delta_y
        pass

    def on_mouse_press(self, x, y, button, key_modifiers):
        """
        Called when the user presses a mouse button.
        """
        print(f"{x} {y}")
        # self.player.center_x = x
        # self.player.center_y = y
        under_mouse = arcade.get_sprites_at_point((x, y), self.all_sprites)
        if under_mouse:
            self.grabbed_sprite = under_mouse[0]
            blank = arcade.get_sprites_at_point((x, y), self.blank_spaces)
            if blank:
                blank[0].occupant = None
            # print(self.grabbed_sprite.gate_type)
        pass

    def on_mouse_release(self, x, y, button, key_modifiers):
        """
        Called when a user releases a mouse button.
        """
        # self.is_player_grabbed = False
        blank_space = arcade.get_sprites_at_point((x, y), self.blank_spaces)
        if blank_space and self.grabbed_sprite:
            blank = blank_space[0]
            if blank.occupant is not None:
                blank.occupant.center_x = blank.occupant.default_x
                blank.occupant.center_y = blank.occupant.default_y
            self.grabbed_sprite.center_x = blank.center_x
            self.grabbed_sprite.center_y = blank.center_y
            blank.occupant = self.grabbed_sprite
        elif self.grabbed_sprite:
            self.grabbed_sprite.center_x = self.grabbed_sprite.default_x
            self.grabbed_sprite.center_y = self.grabbed_sprite.default_y
        self.grabbed_sprite = None
        pass

    def draw_gates(self):
        gates_height = self.height // 6

        gate = arcade.Sprite("../../assets/xor_gate.png")
        gate.gate_type = "xor"
        gate.top = gates_height
        gate.left = self.width // 7
        gate.default_x = gate.center_x
        gate.default_y = gate.center_y
        self.all_sprites.append(gate)

        gate = arcade.Sprite("../../assets/not_gate.png")
        gate.top = gates_height
        gate.gate_type = "not"
        gate.left = self.width // 7 * 2
        gate.default_x = gate.center_x
        gate.default_y = gate.center_y
        self.all_sprites.append(gate)

        gate = arcade.Sprite("../../assets/and_gate.png")
        gate.top = gates_height
        gate.gate_type = "and"
        gate.left = self.width // 7 * 3
        gate.default_x = gate.center_x
        gate.default_y = gate.center_y
        self.all_sprites.append(gate)

        gate = arcade.Sprite("../../assets/and_gate.png")
        gate.top = gates_height
        gate.gate_type = "and"
        gate.left = self.width // 7 * 4
        gate.default_x = gate.center_x
        gate.default_y = gate.center_y
        self.all_sprites.append(gate)

        gate = arcade.Sprite("../../assets/cable_gate.png")
        gate.top = gates_height
        gate.gate_type = "cable"
        gate.left = self.width // 7 * 5
        gate.default_x = gate.center_x
        gate.default_y = gate.center_y
        self.all_sprites.append(gate)

        gate = arcade.Sprite("../../assets/or_gate.png")
        gate.top = gates_height
        gate.gate_type = "or"
        gate.left = self.width // 7 * 6
        gate.default_x = gate.center_x
        gate.default_y = gate.center_y
        self.all_sprites.append(gate)


    def draw_blank_spaces(self):
        blank = arcade.Sprite("../../assets/blank_space.png")
        blank.center_x = 475
        blank.center_y = 700
        blank.occupant = None
        self.blank_spaces.append(blank)

        blank = arcade.Sprite("../../assets/blank_space.png")
        blank.center_x = 475
        blank.center_y = 500
        blank.occupant = None
        self.blank_spaces.append(blank)

        blank = arcade.Sprite("../../assets/blank_space.png")
        blank.center_x = 475
        blank.center_y = 300
        blank.occupant = None
        self.blank_spaces.append(blank)

        blank = arcade.Sprite("../../assets/blank_space.png")
        blank.center_x = 780
        blank.center_y = 400
        blank.occupant = None
        self.blank_spaces.append(blank)

        blank = arcade.Sprite("../../assets/blank_space.png")
        blank.center_x = 780
        blank.center_y = 600
        blank.occupant = None
        self.blank_spaces.append(blank)

        blank = arcade.Sprite("../../assets/blank_space.png")
        blank.center_x = 1074
        blank.center_y = 500
        blank.occupant = None
        self.blank_spaces.append(blank)
        pass

    def draw_wires(self):
        arcade.draw_line(160, 748, 375, 729, arcade.color.BLACK, 5)
        arcade.draw_line(160, 671, 375, 677, arcade.color.BLACK, 5)
        arcade.draw_line(160, 500, 375, 500, arcade.color.BLACK, 5)
        arcade.draw_line(160, 315, 375, 327, arcade.color.BLACK, 5)
        arcade.draw_line(160, 253, 375, 277, arcade.color.BLACK, 5)

        arcade.draw_line(575, 709, 680, 610, arcade.color.BLACK, 5)
        arcade.draw_line(575, 506, 680, 425, arcade.color.BLACK, 5)
        arcade.draw_line(575, 303, 680, 375, arcade.color.BLACK, 5)

        arcade.draw_line(880, 602, 974, 523, arcade.color.BLACK, 5)
        arcade.draw_line(880, 397, 974, 482, arcade.color.BLACK, 5)

        arcade.draw_line(1175, 500, 1360, 500, arcade.color.BLACK, 5)

    # def check_

    def draw_lamp(self):
        if not self.is_correct:
            arcade.draw_circle_filled(1420, 600, 20, arcade.color.RED)
            arcade.draw_line(1420, 500, 1420, 580, arcade.color.RED, 5)
            arcade.draw_line(1360, 500, 1420, 500, arcade.color.RED, 5)
        else:
            arcade.draw_circle_filled(1420, 600, 20, arcade.color.GREEN)
            arcade.draw_line(1420, 500, 1420, 580, arcade.color.GREEN, 5)
            arcade.draw_line(1360, 500, 1420, 500, arcade.color.GREEN, 5)

    def signs_draw(self):
        sign = arcade.Sprite("../../assets/minus_power_off.png")
        sign.center_x = 90
        sign.center_y = 745
        self.signs.append(sign)

        sign = arcade.Sprite("../../assets/plus_power_on.png")
        sign.center_x = 90
        sign.center_y = 680
        self.signs.append(sign)

        sign = arcade.Sprite("../../assets/minus_power_off.png")
        sign.center_x = 90
        sign.center_y = 500
        self.signs.append(sign)

        sign = arcade.Sprite("../../assets/minus_power_off.png")
        sign.center_x = 90
        sign.center_y = 315
        self.signs.append(sign)

        sign = arcade.Sprite("../../assets/plus_power_on.png")
        sign.center_x = 90
        sign.center_y = 260
        self.signs.append(sign)


def main():
    """ Main function """
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    # https://api.arcade.academy/en/latest/tutorials/card_game/index.html
    main()
