import pygame
import os
import random


WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 800, 900
MOVING_GUN = 15
MOVING_LASER = 10
FPS = 30


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


class Laser(pygame.sprite.Sprite):
    image = load_image("laser.png")
    def __init__(self, pos, *group):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно!!!
        super().__init__(*group)
        self.image = Laser.image
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, barrier):
        if not pygame.sprite.spritecollideany(self, barrier):
            self.rect = self.rect.move(0, -20)
        else:
            self.kill()


class Spaceships(pygame.sprite.Sprite):
    image = load_image("spaceship.png")

    def __init__(self, *group):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно!!!
        super().__init__(*group)
        self.image = Spaceships.image
        self.speed_x = random.randrange(1,3)
        self.speed_y = random.randrange(1, 3)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WINDOW_WIDTH // 1.5)
        self.rect.y = 60
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, barrier):
        if not pygame.sprite.spritecollideany(self, barrier):
            self.rect = self.rect.move(0, self.speed_y)
        else:
            self.kill()


def main():
    ships = pygame.sprite.Group()
    for _ in range(5):
        Spaceships(ships)
    lasers = pygame.sprite.Group()
    # lasers = []
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
                    Laser((gun.get_position()[0]+10, gun.get_position()[1]-50), lasers)
                    # lasers.fire(screen, gun.get_position(), gun.gun_size())
                    flag = True
                    flags.append(flag)

        gun.move()
        screen.fill((0, 0, 0))
        screen.blit(image, (0, 0))
        gun.drawing(screen)
        # рисуем srites, которые двигаются
        ships.draw(screen)
        ships.update(lasers)
        lasers.draw(screen)
        lasers.update(ships)

        # for i in range(len(lasers)):
        #     if flags[i]:
        #         lasers[i].move()
        #         lasers[i].render(screen)
        #         if lasers[i].get_position()[1] - lasers[i].get_size()[1] >= WINDOW_HEIGHT:
        #             flags[i] = False
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()


if __name__ == '__main__':
    main()
