import pygame
import random
from utility import load_image
WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 800, 900
MOVING_GUN = 15
MOVING_LASER = 40


class Spaceships(pygame.sprite.Sprite):
    image = load_image("spaceship.png")

    def __init__(self, *group):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно!!!
        super().__init__(*group)
        self.image = Spaceships.image
        self.speed_x = random.randrange(1, 3)
        self.speed_y = random.randrange(2, 4)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WINDOW_WIDTH - 50)
        self.rect.y = 60
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)

    def get_position(self):
        return self.rect.y

    def update(self):
        self.rect = self.rect.move(0, self.speed_y)
