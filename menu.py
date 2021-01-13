import pygame
from oop_menu import Board, load_image
from constans import *


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Решение')
    size = width, height = WIDTH, HEIGHT
    screen = pygame.display.set_mode(size)
    screen.fill((0, 0, 0))

    board = Board('map-obj.txt', load_image)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        all_sprites.draw(screen)
        board.render(screen)
        pygame.display.flip()
        screen.fill((0, 0, 0))
    pygame.quit()
