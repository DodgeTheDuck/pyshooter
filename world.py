
from game_level import GameLevel
from game_map import GameMap
from player import Player
import game as Game

class World:
    def __init__(self):
        self.level = GameLevel()
        self.player = Player(0, 0)
        self.map = GameMap()

    def update(self, delta: float) -> None:
        self.player.update(delta)
        pass

    def render(self) -> None:
        self.map.render()
        self.player.render()
        pass

