import pygame
import sys
import os
import pytmx
from oop_maybe import *
from constans import *
from load_functions import *

# это лучше делать вне класса
pygame.init()
pygame.display.set_caption('Level')
size = WIDTH, HEIGHT
clock = pygame.time.Clock()
screen = pygame.display.set_mode(size)


def game_over():
    img = load_image('gameover.jpg', 'data')
    x = WIDTH // 2 - img.get_width() // 2
    y = HEIGHT // 2 - img.get_height() // 2
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN or \
                    event.type == pygame.KEYDOWN:
                return
        screen.fill(BLACK)
        screen.blit(img, (x, y))
        pygame.display.flip()


def win_window(screen_p, coin_count, max_coin):
    pygame.mouse.set_visible(True)
    screen2 = pygame.Surface([WIDTH // 2, HEIGHT // 1.5])
    screen2.fill((20, 20, 20))
    color_text = (255, 204, 0)
    font = pygame.font.Font(None, 180)
    text_win = font.render("YOU WIN!", True, color_text)
    font = pygame.font.Font(None, 50)
    text_coin = font.render(f"+{coin_count}/{max_coin}!", True, color_text)
    text_help = font.render("to exit tub anyone key", True, color_text)
    image_star = pygame.transform.scale(load_image('star.png', 'data'), (screen2.get_width() // 3,
                                                                         screen2.get_width() // 3))
    image_coin = pygame.transform.scale(load_image('coin.png', 'data'), (text_coin.get_height(),
                                                                         text_coin.get_height()))
    star_int = 0

    if 0 < coin_count <= max_coin // 3:
        star_int = 1
    elif max_coin // 3 < coin_count <= 2 * max_coin // 3:
        star_int = 2
    elif coin_count > 2 * max_coin // 3:
        star_int = 3

    for i in range(star_int):
        if i == 0:
            screen2.blit(pygame.transform.scale(pygame.transform.rotate(image_star, -45),
                                                (screen2.get_width() // 3, screen2.get_width() // 3)),
                         (0, screen2.get_height() // 6))
        elif i == 1:
            screen2.blit(image_star, (screen2.get_width() // 3, 0))
        elif i == 2:
            screen2.blit(pygame.transform.scale(pygame.transform.rotate(image_star, 45),
                                                (screen2.get_width() // 3, screen2.get_width() // 3)),
                         (screen2.get_width() * 2 // 3, screen2.get_height() // 6))

    screen2.blit(text_win, (screen2.get_width() // 2 - text_win.get_width() // 2, screen2.get_width() // 2.6))
    screen2.blit(text_coin, (screen2.get_width() // 2 - text_coin.get_width() // 2 - image_coin.get_width() // 2,
                             screen2.get_width() // 2.6 + text_win.get_height()))
    screen2.blit(image_coin, (screen2.get_width() // 2 + text_coin.get_width() // 2 - image_coin.get_width() // 2,
                 screen2.get_width() // 2.6 + text_win.get_height()))
    screen2.blit(text_help, (screen2.get_width() // 2 - text_help.get_width() // 2, screen2.get_height() // 1.1))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                pygame.mouse.set_visible(False)
                return
        clock.tick(FPS)
        pygame.display.flip()
        screen_p.blit(screen2, (WIDTH // 4, HEIGHT // 6))


class Question(pygame.sprite.Sprite):
    def __init__(self, s_x, s_y, *group):
        super().__init__(*group)


class Level(pygame.sprite.Sprite):
    def __init__(self, pers_x, pers_y, map_name, image, sound, *group, ready=False):
        super().__init__(*group)

        self.image = pygame.transform.scale(load_image(image, 'data'), (WIDTH // 20, WIDTH // 20))
        self.rect = pygame.rect.Rect(0, 0, *self.image.get_size())
        self.default_parameters = (pers_x, pers_y, map_name, image, group, ready)

        self.pers_x = pers_x
        self.pers_y = pers_y
        self.map_name = map_name

        self.sound = pygame.mixer.Sound(os.path.join('sounds', sound))

        self.ready = ready
        self.passed = False

    def create(self):
        self.running = True
        self.pers = Hero(self.pers_x, self.pers_y, pers_sprites, load_image('pers.png', 'data'), 5, 2, Weapon())
        self.tiles = load_level(self.map_name)
        self.end_of_level = self.tiles.width * TILE_WIDTH
        self.height_of_level = self.tiles.height * TILE_HEIGHT
        self.logs = []
        self.camera = Camera()
        self.generate_level(self.tiles)
        # создаем врагов
        self.enemies = []
        for i in range(1):
            self.enemies.append(
                Enemy(enemies_sprites, load_image('pirat.png', 'data'), 5, 2,
                      (self.end_of_level, self.height_of_level)))
        self.interface = InfoInterface(load_image('coin.png', 'data'))
        self.enemy_count = len(enemies_sprites)

    def run(self):
        max_coin = len(coins_sprites)
        pygame.mouse.set_visible(True)
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.stop_run()
                if event.type == pygame.KEYDOWN:
                    # d down
                    if event.key == pygame.K_d:
                        self.pers.right_run = True
                    # a down
                    elif event.key == pygame.K_a:
                        self.pers.left_run = True
                    # w down
                    if event.key == pygame.K_SPACE:
                        self.pers.jump()
                    # s down
                    if event.key == pygame.K_s:
                        self.pers.g += 0.01
                    # esc - остановка уровня
                    if event.key == pygame.K_ESCAPE:
                        self.stop_run()
                    # для теста пуль
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.pers.kick(event.pos)
                elif event.type == pygame.KEYUP:
                    # d up
                    if event.key == pygame.K_d:
                        self.pers.right_run = False
                    # a up
                    elif event.key == pygame.K_a:
                        self.pers.left_run = False
                    # s up
                    if event.key == pygame.K_s:
                        self.pers.g -= 0.01
            # условия работы камеры
            if not self.camera.cam_on and WIDTH // 2 < self.pers.rect.x:
                self.camera.cam_on = True
            if WIDTH // 2 > self.pers.rect.x:
                self.camera.cam_on = False
            if self.pers.rect.x - self.logs[0].rect.x > self.end_of_level - WIDTH // 2:
                self.camera.cam_on = False
            if WIDTH // 2 < self.pers.rect.x - self.logs[0].rect.x < self.end_of_level - WIDTH // 2:
                self.camera.cam_on = True

            screen.fill((0, 0, 0))
            clock.tick(FPS)
            self.interface.update_info(self.pers.health, self.pers.coins_count)
            self.pers.run()
            all_sprites_lbl.update(self.pers)
            if self.pers.game_over:
                game_over()
                self.stop_level()
            self.drawing()
            pygame.display.flip()
            if self.enemy_count == 0:
                self.passed = True
                # окно победы, собранные очки
                self.stop_level()
                self.running = False
            self.enemy_count = len(enemies_sprites)
        pygame.mouse.set_visible(False)
        if self.passed:
            win_window(screen, self.pers.coins_count, max_coin)
            return self.pers.coins_count
        return 0

    def generate_level(self, level):
        x, y = None, None
        for y in range(level.height):
            for x in range(level.width):
                image = level.get_tile_image(x, y, 0)
                if image:
                    id = level.tiledgidmap[level.get_tile_gid(x, y, 0)]
                    if id == 1:
                        self.logs.append(Log(x, y, image, id))
                    elif id == 2:
                        Coin(x, y, image)
        return x, y

    def drawing(self):
        self.camera.update(self.pers)
        for sprite in all_sprites_lbl:
            self.camera.apply(sprite)
        all_sprites_lbl.draw(screen)
        # обновляем положение интерфейса относительно персонажа
        if self.camera.cam_on:
            self.interface.update((self.pers.rect.x, self.pers.rect.y))
        interface_sprite.draw(screen)

    def restart_level(self):
        for group in SPRITE_GROUPS:
            for item in group:
                item.kill()
        self.__init__(*self.default_parameters)

    def stop_level(self):
        for group in SPRITE_GROUPS:
            for item in group:
                item.kill()

    def stop_run(self):
        font1 = pygame.font.Font(None, 50 * int(HEIGHT * WIDTH / (1366 * 768)))
        font2 = pygame.font.Font(None, 30 * int(HEIGHT * WIDTH / (1366 * 768)))
        text1 = font1.render('Are you sure? To quit push "y", else push "n".', True,
                             (255, 35, 35))
        text2 = font2.render('If you come out, you will lose oll progress on the level', True,
                             (255, 35, 35))
        w1 = text1.get_width()
        w2 = text2.get_width()
        h1 = text1.get_height()
        h2 = text2.get_height()
        check_screen = pygame.Surface((max(w1, w2), h1 + h2))
        check_screen.fill((0, 0, 0))
        check_screen.blit(text1, (max(w1, w2) - w1, 0))
        check_screen.blit(text2, (max(w1, w2) - w2, h1))
        screen.blit(check_screen, (WIDTH // 2 - max(w1, w2) // 2, HEIGHT // 2 - (h1 + h2) // 2))
        pygame.display.flip()
        to_run = True
        error_stop = False
        while to_run:
            event = pygame.event.wait()
            if event.type == pygame.KEYDOWN:
                # y
                if event.key == pygame.K_y:
                    to_run = False
                    self.stop_level()
                # n
                elif event.key == pygame.K_n:
                    to_run = False
                    error_stop = True
        if not error_stop:
            self.running = False
