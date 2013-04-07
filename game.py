import pygame
import sys
import random
import constants
import gridimage

def draw_at_grid(surface, grid, color):
    r = pygame.Rect(grid[0] * constants.IMAGE_SIZE,
                    grid[1] * constants.IMAGE_SIZE,
                    constants.IMAGE_SIZE,
                    constants.IMAGE_SIZE)

    pygame.draw.rect(surface,
                     color,
                     r)

def draw_squares(surface, squares):
    screen.fill(constants.BLACK)
    for col_num, col in enumerate(squares):
        for row_num, gi in enumerate(col):
            if gi == None:
                draw_at_grid(screen, (row_num, col_num),
                             constants.BLACK)
            else:
                draw_at_grid(screen, (row_num, col_num),
                             gi.color)
    pygame.display.flip()

def new_random_square(pos):
    return gridimage.GridImage(pos, constants.D_COLORS[random.randint(0,3)])

def init_squares():
    sqs = []
    for col in range(constants.IMAGES_WIDE):
        col_list = []
        for row in range(constants.IMAGES_HIGH):
            color = new_random_square((row, col))
            col_list.append(color)
        sqs.append(col_list)

    return sqs

def check_clicks(squares, pos):
    for col in squares:
        for square in col:
            if square is None:
                continue
            if square.check_click(pos):
                return square

def all_same(grids):
    prev = grids[0]
    for grid in grids:
        if grid.color != prev.color:
            return False
        prev = grid
    return True

def move(squares):
    new_cols = []
    for col_num, col in enumerate(squares):
        new_col = [x for x in col if x is not None]
        new_squares = [new_random_square((x, col_num)) for x in range(constants.IMAGES_HIGH - len(new_col))]

        new_cols.append(new_squares + new_col)
    squares[:] = new_cols

def update_positions(squares):
    for col_num, col in enumerate(squares):
        for row_num, square in enumerate(col):
            square.pos = row_num, col_num


pygame.init()
width = constants.IMAGE_SIZE * constants.IMAGES_WIDE
height = constants.IMAGE_SIZE * constants.IMAGES_HIGH
size = width, height

screen = pygame.display.set_mode(size)

screen.fill(constants.BLACK)

squares = init_squares()
clock = pygame.time.Clock()

selected_grids = []

while 1:
    clock.tick(60)
    draw_squares(screen, squares)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                selected_grids.append(check_clicks(squares, event.pos))
                if len(selected_grids) == 3:
                    if all_same(selected_grids):
                        for grid in selected_grids:
                            squares[grid.pos[1]][grid.pos[0]] = None
                    selected_grids = []
                    move(squares)
                    update_positions(squares)
            elif event.button == 3:
                selected_grids = []