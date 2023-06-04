
import pygame as pg

key_states = dict()

KEY_MOVE_FORWARD = pg.K_w
KEY_STRAFE_LEFT = pg.K_a
KEY_STRAFE_RIGHT = pg.K_d
KEY_MOVE_BACK = pg.K_s

KEY_ROTATE_LEFT = pg.K_LEFT
KEY_ROTATE_RIGHT = pg.K_RIGHT

KEY_MAP_LEFT = pg.K_LEFT
KEY_MAP_RIGHT = pg.K_RIGHT
KEY_MAP_UP = pg.K_UP
KEY_MAP_DOWN = pg.K_DOWN

KEY_MAP_COMPILE = pg.K_b

def update_key_state(key, state):
    key_states[key] = state

def get_key_state(key) -> int: 
    return key_states.get(key, False)