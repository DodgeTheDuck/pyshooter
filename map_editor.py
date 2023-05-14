
from player import Player
from vector import Vector
from game_map_data import GameMapData
from segment import Segment
import pygame as pg
import config
import engine
import math

class MapEditor:
    def __init__(self) -> None:
        self.map = GameMapData()
        self.player = None
        self.active_segment_index = -1
        self.dragging = False
        self.cam_x = 0
        self.cam_y = 0
        self.grid_size = 0.5
        pass

    def update(self, delta) -> None:

        if(self.player is not None):
            self.player.update(delta)  

        (mx, my) = pg.mouse.get_pos()

        mx = mx / config.MAP_2D_SCALE + self.cam_x
        my = my / config.MAP_2D_SCALE + self.cam_y        

        if pg.mouse.get_pressed(3)[0]:
            if self.active_segment_index == -1:
                start_pos = self.__snap_to_grid(Vector(mx, my))
                new_segment = Segment(start_pos, start_pos)
                self.active_segment_index = self.map.add_segment(new_segment)
                self.dragging = True
        else:
            self.dragging = False
            self.active_segment_index = -1

        if pg.mouse.get_pressed(3)[2]:
            self.map.set_spawn_point(self.__snap_to_grid(Vector(mx, my)))
        
        if self.active_segment_index >= 0 and self.dragging:
            active_segment = self.map.get_segment(self.active_segment_index)
            active_segment.pos_to = self.__snap_to_grid(Vector(mx, my))
            self.map.update_segment(self.active_segment_index, active_segment)

        pass

    def render(self) -> None:

        player: Player = self.player

        off_x = -(self.cam_x) if self.player is None else self.player.pos.x
        off_y = -(self.cam_y) if self.player is None else self.player.pos.y
        offset: Vector = Vector((-off_x * config.MAP_2D_SCALE) / config.MAP_2D_SCALE, (-off_y * config.MAP_2D_SCALE) / config.MAP_2D_SCALE)

        half_width = config.WIDTH / 2
        half_height = config.HEIGHT / 2

        for segment in self.map.segments:
            
            in_frustum: bool = player is not None and player.frustum.is_line_intersect(segment.pos_from, segment.pos_to)
            wall_color = (0, 255, 0) if in_frustum else (255, 255, 255)

            engine.gfx.render_line(
                (segment.pos_from.x + offset.x) * config.MAP_2D_SCALE, 
                (segment.pos_from.y + offset.y) * config.MAP_2D_SCALE, 
                (segment.pos_to.x + offset.x) * config.MAP_2D_SCALE, 
                (segment.pos_to.y + offset.y) * config.MAP_2D_SCALE, 
                wall_color
            )
        
        # render spawn point
        engine.gfx.render_circle(self.map.spawn_point.x * config.MAP_2D_SCALE, self.map.spawn_point.y  * config.MAP_2D_SCALE, 0.2 * config.MAP_2D_SCALE, (0, 0, 200))

        # render player if enabled
        if(player is not None):
            engine.gfx.render_circle(half_width, half_height, 0.2 * config.MAP_2D_SCALE, (128, 128, 128))
            engine.gfx.render_line(half_width, half_height, half_width + player.frustum.far_left.x * config.MAP_2D_SCALE, half_height + player.frustum.far_left.y * config.MAP_2D_SCALE, (255, 255, 102))
            engine.gfx.render_line(half_width, half_height, half_width + player.frustum.far_right.x * config.MAP_2D_SCALE, half_height + player.frustum.far_right.y * config.MAP_2D_SCALE, (255, 255, 102))

        pass

    def save(self, name) -> None:
        with open("./maps/{0}.map".format(name), "w+") as f:
            f.write("SPAWN:{0},{1}\n".format(self.map.spawn_point.x, self.map.spawn_point.y))
            for segment in self.map.segments:                
                f.write("SEG:{0},{1},{2},{3}\n".format(
                    segment.pos_from.x,
                    segment.pos_from.y,
                    segment.pos_to.x,
                    segment.pos_to.y
                ))
    
    def load(self, name) -> None:
        self.map.load_map_file(name)

    def __snap_to_grid(self, point: Vector) -> Vector:
        return Vector(
            round(point.x / self.grid_size) * self.grid_size,
            round(point.y / self.grid_size) * self.grid_size
        )
    