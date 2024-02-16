import pygame
import os
from random import *

WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 800, 900
MOVING_GUN = 15
MOVING_LASER = 10
FPS = 40


def load_image(name, colorkey=None):
    fullname = os.path.join('image', name)
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    #else:
    #   image = image.convert_alpha()
    return image


class Gun():
    def __init__(self):
        self.width = 30
        self.height = 50
        self.x = WINDOW_WIDTH // 2 - self.width // 2
        self.y = 780

    def move(self):
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            if self.x > (WINDOW_WIDTH // 2) % MOVING_GUN:
                self.x = self.x - MOVING_GUN
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            if self.x < WINDOW_WIDTH - (WINDOW_WIDTH // 2) % MOVING_GUN - self.width:
                self.x = self.x + MOVING_GUN

    def gun_size(self):
        return self.width, self.height

    def get_position(self):
        return self.x, self.y

    def drawing(self, screen):
        pygame.draw.rect(screen, pygame.Color('Orange'), (self.x, self.y, self.width, self.height), 0)


class Laser():
    def __init__(self):
        self.width = 6
        self.height = 30
        self.x = 350
        self.y = 350

    def render(self, screen):
        pygame.draw.rect(screen, pygame.Color('Green'), (self.x, self.y, self.width, self.height), 0)

    def fire(self, screen, position, size):
        self.x = position[0] + size[0] // 2 - self.width // 2
        self.y = position[1] - self.height
        pygame.draw.rect(screen, pygame.Color('Green'), (self.x, self.y, self.width, self.height), 0)

    def move(self):
        self.y = self.y - MOVING_LASER

    def get_size(self):
        return self.width, self.height

    def get_position(self):
        return self.x, self.y


def main():
    lasers = []
    flags = []
    image = load_image("вид6.png")
    pygame.init()
    pygame.display.set_caption('Space Defender')
    screen = pygame.display.set_mode(WINDOW_SIZE)
    flag = False

    gun = Gun()

    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    laser = Laser()
                    lasers.append(laser)
                    laser.fire(screen, gun.get_position(), gun.gun_size())
                    flag = True
                    flags.append(flag)
        gun.move()
        screen.fill((0, 0, 0))
        screen.blit(image, (0, 0))
        gun.drawing(screen)
        for i in range(len(lasers)):
            if flags[i]:
                lasers[i].move()
                lasers[i].render(screen)
                if lasers[i].get_position()[1] - lasers[i].get_size()[1] >= WINDOW_HEIGHT:
                    flags[i] = False
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()


if __name__ == '__main__':
    main()
