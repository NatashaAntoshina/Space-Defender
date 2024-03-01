import math

import pygame
import os
import random
import sys

WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 800, 900
MOVING_GUN = 15
MOVING_LASER = 15
FPS = 30
background_list = ['вид2.png', 'вид3.png', 'вид4.png', 'вид5.png', 'вид6.png']


def load_image(name, colorkey=None):
    fullname = os.path.join('image', name)
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    # else:
    #   image = image.convert_alpha()
    return image


class Gun:
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
        pygame.draw.rect(screen, pygame.Color('Orange'), (self.x, self.y, self.width, self.height),
                         0)


class Laser(pygame.sprite.Sprite):
    image = load_image("laser.png")

    def __init__(self, pos, k=0, *group):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно!!!
        super().__init__(*group)
        self.origimage = Laser.image
        self.image = Laser.image
        self.rect = self.image.get_rect()
        self.positions = pos
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.angle = 0  # угол, на который повернута пулька относительно вертикальной прямой
        # (отсчитывается по часовой стрелке в градусах)
        self.k = k  # коэффициент наклона прямой dy/dx
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        if self.k:
            self.rect.x += -40 / self.k
        self.rect.y -= 40


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


class Asteroids(pygame.sprite.Sprite):
    image = load_image("asteroids.png")

    def __init__(self, *group):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно!!!
        super().__init__(*group)
        self.image = Asteroids.image
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WINDOW_WIDTH)
        self.rect.y = random.randrange(100, WINDOW_HEIGHT - 300)
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)


class Mirror(pygame.sprite.Sprite):
    image = load_image("mirror.png")

    def __init__(self, *group):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно!!!
        super().__init__(*group)
        self.image = Mirror.image
        self.rect = self.image.get_rect()
        self.rect.x = 20
        self.rect.y = 500
        # угол, на который повернуто зеркало относительно вертикальной прямой
        # (отсчитывается по часовой стрелке в градусах)
        self.angle = 0
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)


class Button(pygame.sprite.Sprite):
    """Class used to create a button, use setCords to set
        position of topleft corner. Method pressed() returns
        a boolean and should be called inside the input loop."""

    image = load_image("restart_button.png")

    def __init__(self, name, *group):
        super().__init__(*group)
        self.image = load_image(name)
        self.rect = self.image.get_rect()

    def setCords(self, x, y):
        self.rect.topleft = x, y

    def pressed(self, mouse):
        if mouse[0] > self.rect.topleft[0]:
            if mouse[1] > self.rect.topleft[1]:
                if mouse[0] < self.rect.bottomright[0]:
                    if mouse[1] < self.rect.bottomright[1]:
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                return False
        else:
            return False


# hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh
def terminate():
    pygame.quit()
    sys.exit()


