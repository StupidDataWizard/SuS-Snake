import random

import numpy as np
import pygame

import conf as c
from elements import Block
from events import EventHandler

FRUIT_EVENT = pygame.event.Event(pygame.event.custom_type())
GAME_OVER_EVENT = pygame.event.Event(pygame.event.custom_type())


class Snake:
    def __init__(self, size):
        self.size = size
        self.dir_x = 1
        self.dir_y = 0
        self.array = np.zeros([self.size, self.size], dtype=int)

        self.initialize()

    def initialize(self):
        # create snake
        self[c.SNAKE_START_X, c.SNAKE_START_Y] = 1
        self.spawn_fruit()

    @property
    def head_pos(self):
        pos = np.where(self.array == 1)
        return pos[1][0], pos[0][0]

    @property
    def tail_pos(self):
        pos = np.where(self.array == np.amax(self.array))
        return pos[1][0], pos[0][0]

    @property
    def fruit_pos(self):
        pos = np.where(self.array == -1)
        return pos[1][0], pos[0][0]

    @property
    def pos(self):
        pos = np.where(self.array > 0)
        pos = np.array(pos).transpose()
        tmp = np.copy(pos[:, 0])
        pos[:, 0] = pos[:, 1]
        pos[:, 1] = tmp
        return pos

    def spawn_fruit(self):
        empty_blocks = np.where(self.array == 0)
        idx = random.choice(range(len(empty_blocks[0])))

        fruit_x = empty_blocks[1][idx]
        fruit_y = empty_blocks[0][idx]
        self[fruit_x, fruit_y] = -1

    def change_dir(self, x, y):
        # deny movement in opposite direction
        if self.dir_x * x >= 0 and self.dir_y * y >= 0:
            self.dir_x = x
            self.dir_y = y

    def move(self):
        head_x, head_y = self.head_pos
        head_move_x = head_x + self.dir_x
        head_move_y = head_y + self.dir_y

        # game over condition if snake bounces on itself or leaves border
        try:
            if self[head_move_x, head_move_y] > 0:
                pygame.event.post(GAME_OVER_EVENT)
            if head_y + self.dir_y < 0 or head_x + self.dir_x < 0:
                pygame.event.post(GAME_OVER_EVENT)
        except IndexError:
            pygame.event.post(GAME_OVER_EVENT)
            return

        # move snake in grid by adding +1 to all snake fields
        for pos in self.pos:
            self[pos] += 1

        # check if on fruit
        if self[head_move_x, head_move_y] == -1:
            pygame.event.post(FRUIT_EVENT)
            self.spawn_fruit()
        else:
            self[self.tail_pos] = 0
        self[head_move_x, head_move_y] = 1

    def __len__(self):
        return np.amax(self.array)

    def __getitem__(self, pos):
        x, y = pos
        return self.array[y][x]

    def __setitem__(self, key, value):
        x, y = key
        self.array[y][x] = value

    def __repr__(self):
        return self.array


class SnakeGUI:
    def __init__(self, state):
        self.state = state
        self.blocks = pygame.sprite.OrderedUpdates()
        self.fruit = pygame.sprite.OrderedUpdates()
        self.register_fruit_event()

        for pos in self.state.snake.pos:
            self.blocks.add(Block(*pos))
        self.fruit.add(Block(*self.state.snake.fruit_pos, offset=c.FRUIT_SIZE, color=c.ORANGE))

    def register_fruit_event(self):
        @EventHandler.register(FRUIT_EVENT.type)
        def on_fruit_wrapper(event):
            self.blocks.add(Block(*self.state.snake.tail_pos))
            for fruit in self.fruit.spritedict:
                fruit.reposition(*self.state.snake.fruit_pos)

    def reposition_blocks(self):
        for pos, block in zip(self.state.snake.pos, self.blocks.spritedict):
            block.reposition(*pos)

    def update(self):
        self.reposition_blocks()
        self.blocks.update()
        self.fruit.update()

    def draw(self, screen):
        self.blocks.draw(screen)
        self.fruit.draw(screen)
