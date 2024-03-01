import math

import pygame
import os
from dotenv import load_dotenv
import random
import sys
from objects.gun import Gun
from objects.laser import Laser
from objects.spaceship import Spaceships
from objects.asteroids import Asteroids
from objects.mirror import Mirror
from objects.button import Button
from utility import load_image


load_dotenv()
WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 800, 900
MOVING_GUN = os.getenv("MOVING_GUN")
MOVING_LASER = os.getenv("MOVING_LASER")
FPS = int(os.getenv("FPS"))
background_list = ['вид2.png', 'вид3.png', 'вид4.png', 'вид5.png', 'вид6.png']
score = 0


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

    font = pygame.font.Font('ofont.ru_Pixeloid Sans.ttf', 40)
    string_rendered = font.render(f'score: {score}', 1, pygame.Color('black'))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = 600
    intro_rect.x = 400
    screen.blit(string_rendered, intro_rect)
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


def win_screen(screen, clock):
    fon = pygame.transform.scale(load_image('win.jpg'), (WINDOW_WIDTH, WINDOW_HEIGHT))
    screen.blit(fon, (0, 0))

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
    score = 0
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
                new_laser.angle = 90 - (math.atan(k) * 180 / math.pi)
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
        score += 1
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
