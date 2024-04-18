from abc import ABC, abstractmethod

import pygame

import conf as c
from elements import Button
from events import EventHandler
from snake import Snake, SnakeGUI, GAME_OVER_EVENT


class State(ABC):  # Abstrakte Base-Klasse für die verschiedenen Spielzustände
    def __init__(self):
        self.new_state = None

    @abstractmethod
    def update(self, dt):
        return

    @abstractmethod
    def draw(self):
        return

    def next_state(self):
        if self.new_state is None:
            return self
        else:
            state = self.new_state
            self.new_state = None
            return state


class Game(State):  # Subklasse von State, die das eigentliche Spiel repräsentiert
    def __init__(self, screen):
        super().__init__()
        self.clock = 0
        self.speed = (18 - c.SPEED * 2) * c.FRAMES

        self.screen = screen
        self.snake = Snake(c.GRID)
        self.gui = SnakeGUI(self)
        self.add_events()

    def add_events(self):
        @EventHandler.register(pygame.KEYDOWN, c.MOVE_UP)
        def change_dir_up(event):
            self.snake.change_dir(0, -1)

        @EventHandler.register(pygame.KEYDOWN, c.MOVE_DOWN)
        def change_dir_down(event):
            self.snake.change_dir(0, 1)

        @EventHandler.register(pygame.KEYDOWN, c.MOVE_LEFT)
        def change_dir_left(event):
            self.snake.change_dir(-1, 0)

        @EventHandler.register(pygame.KEYDOWN, c.MOVE_RIGHT)
        def change_dir_right(event):
            self.snake.change_dir(1, 0)

        @EventHandler.register(GAME_OVER_EVENT.type)
        def game_over(event):
            score = len(self.snake)
            self.new_state = GameOver(self.screen, "Game Over", score)


    def update(self, dt):
        self.clock += 100 + dt
        if self.clock >= self.speed:
            self.snake.move()
            self.clock = 0

        self.gui.update()

        # change speed when snake length is 10 or more
        if len(self.snake) >= 10:
            self.speed = 2

    def draw(self):
        self.gui.draw(self.screen)


class GameOver(State):  # Subklasse von State, die den Spielzustand nach dem Game Over repräsentiert
    def __init__(self, screen, message, score):
        super().__init__()

        self.screen = screen
        self.message = message

        # play again
        self.play_again_btn = Button(0, 0, text="Play again")

        def click():
            # starts new game here
            self.new_state = Game(self.screen)
        self.play_again_btn.on_click(click)

        self.sprites = pygame.sprite.Group()
        self.sprites.add(self.play_again_btn)

        # game over
        font = pygame.font.SysFont('chalkduster.ttf', 72)
        font_small = pygame.font.SysFont('chalkduster.ttf', 40)
        self.game_over = font.render(self.message, True, c.WHITE)
        self.score = font_small.render(f"Score: {score}", True, c.WHITE)

    def update(self, dt):
        return

    def draw(self):
        center = self.game_over.get_rect(center=self.screen.get_rect().center)

        self.screen.blit(self.game_over, center)
        self.screen.blit(self.play_again_btn.rendered, self.play_again_btn.pos)

        # positioning score centered below game over message
        center = self.score.get_rect(center=(center[0] + self.game_over.get_rect().width / 2, center[1] + 60))
        self.screen.blit(self.score, center)


class StartGame(State):
    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        # start button
        self.start_btn = Button(0, 0, text="Start")

        def click():
            # starts the game here
            self.new_state = Game(self.screen)

        self.start_btn.on_click(click)

        self.sprites = pygame.sprite.Group()
        self.sprites.add(self.start_btn)

    def update(self, dt):
        return

    def draw(self):
        self.screen.blit(self.start_btn.rendered, self.start_btn.pos)
