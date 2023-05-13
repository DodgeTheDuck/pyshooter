
from vector import Vector
from segment import Segment
from ray_hit_result import RayHitResult
import math as Math

class Ray:
    
    def __init__(self, pos_from: Vector, angle: float):
        self.pos_from = pos_from
        self.angle = angle

    def cast(self,  segments: list[Segment]) -> RayHitResult:
        for segment in segments:
            result = self.__test_intersect_new(segment)
            if result is not None:
                depth = round(Math.sqrt(result.x * result.x + result.y * result.y))
                return RayHitResult(depth, result.x, result.y, segment)
        return None

    def __test_intersect_new(self, segment: Segment) -> Vector:        

        pos_end = Vector(
            self.pos_from.x + Math.cos(self.angle) * 1000,
            self.pos_from.y + Math.sin(self.angle) * 1000
        )

        p0 = [self.pos_from.x, self.pos_from.y]
        p1 = [pos_end.x, pos_end.y]
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

    def __test_intersect(self, segment: Segment) -> RayHitResult:

        pos_end = Vector(
            self.pos_from.x + Math.cos(self.angle) * 1000,
            self.pos_from.y + Math.sin(self.angle) * 1000
        )

        p1 = self.pos_from
        q1 = pos_end
        p2 = segment.pos_from
        q2 = segment.pos_to

        o1 = self.__orientation(p1, q1, p2)
        o2 = self.__orientation(p1, q1, q2)
        o3 = self.__orientation(p2, q2, p1)
        o4 = self.__orientation(p2, q2, q1)

            # General case
        if ((o1 != o2) and (o3 != o4)):
            return True 
    
        # Special Cases
    
        # p1 , q1 and p2 are collinear and p2 lies on segment p1q1
        if ((o1 == 0) and self.__onSegment(p1, p2, q1)):
            return True
    
        # p1 , q1 and q2 are collinear and q2 lies on segment p1q1
        if ((o2 == 0) and self.__onSegment(p1, q2, q1)):
            return True
    
        # p2 , q2 and p1 are collinear and p1 lies on segment p2q2
        if ((o3 == 0) and self.__onSegment(p2, p1, q2)):
            return True
    
        # p2 , q2 and q1 are collinear and q1 lies on segment p2q2
        if ((o4 == 0) and self.__onSegment(p2, q1, q2)):
            return True
    
        # If none of the cases
        return False

    def __orientation(self, p, q, r):        
        val = (float(q.y - p.y) * (r.x - q.x)) - (float(q.x - p.x) * (r.y - q.y))
        if (val > 0):            
            # Clockwise orientation
            return 1
        elif (val < 0):            
            # Counterclockwise orientation
            return 2
        else:            
            # Collinear orientation
            return 0
        
    def __onSegment(self, p, q, r):
        if ( (q.x <= max(p.x, r.x)) and (q.x >= min(p.x, r.x)) and 
            (q.y <= max(p.y, r.y)) and (q.y >= min(p.y, r.y))):
            return True
        return False