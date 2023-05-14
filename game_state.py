
import pygame as pg
from world import World
from engine_state import EngineState

class GameState(EngineState):
    def __init__(self) -> None:
        self.world = World()
        super().__init__()
    
    def update(self, delta) -> None:        
        self.world.update(delta)
        return super().update(delta)
    
    def render(self) -> None:
        self.world.render()        
        return super().render()
    
    def handle_event(self, event: pg.event.Event) -> None:
        return super().handle_event(event)