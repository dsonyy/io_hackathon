"""
Starting Template

Once you have learned how to use classes, you can begin your program with this
template.

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.starting_template
"""
import time

import arcade
import arcade.gui

from .level import Level
from .. import State

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
SCREEN_TITLE = "Starting Template"

BLACK = arcade.color.BLACK
RED = arcade.color.RED


class Electronics(Level):
    """
    Main application class.

    NOTE: Go ahead and delete the methods you don't need.
    If you do need a method, delete the 'pass' and replace it
    with your own code. Don't leave 'pass' in this program.
    """


    # def __init__(self, width, height, title, n_gates=4):
    def __init__(self, window: arcade.Window) -> None:


        self.window = window
        # self.all_sprites = arcade.SpriteList()
        # self.blank_spaces = arcade.SpriteList()
        # self.signs = arcade.SpriteList()
        # self.held_blocks = None
        # self.held_blocks_original_position = None

        self.level = -3

        self.wires_group = None

        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        # If you have sprite lists, you should create them here,
        # and set them to None

    def setup(self):
        """ Set up the game variables. Call to re-start the game. """
        self.all_sprites = arcade.SpriteList()
        self.blank_spaces = arcade.SpriteList()
        self.signs = arcade.SpriteList()

        self.is_player_grabbed = False
        self.grabbed_sprite = None
        self.is_correct = False
        self.is_level_complete = False
        # arcade.set_background_color(arcade.color.AMAZON)

        # Create your sprites and sprite lists here

        # self.player = arcade.Sprite("hackathon/assets/cyfrowka/dirt.png", 3)
        # self.player.center_y = self.height / 2
        # self.player.left = 10
        # self.all_sprites.append(self.player)

        # self.held_blocks_original_position = []

        # for i in range(self.number_of_gates):
        self.draw_tutorial()
        self.set_wires_groups()

        self.draw_gates()

        self.draw_blank_spaces()

        self.signs_draw()


        pass

    @property
    def finished(self) -> bool:
        return False


    def draw(self):
        """
        Render the screen.
        """
        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        self.window.clear()

        # Call draw() on all your sprite lists below

        arcade.start_render()
        if self.level < 1:
            self.all_sprites.draw()
            return

        self.blank_spaces.draw()
        self.all_sprites.draw()
        self.signs.draw()
        self.draw_lamp()
        self.draw_wires()
        arcade.draw_rectangle_outline(
            760,
            500,
            1200,
            600,
            arcade.color.BLACK,
            5
        )

        self.manager.draw()


    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        self.all_sprites.update()

        if self.is_level_complete:
            if self.level == 3:
                self.win_window()
            else:
                time.sleep(2)
                self.level += 1
                self.setup()

        if (self.level == 1 and self.wires_group[1][2]) or (self.level == 2 and self.wires_group[2][2]) or (self.level == 3 and self.wires_group[5][2]):
            self.is_correct = True

        # super().update(delta_time)
        pass

    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.

        For a full list of keys, see:
        https://api.arcade.academy/en/latest/arcade.key.html
        """
        if key == 32 and self.level < 1:
            self.level += 1
            self.setup()
        # if key == 100:
        #     print(self.wires_group)
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

    def draw_gates(self):
        gates_height = self.window.height // 6

        def level1():
            gate = arcade.Sprite("hackathon/assets/cyfrowka/xor_gate.png")
            gate.gate_type = "xor"
            gate.top = gates_height
            gate.left = self.window.width // 7
            gate.default_x = gate.center_x
            gate.default_y = gate.center_y
            self.all_sprites.append(gate)

            gate = arcade.Sprite("hackathon/assets/cyfrowka/or_gate.png")
            gate.gate_type = "or"
            gate.top = gates_height
            gate.left = self.window.width // 7 * 2
            gate.default_x = gate.center_x
            gate.default_y = gate.center_y
            self.all_sprites.append(gate)

        def level2():
            gate = arcade.Sprite("hackathon/assets/cyfrowka/cable_gate.png")
            gate.gate_type = "cable"
            gate.top = gates_height
            gate.left = self.window.width // 7
            gate.default_x = gate.center_x
            gate.default_y = gate.center_y
            self.all_sprites.append(gate)

            gate = arcade.Sprite("hackathon/assets/cyfrowka/not_gate.png")
            gate.gate_type = "not"
            gate.top = gates_height
            gate.left = self.window.width // 7 * 2
            gate.default_x = gate.center_x
            gate.default_y = gate.center_y
            self.all_sprites.append(gate)

            gate = arcade.Sprite("hackathon/assets/cyfrowka/and_gate.png")
            gate.gate_type = "and"
            gate.top = gates_height
            gate.left = self.window.width // 7 * 3
            gate.default_x = gate.center_x
            gate.default_y = gate.center_y
            self.all_sprites.append(gate)

        def level3():
            gate = arcade.Sprite("hackathon/assets/cyfrowka/xor_gate.png")
            gate.gate_type = "xor"
            gate.top = gates_height
            gate.left = self.window.width // 7
            gate.default_x = gate.center_x
            gate.default_y = gate.center_y
            self.all_sprites.append(gate)

            gate = arcade.Sprite("hackathon/assets/cyfrowka/not_gate.png")
            gate.top = gates_height
            gate.gate_type = "not"
            gate.left = self.window.width // 7 * 2
            gate.default_x = gate.center_x
            gate.default_y = gate.center_y
            self.all_sprites.append(gate)

            gate = arcade.Sprite("hackathon/assets/cyfrowka/and_gate.png")
            gate.top = gates_height
            gate.gate_type = "and"
            gate.left = self.window.width // 7 * 3
            gate.default_x = gate.center_x
            gate.default_y = gate.center_y
            self.all_sprites.append(gate)

            gate = arcade.Sprite("hackathon/assets/cyfrowka/and_gate.png")
            gate.top = gates_height
            gate.gate_type = "and"
            gate.left = self.window.width // 7 * 4
            gate.default_x = gate.center_x
            gate.default_y = gate.center_y
            self.all_sprites.append(gate)

            gate = arcade.Sprite("hackathon/assets/cyfrowka/cable_gate.png")
            gate.top = gates_height
            gate.gate_type = "cable"
            gate.left = self.window.width // 7 * 5
            gate.default_x = gate.center_x
            gate.default_y = gate.center_y
            self.all_sprites.append(gate)

            gate = arcade.Sprite("hackathon/assets/cyfrowka/or_gate.png")
            gate.top = gates_height
            gate.gate_type = "or"
            gate.left = self.window.width // 7 * 6
            gate.default_x = gate.center_x
            gate.default_y = gate.center_y
            self.all_sprites.append(gate)

        match self.level:
            case 1:
                level1()
            case 2:
                level2()
            case 3:
                level3()


    def draw_blank_spaces(self):
        def level1():
            blank = arcade.Sprite("hackathon/assets/cyfrowka/blank_space.png")
            blank.center_x = 500
            blank.center_y = 600
            blank.occupant = None
            self.blank_spaces.append(blank)

            blank = arcade.Sprite("hackathon/assets/cyfrowka/blank_space.png")
            blank.center_x = 1000
            blank.center_y = 450
            blank.occupant = None
            self.blank_spaces.append(blank)

        def level2():
            blank = arcade.Sprite("hackathon/assets/cyfrowka/blank_space.png")
            blank.center_x = 500
            blank.center_y = 600
            blank.occupant = None
            self.blank_spaces.append(blank)

            blank = arcade.Sprite("hackathon/assets/cyfrowka/blank_space.png")
            blank.center_x = 500
            blank.center_y = 350
            blank.occupant = None
            self.blank_spaces.append(blank)

            blank = arcade.Sprite("hackathon/assets/cyfrowka/blank_space.png")
            blank.center_x = 1000
            blank.center_y = 450
            blank.occupant = None
            self.blank_spaces.append(blank)

        def level3():
            blank = arcade.Sprite("hackathon/assets/cyfrowka/blank_space.png")
            blank.center_x = 475
            blank.center_y = 700
            blank.occupant = None
            self.blank_spaces.append(blank)

            blank = arcade.Sprite("hackathon/assets/cyfrowka/blank_space.png")
            blank.center_x = 475
            blank.center_y = 500
            blank.occupant = None
            self.blank_spaces.append(blank)

            blank = arcade.Sprite("hackathon/assets/cyfrowka/blank_space.png")
            blank.center_x = 475
            blank.center_y = 300
            blank.occupant = None
            self.blank_spaces.append(blank)

            blank = arcade.Sprite("hackathon/assets/cyfrowka/blank_space.png")
            blank.center_x = 780
            blank.center_y = 600
            blank.occupant = None
            self.blank_spaces.append(blank)

            blank = arcade.Sprite("hackathon/assets/cyfrowka/blank_space.png")
            blank.center_x = 780
            blank.center_y = 400
            blank.occupant = None
            self.blank_spaces.append(blank)

            blank = arcade.Sprite("hackathon/assets/cyfrowka/blank_space.png")
            blank.center_x = 1074
            blank.center_y = 500
            blank.occupant = None
            self.blank_spaces.append(blank)


        match self.level:
            case 1:
                level1()
            case 2:
                level2()
            case 3:
                level3()

    def draw_wires(self):
        def level1():
            arcade.draw_line(160, 630, 400, 630, arcade.color.RED, 5)
            arcade.draw_line(160, 570, 400, 570, arcade.color.RED, 5)
            arcade.draw_line(160, 420, 900, 420, arcade.color.BLACK, 5)

            arcade.draw_line(600, 600, 900, 480, self.get_color_by_logic(0, 0), 5)

            arcade.draw_line(1100, 450, 1360, 500, self.get_color_by_logic(1, 1), 5)

        def level2():
            arcade.draw_line(160, 600, 400, 600, arcade.color.RED, 5)
            arcade.draw_line(160, 350, 400, 350, arcade.color.BLACK, 5)

            arcade.draw_line(600, 600, 900, 480, self.get_color_by_logic(0, 0), 5)

            arcade.draw_line(600, 350, 900, 420, self.get_color_by_logic(1, 1), 5)

            arcade.draw_line(1100, 450, 1360, 500, self.get_color_by_logic(2, 2), 5)

        def level3():
            arcade.draw_line(160, 730, 375, 730, arcade.color.BLACK, 5)
            arcade.draw_line(160, 670, 375, 670, arcade.color.RED, 5)
            arcade.draw_line(160, 500, 375, 500, arcade.color.BLACK, 5)
            arcade.draw_line(160, 325, 375, 325, arcade.color.BLACK, 5)
            arcade.draw_line(160, 270, 375, 270, arcade.color.RED, 5)


            arcade.draw_line(575, 709, 680, 600, self.get_color_by_logic(0, 0), 5)
            arcade.draw_line(575, 506, 680, 425, self.get_color_by_logic(1, 1), 5)
            arcade.draw_line(575, 303, 680, 375, self.get_color_by_logic(2, 2), 5)

            arcade.draw_line(880, 602, 974, 523, self.get_color_by_logic(3, 3), 5)
            arcade.draw_line(880, 397, 974, 482, self.get_color_by_logic(4, 4), 5)

            arcade.draw_line(1175, 500, 1360, 500, self.get_color_by_logic(5, 5), 5)

        match self.level:
            case 1:
                level1()
            case 2:
                level2()
            case 3:
                level3()

    # def check_

    def get_color_by_logic(self, blank_id, wire_group_id):
        if self.blank_spaces[blank_id] and self.blank_spaces[blank_id].occupant:
            gate = self.blank_spaces[blank_id].occupant.gate_type
            if len(self.wires_group[wire_group_id]) == 2:
                match gate:
                    case "not":
                        self.wires_group[wire_group_id][1] = not self.wires_group[wire_group_id][0]
                        i, j = self.get_next_wire_group(wire_group_id)
                        self.wires_group[i][j] = self.wires_group[wire_group_id][1]
                        return RED if self.wires_group[wire_group_id][1] else BLACK
                    case "cable":
                        self.wires_group[wire_group_id][1] = self.wires_group[wire_group_id][0]
                        i, j = self.get_next_wire_group(wire_group_id)
                        self.wires_group[i][j] = self.wires_group[wire_group_id][1]
                        return RED if self.wires_group[wire_group_id][1] else BLACK
                    case _:
                        self.wires_group[wire_group_id][1] = 0
                        i, j = self.get_next_wire_group(wire_group_id)
                        self.wires_group[i][j] = 0
                        return BLACK
            elif len(self.wires_group[wire_group_id]) == 3:
                # print(f"{wire_group_id},    {gate}")
                match gate:
                    case "and":
                        self.wires_group[wire_group_id][2] = self.wires_group[wire_group_id][0] and self.wires_group[wire_group_id][1]
                        i, j = self.get_next_wire_group(wire_group_id)
                        self.wires_group[i][j] = self.wires_group[wire_group_id][2]
                        return RED if self.wires_group[wire_group_id][2] else BLACK
                    case "or":
                        self.wires_group[wire_group_id][2] = self.wires_group[wire_group_id][0] or \
                                                             self.wires_group[wire_group_id][1]
                        i, j = self.get_next_wire_group(wire_group_id)
                        self.wires_group[i][j] = self.wires_group[wire_group_id][2]
                        return RED if self.wires_group[wire_group_id][2] else BLACK
                    case "xor":
                        self.wires_group[wire_group_id][2] = self.wires_group[wire_group_id][0] ^ \
                                                             self.wires_group[wire_group_id][1]
                        i, j = self.get_next_wire_group(wire_group_id)
                        self.wires_group[i][j] = self.wires_group[wire_group_id][2]
                        return RED if self.wires_group[wire_group_id][2] else BLACK
                    case _:
                        self.wires_group[wire_group_id][2] = 0
                        i, j = self.get_next_wire_group(wire_group_id)
                        self.wires_group[i][j] = self.wires_group[wire_group_id][2]
                        return BLACK
        elif len(self.wires_group[wire_group_id]) == 2:
            self.wires_group[wire_group_id][1] = 0
            i, j = self.get_next_wire_group(wire_group_id)
            self.wires_group[i][j] = 0
            return BLACK
        else:
            self.wires_group[wire_group_id][2] = 0
            i, j = self.get_next_wire_group(wire_group_id)
            self.wires_group[i][j] = self.wires_group[wire_group_id][2]
            return BLACK

    def get_next_wire_group(self, id):
        if self.level == 1:
            match id:
                case 0: return 1, 0
                case 1: return 1, 2
        elif self.level == 2:
            match id:
                case 0: return 2, 0
                case 1: return 2, 1
                case 2: return 2, 2
        elif self.level == 3:
            match id:
                case 0: return 3, 0
                case 1: return 4, 0
                case 2: return 4, 1
                case 3: return 5, 0
                case 4: return 5, 1
                case 5: return 5, 2



    def draw_lamp(self):
        if not self.is_correct:
            arcade.draw_circle_filled(1420, 600, 20, arcade.color.RED)
            arcade.draw_line(1420, 500, 1420, 580, arcade.color.BLACK, 5)
            arcade.draw_line(1360, 500, 1420, 500, arcade.color.BLACK, 5)
        else:
            arcade.draw_circle_filled(1420, 600, 20, arcade.color.GREEN)
            arcade.draw_line(1420, 500, 1420, 580, arcade.color.RED, 5)
            arcade.draw_line(1360, 500, 1420, 500, arcade.color.RED, 5)
            self.is_level_complete = True


    def win_window(self):
        message_box = arcade.gui.UIMessageBox(
            width=300,
            height=200,
            message_text=(
                "Ja używam glukoza. "
                "Glokoza glukoza 4 używa myśle 2 opcje "
                "I każda chce użyć najwieksze opcje, pierwsza lub druga"
            ),
            callback=self.on_message_box_close,
            buttons=["Jupijajej!"]
        )

        self.manager.add(message_box)

    def on_message_box_close(self, button_text):
        # make action after OK | windows switch to lvl main
        # print(f"User pressed {button_text}.")
        if self.level == 3:
            self.manager.clear()
            self.window.add_ects()
            self.window.switch_to_level(State.World)

    def signs_draw(self):
        def level1():
            sign = arcade.Sprite("hackathon/assets/cyfrowka/plus_power_on.png")
            sign.center_x = 90
            sign.center_y = 600
            self.signs.append(sign)

            sign = arcade.Sprite("hackathon/assets/cyfrowka/minus_power_off.png")
            sign.center_x = 90
            sign.center_y = 420
            self.signs.append(sign)

        def level2():
            sign = arcade.Sprite("hackathon/assets/cyfrowka/plus_power_on.png")
            sign.center_x = 90
            sign.center_y = 600
            self.signs.append(sign)

            sign = arcade.Sprite("hackathon/assets/cyfrowka/minus_power_off.png")
            sign.center_x = 90
            sign.center_y = 350
            self.signs.append(sign)

        def level3():
            sign = arcade.Sprite("hackathon/assets/cyfrowka/minus_power_off.png")
            sign.center_x = 90
            sign.center_y = 730
            self.signs.append(sign)

            sign = arcade.Sprite("hackathon/assets/cyfrowka/plus_power_on.png")
            sign.center_x = 90
            sign.center_y = 670
            self.signs.append(sign)

            sign = arcade.Sprite("hackathon/assets/cyfrowka/minus_power_off.png")
            sign.center_x = 90
            sign.center_y = 500
            self.signs.append(sign)

            sign = arcade.Sprite("hackathon/assets/cyfrowka/minus_power_off.png")
            sign.center_x = 90
            sign.center_y = 325
            self.signs.append(sign)

            sign = arcade.Sprite("hackathon/assets/cyfrowka/plus_power_on.png")
            sign.center_x = 90
            sign.center_y = 270
            self.signs.append(sign)


        match self.level:
            case 1:
                level1()
            case 2:
                level2()
            case 3:
                level3()

    def set_wires_groups(self):
        match self.level:
            case 1:
                self.wires_group = [[1, 1, 0], [0, 0, 0]]
            case 2:
                self.wires_group = [[1, 0], [0, 0], [0, 0, 0]]
            case 3:
                self.wires_group = [[0, 1, 0], [0, 0], [0, 1, 0], [0, 0], [0, 0, 0], [0, 0, 0]]

    def draw_tutorial(self):
        if self.level < 1:
            photo = arcade.Sprite(f"hackathon/assets/cyfrowka/tutorial/wyklad{self.level+4}.png", 0.75)
            photo.center_x = self.window.width // 2
            photo.center_y = self.window.height // 2
            self.all_sprites.append(photo)
            # photo.draw()

# def main():
#     """ Main function """
#     game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
#     game.setup()
#     arcade.run()


# if __name__ == "__main__":
#     # https://api.arcade.academy/en/latest/tutorials/card_game/index.html
#     main()