def start_screen(screen, clock):
    intro_text = ["                                          SPACE-DEFENDER", "",
                  "      Вашу родную планету атакуют вражеские корабли! Защитите ее!",
                  "      Вы можете двигать пушку клавишами стрелочками на клавиатуре",
                  "      и при нажатии на пробел совершать выстрел.",
                  "      Если хотя бы один космический корабль опустится ниже уровня",
                  "      вашей пушки, то тогда вы проиграете.",
                  "      Если в течении всего времени игры вы сможете отбить ",
                  "                      атаку всех кораблей, то вы победили.",
                  "                                                     Удачи!   ",
                  "                                       Для начала нажмите на экран"
                  ]

    fon = pygame.transform.scale(load_image('back1.png'), (WINDOW_WIDTH, WINDOW_HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font('ofont.ru_Pixeloid Sans.ttf', 20)
    text_coord = 100
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 30
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


def end_screen(screen, clock):
    intro_text = ["",
                  "",
                  "",
                  "",
                  "",
                  "                                                  Игра окончена", ""
                  ]

    fon = pygame.transform.scale(load_image('game_over.png'), (WINDOW_WIDTH, WINDOW_HEIGHT))
    screen.blit(fon, (0, 0))
    # font = pygame.font.Font(None, 30)
    # text_coord = 100
    # for line in intro_text:
    #     string_rendered = font.render(line, 1, pygame.Color('black'))
    #     intro_rect = string_rendered.get_rect()
    #     text_coord += 30
    #     intro_rect.top = text_coord
    #     intro_rect.x = 10
    #     text_coord += intro_rect.height
    #     screen.blit(string_rendered, intro_rect)

    buttons = pygame.sprite.Group()  # кнопка начать заново
    button = Button("restart_button.png", buttons)  # Button class is created
    button.setCords(180, 500)  # Button is displayed at 200,200
    while True:
        buttons.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if button.pressed(mouse):
                    main()
            # elif event.type == pygame.KEYDOWN or \
            #         event.type == pygame.MOUSEBUTTONDOWN:
            #     return  # начинаем игру

        pygame.mouse.set_visible(True)
        pygame.display.flip()
        clock.tick(FPS)


def win_screen(screen, clock):
    # intro_text = ["",
    #               "",
    #               "",
    #               "",
    #               "",
    #               "                                                  Вы выиграли"
    #               ]

    fon = pygame.transform.scale(load_image('win.jpg'), (WINDOW_WIDTH, WINDOW_HEIGHT))
    screen.blit(fon, (0, 0))
    # font = pygame.font.Font(None, 30)
    # text_coord = 100
    # for line in intro_text:
    #     string_rendered = font.render(line, 1, pygame.Color('black'))
    #     intro_rect = string_rendered.get_rect()
    #     text_coord += 30
    #     intro_rect.top = text_coord
    #     intro_rect.x = 10
    #     text_coord += intro_rect.height
    #     screen.blit(string_rendered, intro_rect)

    # кнопка начать заново
    buttons = pygame.sprite.Group()
    button = Button("restart_button.png", buttons)  # Button class is created
    button.setCords(180, 500)  # Button is displayed at 200,200

    while True:
        buttons.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if button.pressed(mouse):
                    main()
        pygame.mouse.set_visible(True)
        pygame.display.flip()
        clock.tick(FPS)


def main():
    esli_win = True
    big_c = 0
    asteroids = pygame.sprite.Group()
    for _ in range(4):
        Asteroids(asteroids)
    ships = pygame.sprite.Group()
    for _ in range(7):
        Spaceships(ships)
    lasers = pygame.sprite.Group()
    flags = []
    # background = random.choice(background_list)
    # image = load_image(background)
    image = pygame.transform.scale(load_image('back3.jpg'), (WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.init()
    pygame.display.set_caption('Space Defender')
    screen = pygame.display.set_mode(WINDOW_SIZE)
    clock = pygame.time.Clock()
    # jjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj
    start_screen(screen, clock)
    flag = False

    gun = Gun()

    running = True

    while running:
        big_c += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            laser_x = gun.get_position()[0] + 10
            laser_y = gun.get_position()[1] - 35
            if event.type == pygame.MOUSEBUTTONDOWN:
                k = 0
                if pygame.mouse.get_pos()[0] != laser_x:
                    k = (pygame.mouse.get_pos()[1] - laser_y) / (
                            pygame.mouse.get_pos()[0] - laser_x)
                new_laser = Laser((laser_x, laser_y), k, lasers)
                # Rotate the image by any degree
                new_laser.angle = 90 - (math.atan(-k) * 180 / math.pi)
                new_laser.image = pygame.transform.rotate(new_laser.origimage, new_laser.angle)
                new_laser.rect = new_laser.image.get_rect(center=new_laser.positions)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                Laser((laser_x, laser_y), 0, lasers)

        for g in ships:
            # print(g.get_position())
            if g.get_position() >= 720:  # Здесь координаты пушки и размер корабля
                esli_win = False
        screen.fill((0, 0, 0))
        screen.blit(image, (0, 0))

        pygame.mouse.set_visible(False)
        # курсор заменен на зелененький прицел. в эту точку будет стрелять пулька
        if pygame.mouse.get_focused():
            screen.blit(load_image('cursor.png'), pygame.mouse.get_pos())

        gun.move()
        gun.drawing(screen)
        # рисуем srites, которые двигаются
        ships.draw(screen)
        lasers.draw(screen)
        asteroids.draw(screen)
        ships.update()
        lasers.update()
        if big_c % 110 == 0 and big_c != 0:
            for _ in range(10):
                Spaceships(ships)
        # если лазер попадает в корабль, то удаляем и пульку, и корабль
        pygame.sprite.groupcollide(lasers, ships, True, True)
        # Если лазер попадает в астероиды, то удаляем пульку
        pygame.sprite.groupcollide(lasers, asteroids, True, False)

        pygame.display.flip()
        clock.tick(FPS)
        if esli_win:
            if big_c == 1000:
                win_screen(screen, clock)

        else:
            end_screen(screen, clock)
    pygame.quit()


if __name__ == '__main__':
    main()
