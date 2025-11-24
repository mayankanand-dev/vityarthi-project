import pygame
import random
import time

pygame.init()

S_WIDTH = 800
S_HEIGHT = 700
PLAY_WIDTH = 300
PLAY_HEIGHT = 600
BLOCK_SIZE = 30

TOP_LEFT_X = (S_WIDTH - PLAY_WIDTH) // 2
TOP_LEFT_Y = S_HEIGHT - PLAY_HEIGHT - 50

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)

S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

SHAPES = [S, Z, I, O, J, L, T]
SHAPE_COLORS = [GREEN, RED, CYAN, YELLOW, ORANGE, BLUE, PURPLE]

class Piece(object):
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = SHAPE_COLORS[SHAPES.index(shape)]
        self.rotation = 0

def create_grid(locked_positions={}):
    grid = [[BLACK for _ in range(10)] for _ in range(20)]

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_positions:
                c = locked_positions[(j, i)]
                grid[i][j] = c
    return grid

def convert_shape_format(piece):
    positions = []
    format = piece.shape[piece.rotation % len(piece.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((piece.x + j, piece.y + i))

    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions

def valid_space(piece, grid):
    accepted_pos = [[(j, i) for j in range(10) if grid[i][j] == BLACK] for i in range(20)]
    accepted_pos = [j for sub in accepted_pos for j in sub]

    formatted = convert_shape_format(piece)

    for pos in formatted:
        if pos not in accepted_pos:
            if pos[1] > -1:
                return False
    return True

def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False

def get_random_shape():
    return Piece(5, 0, random.choice(SHAPES))

def draw_text_middle(surface, text, size, color):
    font = pygame.font.SysFont("comicsans", size, bold=True)
    label = font.render(text, 1, color)
    surface.blit(label, (TOP_LEFT_X + PLAY_WIDTH/2 - (label.get_width()/2), TOP_LEFT_Y + PLAY_HEIGHT/2 - label.get_height()/2))

def draw_grid(surface, grid):
    sx = TOP_LEFT_X
    sy = TOP_LEFT_Y

    for i in range(len(grid)):
        pygame.draw.line(surface, GRAY, (sx, sy + i * BLOCK_SIZE), (sx + PLAY_WIDTH, sy + i * BLOCK_SIZE))
    for j in range(len(grid[0])):
        pygame.draw.line(surface, GRAY, (sx + j * BLOCK_SIZE, sy), (sx + j * BLOCK_SIZE, sy + PLAY_HEIGHT))

def clear_rows(grid, locked):
    increment = 0
    for i in range(len(grid) - 1, -1, -1):
        row = grid[i]
        if BLACK not in row:
            increment += 1
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except:
                    continue

    if increment > 0:
        for key in sorted(list(locked), key=lambda x: x[1]):
            x, y = key
            if y < ind:
                newKey = (x, y + increment)
                locked[newKey] = locked.pop(key)

    return increment

def draw_next_shape(piece, surface):
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Next Shape', 1, WHITE)

    sx = TOP_LEFT_X + PLAY_WIDTH + 50
    sy = TOP_LEFT_Y + PLAY_HEIGHT/2 - 100
    
    format = piece.shape[piece.rotation % len(piece.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, piece.color, (sx + j*BLOCK_SIZE, sy + i*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

    surface.blit(label, (sx + 10, sy - 30))

def draw_window(surface, grid, score=0):
    surface.fill(BLACK)

    pygame.font.init()
    font = pygame.font.SysFont('comicsans', 60)
    label = font.render('TETRIS', 1, (255, 255, 255))
    surface.blit(label, (TOP_LEFT_X + PLAY_WIDTH / 2 - (label.get_width() / 2), 10))

    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Score: ' + str(score), 1, WHITE)
    sx = TOP_LEFT_X - 200
    sy = TOP_LEFT_Y + 200
    surface.blit(label, (sx + 10, sy))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (TOP_LEFT_X + j * BLOCK_SIZE, TOP_LEFT_Y + i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

    pygame.draw.rect(surface, RED, (TOP_LEFT_X, TOP_LEFT_Y, PLAY_WIDTH, PLAY_HEIGHT), 5)

    draw_grid(surface, grid)

def main(win):
    last_score = 0
    try:
        with open('highscore.txt', 'r') as f:
            last_score = int(f.read())
    except:
        last_score = 0

    locked_positions = {}
    grid = create_grid(locked_positions)

    change_piece = False
    run = True
    current_piece = get_random_shape()
    next_piece = get_random_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.27
    level_time = 0
    score = 0

    while run:
        grid = create_grid(locked_positions)
        
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        clock.tick()

        if level_time/1000 > 5:
            level_time = 0
            if fall_speed > 0.12:
                fall_speed -= 0.005
        
        if fall_time/1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1
            
            if not (valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not (valid_space(current_piece, grid)):
                        current_piece.x += 1

                if event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not (valid_space(current_piece, grid)):
                        current_piece.x -= 1

                if event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not (valid_space(current_piece, grid)):
                        current_piece.y -= 1

                if event.key == pygame.K_UP:
                    current_piece.rotation += 1
                    if not (valid_space(current_piece, grid)):
                        current_piece.rotation -= 1

                if event.key == pygame.K_SPACE:
                    while valid_space(current_piece, grid):
                        current_piece.y += 1
                    current_piece.y -= 1
                    change_piece = True

        shape_pos = convert_shape_format(current_piece)
        
        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color

        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            
            current_piece = next_piece
            next_piece = get_random_shape()
            change_piece = False

            rows_cleared = clear_rows(grid, locked_positions)
            score += rows_cleared * 10

        draw_window(win, grid, score)
        draw_next_shape(next_piece, win)
        pygame.display.update()

        if check_lost(locked_positions):
            draw_text_middle(win, "GAME OVER", 80, RED)
            pygame.display.update()
            
            if score > last_score:
                last_score = score
                with open('highscore.txt', 'w') as f:
                    f.write(str(last_score))
            
            pygame.time.delay(2000)
            run = False

def main_menu(win):
    run = True
    while run:
        win.fill(BLACK)
        draw_text_middle(win, 'Press Any Key To Play', 60, WHITE)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main(win)

    pygame.quit()

if __name__ == '__main__':
    win = pygame.display.set_mode((S_WIDTH, S_HEIGHT))
    pygame.display.set_caption('Tetris')
    main_menu(win)