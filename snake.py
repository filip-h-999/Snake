import random
import sys
from enum import Enum
import pygame
from pygame import draw, display, font, mixer, image

BLACK = ("#000000")
WHITE = ("#c8c8c8")
RED = ("#ff0000")
BLUE = ("#273546")
GREEN = ("#08d445")
Dark1 = ("#263445")
Dark2 = ("#1f2836")
colorSnake = ("#21d6db")
GOLD = ("#fceb55")
ORANGE = ("#f79503")

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
highscore = int

with open("highscore.txt", "r") as file:
    highscore = int(file.read())

body = [(snake_position_x, snake_position_y),
        (snake_position_x, snake_position_y + 1)]

running = True
isAlive = True
isPaused = False
gameStarted = False

start_screen = pygame.transform.scale(image.load(r"resources\img\titleScreen.jpg"), (WINDOW_WIDTH, WINDOW_HEIGHT))


class MoveSounds:
    def playMoveUpSound():
        moveUp = r"resources\sound\moveU.wav"
        mixer.music.load(moveUp)
        pygame.mixer.Channel(4).play(pygame.mixer.Sound(moveUp))
        pygame.mixer.Channel(4).set_volume(0.2)

        if not isAlive or isPaused or not gameStarted:
            pygame.mixer.Channel(4).stop()

    def playMoveDownSound():
        moveDown = r"resources\sound\moveD.wav"
        mixer.music.load(moveDown)
        pygame.mixer.Channel(5).play(pygame.mixer.Sound(moveDown))
        pygame.mixer.Channel(5).set_volume(0.2)

        if not isAlive or isPaused or not gameStarted:
            pygame.mixer.Channel(5).stop()

    def playMoveLeftSound():
        moveLeft = r"resources\sound\moveL.wav"
        mixer.music.load(moveLeft)
        pygame.mixer.Channel(6).play(pygame.mixer.Sound(moveLeft))
        pygame.mixer.Channel(6).set_volume(0.2)
        
        if not isAlive or isPaused or not gameStarted:
            pygame.mixer.Channel(6).stop()

    def playMoveRightSound():
        moveRight = r"resources\sound\moveR.wav"
        mixer.music.load(moveRight)
        pygame.mixer.Channel(7).play(pygame.mixer.Sound(moveRight))
        pygame.mixer.Channel(7).set_volume(0.2)

        if not isAlive or isPaused or not gameStarted:
            pygame.mixer.Channel(7).stop()


def playEat():
    eat = r"resources\sound\apple.mp3"
    mixer.music.load(eat)
    mixer.music.play()


def playDead():
    dead = r"resources\sound\dead.mp3"
    pygame.mixer.Channel(0).play(pygame.mixer.Sound(dead), maxtime=3000)


def playGameOver():
    gameOver = r"resources\sound\game Over.mp3"
    pygame.mixer.Channel(1).play(pygame.mixer.Sound(gameOver), maxtime=3000)


def palyStartSound():
    play = r"resources\sound\startSound.wav"
    mixer.music.load(play)
    mixer.music.play()
    mixer.music.set_volume(0.5)


def playButtonSound():
    move = r"resources\sound\button.wav"
    mixer.music.load(move)
    pygame.mixer.Channel(2).play(pygame.mixer.Sound(move), maxtime=800)
    pygame.mixer.Channel(2).set_volume(0.2)


def playHighscoreSound():
    highscore = r""
    mixer.music.load(highscore)
    pygame.mixer.Channel(3).play(pygame.mixer.Sound(highscore))

# todo new highscore sound


class Direction(Enum):
    up = 1
    down = 2
    left = 3
    right = 4


direction = Direction.up


def main():
    global window, food_position_x, food_position_y, running, isAlive, direction, isPaused, highscore, gameStarted
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
                    MoveSounds.playMoveUpSound()
                elif event.key == pygame.K_DOWN:
                    direction = Direction.down
                    MoveSounds.playMoveDownSound()
                elif event.key == pygame.K_LEFT:
                    direction = Direction.left
                    MoveSounds.playMoveLeftSound()
                elif event.key == pygame.K_RIGHT:
                    direction = Direction.right
                    MoveSounds.playMoveRightSound()
                if event.key == pygame.K_c:
                    isAlive = True
                    playButtonSound()
                    reset()
                    gameStarted = True
                elif event.key == pygame.K_n:
                    running = False
                if event.key == pygame.K_p:
                    isPaused = not isPaused

        if not gameStarted:
            window.blit(start_screen, (0, 0))

        if not isPaused and gameStarted:
            moveSnake(direction)
            body.insert(0, (snake_position_x, snake_position_y))

        if isAlive and (snake_position_x == 17 or
                        snake_position_x == -1 or
                        snake_position_y == 17 or
                        snake_position_y == -1 or
                        collision()):
            isAlive = False
            playDead()
            playGameOver()
            gameOverScreen()

        if isAlive and not isPaused and gameStarted:
            window.fill(BLUE)
            drawScore()
            drawGameBorder()
            drawGrid()
            drawFood(food_position_x, food_position_y)
            drawSnake()
            changeScore()
            if highscore < score:
                highscore += 1
                with open("highscore.txt", "w") as file:
                    file.write(str(highscore))
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
    apple = pygame.image.load(r"resources\img\apple.gif")
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


def drawSnake():
    snakeHead = body[0]
    for segment in body:
        color = GOLD if snakeHead == segment else colorSnake
        drawCell(segment[0], segment[1], color)


def collision():
    snakeHead = body[0]
    snakeBody = body[1:]
    if snakeHead in snakeBody:
        return True


def drawCell(x, y, color):
    rect = pygame.Rect(border_left + x * blockSize, border_top + y * blockSize, blockSize, blockSize)
    draw.rect(window, color, rect, 0)


def drawScore():
    font2 = font.SysFont('didot.ttc', 50)
    highScoreText = font2.render("High Score: %d" % highscore, True, ORANGE)
    window.blit(highScoreText, (375, 75))
    # fist x second y


def changeScore():
    global score
    if food_position_x == snake_position_x and food_position_y == snake_position_y:
        score += 1
    font1 = font.SysFont('didot.ttc', 50)
    scoreText = font1.render("Score: %d" % score, True, GREEN)
    window.blit(scoreText, (140, 75))
    # fist x second y


def eatFood():
    global food_position_y, food_position_x
    if food_position_x == snake_position_x and food_position_y == snake_position_y:
        checkFood()
        playEat()
        return True


def checkFood():
    global food_position_y, food_position_x
    while True:
        food_position_x = random.randint(0, rows - 1)
        food_position_y = random.randint(0, rows - 1)
        if not (food_position_x, food_position_y) in body:
            break


def reset():
    global snake_position_x, snake_position_y, score, food_position_x, food_position_y, direction, body, isPaused
    snake_position_x = int(rows / 2)
    snake_position_y = int(columns / 2)
    food_position_x = random.randint(0, rows - 1)
    food_position_y = random.randint(0, rows - 1)
    body = [(snake_position_x, snake_position_y),
            (snake_position_x, snake_position_y + 1)]
    score = 0
    isPaused = False
    direction = Direction.up


def gameOverScreen():
    window.fill(BLACK)
    image = pygame.image.load(r'resources\img\BackGO.jpg')
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
