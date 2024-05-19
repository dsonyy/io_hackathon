from enum import IntEnum, auto
from typing import Any, Optional

import arcade
import arcade.key

import arcade.key
from pyglet import math as pyglet_math

from ...player.player import Player as BasePlayer
from ..level import Level

from ....game.state import State as GameState

import PIL as pil


HITBOX_COLLISION_COLOR: int = 0

BORDER_OFFSET = 16
CELL_SIZE = 128

class Active(IntEnum):
    MathClassroom = auto()
    ElectronicsClassroom = auto()
    PaperSheet = auto()
    Laptop = auto()


ACTIVES: list[tuple[tuple[int, int], Any]] = [
    ((200, 300), Active.ElectronicsClassroom),
    ((300, 400), Active.Laptop)
]

class State(IntEnum):
    Idle = auto()


class Player(BasePlayer):
    TEXTURE: str = 'hackathon/assets/world/player.png'
    sprite: arcade.Sprite

    def __init__(self, start_x: int, start_y: int) -> None:
        self.sprite = arcade.Sprite(
            self.TEXTURE,
            center_x=start_x,
            center_y=start_y
        )

    def bounding_box(self) -> tuple[tuple[int, int], ...]:
        '''
        UL, UR, LL, LR
        '''
        x = int(self.sprite.center_x)
        y = int(self.sprite.center_y)
        w = int(self.sprite.width) // 2
        h = int(self.sprite.height) // 2

        return (
            (x - w, y + h),
            (x + w, y + h),
            (x - w, y - h),
            (x + w, y - h)
        )

    def draw(self) -> None:
        self.sprite.draw()

    def update(self, delta_time: int) -> None:
        self.sprite.update()

    def stop(self) -> None:
        self.sprite.change_x = 0
        self.sprite.change_y = 0

    def move_x(self, delta: int) -> None:
        self.sprite.change_x = delta

    def move_y(self, delta: int) -> None:
        self.sprite.change_y = delta


