import pygame
from oop_menu import *
from constants_of_menu import *


class Roles:
    def __init__(self):
        self.count_of_coins = 0
        self.font = pygame.font.Font(None, 30)
        self.text1 = self.font.render("Чтобы начать уровень, нажмите английскую p,", True, (255, 100, 100))
        self.text2 = self.font.render("находясь на нем.", True, (255, 100, 100))
        self.text3 = self.font.render("Чтобы выйти из игры нажмите escape", True, (255, 100, 100))
        self.image_coin = load_image('coin.png', 'data')
        self.screen2 = pygame.Surface(
            [self.text1.get_width(),
             self.image_coin.get_height() +
             + self.text1.get_height() + self.text2.get_height() + self.text3.get_height() + 66])
        self.screen2.fill('black')
        self.screen2.blit(self.image_coin, (0, 0))
        self.screen2.blit(self.text1, (0, self.image_coin.get_height() + 22))
        self.screen2.blit(self.text2, (0, self.image_coin.get_height() + self.text1.get_height() + 44))
        self.screen2.blit(self.text3,
                          (0, self.image_coin.get_height() + self.text1.get_height() + self.text2.get_height() + 66))
        self.font = pygame.font.Font(None, 100)

    def print_rules(self):
        self.coin_count = self.font.render(f"{self.count_of_coins}", True, (255, 100, 100))
        pygame.draw.rect(self.screen2, 'black', (
            self.image_coin.get_width(), 0, self.screen2.get_width() - self.image_coin.get_width(),
            self.coin_count.get_height()))
        self.screen2.blit(self.coin_count, (self.image_coin.get_width() + 10, 0))
        return self.screen2


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Решение')
    size = WIDTH, HEIGHT
    screen = pygame.display.set_mode(size)
    screen.fill((0, 0, 0))
    rules = Roles()
    board = Board('map-obj.txt', load_image)
    board.render(screen)
    for i in level_sprites:
        all_sprites.add(i)
    all_sprites.add(board.pers)
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
    level = None
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
        level = board.pers.level_collide()

        if level:
            if pygame.key.get_pressed()[pygame.K_p] and level.ready:
                rules.count_of_coins += level.run()
                if len(board.level_list) - 1 != board.level_list.index(level):
                    board.level_list[board.level_list.index(level) + 1].ready = True
                clock.tick()
                board.pers.all_flags_move_false()

        board.render(screen)
        all_sprites.draw(screen)
        screen.blit(rules.print_rules(), (WIDTH // 60, HEIGHT // 60))
        pygame.display.flip()
        screen.fill((0, 0, 0))
    pygame.quit()
