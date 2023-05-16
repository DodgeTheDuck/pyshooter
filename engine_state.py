import pygame as pg
import config


class EngineState:

    def __init__(self) -> None:
        self.time_now: int = 0
        self.time_last_update: int = 0
        self.time_last_render: int = 0
        self.time_last_loop: int = 0
        self.fps: int = 0
        self.tps: int = 0
        self.fps_counter: int = 0
        self.tps_counter: int = 0
        self.second_timer: int = 0

    def update(self, delta) -> None:
        pass

    def render(self) -> None:
        pass

    def handle_event(self, event: pg.event.Event) -> None:
        pass
