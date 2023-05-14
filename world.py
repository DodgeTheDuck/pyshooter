
from game_map_data import GameMapData
from game_map_2d import GameMap2d
from player import Player
import engine as Game

class World:
    def __init__(self):
        self.map_data = GameMapData()
        self.map_data.load_map_file("test")
        self.player = Player(self.map_data.spawn_point.x, self.map_data.spawn_point.y)
        self.map = GameMap2d()

    def update(self, delta: float) -> None:
        self.player.update(delta)
        pass

    def render(self) -> None:
        self.map.render()
        self.player.render()
        pass

