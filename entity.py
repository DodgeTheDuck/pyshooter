from vector import Vector


class Entity:
    def __init__(self):
        self.vel: Vector = Vector(0, 0)
        self.pos: Vector = Vector(0, 0)
        self.rotation: float = 0
        self.move_speed = 0
        self.rot_speed = 0

    def update(self, delta) -> None:
        pass

    def render(self) -> None:
        pass
