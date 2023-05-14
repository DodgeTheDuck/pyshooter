
from framebuffer import Framebuffer
from pixel import Pixel
import pygame as pg
import config
import engine as Game

class Gfx:
    def __init__(self, pg_surface: pg.Surface):
        pg.font.init()
        self.surface = pg_surface
        self.framebuffer = Framebuffer(config.WIDTH * config.RENDER_SCALE, config.HEIGHT * config.RENDER_SCALE)        

    def set_framebuffer_pixel(self, x, y, color) -> None: 
        self.framebuffer.set_pixel(x, y, color)

    def draw_framebuffer_wall(self, x, y, width, height, color) -> None:
        pg.draw.rect(self.framebuffer.buffer, color, pg.Rect(x,y, width, height))

    def render_line(self, x0, y0, x1, y1, color) -> None:
        pg.draw.line(self.surface, color, (x0, y0), (x1, y1), 2)

    def render_circle(self, x, y, r, color) -> None:
        pg.draw.circle(self.surface, color, (x, y), r)    

    def clear_buffer(self) -> None:
        self.framebuffer.clear()

    def draw_buffer(self) -> None:
        self.surface.blit(pg.transform.scale(self.framebuffer.buffer, (config.WIDTH, config.HEIGHT)), (0, 0))
        pass

    def swap_buffers(self) -> None:        
        pg.display.flip()    
        