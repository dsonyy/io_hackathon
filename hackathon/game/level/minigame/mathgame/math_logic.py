from hackathon.game.level.level import Level
import arcade

class MathLevel(Level):

    def __init__(self, window):
        self.background = None
        self.window = window
        self.sprites = arcade.SpriteList()
        self.block_list = arcade.SpriteList()
        self.blank_spaces = arcade.SpriteList()
        self.grabbed_sprite = None

    def setup(self) -> None:
        self.draw_numbers([1,2,3,4])
        self.draw_blank_space(100)
        pass


    def draw(self) -> None:
        self.window.clear()
        arcade.start_render()

        # arcade.start_render()
        # self.sprites.draw()
        self.blank_spaces.draw()
        self.block_list.draw()

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
            text_sprite = arcade.create_text_sprite(str(number),300*i+100,600,color=arcade.color.BLACK,font_size=70)
            text_sprite.default_x = 300*i+100
            text_sprite.default_y = 600
            self.block_list.append(text_sprite)

    def draw_blank_space(self,x):
        blank = arcade.Sprite("hackathon/assets/blank_space.png")
        blank.center_x = x
        blank.center_y = 800
        blank.scale = 0.9
        blank.occupant = None
        self.blank_spaces.append(blank)







