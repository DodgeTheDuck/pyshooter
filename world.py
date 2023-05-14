
from game_map_data import GameMapData
from game_map_2d import GameMap2d
from ray import Ray
from vector import Vector
from player import Player
from segment import Segment
import math
import engine
import config

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

        n_rays = round(config.WIDTH * config.RENDER_SCALE)
        fov_rads: float = math.radians(config.FOV)
        fov_rads_half: float = fov_rads / 2
        rad_step = fov_rads / n_rays    
        rad_start = math.radians(self.player.rotation) - fov_rads_half
        mid_screen = round(config.HEIGHT / 2 * config.RENDER_SCALE)
        screen_dist = (config.WIDTH / 2) * math.tan(fov_rads_half)
        
        culled_segments: list[Segment] = []
        for segment in self.map_data.segments:
            in_frustum: bool = self.player.frustum.is_line_intersect(segment.pos_from, segment.pos_to)
            if in_frustum:
                culled_segments.append(segment)

        for i in range(n_rays):        
            ray_angle = rad_start + rad_step * i
            ray = Ray(self.player.pos, ray_angle)
            result = ray.cast(culled_segments)
            if result is not None:
                depth = result.depth
                if depth <= 1: continue
                proj_height = float(screen_dist / (depth + 0.0001))
                wall_x = (config.WIDTH * config.RENDER_SCALE) / (config.WIDTH * config.RENDER_SCALE) * i
                wall_width = (config.WIDTH * config.RENDER_SCALE) / (config.WIDTH * config.RENDER_SCALE)
                engine.gfx.draw_framebuffer_wall(wall_x, mid_screen-proj_height/2, wall_width, proj_height, (255 / abs(depth), 0, 0))

        engine.gfx.draw_buffer()

        self.map.render()
        self.player.render()

        pass

