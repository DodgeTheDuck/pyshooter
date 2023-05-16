from collections import namedtuple
import pygame as pg
import engine


class Metric:
    def __init__(self, name, value, unit, indent=0):
        self.name = name
        self.value = value
        self.unit = unit
        self.indent = indent


class Debug:
    def __init__(self) -> None:
        self.font = pg.font.SysFont("bahnschrift", 30)
        self.metrics: dict[str, any] = dict()
        self.line_height = 32
        self.x = 32
        self.y = 32
        self.indent_size = 32
        pass

    def set_metric(self, name: str, value: str, unit: str = "", indent: int = 0) -> None:
        self.metrics[name] = Metric(name, value, unit, indent)
        pass

    def render(self) -> None:
        for index, key in enumerate(self.metrics):
            metric = self.metrics[key]
            format = "{0}: {1}{2}" if float(metric.value).is_integer() else "{0}: {1:.2f}{2}"
            metric_text: pg.Surface = self.font.render(format.format(key, metric.value, metric.unit), True, (0, 255, 0))
            engine.gfx.surface.blit(metric_text,
                                    (self.x + metric.indent * self.indent_size, self.y + self.line_height * index))
        pass
