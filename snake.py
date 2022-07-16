import random
import sys
from enum import Enum
import pygame
from pygame import draw, display, font


BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
RED = (255, 0, 0)
BLUE = (39, 53, 70)
GREEN = (8, 212, 69)
Dark1 = (38, 52, 69)
Dark2 = (31, 40, 54)
colorSnake = (33, 214, 219)

blockSize = 30
rows = 17
columns = 17
border_top = 120
border_bottom = 50
border_left = 120
border_right = 120
WINDOW_HEIGHT = rows * blockSize + (border_bottom + border_top)
WINDOW_WIDTH = columns * blockSize + (border_left + border_right)
window: pygame.Surface

snake_position_x = int(rows/2)
snake_position_y = int(columns/2)
food_position_x = random.randint(0, rows - 1)
food_position_y = random.randint(0, rows - 1)

clock = pygame.time.Clock()
speed = 7


class Direction(Enum):
    up = 1
    down = 2
    left = 3
    right = 4


def main():
    global window, food_position_x, food_position_y
    direction = Direction.up
    pygame.init()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Snake")
    window.fill(BLUE)
    drawScore()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    direction = Direction.up
                elif event.key == pygame.K_DOWN:
                    direction = Direction.down
                elif event.key == pygame.K_LEFT:
                    direction = Direction.left
                elif event.key == pygame.K_RIGHT:
                    direction = Direction.right

        drawGameBorder()
        drawGrid()
        drawFood(food_position_x, food_position_y)
        moveSnake(direction)
        snake()
        display.update()

        if food_position_x == snake_position_x and food_position_y == snake_position_y:
            food_position_x = random.randint(0, rows - 1)
            food_position_y = random.randint(0, rows - 1)

        clock.tick(speed)


def drawGrid():
    cellCont = 0
    for x in range(0, columns):
        for y in range(0, rows):
            color = Dark1 if cellCont % 2 else Dark2
            drawCell(x, y, color)
            cellCont += 1


def drawFood(x, y):
    draw.circle(window, RED, [border_left + x * blockSize + blockSize / 2,
                              border_top + y * blockSize + blockSize / 2], 12, 0)
# 1/2 Int are the position / 3. ist the size and 4. filling


def drawGameBorder():
    draw.rect(window, WHITE, pygame.Rect(border_left - 5, border_top - 5,
                                         rows * blockSize + 10, columns * blockSize + 10), 3)
# 1/2 are the left and top and 3/4 are the columns


def moveSnake(direction):
    global snake_position_y
    global snake_position_x
    if direction == Direction.up:
        snake_position_y -= 1
    elif direction == Direction.down:
        snake_position_y += 1
    elif direction == Direction.left:
        snake_position_x -= 1
    elif direction == Direction.right:
        snake_position_x += 1


def snake():
    drawCell(snake_position_x, snake_position_y, colorSnake)


def drawCell(x, y, color):
    rect = pygame.Rect(border_left + x * blockSize, border_top + y * blockSize, blockSize, blockSize)
    draw.rect(window, color, rect, 0)


def drawScore():
    font1 = font.SysFont('Arial.ttf', 30)
    scoreText = font1.render("Score: 0", True, GREEN)
    font2 = font.SysFont('didot.ttc', 30)
    highScoreText = font2.render("High Score: 0", True, GREEN)
    window.blit(scoreText, (230, 90))
    window.blit(highScoreText, (390, 90))
    # fist x second y


main()
