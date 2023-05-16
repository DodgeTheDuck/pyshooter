from typing import List
from pixel import Pixel
import pygame as pg


class Framebuffer:
    def __init__(self, width: int, height: int) -> None:
        self.buffer = pg.Surface((width, height))
        self.width: int = width
        self.height: int = height

    def set_pixel(self, x, y, color):
        self.buffer.set_at((x, y), color)

    def clear(self) -> None:
        self.buffer.fill((0, 0, 0))
