
from framebuffer import Framebuffer
from pixel import Pixel
import pygame as pg
import config
import engine as Game
from vector import Vector

class Gfx:
    def __init__(self, pg_surface: pg.Surface):
        pg.font.init()
        self.font = pg.font.SysFont("bahnschrift", 30)
        self.surface = pg_surface
        self.framebuffer = Framebuffer(config.WIDTH * config.RENDER_SCALE, config.HEIGHT * config.RENDER_SCALE)

    def set_framebuffer_pixel(self, x, y, color) -> None: 
        self.framebuffer.set_pixel(x, y, color)

    def draw_framebuffer_wall(self, x, y, width, height, color) -> None:
        pg.draw.rect(self.framebuffer.buffer, color, pg.Rect(x,y, width, height))

    def render_line(self, x0, y0, x1, y1, color, thickness = 1) -> None:
        pg.draw.line(self.surface, color, (x0, y0), (x1, y1), thickness)

    def render_rect(self, x0, y0, x1, y1, color) -> None:
        pg.draw.rect(self.surface, color, (x0, y0, x1, y1))

    def render_dashed_line(self, x0, y0, x1, y1, color, width=1, dash_length=10):
        origin = Vector(x0, y0)
        target = Vector(x1, y1)
        displacement = target - origin
        length = Vector.Length(displacement)
        slope = displacement/length

        for index in range(0, round(length/dash_length), 2):
            start = origin + (slope *    index    * dash_length)
            end   = origin + (slope * (index + 1) * dash_length)
            pg.draw.line(self.surface, color, (start.x, start.y), (end.x, end.y), width)

    def render_circle(self, x, y, r, color) -> None:
        pg.draw.circle(self.surface, color, (x, y), r)

    def render_text(self, x, y, text, color) -> None:
        text = self.font.render(text, True, color)
        self.surface.blit(text, (x, y))

    def clear_buffer(self) -> None:
        self.framebuffer.clear()

    def clear_all(self) -> None:
        self.clear_buffer()
        self.surface.fill((0,0,0))

    def draw_buffer(self) -> None:
        self.surface.blit(pg.transform.scale(self.framebuffer.buffer, (config.WIDTH, config.HEIGHT)), (0, 0))
        pass

    def swap_buffers(self) -> None:        
        pg.display.flip()    
        