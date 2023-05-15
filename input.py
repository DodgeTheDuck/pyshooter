
import pygame as pg

key_states = dict()

KEY_MOVE_FORWARD = pg.K_w
KEY_STRAFE_LEFT = pg.K_a
KEY_STRAFE_RIGHT = pg.K_d
KEY_MOVE_BACK = pg.K_s

KEY_ROTATE_LEFT = pg.K_LEFT
KEY_ROTATE_RIGHT = pg.K_RIGHT

def update_key_state(key, state):
    key_states[key] = state

def get_key_state(key) -> bool: 
    return key_states.get(key, False)