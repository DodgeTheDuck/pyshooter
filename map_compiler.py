
from segment import Segment
from ray import Ray
from game_map_data import GameMapData
from vector import Vector
import math
import threading
import time

class IntersectResult:
    def __init__(self, pos, left, right):
        self.pos = pos
        self.left = left
        self.right = right              

class MapCompiler:
    def __init__(self) -> None:
        self.map_data: GameMapData = None
        self.segments = []
        self.active_segment = None
        self.intersect_line = None
        self.is_building_debug: bool = False
        self.last_segment_first: int = 0
        self.last_segment_second: int = 0        

    def compile_debug(self, map_data) -> GameMapData:
        if self.is_building_debug == False: 
            if len(map_data.segments) <= 1:
                raise Exception("invalid map to compile")
            self.map_data = map_data
            self.is_building_debug = True

        if self.last_segment_first == len(self.map_data.segments):
            self.is_building_debug = False
            self.last_segment_first = 0
            self.last_segment_second = 0

        if self.is_building_debug:
            self.__do_bsp_debug()

    def compile(self, map_data) -> GameMapData:
        if len(map_data.segments) <= 1:
            raise Exception("invalid map to compile")
        self.map_data = map_data
        for segment in self.map_data.segments:
            self.__do_bsp(segment)

    def render(self):
        pass

    def __do_bsp_debug(self) -> None:        
            
            print("testing {0} against {1}".format(self.last_segment_first, self.last_segment_second))

            root: Segment = self.map_data.segments[self.last_segment_first]
            segment: Segment = self.map_data.segments[self.last_segment_second]

            if root == segment: 
                self.last_segment_second += 1
                return None

            angle: Vector = Vector.Normalise(Vector(root.pos_from.x - root.pos_to.x, root.pos_from.y - root.pos_to.y))
            intersect_end_angle = math.atan2(angle.y, angle.x)
            intersect_end_point = Vector(root.pos_from.x + math.cos(intersect_end_angle) * 10000, root.pos_from.y + math.sin(intersect_end_angle) * 10000)
            intersect_start_point = Vector(root.pos_from.x - math.cos(intersect_end_angle) * 10000, root.pos_from.y - math.sin(intersect_end_angle) * 10000)
            self.intersect_line = Segment(intersect_start_point, intersect_end_point)

            intersect = self.__line_segment_intersect(root.pos_from, angle, segment.pos_from, segment.pos_to)
                
            if intersect is not None and intersect.pos is not None:
                self.segments.append(intersect.left)
                self.segments.append(intersect.right)

            if self.last_segment_second == len(self.map_data.segments)-1:
                self.last_segment_second = 0
                self.last_segment_first += 1
            else:
                self.last_segment_second += 1

            return None                
                

    def __do_bsp(self, root: Segment) -> None:        
        for segment in self.map_data.segments:            
            if segment == root: continue                
            angle = Vector.Normalise(Vector(root.pos_from.y - root.pos_to.y, root.pos_from.x - root.pos_to.x))
            intersect = self.__line_segment_intersect(root.pos_from, angle, segment.pos_from, segment.pos_to)
            if intersect is not None and intersect.pos is not None:
                self.segments.append(intersect.left)
                self.segments.append(intersect.right)
            
    def __line_segment_intersect(self, line_pos: Vector, line_direction: Vector, seg_from: Vector, seg_to: Vector) -> IntersectResult:        

        p = seg_from
        r = seg_to - seg_from
        q = line_pos
        s = line_direction

        n = Vector(s.y, -s.x)        
        a = Vector.Dot(q-p, n)
        b = Vector.Dot(r, n)

        if b == 0:
            return None

        t = a / b
        if t >= 0.0 and t <= 1.0:
            intersect_pont: Vector = p + r * t
            return IntersectResult(intersect_pont, Segment(seg_from, intersect_pont), Segment(intersect_pont, seg_to))

        return None

