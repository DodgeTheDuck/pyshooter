import pygame as pg


class Metric:
    def __init__(self, name, parent=None, start=0, end=0, percentage=0):
        self.name = name
        self.parent = parent
        self.indent = 0 if parent is None else parent.indent + 1
        self.start = [start]
        self.end = [end]
        self.avg = 0
        self.percentage = 0


class MetricTimer:
    def __init__(self) -> None:
        self.start_ms = 0
        self.end_ms = 0
        self.points: dict[str, Metric] = dict()
        self.parent_stack = []
        pass

    def start(self) -> None:
        for key in self.points:
            self.points[key].start = []
            self.points[key].end = []
        self.start_ms = pg.time.get_ticks()

    def measure_start(self, name: str) -> None:
        if name in self.points:
            self.points[name].start.append(pg.time.get_ticks())
            self.parent_stack.append(self.points[name])
        else:
            parent = None if len(self.parent_stack) == 0 else self.parent_stack[-1]
            self.points[name] = Metric(name, parent, pg.time.get_ticks())
            self.parent_stack.append(self.points[name])

    def measure_end(self, name: str) -> None:
        self.points[name].end.append(pg.time.get_ticks())
        self.parent_stack.pop()

    def get_metrics(self) -> dict:
        return self.points

    def end(self) -> None:
        self.end_ms = pg.time.get_ticks()
        self.__update_metrics_avg()
        self.__update_metrics_percentage()

    def __update_metrics_avg(self) -> None:
        for key in self.points:
            p = self.points[key]
            total = 0
            for i in range(len(p.start)):
                total += p.end[i] - p.start[i]
            p.avg = total / len([p.start])

    def __update_metrics_percentage(self) -> None:

        for key in self.points:
            p: Metric = self.points[key]
            total_ms = 0
            if p.parent is None:
                total_ms = self.end_ms - self.start_ms
            else:
                total_ms = p.parent.avg

            if total_ms == 0:
                p.percentage = 0
            else:
                p.percentage = float((p.avg / total_ms) * 100)
