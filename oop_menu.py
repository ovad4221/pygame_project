import pygame
from constants_of_menu import *
from load_functions import load_image
from uroven_tren import Level
import os
import json

skin_number = 1


class Shop(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        self.image = pygame.transform.scale(load_image('shop_and_home.jpg', 'data_menu'), (WIDTH // 20, WIDTH // 20))
        self.rect = pygame.rect.Rect(0, 0, *self.image.get_size())

        self.ri_arrow = pygame.transform.scale(load_image('стрелка в право.png', 'data_menu'),
                                               (WIDTH // 10, WIDTH // 20))
        self.le_arrow = pygame.transform.flip(pygame.transform.scale(load_image('стрелка в право.png', 'data_menu'),
                                                                     (WIDTH // 10, WIDTH // 20)), True, False)
        image_coin = load_image('coin.png', 'data')

        self.sound = pygame.mixer.Sound(os.path.join('sounds', 'распродажа.wav'))
        self.sound.set_volume(0.5)

        self.font2 = pygame.font.Font(None, 50)
        self.font1 = pygame.font.Font(None, 150)

        self.now_skin = skin_number
        self.screen2 = pygame.Surface([WIDTH // 2, HEIGHT // 2])
        self.screen2.fill('black')

        self.dict_of_num_skins = {1: {'open': True, 'price': -1, 'name': 'классика', 'img': [
            pygame.transform.scale(load_image(f'boat_diri1.png', 'data_menu'),
                                   (self.screen2.get_width() // 6, self.screen2.get_width() // 6)),
            pygame.transform.scale(load_image(f'horse_diri1.png', 'data_menu'),
                                   (self.screen2.get_width() // 6, self.screen2.get_width() // 6))]},
                                  3: {'open': False, 'price': 50, 'name': 'цветок', 'img': [
                                      pygame.transform.scale(load_image(f'boat_diri3.png', 'data_menu'), (
                                          self.screen2.get_width() // 6, self.screen2.get_width() // 6)),
                                      pygame.transform.scale(load_image(f'horse_diri3.png', 'data_menu'), (
                                          self.screen2.get_width() // 6, self.screen2.get_width() // 6))]}}

        self.screen2.blit(self.le_arrow, (0, self.screen2.get_height() // 2 - self.le_arrow.get_height() // 2))
        self.screen2.blit(self.ri_arrow, (self.screen2.get_width() - self.le_arrow.get_width(),
                                          self.screen2.get_height() // 2 - self.le_arrow.get_height() // 2))
        self.screen2.blit(image_coin, (self.screen2.get_width() // 3, 0))

    def run(self, x_s, y_s, screen, coin_count):
        coin_count = coin_count
        global skin_number
        text = self.font2.render(f'{coin_count}', True, (255, 204, 0))
        text_btn = self.font1.render('надеть', True, (10, 10, 10))
        name_skin = self.font2.render(f'{self.dict_of_num_skins[self.now_skin]["name"]}', True, (200, 140, 180))
        pygame.mouse.set_visible(True)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.mouse.set_visible(False)
                        return coin_count
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if x_s <= x <= x_s + self.le_arrow.get_height() and y_s <= y <= y_s + self.screen2.get_height():
                        if self.now_skin == 3:
                            self.now_skin = 1
                    elif x_s + self.screen2.get_width() - self.ri_arrow.get_width() <= x <= x_s + \
                            self.le_arrow.get_height() + self.screen2.get_width() and \
                            y_s <= y <= y_s + self.screen2.get_height():
                        if self.now_skin == 1:
                            self.now_skin = 3
                    elif x_s + self.screen2.get_width() // 2 - text_btn.get_width() // 2 <= x <= x_s + \
                            self.screen2.get_width() // 2 - text_btn.get_width() // 2 + text_btn.get_width() and \
                            y_s + self.screen2.get_height() - text_btn.get_height() <= y <= y_s + \
                            self.screen2.get_height() - text_btn.get_height() + text_btn.get_height():
                        if self.dict_of_num_skins[self.now_skin]['open']:
                            skin_number = self.now_skin
                        else:
                            if coin_count >= self.dict_of_num_skins[self.now_skin]['price']:
                                coin_count -= self.dict_of_num_skins[self.now_skin]['price']
                                self.dict_of_num_skins[self.now_skin]['open'] = True

            # повторения
            if self.dict_of_num_skins[self.now_skin]['open']:
                text_btn = self.font1.render('надеть', True, (10, 10, 10))
            else:
                text_btn = self.font1.render('купить', True, (10, 10, 10))

            self.screen2.blit(name_skin, (
                self.screen2.get_width() // 2 - name_skin.get_width() // 2, self.screen2.get_height() // 10))

            self.screen2.blit(text_btn, (self.screen2.get_width() // 2 - text_btn.get_width() // 2,
                                         self.screen2.get_height() - text_btn.get_height()))

            self.screen2.blit(self.dict_of_num_skins[self.now_skin]['img'][0], (
                self.screen2.get_width() // 2 - self.dict_of_num_skins[self.now_skin]['img'][
                    0].get_width() // 2,
                self.screen2.get_height() // 6))
            self.screen2.blit(self.dict_of_num_skins[self.now_skin]['img'][1], (
                self.screen2.get_width() // 2 - self.dict_of_num_skins[self.now_skin]['img'][
                    0].get_width() // 2,
                self.screen2.get_height() // 6 + self.dict_of_num_skins[self.now_skin]['img'][
                    0].get_height()))

            self.screen2.blit(text, (self.screen2.get_width() * 2 // 3, self.screen2.get_height() // 50))

            text = self.font2.render(f'{coin_count}', True, (255, 204, 0))
            if self.dict_of_num_skins[self.now_skin]['open']:
                name_skin = self.font2.render(f'{self.dict_of_num_skins[self.now_skin]["name"]}', True, (200, 140, 180))
            else:
                name_skin = self.font2.render(
                    f'{self.dict_of_num_skins[self.now_skin]["name"]}, ' +
                    f'стоимость: {self.dict_of_num_skins[self.now_skin]["price"]} P',
                    True, (200, 140, 180))
            screen.blit(self.screen2, (x_s, y_s))

            # flip
            pygame.display.flip()

            pygame.draw.rect(self.screen2, 'black', (
                self.screen2.get_width() // 4,
                self.screen2.get_height() // 10, self.screen2.get_width() // 2, name_skin.get_height()))

            pygame.draw.rect(self.screen2, 'black',
                             (self.screen2.get_width() * 2 // 3, self.screen2.get_height() // 50, *text.get_size()))

            pygame.draw.rect(self.screen2, '#000000',
                             (self.screen2.get_width() // 2 - self.dict_of_num_skins[self.now_skin]['img'][
                                 0].get_width() // 2, self.screen2.get_height() // 6,
                              self.dict_of_num_skins[1]['img'][0].get_width(),
                              self.dict_of_num_skins[1]['img'][0].get_width() * 2))

            pygame.draw.rect(self.screen2, (100, 200, 100),
                             (self.screen2.get_width() // 2 - text_btn.get_width() // 2,
                              self.screen2.get_height() - text_btn.get_height(),
                              *text_btn.get_size()))


class Barier(pygame.sprite.Sprite):
    def __init__(self, x0, y0, w, h, horizontal, rev, *group):
        super().__init__(*group)
        self.napr = ''
        if horizontal:
            if rev:
                self.image = pygame.transform.scale(load_image('туманность.jpg', 'data_menu'), (w * 2, HEIGHT // 2))
                self.rect = pygame.rect.Rect(x0 - w // 2, y0 - self.image.get_height(), *self.image.get_size())
                self.napr = 'up'
            else:
                self.image = pygame.transform.scale(
                    pygame.transform.flip(load_image('туманность.jpg', 'data_menu'), False, True),
                    (w * 2, HEIGHT // 2))
                self.rect = pygame.rect.Rect(x0 - w // 2, y0 + h, *self.image.get_size())
                self.napr = 'down'
        else:
            if rev:
                self.image = pygame.transform.scale(load_image('туманность_rev.jpg', 'data_menu'), (WIDTH // 2, h))
                self.rect = pygame.rect.Rect(x0 - self.image.get_width(), y0, *self.image.get_size())
                self.napr = 'left'
            else:
                self.image = pygame.transform.scale(
                    pygame.transform.flip(load_image('туманность_rev.jpg', 'data_menu'), False, True), (WIDTH // 2, h))
                self.rect = pygame.rect.Rect(x0 + w, y0, *self.image.get_size())
                self.napr = 'right'


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self, dx, dy):
        self.dx = dx
        self.dy = dy

    def get_delta(self):
        return self.dx, self.dy

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 2)


class WarShipOrPig(pygame.sprite.Sprite):
    def __init__(self, x, y, cell_size, *group):
        super().__init__(*group)

        self.sound_water = pygame.mixer.Sound(os.path.join('sounds', 'бульк.wav'))
        self.sound_horse = pygame.mixer.Sound(os.path.join('sounds', 'horse.wav'))
        self.sound_horse.set_volume(0.15)

        self.change = 0
        self.im_pictures = [
            pygame.transform.scale(load_image(f'boat_up{skin_number}.png', 'data_menu'), (cell_size, cell_size)),
            pygame.transform.scale(load_image(f'boat_up{skin_number + 1}.png', 'data_menu'), (cell_size, cell_size)),
            pygame.transform.flip(
                pygame.transform.scale(load_image(f'boat_up{skin_number}.png', 'data_menu'), (cell_size, cell_size)),
                False,
                True),
            pygame.transform.flip(
                pygame.transform.scale(load_image(f'boat_up{skin_number + 1}.png', 'data_menu'),
                                       (cell_size, cell_size)),
                False,
                True),
            pygame.transform.scale(load_image(f'boat_ri{skin_number}.png', 'data_menu'), (cell_size, cell_size)),
            pygame.transform.scale(load_image(f'boat_ri{skin_number + 1}.png', 'data_menu'), (cell_size, cell_size)),
            pygame.transform.flip(
                pygame.transform.scale(load_image(f'boat_ri{skin_number}.png', 'data_menu'), (cell_size, cell_size)),
                True,
                False),
            pygame.transform.flip(
                pygame.transform.scale(load_image(f'boat_ri{skin_number + 1}.png', 'data_menu'),
                                       (cell_size, cell_size)),
                True,
                False),
            pygame.transform.scale(load_image(f'horse_ri{skin_number}.png', 'data_menu'), (cell_size, cell_size)),
            pygame.transform.scale(load_image(f'horse_up{skin_number}.png', 'data_menu'), (cell_size, cell_size)),
            pygame.transform.flip(
                pygame.transform.scale(load_image(f'horse_up{skin_number}.png', 'data_menu'),
                                       (cell_size, cell_size)),
                False,
                True),
            pygame.transform.flip(
                pygame.transform.scale(load_image(f'horse_ri{skin_number}.png', 'data_menu'),
                                       (cell_size, cell_size)),
                True,
                False),

            pygame.transform.scale(load_image(f'boat_diri{skin_number}.png', 'data_menu'), (cell_size, cell_size)),
            pygame.transform.scale(load_image(f'boat_diri{skin_number + 1}.png', 'data_menu'), (cell_size, cell_size)),

            pygame.transform.flip(
                pygame.transform.scale(load_image(f'boat_diri{skin_number}.png', 'data_menu'),
                                       (cell_size, cell_size)),
                False,
                True),
            pygame.transform.flip(
                pygame.transform.scale(load_image(f'boat_diri{skin_number + 1}.png', 'data_menu'),
                                       (cell_size, cell_size)),
                False,
                True),

            pygame.transform.flip(
                pygame.transform.scale(load_image(f'boat_diri{skin_number}.png', 'data_menu'),
                                       (cell_size, cell_size)),
                True,
                False),
            pygame.transform.flip(
                pygame.transform.scale(load_image(f'boat_diri{skin_number + 1}.png', 'data_menu'),
                                       (cell_size, cell_size)),
                True,
                False),

            pygame.transform.flip(pygame.transform.flip(
                pygame.transform.scale(load_image(f'boat_diri{skin_number}.png', 'data_menu'),
                                       (cell_size, cell_size)), False, True), True, False),
            pygame.transform.flip(pygame.transform.flip(
                pygame.transform.scale(load_image(f'boat_diri{skin_number + 1}.png', 'data_menu'),
                                       (cell_size, cell_size)), False, True), True, False),

            pygame.transform.scale(load_image(f'horse_diri{skin_number}.png', 'data_menu'), (cell_size, cell_size)),
            pygame.transform.flip(
                pygame.transform.scale(load_image(f'horse_diri{skin_number}.png', 'data_menu'),
                                       (cell_size, cell_size)),
                True,
                False),
            pygame.transform.flip(
                pygame.transform.scale(load_image(f'horse_diri{skin_number}.png', 'data_menu'),
                                       (cell_size, cell_size)),
                False,
                True),
            pygame.transform.flip(pygame.transform.flip(
                pygame.transform.scale(load_image(f'horse_diri{skin_number}.png', 'data_menu'),
                                       (cell_size, cell_size)), False, True), True, False)]
        self.image = self.im_pictures[0]
        self.rect = pygame.rect.Rect(x, y, cell_size, cell_size)

        self.ves_lo = False
        self.left_run = False
        self.right_run = False
        self.up_run = False
        self.down_run = False
        self.in_ground = False
        self.arr_collide = [-1, -1]

        self.v = WIDTH // 11

    def anyone(self):
        return self.left_run or self.right_run or self.up_run or self.down_run

    def level_collide(self):
        return pygame.sprite.spritecollideany(self, level_sprites)

    def shop_collide(self):
        return pygame.sprite.spritecollideany(self, shop_sprite)

    def re_list(self, cell_size):
        self.im_pictures = [
            pygame.transform.scale(load_image(f'boat_up{skin_number}.png', 'data_menu'), (cell_size, cell_size)),
            pygame.transform.scale(load_image(f'boat_up{skin_number + 1}.png', 'data_menu'), (cell_size, cell_size)),
            pygame.transform.flip(
                pygame.transform.scale(load_image(f'boat_up{skin_number}.png', 'data_menu'), (cell_size, cell_size)),
                False,
                True),
            pygame.transform.flip(
                pygame.transform.scale(load_image(f'boat_up{skin_number + 1}.png', 'data_menu'),
                                       (cell_size, cell_size)),
                False,
                True),
            pygame.transform.scale(load_image(f'boat_ri{skin_number}.png', 'data_menu'), (cell_size, cell_size)),
            pygame.transform.scale(load_image(f'boat_ri{skin_number + 1}.png', 'data_menu'), (cell_size, cell_size)),
            pygame.transform.flip(
                pygame.transform.scale(load_image(f'boat_ri{skin_number}.png', 'data_menu'), (cell_size, cell_size)),
                True,
                False),
            pygame.transform.flip(
                pygame.transform.scale(load_image(f'boat_ri{skin_number + 1}.png', 'data_menu'),
                                       (cell_size, cell_size)),
                True,
                False),
            pygame.transform.scale(load_image(f'horse_ri{skin_number}.png', 'data_menu'), (cell_size, cell_size)),
            pygame.transform.scale(load_image(f'horse_up{skin_number}.png', 'data_menu'), (cell_size, cell_size)),
            pygame.transform.flip(
                pygame.transform.scale(load_image(f'horse_up{skin_number}.png', 'data_menu'),
                                       (cell_size, cell_size)),
                False,
                True),
            pygame.transform.flip(
                pygame.transform.scale(load_image(f'horse_ri{skin_number}.png', 'data_menu'),
                                       (cell_size, cell_size)),
                True,
                False),

            pygame.transform.scale(load_image(f'boat_diri{skin_number}.png', 'data_menu'), (cell_size, cell_size)),
            pygame.transform.scale(load_image(f'boat_diri{skin_number + 1}.png', 'data_menu'), (cell_size, cell_size)),

            pygame.transform.flip(
                pygame.transform.scale(load_image(f'boat_diri{skin_number}.png', 'data_menu'),
                                       (cell_size, cell_size)),
                False,
                True),
            pygame.transform.flip(
                pygame.transform.scale(load_image(f'boat_diri{skin_number + 1}.png', 'data_menu'),
                                       (cell_size, cell_size)),
                False,
                True),

            pygame.transform.flip(
                pygame.transform.scale(load_image(f'boat_diri{skin_number}.png', 'data_menu'),
                                       (cell_size, cell_size)),
                True,
                False),
            pygame.transform.flip(
                pygame.transform.scale(load_image(f'boat_diri{skin_number + 1}.png', 'data_menu'),
                                       (cell_size, cell_size)),
                True,
                False),

            pygame.transform.flip(pygame.transform.flip(
                pygame.transform.scale(load_image(f'boat_diri{skin_number}.png', 'data_menu'),
                                       (cell_size, cell_size)), False, True), True, False),
            pygame.transform.flip(pygame.transform.flip(
                pygame.transform.scale(load_image(f'boat_diri{skin_number + 1}.png', 'data_menu'),
                                       (cell_size, cell_size)), False, True), True, False),

            pygame.transform.scale(load_image(f'horse_diri{skin_number}.png', 'data_menu'), (cell_size, cell_size)),
            pygame.transform.flip(
                pygame.transform.scale(load_image(f'horse_diri{skin_number}.png', 'data_menu'),
                                       (cell_size, cell_size)),
                True,
                False),
            pygame.transform.flip(
                pygame.transform.scale(load_image(f'horse_diri{skin_number}.png', 'data_menu'),
                                       (cell_size, cell_size)),
                False,
                True),
            pygame.transform.flip(pygame.transform.flip(
                pygame.transform.scale(load_image(f'horse_diri{skin_number}.png', 'data_menu'),
                                       (cell_size, cell_size)), False, True), True, False)]

    def all_flags_move_false(self):
        self.left_run = False
        self.right_run = False
        self.up_run = False
        self.down_run = False

    def update(self, time, channel):
        spr = pygame.sprite.spritecollide(self, bar_sprites, False)
        self.arr_collide = [-1, -1]

        if spr:
            for i in range(len(spr)):
                self.arr_collide[i] = spr[i].napr
        if pygame.sprite.spritecollideany(self, ground_sprites):
            self.in_ground = True
        else:
            self.in_ground = False

        if self.left_run and not self.right_run and 'left' not in self.arr_collide:
            self.rect.x += round(self.v * -1 * time / 1000)
            if not self.in_ground:
                self.image = self.im_pictures[6 + self.ves_lo]
            else:
                self.image = self.im_pictures[11]

        elif not self.left_run and self.right_run and 'right' not in self.arr_collide:
            self.rect.x += round(self.v * time / 1000)
            if not self.in_ground:
                self.image = self.im_pictures[4 + self.ves_lo]
            else:
                self.image = self.im_pictures[8]

        if self.up_run and not self.down_run and 'up' not in self.arr_collide:
            self.rect.y += round(self.v * -1 * time / 1000)
            if not self.in_ground:
                self.image = self.im_pictures[0 + self.ves_lo]
            else:
                self.image = self.im_pictures[9]

        elif not self.up_run and self.down_run and 'down' not in self.arr_collide:
            self.rect.y += round(self.v * time / 1000)
            if not self.in_ground:
                self.image = self.im_pictures[2 + self.ves_lo]
            else:
                self.image = self.im_pictures[10]

        # правая диагональка вверх
        if self.right_run and self.up_run and not self.left_run and not self.down_run and \
                'up' not in self.arr_collide and 'right' not in self.arr_collide:
            if not self.in_ground:
                self.image = self.im_pictures[12 + self.ves_lo]
            else:
                self.image = self.im_pictures[20]
        # правая диагональка вниз
        elif self.right_run and self.down_run and not self.left_run and not self.up_run and \
                'down' not in self.arr_collide and 'right' not in self.arr_collide:
            if not self.in_ground:
                self.image = self.im_pictures[14 + self.ves_lo]
            else:
                self.image = self.im_pictures[22]
        # левая диагональка вверх
        elif self.up_run and self.left_run and not self.right_run and not self.down_run and \
                'up' not in self.arr_collide and 'left' not in self.arr_collide:
            if not self.in_ground:
                self.image = self.im_pictures[16 + self.ves_lo]
            else:
                self.image = self.im_pictures[21]
        # левая диагональка вниз
        elif self.down_run and self.left_run and not self.right_run and not self.up_run and \
                'down' not in self.arr_collide and 'left' not in self.arr_collide:
            if not self.in_ground:
                self.image = self.im_pictures[18 + self.ves_lo]
            else:
                self.image = self.im_pictures[23]

        if not self.change % 40:
            self.ves_lo = not self.ves_lo
            if not self.in_ground and self.anyone() and self.ves_lo:
                channel.play(self.sound_water)
            elif self.anyone() and self.in_ground:
                channel.play(self.sound_horse)
        self.change = (self.change + 1) % 40


class Ground(pygame.sprite.Sprite):
    def __init__(self, x, y, image, *group):
        super().__init__(*group)
        self.image = image
        self.rect = pygame.rect.Rect(x, y, *image.get_size())


class Board:
    # создание поля
    def __init__(self, file, load_image):
        read_list = open(file, encoding='utf-8').readlines()
        self.w_n = len(read_list[0]) - 1
        self.h_n = len(read_list)
        self.board = [list(i.strip()) for i in read_list]

        # json
        read_list = open('list_levels_j.json', 'r', encoding='utf-8').readline()
        read_list = json.loads(read_list)
        self.level_list = [Level(int(i[0]), int(i[1]), i[2], i[3], i[4], level_sprites, ready=i[5]) for i in read_list]

        self.shop = Shop(shop_sprite)

        self.left = 0
        self.top = 0

        self.pers = ''
        self.cell_size = WIDTH // 60
        self.bereg = pygame.transform.scale(load_image('bereg.jpg', 'data_menu'), (self.cell_size, self.cell_size))
        self.bereg_gor = pygame.transform.scale(load_image('bereg_gor.jpg', 'data_menu'),
                                                (self.cell_size, self.cell_size))
        self.more_spok = pygame.transform.scale(load_image('more_spok.jpg', 'data_menu'),
                                                (self.cell_size, self.cell_size))
        self.pesok = pygame.transform.scale(load_image('pesok.jpg', 'data_menu'), (self.cell_size, self.cell_size))
        self.zemlya = pygame.transform.scale(load_image('zemlya.jpg', 'data_menu'), (self.cell_size, self.cell_size))

        self.bereg_gor2 = pygame.transform.flip(self.bereg_gor, True, False)
        self.bereg2 = pygame.transform.flip(self.bereg, False, True)

    def render(self, screen):
        x = self.left
        y = self.top
        for i in range(self.h_n):
            for j in range(self.w_n):
                if self.board[i][j] == '~':
                    screen.blit(self.more_spok, (x, y))
                elif self.board[i][j] == '^':
                    screen.blit(self.bereg2, (x, y))
                elif self.board[i][j] == '<':
                    screen.blit(self.bereg_gor, (x, y))
                elif self.board[i][j] == '>':
                    screen.blit(self.bereg_gor2, (x, y))
                elif self.board[i][j] == '_':
                    screen.blit(self.bereg, (x, y))

                elif self.board[i][j] == 'X':
                    self.pers = WarShipOrPig(x, y, self.cell_size)
                    self.board[i][j] = '>'
                elif self.board[i][j].isdigit():
                    self.level_list[int(self.board[i][j]) - 1].rect.x = x
                    self.level_list[int(self.board[i][j]) - 1].rect.y = y
                    self.board[i][j] = '+'
                elif self.board[i][j] == 'S':
                    self.shop.rect.x = x
                    self.shop.rect.y = y
                    self.board[i][j] = '+'
                elif self.board[i][j] == '#':
                    Ground(x, y, self.pesok, all_sprites, ground_sprites)
                    self.board[i][j] = '+'
                elif self.board[i][j] == '@':
                    Ground(x, y, self.zemlya, all_sprites, ground_sprites)
                    self.board[i][j] = '+'
                x += self.cell_size
            x = self.left
            y += self.cell_size
