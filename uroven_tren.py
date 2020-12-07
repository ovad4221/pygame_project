import pygame
from oop_maybe import Person, Log


class Level:
    def __init__(self, pers_x, pers_y, logs=[], enemies=[]):
        pygame.init()
        pygame.display.set_caption('Level')
        size = self.width, self.height = 600, 600
        self.screen = pygame.display.set_mode(size)
        self.screen.fill((0, 0, 0))
        self.clock = pygame.time.Clock()
        self.fps = 500
        self.running = True
        self.pers = Person(pers_x, pers_y)
        self.logs = logs
        self.enemies = enemies

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
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
                        self.pers.g += 100
                    if event.key == 27:
                        self.stop_run()
                        # esc - остановка уровня
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
                        self.pers.g -= 100
            for i in self.logs:
                if i.log_in(self.pers):
                    self.pers.on_log = True
                    self.pers.jump_v = 0
                    self.pers.y = i.y_u - self.pers.height
                    break
                else:
                    self.pers.on_log = False
            time = self.clock.tick(self.fps)
            self.pers.run(time)
            self.pers.fly(time)
            self.pers.draw(self.screen)
            for i in self.logs:
                i.draw(self.screen)
            for i in self.enemies:
                i.draw(self.screen)
            pygame.display.flip()
            self.screen.fill((0, 0, 0))
        pygame.quit()

    def stop_run(self):
        self.running = False


x = Level(300, 250, [Log((100, 300, 400, 5)), Log((50, 400, 400, 5))])
x.run()
