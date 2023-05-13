
from vector import Vector

class Player:
    def __init__(self, x, y):
        self.pos = Vector(x, y)
        self.angle = 0