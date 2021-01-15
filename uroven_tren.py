import pygame
import sys
import os
import pytmx
from random import randrange
from oop_maybe import *
from constans import *
from load_functions import *


# это лучше делать вне класса
pygame.init()
pygame.display.set_caption('Level')
size = WIDTH, HEIGHT
clock = pygame.time.Clock()
screen = pygame.display.set_mode(size)


def terminate():
    pygame.quit()
    sys.exit()


def game_over():
    img = load_image('gameover.jpg', 'data')
    x = WIDTH // 2 - img.get_width() // 2
    y = HEIGHT // 2 - img.get_height() // 2
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN or\
                    event.type == pygame.KEYDOWN:
                return
        screen.fill(BLACK)
        screen.blit(img, (x, y))
        pygame.display.flip()


class Question(pygame.sprite.Sprite):
    def __init__(self, s_x, s_y, *group):
        super().__init__(*group)


class Level(pygame.sprite.Sprite):
    def __init__(self, pers_x, pers_y, map_name, image, sound, *group, ready=False):
        super().__init__(*group)

        self.image = pygame.transform.scale(load_image(image, 'data'), (WIDTH // 30, WIDTH // 30))
        self.rect = pygame.rect.Rect(0, 0, *self.image.get_size())
        self.default_parameters = (pers_x, pers_y, map_name, image, group, ready)

        self.pers_x = pers_x
        self.pers_y = pers_y
        self.map_name = map_name

        self.sound = pygame.mixer.Sound(os.path.join('sounds', sound))
        self.max_enemy = randrange(10, 15)
        self.dead_enemies = 0
        self.ready = ready
        self.passed = False
        self.win = False

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
        for i in range(3):
            self.enemies.append(
                Enemy(enemies_sprites, load_image('pirat.png', 'data'), 5, 2, (0, self.end_of_level, 0, self.height_of_level)))
        self.interface = InfoInterface(load_image('coin.png', 'data'))
        self.enemy_count = len(enemies_sprites)

    def run(self):
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
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.pers.kick(event.pos)
                if event.type == pygame.KEYUP:
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
            if self.dead_enemies >= self.max_enemy:
                self.win = True
                # окно победы, собранные очки
                self.stop_level()
                self.running = False

            self.enemy_count = len(enemies_sprites)

            self.dead_enemies += 3 - self.enemy_count
            if self.dead_enemies < self.max_enemy and 3 - self.enemy_count > 0:
                self.enemies.append(
                    Enemy(enemies_sprites, load_image('pirat.png', 'data'), 5, 2,
                          (self.logs[0].rect.x, self.logs[0].rect.x + self.end_of_level,
                           self.logs[0].rect.y, self.logs[0].rect.y + self.height_of_level)))

            print(len(enemies_sprites))
        pygame.mouse.set_visible(False)
        self.passed = True
        return self.pers.coins_count

    def generate_level(self, level):
        x, y = None, None
        for y in range(level.height):
            for x in range(level.width):
                image = level.get_tile_image(x, y, 0)
                if image:
                    id = level.tiledgidmap[level.get_tile_gid(x, y, 0)]
                    if id in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14]:
                        self.logs.append(Log(x, y, image, id))
                    elif id == 13:
                        Water(x, y, image, id)
                    elif id == 15:
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
