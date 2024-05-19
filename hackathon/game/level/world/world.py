from enum import IntEnum, auto
import arcade
import arcade.key

from ...player.player import Player as BasePlayer
from ..level import Level

import numpy as np
import PIL as pil


HITBOX_COLLISION_COLOR: int = 0

BORDER_OFFSET = 16
CELL_SIZE = 128

MAP = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1],
    [1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
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
    hitbox: pil.Image.Image
    sprites: arcade.SpriteList
    obstacles: arcade.SpriteList

    player: Player
    state: State

    player_bbox: tuple[tuple[int, int], ...]
    player_collisions: list[arcade.Sprite]
    player_collides: bool

    physics: arcade.PhysicsEngineSimple

    PLAYER_SPEED: int = 5
    PLAYER_START: tuple[int, int] = 600, 600

    def __init__(self, window: arcade.Window) -> None:
        super().__init__()
        self.window = window
        
        self.state = State.Idle

        self.player_collisions = []
        self.player_collides = False

        self.background = arcade.SpriteList()
        self.sprites = arcade.SpriteList()

        self.obstacles = arcade.SpriteList()

    def setup(self) -> None:
        self.__setup_obstacles()
        self.__setup_player()
        self.__setup_engine()

        self.__setup_background()
        self.__setup_sprites()

    def __setup_player(self) -> None:
        self.player = Player(*self.PLAYER_START)
        
    def __setup_background(self) -> None:
        self.background.append(arcade.Sprite(
            'hackathon/assets/world/map.png',
            center_x=960,
            center_y=540
        ))

    def __setup_obstacles(self) -> None:
        self.hitbox = pil.Image.open('hackathon/assets/world/map_obstacle_h.png')

        # self.obstacles.append(arcade.Sprite(
        #     'hackathon/assets/world/map_obstacle_v.png',
        #     center_x=960,
        #     center_y=540,
        #     hit_box_algorithm="Detailed"
        # ))

        self.obstacles.append(arcade.Sprite(
            'hackathon/assets/world/map_obstacle_h.png',
            center_x=960,
            center_y=540,
            hit_box_algorithm="Detailed"
        ))

        return

        for y, row in enumerate(MAP):
            for x, obj in enumerate(row):
                match obj:
                    case 0:
                        pass

                    case 1:
                        self.obstacles.append(arcade.Sprite(
                            'hackathon/assets/world/wall.png',
                            center_x=CELL_SIZE * x + BORDER_OFFSET,
                            center_y=CELL_SIZE * y + BORDER_OFFSET
                        ))

    def __setup_sprites(self) -> None:
        pass

    def __setup_engine(self) -> None:
        self.physics = arcade.PhysicsEngineSimple(
            self.player.sprite,
            self.obstacles
        )
    
    def draw(self) -> None:
        self.window.clear()

        self.obstacles.draw()

        self.background.draw()
        self.sprites.draw()

        self.player.draw()

        obs: arcade.Sprite = self.obstacles[0]
        obs.draw_hit_box(color=arcade.color.RED, line_thickness=10)
    
    @property
    def finished(self) -> bool:
        return False

    def on_update(self, delta_time: int) -> bool:
        self.player.update(delta_time)

        self.player_bbox = self.player.bounding_box()

        print(f'bbox: {self.player_bbox}')

        corner_collisions = [
            self.hitbox.getpixel(corner)
            for corner in self.player_bbox
        ]

        self.player_collides = any(
            all(pixel[component] == HITBOX_COLLISION_COLOR for component in range(3))
            for pixel in corner_collisions
        )

        print(f'corner_collisions: {corner_collisions}')
        print(f'player_collides: {self.player_collides}')

        # self.physics.update()
    
    def on_key_press(self, key: int, modifiers: int) -> bool:

        if not self.player_collides:
            match key:
                case arcade.key.W:
                    self.player.move_y(self.PLAYER_SPEED)

                case arcade.key.S:
                    self.player.move_y(-self.PLAYER_SPEED)

                case arcade.key.A:
                    self.player.move_x(-self.PLAYER_SPEED)

                case arcade.key.D:
                    self.player.move_x(self.PLAYER_SPEED)
    
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
    
