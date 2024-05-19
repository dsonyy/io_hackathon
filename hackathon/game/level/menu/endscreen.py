import arcade.csscolor
from ..level import Level
from ...state import State

import arcade
import pathlib


class EndScreen(Level):
    def __init__(self, window: arcade.Window):
        self.window = window

        # TODO: this is hardcoded, shoule be passed from the root level
        self.path_assets = pathlib.Path() / "hackathon" / "assets"

        self.width, self.height = self.window.get_size()

        self.text = ''
        self.names = []

        # load sprites

        # fonts
        self.font_main = str(self.path_assets / "fonts" / "upheavtt.ttf")
        arcade.load_font(self.font_main)

    def _build_text(self, text: str, x: int, y: int, size: int = 36) -> arcade.Text:
        return arcade.Text(
            text=text,
            start_x=x,
            start_y=y,
            color=arcade.csscolor.WHITE,
            font_size=size,
            font_name="upheaval tt (brk)",
            anchor_x="center",
            anchor_y="center")

    def _get_text_bounds(self, text: arcade.Text) -> tuple[int, int, int, int]:
        return text.left, text.right, text.bottom, text.top

    def _is_in_bounds(self, x: int, y: int, left: int, right: int, bottom: int, top: int) -> bool:
        return left <= x <= right and bottom <= y <= top

    def setup(self) -> None:
        # state
        self.option: int = 0
        self.max_options: int = 2

        # texts
        self.text_copy = self._build_text(
            text="© 2024 - 100 Twarzy Grzybiarzy",
            x=self.width // 2,
            y=int(0.15 * self.height),
        )
        self.text_start = self._build_text(
            text="RESTART",
            x=self.width // 2,
            y=int(0.40 * self.height),
        )
        self.text_exit = self._build_text(
            text="WYJSCIE",
            x=self.width // 2,
            y=int(0.35 * self.height),
        )
        self.text_studia = self._build_text(
            text="Brawo, ukończyłeś studia!",
            x=self.width // 2,
            y=int(0.75 * self.height),
            size=72,
        )
        self.text_button = self._build_text(
            text="Dopisz się do listy studentów",
            x=self.width // 2,
            y=int(0.60 * self.height),
        )
        # arcade.draw_rectangle_outline(self.width//2, int(0.55 * self.height), self.width//8, int(self.height * 0.1), arcade.color.WHITE)

        # cursor
        self.cursor_normal = arcade.Sprite(
            filename=str(self.path_assets / "cursor_normal.png"),
        )
        self.cursor_pointer = arcade.Sprite(
            filename=str(self.path_assets / "cursor_pointer.png"),
        )
        self.cursor = self.cursor_normal

    def draw(self) -> None:
        self.window.clear()
        self.window.set_mouse_visible(False)

        arcade.set_background_color(arcade.csscolor.BLACK)

        self.text_copy.draw()
        self.text_start.draw()
        self.text_exit.draw()
        self.text_studia.draw()
        self.text_button.draw()

        # self.sprite_logo.draw()
        arcade.draw_rectangle_filled(self.width // 2, int(0.50 * self.height), self.width // 4, int(self.height * 0.05),
                                     arcade.color.VIOLET)

        self.cursor.draw()

        self.text_display = self._build_text(
            text=self.text,
            x=self.width // 2,
            y=int(0.50 * self.height),
        )
        self.text_display.draw()

        for i, name in enumerate(self.names):
            self.text_lista = self._build_text(
                text=name,
                x=self.width // 8,
                y=int((0.70 - 0.05 * (i + 1)) * self.height),
            )
            self.text_lista.draw()

    @property
    def finished(self) -> bool:
        return False

    def on_update(self, delta_time: int) -> bool:
        return False

    def on_key_press(self, key: int, modifiers: int) -> bool:
        if chr(key).isalpha():
            self.text += chr(key)
        return False

    def on_key_release(self, key: int, modifiers: int) -> bool:
        return False

    def on_mouse_motion(self, x: int, y: int, delta_x: int, delta_y: int) -> None:
        is_hovering = False
        is_hovering |= self._update_text_option_hover(x, y, self.text_start)
        is_hovering |= self._update_text_option_hover(x, y, self.text_exit)
        is_hovering |= self._update_text_option_hover(x, y, self.text_button)

        if is_hovering:
            self.cursor = self.cursor_pointer
        else:
            self.cursor = self.cursor_normal

        self.cursor.position = x + self.cursor.width / 2, y - self.cursor.height / 2

    def on_mouse_press(self, x: int, y: int, button: int, key_modifiers: int) -> None:
        if self._is_in_bounds(x, y, *self._get_text_bounds(self.text_start)):
            self.window.switch_to_level(State.World)
        if self._is_in_bounds(x, y, *self._get_text_bounds(self.text_button)):
            self.names.append(self.text)
            self.text = ''
        if self._is_in_bounds(x, y, *self._get_text_bounds(self.text_exit)):
            arcade.close_window()

    def on_mouse_release(self, x: int, y: int, button: int, key_modifiers: int) -> None:
        pass

    def _update_text_option_hover(self, x: int, y: int, text: arcade.Text) -> bool:
        if self._is_in_bounds(x, y, *self._get_text_bounds(text)):
            text.color = arcade.csscolor.RED
            return True

        text.color = arcade.csscolor.WHITE
        return False
