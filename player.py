
from entity import Entity
from vector import Vector
from frustum import Frustum
import input
import config
import engine

class Player(Entity):
    def __init__(self, x, y):
        super().__init__()
        self.pos.x = x
        self.pos.y = y        
        self.frustum = Frustum()
        self.move_speed = 1.2
        self.rot_speed = 90

    def update(self, delta) -> None:

        if(input.get_key_state(input.KEY_MOVE_UP)):
            self.pos.y -= self.move_speed * delta
        if(input.get_key_state(input.KEY_MOVE_RIGHT)):
            self.pos.x += self.move_speed * delta
        if(input.get_key_state(input.KEY_MOVE_DOWN)):
            self.pos.y += self.move_speed * delta
        if(input.get_key_state(input.KEY_MOVE_LEFT)):
            self.pos.x -= self.move_speed * delta

        if(input.get_key_state(input.KEY_ROTATE_LEFT)):
            self.rotation -= self.rot_speed * delta
        if(input.get_key_state(input.KEY_ROTATE_RIGHT)):
            self.rotation += self.rot_speed * delta

        self.frustum.update(self.pos, self.rotation, config.FOV, config.VIEW_DIST)

        return super().update(delta)
    
    def render(self) -> None:        
        return super().render()