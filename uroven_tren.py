import pygame
from oop_maybe import Person, Log, Camera
from constans import *


class Level:
    def __init__(self, pers_x, pers_y, end_of_level, logs=[], enemies=[], do_center=True):
        pygame.init()
        pygame.display.set_caption('Level')
        size = WIDTH, HEIGHT
        self.end_of_level = end_of_level
        self.do_center = do_center
        self.screen = pygame.display.set_mode(size)
        self.screen.fill((0, 0, 0))
        self.clock = pygame.time.Clock()
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
                    self.stop_drun()
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
                    self.clock.tick()
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

            self.screen.fill((0, 0, 0))
            self.clock.tick(FPS)
            self.pers.run()
            self.pers.fly()
            self.drawing()
            pygame.display.flip()
        pygame.quit()

    def drawing(self):
        self.camera.update(self.pers)
        for sprite in all_sprites:
            self.camera.apply(sprite)
        all_sprites.draw(self.screen)

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
        self.screen.blit(check_screen, (WIDTH // 2 - max(w1, w2) // 2, HEIGHT // 2 - (h1 + h2) // 2))
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
