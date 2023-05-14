
from segment import Segment
from vector import Vector
import game as Game
import config

class GameLevel:
    def __init__(self):
        self.segments = [
            Segment(Vector(-5, 5), Vector(5, 5)),
            Segment(Vector(5, 5), Vector(5, -5)),
            Segment(Vector(5, -5), Vector(-5, -5)),
            Segment(Vector(-5, -5), Vector(-5, 5))
        ]    
