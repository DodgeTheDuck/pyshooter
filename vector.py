import math


class Vector:
    def __init__(self, x: float, y: float):
        self.x: float = x
        self.y: float = y

    @staticmethod
    def dot(left, right) -> float:
        return left.x * right.x + left.y * right.y

    @staticmethod
    def length(v) -> float:
        return math.sqrt(v.x * v.x + v.y * v.y)

    @staticmethod
    def normalise(v):
        vlen = Vector.length(v)
        return Vector(v.x / vlen, v.y / vlen)
