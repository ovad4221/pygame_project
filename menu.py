import pygame
from oop_menu import *
from constans import *

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Решение')
    size = width, height = WIDTH, HEIGHT
    screen = pygame.display.set_mode(size)
    screen.fill((0, 0, 0))
    board = Board('map-obj.txt', load_image)
    board.render(screen)
    Barier(board.left, board.top, board.w_n * board.cell_size, board.h_n * board.cell_size, False, False, all_sprites,
           bar_sprites)
    Barier(board.left, board.top, board.w_n * board.cell_size, board.h_n * board.cell_size, True, False, all_sprites,
           bar_sprites)
    Barier(board.left, board.top, board.w_n * board.cell_size, board.h_n * board.cell_size, False, True, all_sprites,
           bar_sprites)
    Barier(board.left, board.top, board.w_n * board.cell_size, board.h_n * board.cell_size, True, True, all_sprites,
           bar_sprites)
    camera = Camera(board.pers.rect.x, board.pers.rect.y)
    pygame.mouse.set_visible(False)
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_w:
                    board.pers.up_run = True
                elif event.key == pygame.K_s:
                    board.pers.down_run = True
                elif event.key == pygame.K_a:
                    board.pers.left_run = True
                elif event.key == pygame.K_d:
                    board.pers.right_run = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    board.pers.up_run = False
                elif event.key == pygame.K_s:
                    board.pers.down_run = False
                elif event.key == pygame.K_a:
                    board.pers.left_run = False
                elif event.key == pygame.K_d:
                    board.pers.right_run = False
        all_sprites.update(clock.tick(FPS))
        camera.update(board.pers)
        board.left += camera.get_delta()[0]
        board.top += camera.get_delta()[1]
        for sprite in all_sprites:
            camera.apply(sprite)
        board.render(screen)
        all_sprites.draw(screen)
        pygame.display.flip()
        screen.fill((0, 0, 0))
    pygame.quit()
