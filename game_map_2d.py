
import engine
import config
import math
from segment import Segment
from game_map_data import GameMapData
from player import Player
from vector import Vector
from ray import Ray

class GameMap2d:
    def __init__(self):
        pass

    def update(self, delta) -> None:
        pass

    def render(self) -> None:

        #TODO: work out a more elegant scaling/transform thing

        map: GameMapData = engine.get_top_state().world.map_data
        player: Player = engine.get_top_state().world.player
        offset: Vector = Vector((-player.pos.x * config.MAP_2D_SCALE + config.WIDTH / 2) / config.MAP_2D_SCALE, (-player.pos.y * config.MAP_2D_SCALE + config.HEIGHT / 2) / config.MAP_2D_SCALE)

        half_width = config.WIDTH / 2
        half_height = config.HEIGHT / 2

        for segment in map.segments:

            in_frustum: bool = player.frustum.is_line_intersect(segment.pos_from, segment.pos_to)
            wall_color = (0, 255, 0) if in_frustum else (255, 255, 255)

            engine.gfx.render_line(
                (segment.pos_from.x + offset.x) * config.MAP_2D_SCALE, 
                (segment.pos_from.y + offset.y) * config.MAP_2D_SCALE, 
                (segment.pos_to.x + offset.x) * config.MAP_2D_SCALE, 
                (segment.pos_to.y + offset.y) * config.MAP_2D_SCALE, 
                wall_color
            )

        
        n_rays = round(config.WIDTH * config.RENDER_SCALE)
        fov_rads: float = math.radians(config.FOV)
        fov_rads_half: float = fov_rads / 2
        rad_step = fov_rads / n_rays    
        rad_start = math.radians(player.rotation) - fov_rads_half
        
        culled_segments: list[Segment] = []
        for segment in map.segments:
            in_frustum: bool = player.frustum.is_line_intersect(segment.pos_from, segment.pos_to)
            if in_frustum:
                culled_segments.append(segment)

        for i in range(n_rays):
            ray_angle = rad_start + rad_step * i

            # engine.gfx.render_line(
            #     half_width, half_height, 
            #     half_width + math.cos(ray_angle) * config.VIEW_DIST * config.MAP_2D_SCALE, 
            #     half_height + math.sin(ray_angle) * config.VIEW_DIST * config.MAP_2D_SCALE,
            #     (255, 0, 0)
            # )
            
            ray: Ray = Ray(player.pos, ray_angle)
            result = ray.cast(culled_segments)            

            if result is not None:                
                engine.gfx.render_circle(result.hit_x * config.MAP_2D_SCALE + offset.x * config.MAP_2D_SCALE, result.hit_y * config.MAP_2D_SCALE + offset.y * config.MAP_2D_SCALE, 0.05 * config.MAP_2D_SCALE, (128, 128, 255))
        
        engine.gfx.render_circle(half_width, half_height, 0.2 * config.MAP_2D_SCALE, (128, 128, 128))
        engine.gfx.render_line(half_width, half_height, half_width + player.frustum.far_left.x * config.MAP_2D_SCALE, half_height + player.frustum.far_left.y * config.MAP_2D_SCALE, (255, 255, 102))
        engine.gfx.render_line(half_width, half_height, half_width + player.frustum.far_right.x * config.MAP_2D_SCALE, half_height + player.frustum.far_right.y * config.MAP_2D_SCALE, (255, 255, 102))

        pass