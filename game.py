import config
from gfx import Gfx
import sys
import pygame as pg

gfx: Gfx = None
time_last_render: int = 0
time_last_update: int = 0
time_last_loop: int = 0
second_timer: int = 0
fps_counter: int = 0
tps_counter: int = 0
fps: int = 0
tps: int = 0

def init() -> None:
    global gfx, fps, time_last_frame    
    pg.init()
    gfx = Gfx(pg.display.set_mode(config.RESOLUTION))
    time_last_frame = pg.time.get_ticks()    

def run() -> None:
    global fps, fps_counter, tps, tps_counter, time_last_update, time_last_render, time_last_loop, second_timer
    while True:
        check_events()

        #TODO: perhaps wrap timing shizzle in class/module
        time_now: int = pg.time.get_ticks()
        update_delta: int = time_now - time_last_update
        render_delta: int = time_now - time_last_render
        loop_delta: int = time_now - time_last_loop

        second_timer += loop_delta

        if(second_timer >= 1000):
            fps = fps_counter
            tps = tps_counter
            fps_counter = 0
            tps_counter = 0
            second_timer = 0            

        if(update_delta > 1000.0/config.TPS_MAX):
            __update(update_delta)
            tps_counter+=1
            time_last_update = time_now
            
        if(render_delta > 1000.0/config.FPS_MAX):
            __render()
            fps_counter+=1
            time_last_render = time_now

        time_last_loop = time_now

def __update(delta) -> None: 
    pass

def __render() -> None:
    global gfx
    for i in range(1, round(config.HEIGHT * config.RENDER_SCALE)-1):
        if i % 2: gfx.set_pixel(16, i, (255, 0, 0))
    gfx.draw_buffer()
    gfx.draw_ui()
    gfx.swap_buffers()
    pass

def check_events():        
    for event in pg.event.get():
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
            pg.quit()
            sys.exit()
