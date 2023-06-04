
from segment import Segment
from vector import Vector
import engine as Game
import config

class GameMapData:
    def __init__(self):
        self.segments: list[Segment] = []        
        self.spawn_point: Vector = Vector(0, 0)

    def load_map_file(self, name) -> None:
        with open("maps/{0}.map".format(name), "r") as f:
            line = f.readline()
            while line:
                if "SPAWN" in line:
                    line = line.replace("SPAWN:", "")
                    coords = line.split(",")
                    if len(coords) != 2: raise Exception("!!currupt spawn!!")
                    self.set_spawn_point(Vector(float(coords[0]), float(coords[1])))
                elif "SEG" in line:
                    line = line.replace("SEG:", "")
                    coords = line.split(",")
                    if len(coords) != 4: raise Exception("!!currupt segment!!")
                    self.segments.append(Segment(
                        Vector(float(coords[0]), float(coords[1])),
                        Vector(float(coords[2]), float(coords[3])),
                    ))
                line = f.readline()

    def set_spawn_point(self, point: Vector) -> None:
        self.spawn_point = point

    def add_segment(self, segment: Segment) -> int:
        self.segments.append(segment)
        return len(self.segments) - 1
    
    def get_segment(self, index: int) -> Segment:
        return self.segments[index]
    
    def update_segment(self, index: int, segment: Segment) -> None:
        self.segments[index] = segment
