import pygame
import random

pygame.init()

display = pygame.display.set_mode((600, 660))
pygame.display.set_caption("Pythonka")
FPS = pygame.time.Clock()
fontBig = pygame.font.Font(None, 36)
fontSmall = pygame.font.Font(None, 16)
fontScore = pygame.font.Font(None, 28)

CELL = 30
FIELD = 20
SPEED_DEF = 5
apple_xy = [-1, -1]


def draw_text(text, placement, font=fontBig, shadow=True):
    if shadow:
        textObj2 = font.render(text, 1, (30, 140, 10))
        display.blit(textObj2, (placement[0] + 3, placement[1] + 3))
    textObj = font.render(text, 1, (255, 255, 255))
    display.blit(textObj, placement)

def scores():
    pygame.draw.rect(display, (50, 55, 60), (0, 604, 600, 56))
    
    #Градиент
    pygame.draw.rect(display, (23, 25, 28), (0, 600, 600, 1))
    pygame.draw.rect(display, (30, 33, 36), (0, 601, 600, 1))
    pygame.draw.rect(display, (37, 40, 44), (0, 602, 600, 1))
    pygame.draw.rect(display, (44, 48, 52), (0, 603, 600, 1))
    
    draw_text("Очки: " + str(apple_count), (20, 620), fontScore, False)

def apple():
    global apple_xy
    while True:
        apple_xy = [random.randint(0, FIELD - 1) * CELL, random.randint(0, FIELD - 1) * CELL]
        if tuple(apple_xy) not in body:  # Реген яблока, если оно оказалось в теле
            break
    pygame.draw.rect(display, (240, 20, 20), (apple_xy[0], apple_xy[1], CELL, CELL))
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
                    pygame.draw.rect(display, (30, 160, 20), (x, y, CELL, CELL))
                else:
                    pygame.draw.rect(display, (30, 180, 10), (x, y, CELL, CELL))
            else:
                if int(y / CELL) % 2 == 1:
                    pygame.draw.rect(display, (30, 160, 20), (x, y, CELL, CELL))
                else:
                    pygame.draw.rect(display, (30, 180, 10), (x, y, CELL, CELL))
        else:
            skip_kpop = False


def snake(): #Рисуем только 1, 2 и последнюю клетку змейки. Bust FPS 9999%
    pygame.draw.rect(display, (255, 255, 255), (body[-1][0], body[-1][1], CELL, CELL))
    pygame.draw.rect(display, (255, 255, 255), (body[1][0],  body[1][1],  CELL, CELL))
    pygame.draw.rect(display, (255, 115,   3), (body[0][0],  body[0][1],  CELL, CELL))


def area():
    i = False
    display.fill((30, 160, 20))
    for x in range(FIELD):
        i = not i
        for y in range(FIELD):
            i = not i
            if i:
                pygame.draw.rect(display, (30, 180, 10), (CELL * x, CELL * y, CELL, CELL))

def draw_config():
    scores()
    draw_text("РАЗМЕР КЛЕТКИ", (495, 612), fontSmall, False)
    draw_text("ЗАДЕРЖКА", (400, 612), fontSmall, False)

    if CELL >= 100:
        draw_text(str(CELL), (520, 626), fontBig, False)
    elif CELL < 10:
        draw_text(str(CELL), (534, 626), fontBig, False)
    else:
        draw_text(str(CELL), (528, 626), fontBig, False)
        
    draw_text(str(SPEED_DEF), (426, 626), fontBig, False)

    pygame.draw.rect(display, (74, 82, 89), (498, 628, 18, 18))
    pygame.draw.rect(display, (74, 82, 89), (568, 628, 18, 18))
    draw_text("+", (504, 631), fontSmall, False)
    draw_text("-", (575, 631), fontSmall, False)

    pygame.draw.rect(display, (74, 82, 89), (390, 628, 18, 18))
    pygame.draw.rect(display, (74, 82, 89), (460, 628, 18, 18))
    draw_text("+", (396, 631), fontSmall, False)
    draw_text("-", (467, 631), fontSmall, False)

    draw_text("-", (575, 631), fontSmall, False)
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
                if 631 < i.pos[1] < 649:
                    if 498 < i.pos[0] < 516 and prs < 11:
                        prs += 1
                        CELL = cell_presets[prs]
                        FIELD = int(600 / CELL)
                    elif 568 < i.pos[0] < 586 and prs > 0:
                        prs -= 1
                        CELL = cell_presets[prs]
                        FIELD = int(600 / CELL)
                    elif 390 < i.pos[0] < 408 and SPEED_DEF < 9:
                        SPEED_DEF += 1
                    elif 460 < i.pos[0] < 478 and SPEED_DEF > 0:
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
while True:
    apple_count = 0

    show_config()

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
