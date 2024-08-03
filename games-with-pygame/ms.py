import pygame
from pygame.locals import *
import sys
from random import randint

## ゲーム定数
# マスのサイズ
SQR_SIZE = 30
# x方向のマスの数
GRID_WIDTH = 20
# z方向のマスの数
GRID_HEIGHT = 20

## ゲームステータス
# ゲームレベル
LEVEL = 1
# ゲームオーバーフラグ
GAME_OVER = False
# 成功フラグ
WIN = False
# 終了時タイム
SECONDS = 0

# 画像の読み込み
IMAGES = [
    pygame.image.load(f'images/{i}.png') for i in range(9)
] + [pygame.image.load(f'images/b.png'), pygame.image.load(f'images/f.png')]

# Map, button のステータス
MAP_STATE = {'space': 0, 'bomb': -1}
BTN_STATE = {'pressed': 0, 'not_pressed': 1, 'flagged': 2}


def create_maps(level):
    maps = [[{'map': MAP_STATE['space'], 'btn': BTN_STATE['not_pressed']} for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    bomb_count = int(GRID_WIDTH * GRID_HEIGHT * 0.05) + level * 5

    while bomb_count > 0:
        dx, dy = randint(0, GRID_WIDTH - 1), randint(0, GRID_HEIGHT - 1)
        if maps[dy][dx]['map'] == MAP_STATE['space']:
            maps[dy][dx]['map'] = MAP_STATE['bomb']
            bomb_count -= 1

    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if maps[y][x]['map'] == MAP_STATE['bomb']:
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        if 0 <= y + j < GRID_HEIGHT and 0 <= x + i < GRID_WIDTH and maps[y + j][x + i]['map'] != MAP_STATE['bomb']:
                            maps[y + j][x + i]['map'] += 1

    return maps


def reveal_zero_area(maps, x, y):
    def is_within_bounds(x, y):
        return 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT

    def explore(x, y):
        if not is_within_bounds(x, y) or (x, y) in checked or maps[y][x]['btn'] == BTN_STATE['pressed']:
            return
        checked.add((x, y))
        maps[y][x]['btn'] = BTN_STATE['pressed']
        if maps[y][x]['map'] == 0:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    explore(x + i, y + j)

    checked = set()
    explore(x, y)


def reveal_all_buttons(maps):
    for row in maps:
        for cell in row:
            cell['btn'] = BTN_STATE['pressed']


def check_win_condition(maps):
    for row in maps:
        for cell in row:
            if cell['map'] != MAP_STATE['bomb'] and cell['btn'] != BTN_STATE['pressed']:
                return False
    return True


def reset_game():
    global GAME_OVER, WIN, maps, start_ticks
    GAME_OVER, WIN = False, False
    maps = create_maps(LEVEL)
    start_ticks = pygame.time.get_ticks()


def draw_end_screen(screen, font, message):
    screen.fill((220, 220, 220))
    text = font.render(message, True, (0, 0, 0))
    text_rect = text.get_rect(center=(GRID_WIDTH * SQR_SIZE / 2, GRID_HEIGHT * SQR_SIZE / 3))
    screen.blit(text, text_rect)

    time_text = font.render(f'Time: {SECONDS:.2f}', True, (0, 0, 0))
    time_rect = time_text.get_rect(center=(GRID_WIDTH * SQR_SIZE / 2, GRID_HEIGHT * SQR_SIZE / 2))
    screen.blit(time_text, time_rect)

    reset_button = pygame.Rect(GRID_WIDTH * SQR_SIZE / 2 - 60, GRID_HEIGHT * SQR_SIZE / 2 + 40, 120, 40)
    quit_button = pygame.Rect(GRID_WIDTH * SQR_SIZE / 2 - 60, GRID_HEIGHT * SQR_SIZE / 2 + 100, 120, 40)
    pygame.draw.rect(screen, (0, 0, 0), reset_button)
    pygame.draw.rect(screen, (0, 0, 0), quit_button)

    reset_text = font.render("Reset", True, (255, 255, 255))
    quit_text = font.render("Quit", True, (255, 255, 255))
    screen.blit(reset_text, reset_text.get_rect(center=reset_button.center))
    screen.blit(quit_text, quit_text.get_rect(center=quit_button.center))

    level_buttons = []
    for i in range(1, 4):
        button = pygame.Rect(GRID_WIDTH * SQR_SIZE / 2 - 60, GRID_HEIGHT * SQR_SIZE / 2 + 160 + i * 60, 120, 40)
        pygame.draw.rect(screen, (0, 0, 0), button)
        level_text = font.render(f"Level {i}", True, (255, 255, 255))
        screen.blit(level_text, level_text.get_rect(center=button.center))
        level_buttons.append(button)

    return reset_button, quit_button, level_buttons


def main():
    global GAME_OVER, WIN, start_ticks, SECONDS, LEVEL
    pygame.init()
    screen = pygame.display.set_mode((GRID_WIDTH * SQR_SIZE, GRID_HEIGHT * SQR_SIZE + 300))
    pygame.display.set_caption("Mine Sweeper")
    reset_game()
    font = pygame.font.Font(None, 36)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if GAME_OVER:
                reset_button, quit_button, level_buttons = draw_end_screen(screen, font, "You Win!" if WIN else "You are Dead")
                if event.type == MOUSEBUTTONDOWN:
                    if reset_button.collidepoint(event.pos):
                        reset_game()
                    elif quit_button.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()
                    else:
                        for i, button in enumerate(level_buttons):
                            if button.collidepoint(event.pos):
                                LEVEL = i + 1
                                reset_game()
                pygame.display.update()
                continue

            if event.type == MOUSEBUTTONDOWN:
                p_x, p_y = event.pos
                grid_x, grid_y = p_x // SQR_SIZE, p_y // SQR_SIZE

                # 左クリック
                if event.button == 1:
                    if maps[grid_y][grid_x]['btn'] != BTN_STATE['flagged']:
                        if maps[grid_y][grid_x]['map'] == MAP_STATE['bomb']:
                            reveal_all_buttons(maps)
                            GAME_OVER = True
                        else:
                            if maps[grid_y][grid_x]['map'] == 0:
                                reveal_zero_area(maps, grid_x, grid_y)
                            else:
                                maps[grid_y][grid_x]['btn'] = BTN_STATE['pressed']
                            if check_win_condition(maps):
                                GAME_OVER, WIN = True, True
                
                # 右クリック
                elif event.button == 3:
                    if maps[grid_y][grid_x]['btn'] == BTN_STATE['flagged']:
                        maps[grid_y][grid_x]['btn'] = BTN_STATE['not_pressed']
                    elif maps[grid_y][grid_x]['btn'] == BTN_STATE['not_pressed']:
                        maps[grid_y][grid_x]['btn'] = BTN_STATE['flagged']

        if not GAME_OVER:
            screen.fill((220, 220, 220))

            for y in range(GRID_HEIGHT):
                for x in range(GRID_WIDTH):
                    cell = maps[y][x]
                    if cell['btn'] == BTN_STATE['pressed']:
                        image = IMAGES[cell['map']]
                    elif cell['btn'] == BTN_STATE['flagged']:
                        image = IMAGES[10]
                    else:
                        image = pygame.Surface((SQR_SIZE, SQR_SIZE))
                        image.fill((255, 255, 255))
                        pygame.draw.rect(image, (0, 0, 0), image.get_rect(), 1)
                    screen.blit(image, (x * SQR_SIZE, y * SQR_SIZE))

            if start_ticks is not None:
                SECONDS = (pygame.time.get_ticks() - start_ticks) / 1000
                timer_text = font.render(f'Time: {SECONDS:.2f}', True, (0, 0, 0))
                screen.blit(timer_text, (10, GRID_HEIGHT * SQR_SIZE + 10))

            pygame.display.update()


if __name__ == "__main__":
    main()
