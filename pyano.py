#!/usr/local/bin/python3
# stdlib
import sys

# first party
from key import Key

# external libs
import pygame

# event type constants
from pygame import KEYDOWN, KEYUP, QUIT, MOUSEBUTTONDOWN, MOUSEBUTTONUP

# allowed key constants
from pygame import (K_ESCAPE, 
    K_1, K_2, K_4, K_5, K_6, K_8, K_9, K_MINUS, K_EQUALS, K_BACKSPACE,
    K_TAB, K_q, K_w, K_e, K_r, K_t, K_y, K_u, K_i, K_o, K_p, 
    K_LEFTBRACKET, K_RIGHTBRACKET,  K_BACKSLASH)

WINDOW_HEIGHT = 400  # arbitrarily chosen

NUM_OCTAVES = 2

NUM_WHITE_KEYS = NUM_OCTAVES * 7
WHITE_KEY_WIDTH = 90
WHITE_KEY_HEIGHT = WINDOW_HEIGHT
WHITE_KEY_SPACING = 4  # needs to be even
LABEL_V_OFFSET = 10

BLACK_KEY_WIDTH = WHITE_KEY_WIDTH/3*2  # also arbitrary
BLACK_KEY_HEIGHT = 300  # also arbitrary

WINDOW_WIDTH = NUM_WHITE_KEYS*WHITE_KEY_WIDTH + (NUM_WHITE_KEYS-1) * WHITE_KEY_SPACING

keys = [
    Key('TAB', K_TAB, 40),               # C4
    Key('1', K_1, 41, False),                  # CS4
    Key('Q', K_q, 42),                   # D4
    Key('2', K_2, 43, False),                  # DS4
    Key('W', K_w, 44),                   # E4
    Key('E', K_e, 45),                   # F4
    Key('4', K_4, 46, False),                  # FS4
    Key('R', K_r, 47),                   # G4
    Key('5', K_5, 48, False),                  # GS4
    Key('T', K_t, 49),                   # A4
    Key('6', K_6, 50, False),                  # AS4
    Key('Y', K_y, 51),                   # B4
    Key('U', K_u, 52),                   # C5
    Key('8', K_8, 53, False),                  # CS5
    Key('I', K_i, 54),                   # D5
    Key('9', K_9, 55, False),                  # DS5
    Key('O', K_o, 56),                   # E5
    Key('P', K_p, 57),                   # F5
    Key('-', K_MINUS, 58, False),              # FS5
    Key('[', K_LEFTBRACKET, 59),         # G5
    Key('=', K_EQUALS, 60, False),             # GS5
    Key(']', K_RIGHTBRACKET, 61),        # A5
    Key('DEL', K_BACKSPACE, 62, False),        # AS5
    Key('\\', K_BACKSLASH, 63)           # B5
]


def get_keys(type):
    # returns generator for all keys of given type
    return (k for k in keys if k.type == type)


def get_key_of(keycode):
    # returns the key which corresponds to the given keycode, or None if no such key exists
    return next( (k for k in keys if k.keyboard_code==keycode), None)


def get_key_at(pos):
    # returns the top-most (ie. visible) key at a given coordinate
    # check black keys first (because black keys are 'on top' of white keys)
    candidate = next( (bkey for bkey in get_keys('black') if bkey.mouse_trigger.collidepoint(pos)), None)
    if candidate is None:
        candidate = next( (bkey for bkey in get_keys('white') if bkey.mouse_trigger.collidepoint(pos)), None)
    return candidate


def build_keys():
    left_offset = 0
    left_increment = WHITE_KEY_WIDTH + WHITE_KEY_SPACING
    black_key_offset = BLACK_KEY_WIDTH/2 + (WHITE_KEY_SPACING/2)
    for k in keys:
        left = left_offset
        top = 0
        if k.type == 'white':
            width = WHITE_KEY_WIDTH
            height = WHITE_KEY_HEIGHT
            # increment if we're building a white key
            left_offset += left_increment
        else:
            width = BLACK_KEY_WIDTH
            height = BLACK_KEY_HEIGHT
            left = left - black_key_offset
        # this is the bounding Rect for capture mouse clicks
        # and for drawing
        k.mouse_trigger = pygame.Rect(left, top, width, height)

        # font.render returns a pygame Surface object
        # we'll need to blit it to the screen after we draw the bounding rect
        k.label_text = font.render(k.label, True, pygame.Color(k.label_color))
        # determine position to draw the text
        label_left = left + (width - k.label_text.get_width())/2
        label_top = height - LABEL_V_OFFSET - k.label_text.get_height()
        k.label_position = (label_left, label_top)


def draw_key(key):
    window.fill(color=pygame.Color(key.color), rect=key.mouse_trigger)
    window.blit(key.label_text, key.label_position) 


def draw_keys():
    for k in get_keys('white'):
        draw_key(k)
    for k in get_keys('black'):
        draw_key(k)


def manipulate_audio(key_num):
    # 440 Hz A4
    offset = key_num - 49
    pitch = 2 ** (offset/12.0)
    # TODO play A4 track sped up/slowed down to correct pitch


def play_note(key):
    if key is None:
        return
    key.toggle_highlight()
    print('playing %s' % key.key_num)  # placeholder


def stop_note(key):
    if key is None:
        return
    key.toggle_highlight()
    print('stopping %s' % key.key_num)  # placeholder


def init():
    global window, font  # ew global variables
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.init()
    font = pygame.font.SysFont('Arial', size=36)
    window.fill(color=pygame.Color('black'))
    build_keys()


def main():
    init()
    clicked_key = None
    while True:
        draw_keys()
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    quit()
                else:
                    play_note(get_key_of(event.key))

            if event.type == KEYUP:
                stop_note(get_key_of(event.key))

            if event.type == MOUSEBUTTONDOWN:
                mPos = pygame.mouse.get_pos()
                clicked_key = get_key_at(mPos)
                play_note(clicked_key)

            if event.type == MOUSEBUTTONUP:
                stop_note(clicked_key)

            if event.type == QUIT:
                quit()

        pygame.display.flip()
        pygame.time.wait(30)  # not strictly necessary to wait


def quit():
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()