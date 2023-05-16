from vector import Vector
import line_clipping
import math


class Frustum:
    def __init__(self) -> None:
        self.eye_pos = Vector(0, 0)
        self.far_left = Vector(0, 0)
        self.far_right = Vector(0, 0)
        pass

    def update(self, eye: Vector, view_angle: float, fov: float, range: float):
        half_fov_rads: float = math.radians(fov) / 2.0
        view_angle = math.radians(view_angle)

        self.eye_pos = eye
        self.far_left.x = self.eye_pos.x + math.cos(view_angle - half_fov_rads) * range
        self.far_left.y = self.eye_pos.y + math.sin(view_angle - half_fov_rads) * range

        self.far_right.x = self.eye_pos.x + math.cos(view_angle + half_fov_rads) * range
        self.far_right.y = self.eye_pos.y + math.sin(view_angle + half_fov_rads) * range

    def is_point_inside(self, point: Vector) -> bool:
        # NOTE: barycentric triangle/point intersection thing that I don't fully understand
        # http://totologic.blogspot.com/2014/01/accurate-point-in-triangle-test.html

        x, y = point.x, point.y
        x1, y1 = self.eye_pos.x, self.eye_pos.y
        x2, y2 = self.far_left.x, self.far_left.y
        x3, y3 = self.far_right.x, self.far_right.y

        denominator: float = ((y2 - y3) * (x1 - x3) + (x3 - x2) * (y1 - y3))
        a: float = ((y2 - y3) * (x - x3) + (x3 - x2) * (y - y3)) / denominator
        b: float = ((y3 - y1) * (x - x3) + (x1 - x3) * (y - y3)) / denominator
        c: float = 1 - a - b

        return 0 <= a <= 1 and 0 <= b <= 1 and 0 <= c <= 1

    def is_line_intersect(self, line_from: Vector, line_to: Vector) -> bool:
        return line_clipping.cyrus_beck_clip([self.eye_pos, self.far_left, self.far_right], line_from, line_to)
