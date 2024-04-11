from abc import ABC

import pygame
from pygame.sprite import Sprite

import conf as c
from events import EventHandler


class Block(Sprite):
    def __init__(self, x, y, offset=12, color=c.WHITE):
        super().__init__()

        self.x = x * c.BLOCK_HEIGHT
        self.y = y * c.BLOCK_HEIGHT
        self.pos_x = x
        self.pos_y = y
        self.color = color

        self.image = pygame.Surface((c.BLOCK_HEIGHT - offset, c.BLOCK_HEIGHT - offset))
        self.rect = self.image.get_rect()

    def reposition(self, x, y):
        self.x = x * c.BLOCK_HEIGHT
        self.y = y * c.BLOCK_HEIGHT
        self.pos_x = x
        self.pos_y = y

    def update(self):
        pygame.draw.rect(self.image, self.color, self.rect)
        self.rect.center = (self.x + 0.5 * c.BLOCK_HEIGHT, self.y + 0.5 * c.BLOCK_HEIGHT)


class Clickable(ABC, Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y

    def on_click(self, func, mouse_type=1):
        @EventHandler.register(pygame.MOUSEBUTTONDOWN)
        def wrapper(event):
            if self.rect.collidepoint(event.pos) and event.button == mouse_type:
                func()


class Button(Clickable):
    def __init__(self, x, y, text, font_color=c.WHITE):
        super().__init__(x, y)

        self.pos = (x, y)
        self.text = text
        self.font_color = font_color

        font = pygame.font.SysFont('chalkduster.ttf', 72)
        self.rendered = font.render(text, True, self.font_color)

        self.click_box = pygame.Surface((self.rendered.get_width(), self.rendered.get_height()))
        self.rect = self.click_box.get_rect()
