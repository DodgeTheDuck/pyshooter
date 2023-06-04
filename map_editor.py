
from camera_ortho import CameraOrtho
from vector import Vector
from game_map_data import GameMapData
from segment import Segment
from map_compiler import MapCompiler
import pygame as pg
import config
import engine
import input
import os
import math

class MapEditor:
    def __init__(self) -> None:
        self.map_data = GameMapData()
        self.player = None
        self.active_segment_index = -1
        self.dragging = False
        self.camera = CameraOrtho(Vector(1, 1))
        self.grid_size = 0.5
        self.draw_bsp = False
        self.compiler: MapCompiler = MapCompiler()

        pass

    def update(self, delta) -> None:

        if(self.player is not None):
            self.player.update(delta)  

        m_pos: Vector = Vector(pg.mouse.get_pos()[0], pg.mouse.get_pos()[1])
        m_pos_world: Vector = self.camera.screen_to_world(m_pos)

        if input.get_key_state(input.KEY_MAP_UP):
            self.camera.pos.y -= 3 * delta

        if input.get_key_state(input.KEY_MAP_DOWN):
            self.camera.pos.y += 3 * delta

        if input.get_key_state(input.KEY_MAP_LEFT):
            self.camera.pos.x -= 3 * delta

        if input.get_key_state(input.KEY_MAP_RIGHT):
            self.camera.pos.x += 3 * delta            

        if pg.mouse.get_pressed(3)[0]:
            if self.active_segment_index == -1:
                start_pos = self.__snap_to_grid(m_pos_world)
                new_segment = Segment(start_pos, start_pos)
                self.active_segment_index = self.map_data.add_segment(new_segment)
                self.dragging = True
        else:
            self.dragging = False
            self.active_segment_index = -1
        
        #print(self.camera.pos)

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

        pass

    def render_editor(self) -> None:        

        self.__draw_grid()
        self.__draw_segments(self.map_data.segments)        
        self.__draw_spawn()
        self.__draw_info()

        pass

    def render_compiler(self, map_compiler: MapCompiler) -> None:        

        self.__draw_grid()
        self.__draw_segments(map_compiler.segments)      
        self.__draw_segment(map_compiler.active_segment, (0, 255, 0))  
        self.__draw_segment(map_compiler.intersect_line, (255, 0, 102))  
        self.__draw_info_compiler(map_compiler)

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
    
    def __draw_segments(self, segments) -> None:         

        for segment in segments:                        
            segment_color = (255, 255, 255)
            
            seg_from_screen: Vector = self.camera.world_to_screen(segment.pos_from)
            seg_to_screen: Vector = self.camera.world_to_screen(segment.pos_to)

            engine.gfx.render_line(
                seg_from_screen.x, 
                seg_from_screen.y, 
                seg_to_screen.x, 
                seg_to_screen.y, 
                segment_color
            )
            engine.gfx.render_circle(
                seg_to_screen.x, 
                seg_to_screen.y,
                8,
                (255, 0, 0)
            )
            engine.gfx.render_circle(
                seg_from_screen.x, 
                seg_from_screen.y,
                8,
                (255, 0, 0)
            )
    
    def __draw_segment(self, segment, color, dashed: bool = False) -> None:

        if segment is None: return None        
            
        seg_from_screen: Vector = self.camera.world_to_screen(segment.pos_from)
        seg_to_screen: Vector = self.camera.world_to_screen(segment.pos_to)

        if dashed:
            engine.gfx.render_dashed_line(
                seg_from_screen.x, 
                seg_from_screen.y, 
                seg_to_screen.x, 
                seg_to_screen.y, 
                color,
                2,
                5
            )
        else:
            engine.gfx.render_line(
                seg_from_screen.x, 
                seg_from_screen.y, 
                seg_to_screen.x, 
                seg_to_screen.y, 
                color
            )

    def __draw_spawn(self) -> None:
        spawn_screen: Vector = self.camera.world_to_screen(self.map_data.spawn_point)
        engine.gfx.render_circle(spawn_screen.x, spawn_screen.y, 4, (0, 0, 200))

    def __draw_grid(self) -> None:      

        #TODO: can probs optimise some of this messy maff

        cols = round(config.WIDTH / (config.MAP_2D_SCALE * self.grid_size))
        rows = round(config.HEIGHT / (config.MAP_2D_SCALE * self.grid_size))

        x = round((self.camera.pos.x * config.MAP_2D_SCALE) / (self.grid_size * config.MAP_2D_SCALE))
        y = round((self.camera.pos.y * config.MAP_2D_SCALE) / (self.grid_size * config.MAP_2D_SCALE))

        for i in range(x, x + cols):
            col_pos: Vector = self.camera.world_to_screen(Vector(i * self.grid_size, 0))         
            engine.gfx.render_line(col_pos.x, 0, col_pos.x, config.HEIGHT, (128, 128, 128))
            for j in range(y, y + rows):
                row_pos: Vector = self.camera.world_to_screen(Vector(0, j * self.grid_size))
                engine.gfx.render_line(0, row_pos.y, config.WIDTH, row_pos.y, (128, 128, 128))

    def __draw_info(self) -> None:
        m_pos: Vector = Vector(pg.mouse.get_pos()[0], pg.mouse.get_pos()[1])
        m_pos_world: Vector = self.camera.screen_to_world(m_pos)
        engine.gfx.render_rect(config.WIDTH - 256, 8, config.WIDTH - 8, 8+256, (0,0,0))
        engine.gfx.render_text(config.WIDTH - 256, 8, str(m_pos_world), (255, 255, 255))

    def __draw_info_compiler(self, compiler: MapCompiler) -> None:
        m_pos: Vector = Vector(pg.mouse.get_pos()[0], pg.mouse.get_pos()[1])
        m_pos_world: Vector = self.camera.screen_to_world(m_pos)
        engine.gfx.render_rect(config.WIDTH - 256, 8, config.WIDTH - 8, 8+256, (0,0,0))
        engine.gfx.render_text(config.WIDTH - 256, 8, str(m_pos_world), (255, 255, 255))
        engine.gfx.render_text(config.WIDTH - 256, 24, "Segments: {0}".format(len(compiler.segments)), (255, 255, 255))
