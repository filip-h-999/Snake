import random
import sys
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
rows = 15
columns = 15
border_top = 120
border_bottom = 50
border_left = 120
border_right = 120
WINDOW_HEIGHT = rows * blockSize + (border_bottom + border_top)
WINDOW_WIDTH = columns * blockSize + (border_left + border_right)
window: pygame.Surface


def main():
    global window
    pygame.init()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Snake")
    window.fill(BLUE)
    x = random.randint(0, rows - 1)
    y = random.randint(0, columns - 1)
    drawScore()

    while True:
        drawGameBorder()
        drawGrid()
        drawFood(x, y)
        snake(int(rows/2), int(columns/2))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        display.update()


def drawGrid():
    cellCont = 0
    for x in range(0, rows):
        for y in range(0, columns):
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


def snake(x, y):
    drawCell(x, y, colorSnake)


def drawCell(x, y, color):
    rect = pygame.Rect(border_left + x * blockSize, border_top + y * blockSize, blockSize, blockSize)
    draw.rect(window, color, rect, 0)


def drawScore():
    font1 = font.SysFont('Arial.ttf', 30)
    scoreText = font1.render("Score: 10", True, GREEN)
    font2 = font.SysFont('didot.ttc', 30)
    highScoreText = font2.render("High Score: 10", True, GREEN)
    window.blit(scoreText, (200, 90))
    window.blit(highScoreText, (360, 90))
    # fist x second y


main()
