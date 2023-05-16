import pygame as pg

from map_editor import MapEditor
from engine_state import EngineState


class MapEditorState(EngineState):
    def __init__(self) -> None:
        self.editor = MapEditor()
        self.editor.load("test")
        super().__init__()

    def update(self, delta) -> None:
        self.editor.update(delta)
        return super().update(delta)

    def render(self) -> None:
        self.editor.render()
        return super().render()

    def handle_event(self, event: pg.event.Event) -> None:
        if event.type == pg.KEYDOWN and event.key == pg.K_s and pg.key.get_mods() & pg.KMOD_CTRL:
            self.editor.save("test")
        return super().handle_event(event)