class World(Level):
    window: arcade.Window
    
    background: arcade.SpriteList
    
    hitboxes: list[pil.Image.Image]
    chunk: int = 0

    sprites: arcade.SpriteList
    obstacles: arcade.SpriteList

    actives: arcade.SpriteList

    player: Player
    state: State

    player_bbox: tuple[tuple[int, int], ...]
    player_collisions: tuple[bool, ...]
    player_actives_collision: Optional[arcade.Sprite]

    physics: arcade.PhysicsEngineSimple

    player_camera: arcade.Camera
    overlay_camera: arcade.Camera

    PLAYER_SPEED: int = 5
    PLAYER_START: tuple[int, int] = 0, 0

    def __init__(self, window: arcade.Window) -> None:
        super().__init__()
        self.window = window
        
        self.state = State.Idle

        self.player_collisions = []

        self.actives = arcade.SpriteList()
        self.player_actives_collision = None

        self.background = arcade.SpriteList()
        self.sprites = arcade.SpriteList()

        self.obstacles = arcade.SpriteList()

        self.player_camera = arcade.Camera(
            window.width,
            window.height
        )

        self.overlay_camera = arcade.Camera(
            window.width,
            window.height
        )

    def setup(self) -> None:
        self.__setup_obstacles()
        self.__setup_player()
        self.__setup_background()
        self.__setup_sprites()
        self.__setup_actives()

        self.__setup_engine()
        self.scroll_to_player()

    def __setup_player(self) -> None:
        self.player = Player(*self.PLAYER_START)
    
    def __setup_actives(self) -> None:
        for position, type in ACTIVES:
            active = arcade.Sprite(
                'hackathon/assets/world/consumable.png',
                center_x=position[0],
                center_y=position[1]
            )

            active.type = type

            self.actives.append(active)

    def __setup_background(self) -> None:
        self.background.append(arcade.Sprite(
            'hackathon/assets/world/map1/ground.png'
        ))

    def __setup_obstacles(self) -> None:
        self.hitboxes = [
            pil.Image.open('hackathon/assets/world/map1/ground.png')
        ]

    def __setup_sprites(self) -> None:
        self.sprites.append(arcade.Sprite(
            'hackathon/assets/world/map1/walls.png'
        ))

    def __setup_engine(self) -> None:
        self.physics = arcade.PhysicsEngineSimple(
            self.player.sprite,
            self.actives
        )
    
    def draw(self) -> None:
        self.player_camera.use()

        self.background.draw()
        self.sprites.draw()
        self.actives.draw()
        self.player.draw()
        
        self.overlay_camera.use()
        self.__draw_overlay()

    def __draw_overlay(self) -> None:
        arcade.draw_rectangle_filled(
            self.window.width // 2,
            20,
            self.window.width,
            40,
            arcade.color.ALMOND
        )

        text = f"ECTS: {self.window.plot['ects']}"
        arcade.draw_text(text, 10, 10, arcade.color.BLACK_BEAN, 20)

    @property
    def finished(self) -> bool:
        return False
    
    def interaction(self) -> None:
        active = self.player_actives_collision

        match active.type:
            case Active.PaperSheet:
                pass

            case Active.Laptop:
                pass

            case Active.MathClassroom:
                self.window.switch_to_level(GameState.MinigameMath)
                self.player_camera.move(pyglet_math.Vec2(0, 0))
                self.player_camera.use()

            case Active.ElectronicsClassroom:
                self.window.switch_to_level(GameState.MinigameElectro)
                self.player_camera.move(pyglet_math.Vec2(0, 0))
                self.player_camera.use()

    def on_update(self, delta_time: int) -> bool:
        self.scroll_to_player()
        self.player.update(delta_time)
        self.update_collisions()

    def on_resize(self, width: float, height: float) -> None:
        self.player_camera.resize(int(width), int(height))

    def scroll_to_player(self) -> None:
        position = pyglet_math.Vec2(
            self.player.sprite.center_x - self.window.width / 2,
            self.player.sprite.center_y - self.window.height / 2
        )

        self.player_camera.move_to(position, 0.5)

    def update_collisions(self) -> None:
        self.player_bbox = self.player.bounding_box()
        hitbox = self.hitboxes[self.chunk]

        height = hitbox.height
        x_offset = int(hitbox.width / 2)
        y_offset = int(height / 2)

        corner_collisions = [
            hitbox.getpixel((corner[0] + x_offset, height - corner[1] - y_offset))
            for corner in self.player_bbox
        ]

        self.player_collisions = tuple(map(
            lambda pixel: all(
                pixel[i] == HITBOX_COLLISION_COLOR
                for i in range(2)
            ),
            corner_collisions
        ))

        print(corner_collisions)
        print(self.player_collisions)

        if any(self.player_collisions):
            self.player.stop()

        match arcade.check_for_collision_with_list(
            self.player.sprite,
            self.actives
        ):
            case []:
                self.player_actives_collision = None

            case [sprite, *_]:
                self.player_actives_collision = sprite
    
    def on_key_press(self, key: int, modifiers: int) -> bool:
        match (key, self.player_collisions):
            case (arcade.key.W, (False, False, _, _)):
                self.player.move_y(self.PLAYER_SPEED)

            case (arcade.key.S, (_, _, False, False)):
                self.player.move_y(-self.PLAYER_SPEED)

            case (arcade.key.A, (False, _, False, _)):
                self.player.move_x(-self.PLAYER_SPEED)

            case (arcade.key.D, (_, False, _, False)):
                self.player.move_x(self.PLAYER_SPEED)

        match (key, self.player_actives_collision):
            case (_, None):
                pass

            case (arcade.key.E, _):
                self.interaction()
    
    def on_key_release(self, key: int, modifiers: int) -> bool:
        match key:
            case arcade.key.W:
                self.player.stop()

            case arcade.key.S:
                self.player.stop()

            case arcade.key.A:
                self.player.stop()

            case arcade.key.D:
                self.player.stop()
    
    def on_mouse_motion(self, x: int, y: int, delta_x: int, delta_y: int):
        pass
    
    def on_mouse_press(self, x: int, y: int, button: int, key_modifiers: int):
        pass
    
    def on_mouse_release(self, x: int, y: int, button: int, key_modifiers: int):
        pass
    
