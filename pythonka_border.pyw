import pygame
import random
from tkinter import messagebox as mb

pygame.init()

PAD = 8

display = pygame.display.set_mode((616, 670))
pygame.display.set_caption("Pythonka")
FPS = pygame.time.Clock()
fontBig = pygame.font.Font(None, 36)
fontSmall = pygame.font.Font(None, 16)
fontScore = pygame.font.Font(None, 28)
back_surf = pygame.image.load('d:/dsk/back.png')
net_surf = pygame.image.load('d:/dsk/net.png')
back_rect = back_surf.get_rect(center=(38, 35))
net_rect = back_surf.get_rect(topleft=(358, 629))

CELL = 30
FIELD = 20
SPEED_DEF = 5
apple_xy = [-1, -1]

display.fill((50, 55, 60))

def draw_rect(color, cord):
    pygame.draw.rect(display, color, (cord[0] + PAD, cord[1] + PAD, cord[2], cord[3]), 0, 4)

def draw_text(text, cord, font=fontBig, shadow=True, color=(255, 255, 255)):
    if shadow:
        textObj2 = font.render(text, 1, (30, 140, 10))
        display.blit(textObj2, (cord[0] + 3 + PAD, cord[1] + 3 + PAD))
    textObj = font.render(text, 1, color)
    display.blit(textObj, (cord[0] + PAD, cord[1] + PAD))

def scores():
    draw_rect((50, 55, 60), (0, 604, 600, 56))    
    draw_text("Очки: " + str(apple_count), (14, 622), fontScore, False)

def apple():
    global apple_xy
    while True:
        apple_xy = [random.randint(0, FIELD - 1) * CELL, random.randint(0, FIELD - 1) * CELL]
        if tuple(apple_xy) not in body:  # Реген яблока, если оно оказалось в теле
            break
    draw_rect((240, 20, 20), (apple_xy[0], apple_xy[1], CELL, CELL))
    scores()

def collision():
    global skip_kpop, apple_count, game
    if tuple(head) in body[1:] or head[0] >= 600 or head[1] >= 600 or head[0] < 0 or head[1] < 0:
        game = False
    if tuple(apple_xy) in body:
        apple_count += 1
        skip_kpop = True
        apple()

def move():
    global body, head, counter, xm, ym, skip_kpop, direct

    key = pygame.key.get_pressed()
    if counter < SPEED_DEF:
        counter += 1
    else:
        if key[pygame.K_RIGHT] and direct != 1:
            xm = CELL
            ym = 0
            direct = 0  # Блокирует движение в противоположную сторону
        elif key[pygame.K_LEFT] and direct != 0:
            xm = -CELL
            ym = 0
            direct = 1
        elif key[pygame.K_UP] and direct != 3:
            ym = -CELL
            xm = 0
            direct = 2
        elif key[pygame.K_DOWN] and direct != 2:
            ym = CELL
            xm = 0
            direct = 3
        counter = 0
        head[0] += xm
        head[1] += ym
        body.insert(0, (head[0], head[1]))
        if not skip_kpop:  # Убирает конец хвоста и рисует на его месте клетку поля. Bust FPS 1000%
            x, y = body.pop()
            if int(x / CELL) % 2 == 0:
                if int(y / CELL) % 2 == 0:
                    draw_rect((30, 160, 20), (x, y, CELL, CELL))
                else:
                    draw_rect((30, 180, 10), (x, y, CELL, CELL))
            else:
                if int(y / CELL) % 2 == 1:
                    draw_rect((30, 160, 20), (x, y, CELL, CELL))
                else:
                    draw_rect((30, 180, 10), (x, y, CELL, CELL))
        else:
            skip_kpop = False

def snake(): #Рисуем только 1, 2 и последнюю клетку змейки. Bust FPS 9999%
    draw_rect((255, 255, 255), (body[-1][0], body[-1][1], CELL, CELL))
    draw_rect((255, 255, 255), (body[1][0],  body[1][1],  CELL, CELL))
    draw_rect((255, 115,   3), (body[0][0],  body[0][1],  CELL, CELL))

def area():
    
    #Тень
    draw_rect((44, 48, 52), (0, 0, 604, 604))
    draw_rect((37, 40, 44), (0, 0, 603, 603))
    draw_rect((30, 33, 36), (0, 0, 602, 602))
    draw_rect((23, 25, 28), (0, 0, 601, 601))

    i = False
    draw_rect((30, 160, 20), (0, 0, 600, 600))
    for x in range(FIELD):
        i = not i
        for y in range(FIELD):
            i = not i
            if i:
                draw_rect((30, 180, 10), (CELL * x, CELL * y, CELL, CELL))

