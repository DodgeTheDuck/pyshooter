
import game
import config
from game_level import GameLevel
from player import Player
from vector import Vector

class GameMap:
    def __init__(self):
        pass

    def update(self, delta) -> None:
        pass

    def render(self) -> None:

        #TODO: work out a more elegant scaling/transform thing

        map: GameLevel = game.world.level
        player: Player = game.world.player
        offset: Vector = Vector((-player.pos.x * config.MAP_2D_SCALE + config.WIDTH / 2) / config.MAP_2D_SCALE, (-player.pos.y * config.MAP_2D_SCALE + config.HEIGHT / 2) / config.MAP_2D_SCALE)

        half_width = config.WIDTH / 2
        half_height = config.HEIGHT / 2

        for segment in map.segments:
            game.gfx.render_line(
                (segment.pos_from.x + offset.x) * config.MAP_2D_SCALE, 
                (segment.pos_from.y + offset.y) * config.MAP_2D_SCALE, 
                (segment.pos_to.x + offset.x) * config.MAP_2D_SCALE, 
                (segment.pos_to.y + offset.y) * config.MAP_2D_SCALE, 
                (255, 255, 255)
            )
        
        game.gfx.render_circle(half_width, half_height, 0.2 * config.MAP_2D_SCALE, (128, 128, 128))
        game.gfx.render_line(half_width, half_height, half_width + player.frustum.far_left.x * config.MAP_2D_SCALE, half_height + player.frustum.far_left.y * config.MAP_2D_SCALE, (255, 255, 102))
        game.gfx.render_line(half_width, half_height, half_width + player.frustum.far_right.x * config.MAP_2D_SCALE, half_height + player.frustum.far_right.y * config.MAP_2D_SCALE, (255, 255, 102))

        pass