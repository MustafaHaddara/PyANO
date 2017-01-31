#!/usr/local/bin/python
# This class manages a piano key

# stdlib imports
import pygame

class Key():
    pygame.init()
    font = pygame.font.SysFont('Arial', size=36)

    def __init__(self, label, keyboard_trigger, key_num, white_key=True):
        self.label = label
        self.type = 'white' if white_key else 'black'
        self.color = '#FFFFFF' if white_key else '#000000'
        self.shaded = '#BBBBBB' if white_key else '#444444'

        # font.render returns a pygame Surface object
        # we'll need to blit it to the screen after we draw the bounding rect
        self.label_color = '#000000' if white_key else '#FFFFFF'
        self.label_text = Key.font.render(self.label, True, pygame.Color(self.label_color))
        self.label_position = (0,0)

        self.keyboard_code = keyboard_trigger
        self.key_num = key_num
        self.mouse_trigger = pygame.Rect(0,0,0,0)

    def toggle_highlight(self):
        # toggles the highlights
        self.color, self.shaded = self.shaded, self.color

    def draw(self, window):
        # draw the key
        window.fill(color=pygame.Color(self.color), rect=self.mouse_trigger)
        # and the label
        window.blit(self.label_text, self.label_position) 
