import pygame
from pygame.locals import *
import time
import random

SIZE_BLOCK = 40
SCREEN_SIZE_Y = 920
SCREEN_SIZE_X = 1200
class Apple:
    def __init__(self, parentSurface):
        self.apple = pygame.image.load("Pictures/snakeBlock.png").convert()
        self.parentSurface = parentSurface
        self.posX = SIZE_BLOCK*3
        self.posY = SIZE_BLOCK*3

    def drawApple(self):
        self.parentSurface.blit(self.apple, (self.posX, self.posY))
        pygame.display.update()

    def moveApple(self):
        self.posX = random.randint(0, (SCREEN_SIZE_X//SIZE_BLOCK) - 1) * SIZE_BLOCK  #gets a random number from 0 to the SCREEN_SIZE that is a multiple of SIZE_BLOCK
        self.posY = random.randint(0, (SCREEN_SIZE_Y//SIZE_BLOCK) - 1) * SIZE_BLOCK  #gets a random number from 0 to the SCREEN_SIZE that is a multiple of SIZE_BLOCK

class Snake:
    def __init__(self, parentSurface, length):
        self.parentSurface = parentSurface #takes in the surface from Game
        self.length = length
        # create block
        self.snakeBlock = pygame.image.load("Pictures/snakeBlock3.png").convert()
        # draw snake block onto background
        self.posX = [SIZE_BLOCK]*length
        self.posY = [SIZE_BLOCK]*length
        self.moveSize = 40

        self.direction = 'Down'

    def drawSnake(self):
        # remove prev block
        self.parentSurface.fill((110, 100, 100))
        # draw snake blocks onto background
        for i in range(self.length):
            self.parentSurface.blit(self.snakeBlock, (self.posX[i], self.posY[i]))

    def moveRight(self):
        #self.posX += self.sizeBlock
        self.drawSnake()
        self.direction = 'Right'

    def moveLeft(self):
        #self.posX -= self.sizeBlock
        self.drawSnake()
        self.direction = 'Left'

    def moveUp(self):
        #self.posY -= self.sizeBlock
        self.drawSnake()
        self.direction = 'Up'

    def moveDown(self):
        #self.posY += self.sizeBlock
        self.drawSnake()
        self.direction = 'Down'

    def walk(self):
        #for loop in reverse and changing the position of the prev block to the block ahead of it
        for i in range(self.length-1, 0, -1):
            self.posX[i] = self.posX[i-1]
            self.posY[i] = self.posY[i-1]

        if (self.direction == 'Down'):
            self.posY[0] += self.moveSize
        elif (self.direction == 'Up'):
            self.posY[0] -= self.moveSize
        elif (self.direction == 'Right'):
            self.posX[0] += self.moveSize
        elif (self.direction == 'Left'):
            self.posX[0] -= self.moveSize
        self.drawSnake()


    def increaseSize(self):
        self.length += 1
        self.posX.append(-1)
        self.posY.append(-1)






class Game:
    def __init__(self): #constructor
        pygame.init()

        # create background
        self.surface = pygame.display.set_mode((SCREEN_SIZE_X, SCREEN_SIZE_Y))
        self.surface.fill((110, 100, 100))

        #create new snake object and draw it
        self.snake = Snake(self.surface, 1)
        self.snake.drawSnake()

        #create new apple object
        self.apple = Apple(self.surface)
        self.apple.drawApple()

    def play(self):
        self.snake.walk()
        self.apple.drawApple()
        self.displayScore()
        #if snake collide with apple
        if self.checkAppleCollision(self.apple.posX, self.apple.posY, self.snake.posX[0], self.snake.posY[0]):
            self.snake.increaseSize()
            self.apple.moveApple()

        #if snake collide with itself
        if self.checkSnakeCollision(self.snake.posX, self.snake.posY):
            raise "Game Over"



    def displayScore(self):
        font = pygame.font.SysFont('arial', 25) #27:10
        score = font.render(f"Score: {self.snake.length}", True, (200,200,200))
        self.surface.blit(score, (SCREEN_SIZE_X-100,10))
        pygame.display.update()





    def checkAppleCollision(self, applePosX, applePosY, snakePosX, snakePosY):
        if (applePosY == snakePosY and applePosX == snakePosX):
            return True
        return False

    def checkSnakeCollision(self, snakePosX, snakePosY):
        for i in range (1, self.snake.length):
            if (snakePosX[0] == snakePosX[i] and snakePosY[0] == snakePosY[i]):
                return True
        return False

    def gameOverScreen(self):
        font = pygame.font.SysFont('arail', 30)
        self.surface.fill((110,110,5))
        message1 = font.render(f"Game Over! Score: {self.snake.length}", True, (255,255,255))
        self.surface.blit(message1, ( int((SCREEN_SIZE_X/4)), int((SCREEN_SIZE_Y/4))))
        message2 = font.render(f"Press Enter to play again! Press Escape to exit!", True, (255,255,255))
        self.surface.blit(message2, ( int((SCREEN_SIZE_X/4)), ( int((SCREEN_SIZE_Y/4)) + 50 )))

        pygame.display.update()

    def reset(self):
        # recreate new snake object and draw it
        self.snake = Snake(self.surface, 7)
        # recreate new apple object
        self.apple = Apple(self.surface)

    def run(self):
        running = True
        gameOver = False
        while (running):
            for event in pygame.event.get():

                if (event.type == KEYDOWN): #if a key is pressed
                    if (event.key == K_ESCAPE): #stop playing
                        running = False
                    if (event.key == K_RIGHT): #move right
                        self.snake.moveRight()
                    if (event.key == K_LEFT): #move left
                        self.snake.moveLeft()
                    if (event.key == K_DOWN): #move right
                        self.snake.moveDown()
                    if (event.key == K_UP): #move right
                        self.snake.moveUp()

                    if (event.key == K_RETURN):
                        gameOver = False
                elif (event.type == QUIT):
                    running = False
            try:
                if not gameOver:
                    self.play()
            except Exception as e:
                gameOver = True
                self.gameOverScreen()
                self.reset()

            time.sleep(0.3)

if __name__ == "__main__":
    #while(True):
        #random.randint(0, (SCREEN_SIZE_X/SIZE_BLOCK) - 1) * SIZE_BLOCK  #gets a random number from 0 to the SCREEN_SIZE that is a multiple of 40
        #time.sleep(0.2)
    gameInstance = Game()
    gameInstance.run()







