from entity import Entity
from vector import Vector
from frustum import Frustum
from ray import Ray
import input
import engine
import config
import math


class Player(Entity):
    def __init__(self, x, y):
        super().__init__()
        self.pos.x = x
        self.pos.y = y
        self.frustum = Frustum()
        self.move_speed = 1.2
        self.rot_speed = 90

    def update(self, delta) -> None:

        rads = math.radians(self.rotation)

        if input.get_key_state(input.KEY_MOVE_FORWARD):
            self.vel.x += math.cos(rads) * self.move_speed * delta
            self.vel.y += math.sin(rads) * self.move_speed * delta
        if input.get_key_state(input.KEY_MOVE_BACK):
            self.vel.x -= math.cos(rads) * self.move_speed * delta
            self.vel.y -= math.sin(rads) * self.move_speed * delta
        if input.get_key_state(input.KEY_STRAFE_LEFT):
            self.vel.x -= math.cos(rads + math.radians(90)) * self.move_speed * delta
            self.vel.y -= math.sin(rads + math.radians(90)) * self.move_speed * delta
        if input.get_key_state(input.KEY_STRAFE_RIGHT):
            self.vel.x -= math.cos(rads - math.radians(90)) * self.move_speed * delta
            self.vel.y -= math.sin(rads - math.radians(90)) * self.move_speed * delta

        self.pos.x += self.vel.x
        self.pos.y += self.vel.y

        # started some collision stuff, needs to be a lot nicer though. 
        # cur_speed = Vector.Length(self.vel)

        # if(cur_speed > 0):
        #     move_angle = math.atan2(self.vel.y, self.vel.x)
        #     ray: Ray = Ray(self.pos, move_angle, 0.2)
        #     result = ray.cast(engine.get_top_state().world.map_data.segments)
        #     if result is not None:
        #         self.pos.x -= math.cos(move_angle) * result.depth
        #         self.pos.y -= math.sin(move_angle) * result.depth
        #         self.vel.x = 0
        #         self.vel.y = 0

        self.vel.x *= 0.1
        self.vel.y *= 0.1

        if input.get_key_state(input.KEY_ROTATE_LEFT):
            self.rotation -= self.rot_speed * delta
        if input.get_key_state(input.KEY_ROTATE_RIGHT):
            self.rotation += self.rot_speed * delta

        self.frustum.update(self.pos, self.rotation, config.FOV, config.VIEW_DIST)

        return super().update(delta)

    def render(self) -> None:
        return super().render()
