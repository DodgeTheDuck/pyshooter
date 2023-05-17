
from camera_ortho import CameraOrtho
from vector import Vector
from game_map_data import GameMapData
from segment import Segment
import pygame as pg
import config
import engine
import math
import os

class MapEditor:
    def __init__(self) -> None:
        self.map_data = GameMapData()
        self.player = None
        self.active_segment_index = -1
        self.dragging = False
        self.camera = CameraOrtho(Vector(self.map_data.spawn_point.x, self.map_data.spawn_point.y))                
        # self.cam_x = 0
        # self.cam_y = 0
        # self.cam_dragging = False
        # self.cam_drag_x = 0
        # self.cam_drag_y = 0
        # self.cam_drag_x_saved = 0
        # self.cam_drag_y_saved = 0
        self.grid_size = 0.5
        pass

    def update(self, delta) -> None:

        if(self.player is not None):
            self.player.update(delta)  

        m_pos: Vector = Vector(pg.mouse.get_pos()[0], pg.mouse.get_pos()[1])
        m_pos_world: Vector = self.camera.screen_to_world(m_pos)        

        if pg.mouse.get_pressed(3)[0]:
            if self.active_segment_index == -1:
                start_pos = self.__snap_to_grid(m_pos_world)
                new_segment = Segment(start_pos, start_pos)
                self.active_segment_index = self.map_data.add_segment(new_segment)
                self.dragging = True
        else:
            self.dragging = False
            self.active_segment_index = -1
        
        print(m_pos_world)

        if pg.mouse.get_pressed(3)[1]:
            if self.camera.is_dragging == False:
                self.camera.start_drag(m_pos_world)
            self.camera.drag(m_pos_world)
        elif self.camera.is_dragging:
            self.camera.stop_drag()

        if pg.mouse.get_pressed(3)[2]:
            self.map_data.set_spawn_point(self.__snap_to_grid(m_pos_world))
        
        if self.active_segment_index >= 0 and self.dragging:
            active_segment = self.map_data.get_segment(self.active_segment_index)
            active_segment.pos_to = self.__snap_to_grid(m_pos_world)
            self.map_data.update_segment(self.active_segment_index, active_segment)

        #self.cam_y += 1.0 * delta

        pass

    def render(self) -> None:

        #TODO: work out a nice way to make rendering to main screen vs 
        engine.gfx.surface.fill((0,0,0))

        off_x = -(self.camera.pos.x)
        off_y = -(self.camera.pos.y)
        offset: Vector = Vector((-off_x * config.MAP_2D_SCALE) / config.MAP_2D_SCALE, (-off_y * config.MAP_2D_SCALE) / config.MAP_2D_SCALE)        

        # render segments
        for segment in self.map_data.segments:                        
            wall_color = (255, 255, 255)
            engine.gfx.render_line(
                (segment.pos_from.x + offset.x) * config.MAP_2D_SCALE, 
                (segment.pos_from.y + offset.y) * config.MAP_2D_SCALE, 
                (segment.pos_to.x + offset.x) * config.MAP_2D_SCALE, 
                (segment.pos_to.y + offset.y) * config.MAP_2D_SCALE, 
                wall_color
            )
            engine.gfx.render_circle(
                (segment.pos_from.x + offset.x) * config.MAP_2D_SCALE, 
                (segment.pos_from.y + offset.y) * config.MAP_2D_SCALE,
                2,
                (255, 0, 0)
            )
            engine.gfx.render_circle(
                (segment.pos_to.x + offset.x) * config.MAP_2D_SCALE, 
                (segment.pos_to.y + offset.y) * config.MAP_2D_SCALE,
                2,
                (255, 0, 0)
            )
        # render spawn point
        engine.gfx.render_circle((self.map_data.spawn_point.x + self.camera.pos.x) * config.MAP_2D_SCALE + offset.x, (self.map_data.spawn_point.y + self.camera.pos.y)  * config.MAP_2D_SCALE , 4, (0, 0, 200))

        pass

    def save(self, name) -> None:
        with open("./maps/{0}.map".format(name), "w+") as f:
            f.write("SPAWN:{0},{1}\n".format(self.map_data.spawn_point.x, self.map_data.spawn_point.y))
            for segment in self.map_data.segments:                
                f.write("SEG:{0},{1},{2},{3}\n".format(
                    segment.pos_from.x,
                    segment.pos_from.y,
                    segment.pos_to.x,
                    segment.pos_to.y
                ))
    
    def load(self, name) -> None:
        if os.path.isfile("./maps/{0}.map".format(name)) == False: return None
        self.map_data.load_map_file(name)

    def __snap_to_grid(self, point: Vector) -> Vector:
        return Vector(
            round(point.x / self.grid_size) * self.grid_size,
            round(point.y / self.grid_size) * self.grid_size
        )
    