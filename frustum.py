from vector import Vector
import math

class Frustum:
    def __init__(self) -> None:
        self.eye_pos = Vector(0,0)
        self.far_left = Vector(0,0)
        self.far_right = Vector(0,0)            
        pass

    def update(self, eye: Vector, view_angle: float, fov: float, range: float):
        half_fov_rads: float = math.radians(fov) / 2.0

        self.eye_pos = eye
        self.far_left.x = math.cos(view_angle-half_fov_rads) * range
        self.far_left.y = math.sin(view_angle-half_fov_rads) * range

        self.far_right.x = math.cos(view_angle+half_fov_rads) * range
        self.far_right.y = math.sin(view_angle+half_fov_rads) * range