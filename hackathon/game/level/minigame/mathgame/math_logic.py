from hackathon.game.level.level import Level
import arcade
import hackathon.game.minigame.mathgame.math_problems as mp
import hackathon.game.minigame.mathgame.equations as eq
import random
import arcade.gui

class MathLevel(Level):

    def __init__(self, window):
        self.background = arcade.Sprite("hackathon/assets/tablica.png")
        self.background.center_x = 1920/2
        self.background.center_y = 1080/2
        self.window = window
        self.sprites = arcade.SpriteList()
        self.block_list = arcade.SpriteList()
        self.blank_spaces = arcade.SpriteList()
        self.grabbed_sprite = None
        self.math_problem = mp.MathProblems.getProblem(0,3)
        self.eq = None
        self.math_problem.wrong_answers.append(self.math_problem.answer)
        self.buttons = arcade.SpriteList()
        self.right_answer = arcade.Sprite("hackathon/assets/correct_ans.png")
        self.wrong_answer = arcade.Sprite("hackathon/assets/wrong_ans.png")
        self.right_answer.center_y = 400
        self.right_answer.center_x = 400
        self.wrong_answer.center_y = 400
        self.wrong_answer.center_x = 400

        self.wrong_answer.scale = 0.7
        self.right_answer.scale = 0.7

        self.uimanager = arcade.gui.UIManager()
        self.uimanager.enable()
        self.active_answer = arcade.SpriteList()
        check_button = arcade.gui.UIFlatButton(text="Check",
                                               width=200)
        check_button.on_click = self.check_answer
        exit_button = arcade.gui.UIFlatButton(text="Exit",
                                               width=200)
        exit_button.on_click = self.exit_game
        self.uimanager.add(
            arcade.gui.UIAnchorWidget(
                # anchor_x="center_x",
                # anchor_y="center_y",
                align_y=300,
                align_x=500,
                child=exit_button)
        )
        self.uimanager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                align_y=-200,
                child=check_button)
        )

    def setup(self) -> None:
        self.draw_numbers(self.math_problem.wrong_answers)
        self.draw_blank_space(self.math_problem.blank_index)
        self.math_problem.equation.left_side.numbers[self.math_problem.blank_index] = "__"
        eq_txt = str(self.math_problem.equation)
        equation_text = arcade.create_text_sprite(eq_txt, 1920/3, 1080/2, color=arcade.color.BLACK, font_size=90,anchor_x="center")
        self.eq = equation_text

    def draw(self) -> None:
        self.window.clear()
        arcade.start_render()
        self.background.draw()
        self.blank_spaces.draw()
        self.eq.draw()
        self.block_list.draw()
        self.uimanager.draw()
        self.active_answer.draw()


    @property
    def finished(self) -> bool:
        pass

    def on_update(self, delta_time: int) -> bool:
        self.block_list.update()


    def on_key_press(self, key: int, modifiers: int) -> bool:
        pass

    def on_key_release(self, key: int, modifiers: int) -> bool:
        pass

    def on_mouse_motion(self, x: int, y: int, delta_x: int, delta_y: int):
        if self.grabbed_sprite:
            self.grabbed_sprite.center_x += delta_x
            self.grabbed_sprite.center_y += delta_y

    def on_mouse_press(self, x: int, y: int, button: int, key_modifiers: int):
        sprites = arcade.get_sprites_at_point((x, y), self.block_list)
        if sprites:
            self.grabbed_sprite = sprites[0]
            blank = arcade.get_sprites_at_point((x,y),self.blank_spaces)
            if blank:
                blank[0].occupant = None

    def on_mouse_release(self, x: int, y: int, button: int, key_modifiers: int):

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

    def draw_numbers(self,numbers):
        for i, number in enumerate(numbers):
            text_sprite = arcade.create_text_sprite(str(number),300*i+100,300,color=arcade.color.BLACK,font_size=90)
            text_sprite.default_x = 300*i+100
            text_sprite.default_y = 300
            self.block_list.append(text_sprite)

    def draw_blank_space(self,i):
        blank = arcade.Sprite("hackathon/assets/blank_space2.png")
        x_pos = i*220+480-60
        blank.center_x = x_pos
        blank.bottom = 540-20
        blank.scale = 0.8
        blank.occupant = None
        self.blank_spaces.append(blank)

    def check_answer(self,event):
        blank = self.blank_spaces[0]
        arcade.start_render()
        if blank.occupant:
            correct_idx = 0
            for i, number in enumerate(self.math_problem.wrong_answers):
                if number == self.math_problem.answer:
                    correct_idx = i
                    break
            if blank.occupant == self.block_list[correct_idx]:
                print("ha!")
                self.active_answer = self.right_answer
                return True
            print("ah")
            self.active_answer = self.wrong_answer
            return False

    def exit_game(self, event):
        pass







