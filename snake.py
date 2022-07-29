import random
import sys
from enum import Enum
import pygame
from pygame import draw, display, font, mixer

BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
RED = (255, 0, 0)
BLUE = (39, 53, 70)
GREEN = (8, 212, 69)
Dark1 = (38, 52, 69)
Dark2 = (31, 40, 54)
colorSnake = (33, 214, 219)
GOLD = (252, 235, 85)

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

speed = 7
snake_position_x = int(rows / 2)
snake_position_y = int(columns / 2)
food_position_x = random.randint(0, rows - 1)
food_position_y = random.randint(0, rows - 1)

mixer.init()
clock = pygame.time.Clock()
score = 0

body = [(snake_position_x, snake_position_y),
        (snake_position_x, snake_position_y + 1)]

running = True
isAlive = True
isPaused = False


def playEat():
    eat = r"C:\Users\filip\Downloads\apple.mp3"
    mixer.music.load(eat)
    mixer.music.play()


def playDead():
    dead = r"C:\Users\filip\Downloads\dead.mp3"
    pygame.mixer.Channel(0).play(pygame.mixer.Sound(dead), maxtime=3000)


def playGameOver():
    gameOver = r"C:\Users\filip\Downloads\game Over.mp3"
    pygame.mixer.Channel(1).play(pygame.mixer.Sound(gameOver), maxtime=3000)


class Direction(Enum):
    up = 1
    down = 2
    left = 3
    right = 4


direction = Direction.up


def main():
    global window, food_position_x, food_position_y, running, isAlive, direction, isPaused
    pygame.init()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Snake")

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
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
                if event.key == pygame.K_c:
                    isAlive = True
                    reset()
                elif event.key == pygame.K_n:
                    running = False
                if event.key == pygame.K_p:
                    isPaused = not isPaused

        if not isPaused:
            moveSnake(direction)
            body.insert(0, (snake_position_x, snake_position_y))

        if isAlive and (snake_position_x == 17 or snake_position_x == -1 or
                        snake_position_y == 17 or snake_position_y == -1):
            isAlive = False
            playDead()
            playGameOver()
            gameOverScreen()

        if isAlive:
            window.fill(BLUE)
            drawScore()
            drawGameBorder()
            drawGrid()
            drawFood(food_position_x, food_position_y)
            drawBody(body)
            changeScore()
            if not eatFood():
                body.pop()

        display.update()
        clock.tick(speed)


def drawGrid():
    cellCont = 0
    for x in range(0, columns):
        for y in range(0, rows):
            color = Dark1 if cellCont % 2 else Dark2
            drawCell(x, y, color)
            cellCont += 1


def drawFood(x, y):
    apple = pygame.image.load(r"C:\Users\filip\Downloads\tumblr_mrcf12B0fE1rfjowdo1_500.gif")
    window.blit(pygame.transform.scale(apple, (30, 30)), ([border_left + x * blockSize + 1,
                                                           border_top + y * blockSize + 1]))


def drawGameBorder():
    draw.rect(window, WHITE, pygame.Rect(border_left - 5, border_top - 5,
                                         rows * blockSize + 10, columns * blockSize + 10), 3)


# 1/2 are the left and top and 3/4 are the columns


def moveSnake(dire):
    global snake_position_y, snake_position_x
    if dire == Direction.up:
        snake_position_y -= 1
    elif dire == Direction.down:
        snake_position_y += 1
    elif dire == Direction.left:
        snake_position_x -= 1
    elif dire == Direction.right:
        snake_position_x += 1


def drawBody(body):
    for segment in body:
        drawCell(segment[0], segment[1], colorSnake)


def drawCell(x, y, color):
    rect = pygame.Rect(border_left + x * blockSize, border_top + y * blockSize, blockSize, blockSize)
    draw.rect(window, color, rect, 0)


def drawScore():
    font2 = font.SysFont('didot.ttc', 30)
    highScoreText = font2.render("High Score: ", True, GREEN)
    window.blit(highScoreText, (390, 90))
    # fist x second y


def eatFood():
    global food_position_y, food_position_x
    if food_position_x == snake_position_x and food_position_y == snake_position_y:
        food_position_x = random.randint(0, rows - 1)
        food_position_y = random.randint(0, rows - 1)
        playEat()
        return True


def changeScore():
    global score
    if food_position_x == snake_position_x and food_position_y == snake_position_y:
        score += 1
    font1 = font.SysFont('didot.ttc', 30)
    scoreText = font1.render("Score: %d" % score, True, GREEN)
    window.blit(scoreText, (230, 90))
    # fist x second y


def reset():
    global snake_position_x, snake_position_y, score, food_position_x, food_position_y, direction
    snake_position_x = int(rows / 2)
    snake_position_y = int(columns / 2)
    food_position_x = random.randint(0, rows - 1)
    food_position_y = random.randint(0, rows - 1)
    score = 0
    direction = Direction.up


def gameOverScreen():
    window.fill(BLACK)
    image = pygame.image.load(r'C:\Users\filip\Downloads\BackGO.jpg')
    window.blit(pygame.transform.scale(image, (WINDOW_WIDTH, 465)), (0, 0))
    font4 = font.SysFont('didot.ttc', 35)
    playAgain = font4.render("To play again press: c", True, GREEN)
    window.blit(playAgain, (250, 480))
    font5 = font.SysFont('didot.ttc', 35)
    quitGame = font5.render("To end the Game press: n", True, RED)
    window.blit(quitGame, (230, 530))
    fontEndScore = font.SysFont('didot.ttc', 50)
    endScore = fontEndScore.render("Score: %d" % score, True, GOLD)
    window.blit(endScore, (310, 580))


main()
