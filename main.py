import pygame

import conf as c
from events import EventHandler
from states import Game

# init stuff
pygame.init()

screen = pygame.display.set_mode((c.WINDOW_WIDTH, c.WINDOW_HEIGHT))
background = pygame.Surface(screen.get_rect().size)
background.fill(c.BLACK)

pygame.display.set_caption("Let us play Snake!")
active = True
clock = pygame.time.Clock()

state = Game(screen)
dt = 0


@EventHandler.register(pygame.QUIT)
def quit_game(e):
    pygame.quit()
    quit(0)


# game loop
while active:
    for event in pygame.event.get():
        EventHandler.notify(event)

    screen.blit(background, (0, 0))

    state.update(dt)
    state.draw()

    # swap states if needed
    state = state.next_state()

    # renew window
    pygame.display.flip()

    # set frames, we don`t need dt in this game
    dt = clock.tick(c.FRAMES)
