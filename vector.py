
import math

class Vector:
    def __init__(self, x: float, y: float):
        self.x: float = x
        self.y: float = y

    def Dot(left, right) -> float:
        return left.x * right.x + left.y * right.y

    def Length(v) -> float:
        return math.sqrt(v.x * v.x + v.y * v.y)

    def Normalise(v):
        len = Vector.Length(v)
        return Vector(v.x / len, v.y / len)