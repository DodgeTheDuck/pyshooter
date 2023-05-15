
from game_map_data import GameMapData
from game_map_2d import GameMap2d
from ray import Ray
from vector import Vector
from player import Player
from segment import Segment
import math
import engine
import config
import pygame as pg

class World:
    def __init__(self):
        self.map_data = GameMapData()
        self.map_data.load_map_file("test")
        self.player = Player(self.map_data.spawn_point.x, self.map_data.spawn_point.y)
        self.map = GameMap2d()
        self.time_last_culling = 0
        self.time_last_casting = 0

    def update(self, delta: float) -> None:
        self.player.update(delta)
        pass

    def render(self) -> None:

        engine.metric_timer.measure_start("casting init")

        n_rays = round(config.WIDTH * config.RENDER_SCALE)
        fov_rads: float = math.radians(config.FOV)
        fov_rads_half: float = fov_rads / 2
        rad_step = fov_rads / n_rays    
        rad_start = math.radians(self.player.rotation) - fov_rads_half
        mid_screen = round(config.HEIGHT / 2 * config.RENDER_SCALE)
        screen_dist = (config.WIDTH / 2 * config.RENDER_SCALE) * math.tan(fov_rads_half)                

        engine.metric_timer.measure_end("casting init")

        engine.metric_timer.measure_start("culling")
        culled_segments: list[Segment] = []
        for segment in self.map_data.segments:
            in_frustum: bool = self.player.frustum.is_line_intersect(segment.pos_from, segment.pos_to)
            if in_frustum:
                culled_segments.append(segment)
        engine.metric_timer.measure_end("culling")

        engine.metric_timer.measure_start("casting")
        for i in range(n_rays):        
            ray_angle = rad_start + rad_step * i
            ray = Ray(self.player.pos, ray_angle)
            result = ray.cast(culled_segments)
            if result is not None:                
                depth = result.depth * math.cos(math.radians(self.player.rotation) - ray_angle) # fishbowl fix
                #if depth <= 0.000: continue
                proj_height = float(screen_dist / (depth + 0.0001))                                
                engine.metric_timer.measure_start("wall draw")
                engine.gfx.draw_framebuffer_wall(i, mid_screen-proj_height/2, 1, proj_height, (255 / (depth + 1), 0, 0))
                engine.metric_timer.measure_end("wall draw")                
        engine.metric_timer.measure_end("casting")
        
        engine.metric_timer.measure_start("draw buffer")
        engine.gfx.draw_buffer()
        engine.metric_timer.measure_end("draw buffer")

        self.map.render()
        self.player.render()

        pass

