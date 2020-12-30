import pygame
import sys
from oop_maybe import Person, Log, Camera
from constans import *


# это лучше делать вне класса
pygame.init()
pygame.display.set_caption('Level')
size = WIDTH, HEIGHT
clock = pygame.time.Clock()
screen = pygame.display.set_mode(size)


def terminate():
    pygame.quit()
    sys.exit()


# тестовое стартовое меню
def start_window():
    screen.fill((0, 0, 0))
    color_play = (100, 255, 100)
    color_quit = (100, 255, 100)
    font = pygame.font.Font(None, 150)
    text_play = font.render("Play", True, color_play)
    text_quit = font.render("Quit", True, color_quit)
    text_x = WIDTH // 2 - text_play.get_width() // 2
    text_y_play = HEIGHT // 2 - text_play.get_height() // 2 - HEIGHT // 8
    text_y_quit = HEIGHT // 2 - text_quit.get_height() // 2 + HEIGHT // 8

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEMOTION:
                if text_x <= event.pos[0] <= text_x + text_play.get_width() and \
                        text_y_play <= event.pos[1] <= text_y_play + text_play.get_height():
                    color_play = (50, 125, 50)
                else:
                    color_play = (100, 255, 100)
                if text_x <= event.pos[0] <= text_x + text_play.get_width() and \
                        text_y_quit <= event.pos[1] <= text_y_quit + text_quit.get_height():
                    color_quit = (50, 125, 50)
                else:
                    color_quit = (100, 255, 100)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if text_x <= event.pos[0] <= text_x + text_play.get_width() and\
                        text_y_play <= event.pos[1] <= text_y_play + text_play.get_height():
                    return
                if text_x <= event.pos[0] <= text_x + text_play.get_width() and \
                        text_y_quit <= event.pos[1] <= text_y_quit + text_quit.get_height():
                    terminate()

        text_play = font.render("Play", True, color_play)
        text_quit = font.render("Quit", True, color_quit)
        screen.blit(text_play, (text_x, text_y_play))
        screen.blit(text_quit, (text_x, text_y_quit))
        clock.tick(FPS)
        pygame.display.flip()


start_window()


class Level:
    def __init__(self, pers_x, pers_y, end_of_level, logs=[], enemies=[], do_center=True):
        self.end_of_level = end_of_level
        self.do_center = do_center
        screen.fill((0, 0, 0))
        self.running = True
        self.alp = 0
        self.pers = Person(pers_x, pers_y)
        self.logs = logs
        self.enemies = enemies
        self.camera = Camera()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.stop_run()
                if event.type == pygame.KEYDOWN:
                    # d down
                    if event.key == pygame.K_d:
                        self.pers.right_ran = True
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
                    clock.tick()
                if event.type == pygame.KEYUP:
                    # d up
                    if event.key == pygame.K_d:
                        self.pers.right_ran = False
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
            self.pers.run()
            self.pers.fly()
            self.drawing()
            pygame.display.flip()
        pygame.quit()

    def drawing(self):
        self.camera.update(self.pers)
        for sprite in all_sprites:
            self.camera.apply(sprite)
        all_sprites.draw(screen)

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
                # n
                elif event.key == pygame.K_n:
                    to_run = False
                    error_stop = True
        if not error_stop:
            self.running = False


x = Level(0, 400, 3700, [Log((0, 500, 400, 5)), Log((400, 460, 400, 5)), Log((1000, 430, 300, 5)),
                         Log((1400, 400, 300, 5)), Log((2000, 400, 300, 5)),
                         Log((2400, 400, 300, 5)), Log((3000, 350, 300, 5)),
                         Log((3000, 250, 300, 5)), Log((3000, 400, 300, 5)),
                         Log((3400, 200, 300, 5)), Log((3000, 300, 300, 5))])
x.run()
