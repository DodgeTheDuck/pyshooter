
from vector import Vector
from segment import Segment
from ray_hit_result import RayHitResult
import config
import engine
import math

class Ray:
    
    def __init__(self, pos_from: Vector, angle: float, range: float = config.VIEW_DIST):
        self.pos_from = pos_from
        self.angle = angle        
        self.pos_end = Vector(
            self.pos_from.x + math.cos(self.angle) * range,
            self.pos_from.y + math.sin(self.angle) * range
        )

    def cast(self,  segments: list[Segment]) -> RayHitResult:

        nearest = None

        for segment in segments:
            engine.metric_timer.measure_start("ray intersect")
            result = self.__test_intersect_new(segment)
            engine.metric_timer.measure_end("ray intersect")
            engine.metric_timer.measure_start("nearest test")
            if result is not None:          
                delta: Vector = Vector(self.pos_from.x - result.x, self.pos_from.y - result.y)
                depth = abs(math.sqrt(delta.x * delta.x + delta.y * delta.y))
                if nearest is None:
                    nearest = RayHitResult(depth, result.x, result.y, segment)
                elif nearest.depth >= depth:
                    nearest = RayHitResult(depth, result.x, result.y, segment)
            engine.metric_timer.measure_end("nearest test")
        
        return nearest

    def __test_intersect_new(self, segment: Segment) -> Vector:                


        p0 = [self.pos_from.x, self.pos_from.y]
        p1 = [self.pos_end.x, self.pos_end.y]
        p2 = [segment.pos_from.x, segment.pos_from.y]
        p3 = [segment.pos_to.x, segment.pos_to.y]

        s10_x = p1[0] - p0[0]
        s10_y = p1[1] - p0[1]
        s32_x = p3[0] - p2[0]
        s32_y = p3[1] - p2[1]

        denom = float(s10_x * s32_y - s32_x * s10_y)

        if denom == 0 : return None # collinear

        denom_is_positive = denom > 0

        s02_x = p0[0] - p2[0]
        s02_y = p0[1] - p2[1]

        s_numer = s10_x * s02_y - s10_y * s02_x

        if (s_numer < 0) == denom_is_positive : return None # no collision

        t_numer = s32_x * s02_y - s32_y * s02_x

        if (t_numer < 0) == denom_is_positive : return None # no collision

        if (s_numer > denom) == denom_is_positive or (t_numer > denom) == denom_is_positive : return None # no collision

        # collision detected

        t = t_numer / denom

        return Vector(p0[0] + (t * s10_x), p0[1] + (t * s10_y))
