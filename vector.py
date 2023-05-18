
import math

class Vector:
    def __init__(self, x: float, y: float):
        self.x: float = x
        self.y: float = y

    def Dot(left, right) -> float:
        return left.x * right.x + left.y * right.y

    def Length(v) -> float:
        return math.sqrt(v.x * v.x + v.y * v.y)

    def Normalise(v) -> None:
        len = Vector.Length(v)
        return Vector(v.x / len, v.y / len)

    def __str__(self) -> str:
        return "[{0},{1}]".format(self.x, self.y)

    def __mul__(self, other: float):
        return Vector(self.x * other, self.y * other)

    def __truediv__(self, other: float):
        return Vector(self.x / other, self.y / other)