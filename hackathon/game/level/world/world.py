from enum import IntEnum, auto
import arcade
import arcade.key

from ...player.player import Player as BasePlayer
from ..level import Level


CELL_SIZE = 32

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
    sprite: arcade.Sprite = arcade.Sprite('hackathon/assets/world/player.png')

    def __init__(self, ) -> None:
        pass

    def draw(self) -> None:
        self.sprite.draw()

    def on_update(self, delta_time: int) -> None:
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
    
    sprites: arcade.SpriteList
    obstacles: arcade.SpriteList

    player: Player
    state: State

    player_speed: int = 5

    def __init__(self, window: arcade.Window) -> None:
        super().__init__()
        self.window = window
        
        self.player = Player()
        self.state = State.Idle

        self.sprites = arcade.SpriteList()
        self.obstacles = arcade.SpriteList()

    def setup(self) -> None:
        self.__setup_sprites()
        self.__setup_obstacles()
        
    def __setup_obstacles(self) -> None:
        for y, row in enumerate(MAP):
            for x, obj in enumerate(row):
                match obj:
                    case 0:
                        pass

                    case 1:
                        self.obstacles.append(arcade.Sprite(
                            'hackathon/assets/world/wall.png',
                            center_x=CELL_SIZE * x,
                            center_y=CELL_SIZE * y
                        ))

    def __setup_sprites(self) -> None:
        self.sprites.append(arcade.Sprite(
            'hackathon/assets/world/background.png'
        ))
    
    def draw(self) -> None:
        self.window.clear()
        self.sprites.draw()
        self.obstacles.draw()
        self.player.draw()
    
    @property
    def finished(self) -> bool:
        return False

    def on_update(self, delta_time: int) -> bool:
        self.player.on_update(delta_time)
    
    def on_key_press(self, key: int, modifiers: int) -> bool:
        match key:
            case arcade.key.W:
                self.player.move_y(self.player_speed)

            case arcade.key.S:
                self.player.move_y(-self.player_speed)

            case arcade.key.A:
                self.player.move_x(-self.player_speed)

            case arcade.key.D:
                self.player.move_x(self.player_speed)
    
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
    
