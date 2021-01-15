import pygame
from constants_of_menu import *
from load_functions import load_image
from uroven_tren import Level
import os
from random import randint
import json


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

        self.im_pictures = [pygame.transform.scale(load_image('boat_up1.png', 'data_menu'), (cell_size, cell_size)),
                            pygame.transform.scale(load_image('boat_up2.png', 'data_menu'), (cell_size, cell_size)),
                            pygame.transform.flip(
                                pygame.transform.scale(load_image('boat_up1.png', 'data_menu'), (cell_size, cell_size)),
                                False,
                                True),
                            pygame.transform.flip(
                                pygame.transform.scale(load_image('boat_up2.png', 'data_menu'), (cell_size, cell_size)),
                                False,
                                True),
                            pygame.transform.scale(load_image('boat_ri1.png', 'data_menu'), (cell_size, cell_size)),
                            pygame.transform.scale(load_image('boat_ri2.png', 'data_menu'), (cell_size, cell_size)),
                            pygame.transform.flip(
                                pygame.transform.scale(load_image('boat_ri1.png', 'data_menu'), (cell_size, cell_size)),
                                True,
                                False),
                            pygame.transform.flip(
                                pygame.transform.scale(load_image('boat_ri2.png', 'data_menu'), (cell_size, cell_size)),
                                True,
                                False),
                            pygame.transform.scale(load_image('horse_ri.png', 'data_menu'), (cell_size, cell_size)),
                            pygame.transform.scale(load_image('horse_up.png', 'data_menu'), (cell_size, cell_size)),
                            pygame.transform.flip(
                                pygame.transform.scale(load_image('horse_up.png', 'data_menu'), (cell_size, cell_size)),
                                False,
                                True),
                            pygame.transform.flip(
                                pygame.transform.scale(load_image('horse_ri.png', 'data_menu'), (cell_size, cell_size)),
                                True,
                                False),

                            pygame.transform.scale(load_image('boat_diri1.png', 'data_menu'), (cell_size, cell_size)),
                            pygame.transform.scale(load_image('boat_diri2.png', 'data_menu'), (cell_size, cell_size)),

                            pygame.transform.flip(
                                pygame.transform.scale(load_image('boat_diri1.png', 'data_menu'),
                                                       (cell_size, cell_size)),
                                False,
                                True),
                            pygame.transform.flip(
                                pygame.transform.scale(load_image('boat_diri2.png', 'data_menu'),
                                                       (cell_size, cell_size)),
                                False,
                                True),

                            pygame.transform.flip(
                                pygame.transform.scale(load_image('boat_diri1.png', 'data_menu'),
                                                       (cell_size, cell_size)),
                                True,
                                False),
                            pygame.transform.flip(
                                pygame.transform.scale(load_image('boat_diri2.png', 'data_menu'),
                                                       (cell_size, cell_size)),
                                True,
                                False),

                            pygame.transform.flip(pygame.transform.flip(
                                pygame.transform.scale(load_image('boat_diri1.png', 'data_menu'),
                                                       (cell_size, cell_size)), False, True), True, False),
                            pygame.transform.flip(pygame.transform.flip(
                                pygame.transform.scale(load_image('boat_diri2.png', 'data_menu'),
                                                       (cell_size, cell_size)), False, True), True, False),

                            pygame.transform.scale(load_image('horse_diri.png', 'data_menu'), (cell_size, cell_size)),
                            pygame.transform.flip(
                                pygame.transform.scale(load_image('horse_diri.png', 'data_menu'), (cell_size, cell_size)),
                                True,
                                False),
                            pygame.transform.flip(
                                pygame.transform.scale(load_image('horse_diri.png', 'data_menu'), (cell_size, cell_size)),
                                False,
                                True),
                            pygame.transform.flip(pygame.transform.flip(
                                pygame.transform.scale(load_image('horse_diri.png', 'data_menu'),
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
        if self.right_run and self.up_run and 'up' not in self.arr_collide and 'right' not in self.arr_collide:
            if not self.in_ground:
                self.image = self.im_pictures[12 + self.ves_lo]
            else:
                self.image = self.im_pictures[20]
        # правая диагональка вниз
        elif self.right_run and self.down_run and 'down' not in self.arr_collide and 'right' not in self.arr_collide:
            if not self.in_ground:
                self.image = self.im_pictures[14 + self.ves_lo]
            else:
                self.image = self.im_pictures[22]
        # левая диагональка вверх
        elif self.up_run and self.left_run and 'up' not in self.arr_collide and 'left' not in self.arr_collide:
            if not self.in_ground:
                self.image = self.im_pictures[16 + self.ves_lo]
            else:
                self.image = self.im_pictures[21]
        # левая диагональка вниз
        elif self.down_run and self.left_run and 'down' not in self.arr_collide and 'left' not in self.arr_collide:
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
        self.level_list = [Level(int(i[0]), int(i[1]), i[2], i[3], i[4], level_sprites, ready=i[4]) for i in read_list]

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
                elif self.board[i][j] == '#':
                    Ground(x, y, self.pesok, all_sprites, ground_sprites)
                    self.board[i][j] = '+'
                elif self.board[i][j] == '@':
                    Ground(x, y, self.zemlya, all_sprites, ground_sprites)
                    self.board[i][j] = '+'
                x += self.cell_size
            x = self.left
            y += self.cell_size
