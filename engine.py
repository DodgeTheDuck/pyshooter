import config
import sys
import input
import pygame as pg
from gfx import Gfx
from engine_state import EngineState

gfx: Gfx = None
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
    global gfx, fps, time_last_frame, world
    pg.init()
    gfx = Gfx(pg.display.set_mode(config.RESOLUTION))
    time_last_frame = pg.time.get_ticks()            

def push_state(state: EngineState) -> None:
    engine_state.append(state)

def run() -> None:
    global fps, fps_counter, tps, tps_counter, time_last_update, time_last_render, time_last_loop, second_timer

    #main game loop
    while True:

        #pygame window event checks
        __check_events()

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
            fps = fps_counter
            tps = tps_counter
            fps_counter = 0
            tps_counter = 0
            second_timer = 0

        #perform update and render when required
        #TODO: stop calculating update/render frequency every frame
        if(update_delta > 1000.0/config.TPS_MAX):
            __update(update_delta / 1000.0)
            tps_counter+=1
            time_last_update = time_now
            
        if(render_delta > 1000.0/config.FPS_MAX):
            __render()
            fps_counter+=1
            time_last_render = time_now

        time_last_loop = time_now

def get_top_state() -> EngineState:
    return engine_state[-1]

def __update(delta) -> None:    
    get_top_state().update(delta)
    pass

def __render() -> None:    

    # n_rays = round(config.WIDTH * config.RENDER_SCALE)
    # fov_rads: float = Math.radians(config.FOV)
    # fov_rads_half: float = fov_rads / 2
    # rad_step = fov_rads / n_rays    
    # mid_screen = round((config.HEIGHT * config.RENDER_SCALE) / 2)

    # screen_dist = ((config.WIDTH * config.RENDER_SCALE) / 2) / Math.tan(fov_rads_half)    

    # for i in range(n_rays):        
    #     ray_angle = -fov_rads_half + (rad_step * i) + player.angle
    #     ray = Ray(Vector(player.pos.x, player.pos.y), ray_angle)
    #     result = ray.cast(segments)
    #     if result is not None:                        
    #         depth = result.depth * Math.cos(player.angle - ray_angle)
    #         proj_height = screen_dist / (depth + 0.0001)
    #         for j in range(round(proj_height)):
    #             gfx.set_framebuffer_pixel(i, round((mid_screen-proj_height/2))+j, (Math.pow(depth, 2) , 0, 0))
    
    gfx.clear_buffer()
    gfx.draw_buffer()

    get_top_state().render()

    gfx.draw_ui()
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
            