def leaderboard():
    draw_rect((250, 250, 250), (0, 0, 600, 652))
    draw_rect((240, 240, 240), (0, 0, 600, 54))
    display.blit(back_surf, back_rect)
    draw_text("Лидеры", (64,18), fontScore, False, (20, 21, 24))
    sc_y = 72

    with open("d:/dsk/scores.txt") as file_scores:
        for line in [line.rstrip() for line in file_scores]:
            draw_text("•     " + line, (28, sc_y), fontScore, False, (20, 21, 24))
            sc_y += 32

    pygame.display.update()
    while True:
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                exit()
            if i.type == pygame.MOUSEBUTTONDOWN and i.button == 1 and i.pos[1] < 62 and i.pos[0] < 64:
                return
        FPS.tick(2) 

def draw_config():
    scores()
    draw_text("РАЗМЕР КЛЕТКИ", (502, 614), fontSmall, False)
    draw_text("ЗАДЕРЖКА", (408, 614), fontSmall, False)

    if CELL >= 100:
        draw_text(str(CELL), (534, 630), fontScore, False)
    elif CELL < 10:
        draw_text(str(CELL), (544, 630), fontScore, False)
    else:
        draw_text(str(CELL), (538, 630), fontScore, False)
        
    draw_text(str(SPEED_DEF), (436, 630), fontScore, False)

    draw_rect((74, 82, 89), (506, 630, 18, 18))
    draw_rect((74, 82, 89), (576, 630, 18, 18))
    draw_text("+", (512, 633), fontSmall, False)
    draw_text("-", (583, 633), fontSmall, False)

    draw_rect((74, 82, 89), (398, 630, 18, 18))
    draw_rect((74, 82, 89), (468, 630, 18, 18))
    draw_text("+", (404, 633), fontSmall, False)
    draw_text("-", (475, 633), fontSmall, False)
    
    draw_rect((74, 82, 89), (344, 614, 34, 34))
    display.blit(net_surf, net_rect)

    draw_rect((140, 140, 140), (14, 646, 56, 2))

    if apple_xy == [-1, -1]:
        draw_text('Pythonka', (245, 270))
        draw_text('Copyright © 2020, Vnukov D., Prodeus D., Perfilev D.', (162, 550), fontSmall)
    else:
        draw_text('Game Over', (232, 270))

    draw_text('Нажмите Enter для начала игры', (107, 306))

    pygame.display.update()

def show_config():
    global CELL, SPEED_DEF, FIELD
    draw_config()
    need_key = True
    cell_presets = (2, 4, 6, 10, 12, 20, 25, 30, 50, 60, 75, 100) #8, 40
    prs = cell_presets.index(CELL)

    while need_key:
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                exit()
            elif i.type == pygame.KEYDOWN and i.key == pygame.K_RETURN:
                    need_key = False
            if i.type == pygame.MOUSEBUTTONDOWN and i.button == 1:
                if 608 < i.pos[1] and i.pos[0] < 100:
                    leaderboard()
                    display.fill((50, 55, 60))
                    area()
                    show_config()
                elif 622 < i.pos[1] < 656 and 352 < i.pos[0] < 386:
                    mb.showinfo("Игра по сети", "Код пока не написан(")
                elif 638 < i.pos[1] < 656:
                    if 514 < i.pos[0] < 532 and prs < 11:
                        prs += 1
                        CELL = cell_presets[prs]
                        FIELD = int(600 / CELL)
                    elif 584 < i.pos[0] < 602 and prs > 0:
                        prs -= 1
                        CELL = cell_presets[prs]
                        FIELD = int(600 / CELL)
                    elif 406 < i.pos[0] < 424 and SPEED_DEF < 9:
                        SPEED_DEF += 1
                    elif 476 < i.pos[0] < 496 and SPEED_DEF > 0:
                        SPEED_DEF -= 1
                    else:
                        continue
                    area()
                    draw_config()
        FPS.tick(10) 

def run_game():
    need_key = True
    area()
    apple()
    while game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif need_key and event.type == pygame.KEYDOWN:  # Ждем кнопку
                need_key = False

        snake()

        if need_key:
            pygame.display.update()
            FPS.tick(10)  # оптимизация
            continue

        move()
        collision()
        pygame.display.update()
        FPS.tick(60)

area()
apple_count = 0
while True:
    show_config()
    
    apple_count = 0
    i = 0
    xm = CELL
    ym = 0
    direct = 0
    counter = 0
    skip_kpop = False
    head = [2 * CELL, 1 * CELL]
    body = [(2 * CELL, 1 * CELL), (1 * CELL, 1 * CELL), (0, 1 * CELL)]
    game = True
    run_game()
