import pygame
from random import choice
from copy import deepcopy

WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 600, 700
BOARD_WIDTH, BOARD_HEIGHT = 10, 20
TILE_SIZE = 35
BOARD_SIZE = BOARD_WIDTH * TILE_SIZE, BOARD_HEIGHT * TILE_SIZE
FPS = 120
figures_positions = [[(0, 0), (0, -1), (0, 1), (1, -1)],
                     [(0, -1), (-1, -1), (-1, 0), (0, 0)],
                     [(0, 0), (-1, 0), (0, 1), (-1, -1)],
                     [(-1, 0), (-2, 0), (0, 0), (1, 0)],
                     [(0, 0), (0, -1), (0, 1), (-1, -1)],
                     [(-1, 0), (-1, 1), (0, 0), (0, -1)],
                     [(0, 0), (0, -1), (0, 1), (-1, 0)]]
figures = [[pygame.Rect(x + BOARD_WIDTH // 2, y + 1, 1, 1) for x, y in figure] for figure in figures_positions]
figure_rect = pygame.Rect(0, 0, TILE_SIZE - 2, TILE_SIZE - 2)
field = [[0] * BOARD_WIDTH for _ in range(BOARD_HEIGHT)]
count, limit, speed = 0, 1000, 20
figure, next_figure = deepcopy(choice(figures)), deepcopy(choice(figures))
score1, lines = 0, 0
scores = {0: 0, 1: 100, 2: 300, 3: 700, 4: 1500}


def check_borders(i):
    if figure[i].x < 0 or figure[i].x > BOARD_WIDTH - 1:
        return False
    elif figure[i].y > BOARD_HEIGHT - 1 or field[figure[i].y][figure[i].x]:
        return False
    return True


def get_record():
    try:
        with open('record.txt') as f:
            return f.readline()
    except FileNotFoundError:
        with open('record.txt', 'w') as f:
            f.write('0')


def set_record(record1, score1):
    record1 = max(int(record1), score1)
    with open('record.txt', 'w') as f:
        f.write(str(record1))


def main():
    global figure, count, limit, next_figure, speed, lines, score1, field
    pygame.init()
    pygame.display.set_caption("Тетрис")
    screen = pygame.display.set_mode(WINDOW_SIZE)
    clock = pygame.time.Clock()
    board = [pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
             for x in range(BOARD_WIDTH) for y in range(BOARD_HEIGHT)]
    main_font = pygame.font.Font("font/19844.otf", 60)
    font = pygame.font.Font("font/19844.otf", 40)
    font2 = pygame.font.Font("font/19844.otf", 36)
    font1 = pygame.font.SysFont("Arial", 12)
    tetris = main_font.render('TETRIS', True, pygame.Color('Blue'))
    score = font.render('score:', True, pygame.Color('green'))

    record = font.render('record:', True, pygame.Color('purple'))
    for i in range(lines):
        pygame.time.wait(200)
    pygame.mixer.music.load('music/tetris.wav')
    pygame.mixer.music.play(-1)
    sound = pygame.mixer.Sound('music/failure.wav')
    pause = True
    music = True
    running = True
    volume = 0.1
    pygame.mixer.music.set_volume(volume)
    while running:
        record1 = get_record()
        rotate = False
        dx = 0
        screen.fill("Black")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    dx = -1
                elif event.key == pygame.K_RIGHT:
                    dx = 1
                elif event.key == pygame.K_DOWN:
                    limit = 100
                elif event.key == pygame.K_SPACE:
                    rotate = True
                if event.key == pygame.K_k:
                    music = False
                    pygame.mixer.music.pause()
                if event.key == pygame.K_l:
                    music = True
                    pygame.mixer.music.unpause()
                if event.key == pygame.K_ESCAPE:
                    pause = not pause
            if event.type == pygame.KEYUP:
                limit = 1000
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    if volume < 1:
                        volume += 0.1
                        pygame.mixer.music.set_volume(volume)
                elif event.button == 5:
                    if volume > 0:
                        volume -= 0.1
                        pygame.mixer.music.set_volume(volume)

        if not pause:
            if music:
                pygame.mixer.music.unpause()
            save_figure = deepcopy(figure)
            for i in range(4):
                figure[i].x += dx
                if not check_borders(i):
                    figure = deepcopy(save_figure)
                    break
            count += speed
            if count >= limit:
                count = 0
                save_figure = deepcopy(figure)
                for i in range(4):
                    figure[i].y += 1
                    if not check_borders(i):
                        for i in range(4):
                            field[save_figure[i].y][save_figure[i].x] = pygame.Color("White")
                        figure = next_figure
                        next_figure = deepcopy(choice(figures))
                        break
            save_figure = deepcopy(figure)
            center = figure[0]
            if rotate:
                print(figure)
                for i in range(4):
                    x = figure[i].y - center.y
                    y = figure[i].x - center.x
                    figure[i].x = center.x - x
                    figure[i].y = center.y + y
                    if not check_borders(i):
                        figure = deepcopy(save_figure)
                        break
            end_line, lines = BOARD_HEIGHT - 1, 0
            for row in range(BOARD_HEIGHT - 1, -1, -1):
                count1 = 0
                for i in range(BOARD_WIDTH):
                    if field[row][i]:
                        count1 += 1
                    field[end_line][i] = field[row][i]
                if count1 < BOARD_WIDTH:
                    end_line -= 1
                else:
                    speed += 1
                    lines += 1
            score1 += scores[lines]
            [pygame.draw.rect(screen, (30, 30, 30), rect, 1) for rect in board]
            for i in range(4):
                figure_rect.x = figure[i].x * TILE_SIZE
                figure_rect.y = figure[i].y * TILE_SIZE
                pygame.draw.rect(screen, "White", figure_rect)

            for y, raw in enumerate(field):
                for x, col in enumerate(raw):
                    if col:
                        figure_rect.x = x * TILE_SIZE
                        figure_rect.y = y * TILE_SIZE
                        pygame.draw.rect(screen, "White", figure_rect)
            for i in range(4):
                figure_rect.x = next_figure[i].x * TILE_SIZE + 300
                figure_rect.y = next_figure[i].y * TILE_SIZE + 185
                pygame.draw.rect(screen, "White", figure_rect)

            screen.blit(tetris, (370, 30))
            screen.blit(score, (380, 500))
            screen.blit(font.render(str(score1), True, pygame.Color('white')), (390, 550))
            screen.blit(record, (380, 400))
            screen.blit(font.render(record1, True, pygame.Color('white')), (390, 450))
            screen.blit(font1.render("Для вращения фигуры используйте кнопку Space", True, pygame.Color("white")),
                        (355, 600))
            screen.blit(font1.render("Чтобы поставить музыку на паузу нажмите K", True, pygame.Color("white")),
                        (355, 615))
            screen.blit(font1.render("Чтобы возобновить музыку нажмите L", True, pygame.Color("white")),
                        (355, 630))
            screen.blit(font1.render("Громкость музыки можно изменить колёсиком мыши", True, pygame.Color("White")),
                        (355, 645))

            for i in range(BOARD_WIDTH):
                if field[0][i]:
                    set_record(record1, score1)
                    field = [[0] * BOARD_WIDTH for _ in range(BOARD_HEIGHT)]
                    count, limit, speed = 0, 1000, 20
                    score1 = 0
                    pygame.mixer.music.pause()
                    sound.play()
                    pygame.time.wait(1500)
                    pygame.mixer.music.unpause()
        else:
            pygame.mixer.music.pause()
            screen.blit(font2.render("Чтобы начать играть, нажмите Esc", True, pygame.Color("white")),
                        (25, WINDOW_HEIGHT // 2))

        pygame.display.flip()
        clock.tick(FPS)
    pygame.display.quit()


if __name__ == "__main__":
    main()
