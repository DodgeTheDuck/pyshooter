
from vector import Vector
import config
import pygame as pg

class CameraOrtho:
    def __init__(self, pos: Vector) -> None:
        self.pos: Vector = pos
        self.is_dragging: bool = False
        self.drag_origin: Vector = Vector(0,0)
        self.drag_offset: Vector = Vector(0,0)

    def start_drag(self, point: Vector) -> None:
        self.is_dragging = True
        self.drag_origin = point
        self.drag_offset = Vector(self.pos.x, self.pos.y)
        pg.mouse.set_visible(False)

    def drag(self, to: Vector) -> None:
        distance = Vector(to.x - self.drag_origin.x, to.y - self.drag_origin.y)
        self.pos.x = self.drag_offset.x - distance.x
        self.pos.y = self.drag_offset.y - distance.y        

    def stop_drag(self) -> None:
        self.is_dragging = False
        pg.mouse.set_pos((self.drag_origin.x * config.MAP_2D_SCALE, self.drag_origin.y * config.MAP_2D_SCALE))
        pg.mouse.set_visible(True)

    def screen_to_world(self, point: Vector) -> Vector:
        return Vector(point.x / config.MAP_2D_SCALE + self.pos.x, point.y / config.MAP_2D_SCALE + self.pos.y)

    def world_to_screen(self, point: Vector) -> Vector:
        return Vector((point.x - self.pos.x) * config.MAP_2D_SCALE, (point.y - self.pos.y) * config.MAP_2D_SCALE)