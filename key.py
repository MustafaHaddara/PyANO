#!/usr/local/bin/python3

import pygame

class Key():
    def __init__(self, label, keyboard_trigger, key_num, white_key=True):
        self.label = label
        self.type = 'white' if white_key else 'black'
        self.color = '#FFFFFF' if white_key else '#000000'
        self.shaded = '#BBBBBB' if white_key else '#444444'
        self.label_color = '#000000' if white_key else '#FFFFFF'
        self.label_position = (0,0)

        self.keyboard_code = keyboard_trigger
        self.key_num = key_num
        self.mouse_trigger = pygame.Rect(0,0,0,0)

    def toggle_highlight(self):
        self.color, self.shaded = self.shaded, self.color