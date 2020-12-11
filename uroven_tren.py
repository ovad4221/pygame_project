import pygame
from oop_maybe import Person, Log
from constans import WIDTH, HEIGHT, FPS


class Level:
    def __init__(self, pers_x, pers_y, logs=[], enemies=[]):
        pygame.init()
        pygame.display.set_caption('Level')
        size = WIDTH, HEIGHT
        self.screen = pygame.display.set_mode(size)
        self.screen.fill((0, 0, 0))
        self.clock = pygame.time.Clock()
        self.running = True
        self.pers = Person(pers_x, pers_y)
        self.logs = logs
        self.enemies = enemies

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.stop_run()
                if event.type == pygame.KEYDOWN:
                    # d down
                    if event.key == 100:
                        self.pers.right_ran = True
                    # a down
                    elif event.key == 97:
                        self.pers.left_run = True
                    # w down
                    if event.key == 119:
                        self.pers.jump()
                    # s down
                    if event.key == 115:
                        self.pers.g += 100 * int(HEIGHT / 600)
                    # esc - остановка уровня
                    if event.key == 27:
                        self.stop_run()
                    self.clock.tick()
                if event.type == pygame.KEYUP:
                    # d up
                    if event.key == 100:
                        self.pers.right_ran = False
                    # a up
                    elif event.key == 97:
                        self.pers.left_run = False
                    # s up
                    if event.key == 115:
                        self.pers.g -= 100 * int(HEIGHT / 600)
            for i in self.logs:
                if i.log_in(self.pers):
                    self.pers.on_log = True
                    self.pers.jump_v = 0
                    self.pers.y = i.y_u - self.pers.height
                    break
                else:
                    self.pers.on_log = False
                if i.log_knock(self.pers) == 'r':
                    self.pers.right_log = True
                elif i.log_knock(self.pers) == 'l':
                    self.pers.left_log = True
                else:
                    self.pers.left_log = self.pers.right_log = False
                if i.log_knock(self.pers) == 'u':
                    self.pers.jump_v = 0
            self.screen.fill((0, 0, 0))
            time = self.clock.tick(FPS)
            self.pers.run(time)
            self.pers.fly(time)
            self.pers.draw(self.screen)
            for i in self.logs:
                i.draw(self.screen)
            for i in self.enemies:
                i.draw(self.screen)
            pygame.display.flip()
        pygame.quit()

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
                if event.key == 121:
                    to_run = False
                # n
                elif event.key == 110:
                    to_run = False
                    error_stop = True
        if not error_stop:
            self.running = False


x = Level(0, 0, [Log((50, 500, 400, 5)), Log((400, 460, 400, 5)), Log((1000, 430, 300, 5))])
x.run()
