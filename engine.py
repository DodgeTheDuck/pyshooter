import config
import sys
import input
import pygame as pg
from gfx import Gfx
from metric_timer import MetricTimer
from engine_state import EngineState
from debug import Debug

gfx: Gfx = None
debug: Debug = None
metric_timer: MetricTimer = None
time_last_render: int = 0
time_last_update: int = 0
time_last_loop: int = 0
second_timer: int = 0
fps_counter: int = 0
tps_counter: int = 0
fps: int = 0
tps: int = 0
engine_state: list[EngineState] = []

def init() -> None:
    global gfx, debug, fps, time_last_frame, metric_timer
    pg.init()
    gfx = Gfx(pg.display.set_mode(config.RESOLUTION))
    debug = Debug()
    metric_timer = MetricTimer()
    time_last_frame = pg.time.get_ticks()            

def push_state(state: EngineState) -> None:
    engine_state.append(state)

def run() -> None:
    global fps, fps_counter, tps, tps_counter, time_last_update, time_last_render, time_last_loop, second_timer, metric_timer

    #main game loop
    while True:

        metric_timer.start()
        #pygame window event checks
        metric_timer.measure_start("events")
        __check_events()
        metric_timer.measure_end("events")

        #update our timers
        #TODO: perhaps wrap timing shizzle in class/module
        #TODO: i'm sure if i think more, i don't need so many counters...
        time_now: int = pg.time.get_ticks()
        update_delta: int = time_now - time_last_update
        render_delta: int = time_now - time_last_render
        loop_delta: int = time_now - time_last_loop
        
        #keep track of various metrics
        #TODO: make this better
        second_timer += loop_delta        
        if(second_timer >= 1000):
            debug.set_metric("FPS", fps_counter)
            debug.set_metric("TPS", tps_counter)
            for key in metric_timer.get_metrics():
                metric = metric_timer.get_metrics()[key]                
                debug.set_metric(key, metric.percentage, "%", metric.indent)
            fps_counter = 0
            tps_counter = 0
            second_timer = 0

        #perform update and render when required
        #TODO: stop calculating update/render frequency every frame
        metric_timer.measure_start("update")
        if(update_delta > 1000.0/config.TPS_MAX):
            __update(update_delta / 1000.0)
            tps_counter+=1
            time_last_update = time_now
        metric_timer.measure_end("update")
            
        metric_timer.measure_start("render")
        if(render_delta > 1000.0/config.FPS_MAX):
            __render()
            fps_counter+=1
            time_last_render = time_now
        metric_timer.measure_end("render")

        metric_timer.end()        

        time_last_loop = time_now
        

def get_top_state() -> EngineState:
    return engine_state[-1]

def __update(delta) -> None:    
    get_top_state().update(delta)
    pass

def __render() -> None:    
    
    gfx.clear_buffer()

    get_top_state().render()

    debug.render()
    gfx.swap_buffers()

    pass

def __check_events():        
    for event in pg.event.get():
        get_top_state().handle_event(event)
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
            pg.quit()
            sys.exit()
        elif event.type == pg.KEYDOWN:
            input.update_key_state(event.key, True)
        elif event.type == pg.KEYUP:
            input.update_key_state(event.key, False)
            
