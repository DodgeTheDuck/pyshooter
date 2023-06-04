
import pygame as pg

from map_editor import MapEditor
from player import Player
from engine_state import EngineState
from map_compiler import MapCompiler
import input
import engine

class MapEditorState(EngineState):
    def __init__(self) -> None:        
        self.editor = MapEditor()
        self.editor.load("test")
        self.compiler: MapCompiler = MapCompiler()        
        self.compiling: bool = False        
        self.step_compiler: bool = True
        super().__init__()
    
    def update(self, delta) -> None:        
        self.editor.update(delta)
        
        if input.get_key_state(input.KEY_MAP_COMPILE):            
            self.compiling = True
            if self.step_compiler == True:
                self.compiler.compile_debug(self.editor.map_data)
                self.step_compiler = False
        else:
            self.step_compiler = True

        return super().update(delta)
    
    def render(self) -> None:

        engine.gfx.clear_all()

        #TODO: make a map renderer that the compiler and editor can both use
        if self.compiling:
            self.editor.render_compiler(self.compiler)
        else:
            self.editor.render_editor()

        return super().render()
    
    def handle_event(self, event: pg.event.Event) -> None:
        if event.type == pg.KEYDOWN and event.key == pg.K_s and pg.key.get_mods() & pg.KMOD_CTRL:
            self.editor.save("test")
        return super().handle_event(event)