
from framebuffer import Framebuffer
from pixel import Pixel
import pygame as pg
import config
import game as Game

class Gfx:
    def __init__(self, pg_surface: pg.Surface):
        pg.font.init()                    
        self.font = pg.font.SysFont("bahnschrift", 30)
        self.surface = pg_surface
        self.framebuffer = Framebuffer(config.WIDTH * config.RENDER_SCALE, config.HEIGHT * config.RENDER_SCALE)        

    def set_pixel(self, x, y, color): 
        self.framebuffer.set_pixel(x, y, color)

    def clear_buffer(self) -> None:
        self.framebuffer.clear()

    def draw_buffer(self) -> None:
        self.surface.blit(pg.transform.scale(self.framebuffer.buffer, (config.WIDTH, config.HEIGHT)), (0, 0))
        pass

    def draw_ui(self) -> None:
        s_txt_fps: pg.Surface = self.font.render("FPS: {0} / TPS: {1}".format(Game.fps, Game.tps), True, (0, 255, 0))
        self.surface.blit(s_txt_fps, (32, 32))
    

    def swap_buffers(self) -> None:        
        pg.display.flip()    
        