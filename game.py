import config
from gfx import Gfx
import sys
import pygame as pg
from ray import Ray
from segment import Segment
from vector import Vector
import math as Math
from player import Player

gfx: Gfx = None
time_last_render: int = 0
time_last_update: int = 0
time_last_loop: int = 0
second_timer: int = 0
fps_counter: int = 0
tps_counter: int = 0
fps: int = 0
tps: int = 0
player: Player

def init() -> None:
    global gfx, fps, time_last_frame, player 
    pg.init()
    gfx = Gfx(pg.display.set_mode(config.RESOLUTION))
    time_last_frame = pg.time.get_ticks()    
    player = Player(0, 0)

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
    global player
    player.pos.x += 0.5 * float(delta/1000.0)
    #player.angle += 0.1 * float(delta/1000.0)
    pass

def __render() -> None:
    global gfx, player

    gfx.clear_buffer()

    n_rays = round(config.WIDTH * config.RENDER_SCALE)
    fov_rads: float = Math.radians(config.FOV)
    fov_rads_half: float = fov_rads / 2
    rad_step = fov_rads / n_rays    
    mid_screen = round((config.HEIGHT * config.RENDER_SCALE) / 2)

    screen_dist = ((config.WIDTH * config.RENDER_SCALE) / 2) / Math.tan(fov_rads_half)

    segments = [
        Segment(Vector(-10, 10), Vector(10, 10)),
        Segment(Vector(10, 10), Vector(10, -10)),
        Segment(Vector(10, -10), Vector(-10, -10)),
        Segment(Vector(-10, -10), Vector(-10, 10))
    ]    

    for i in range(n_rays):        
        ray_angle = -fov_rads_half + (rad_step * i) + player.angle
        ray = Ray(Vector(player.pos.x, player.pos.y), ray_angle)
        result = ray.cast(segments)
        if result is not None:                        
            depth = result.depth * Math.cos(player.angle - ray_angle)
            proj_height = screen_dist / (depth + 0.0001)
            for j in range(round(proj_height)):
                gfx.set_pixel(i, round((mid_screen-proj_height/2))+j, (Math.pow(depth, 2) , 0, 0))
    
    gfx.draw_buffer()
    gfx.draw_ui()
    gfx.swap_buffers()
    pass

def check_events():        
    for event in pg.event.get():
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
            pg.quit()
            sys.exit()
        elif event.type == pg.KEYDOWN and event.key == pg.K_w:
            player.pos.y += 0.1
        elif event.type == pg.KEYDOWN and event.key == pg.K_s:
            player.pos.y -= 0.1
            
