import pygame
import random
from enum import Enum
from collections import namedtuple

pygame.init()
class Direction(Enum):
    RIGHT = '1'
    LEFT = '2'
    UP = '3'
    DOWN = '4'

font = pygame.font.SysFont('arail', 30)

#named tuple is a lightweight class to be able to use Point.x or Point.y
Point = namedtuple('Point', 'x, y')

WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0, 0, 0)


BLOCK_SIZE = 20
GAME_SPEED = 40
class SnakeGame:
    def __init__(self, width = 680, height = 680):
        self.width = width
        self.height = height

        #init display
        self.display = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Snake")
        self.clock = pygame.time.Clock()

        #init direction
        self.direction = Direction.RIGHT

        #create head of snake in middle of screen
        self.head = Point(self.width/2, self.height/2)
        #original snake 3 long on x axis
        self.snake = [self.head,
                      Point(self.head.x - BLOCK_SIZE, self.head.y),
                      Point(self.head.x - (2* BLOCK_SIZE), self.head.y)]

        self.score = 0
        self.food = None
        self._place_food()

    def _place_food(self):
        posX = random.randint(0, (self.width // BLOCK_SIZE) - 1) * BLOCK_SIZE  # gets a random number from 0 to the SCREEN_SIZE that is a multiple of SIZE_BLOCK
        posY = random.randint(0, (self.height // BLOCK_SIZE) - 1) * BLOCK_SIZE  # gets a random number from 0 to the SCREEN_SIZE that is a multiple of SIZE_BLOCK
        self.food = Point(posX, posY)
        if self.food in self.snake:
            self._place_food()


    def play_step(self):
        #1 collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT:
                    self.direction = Direction.RIGHT
                elif event.key == pygame.K_UP:
                    self.direction = Direction.UP
                elif event.key == pygame.K_DOWN:
                    self.direction = Direction.DOWN

        #2 move
        self._move(self.direction)
        self.snake.insert(0, self.head)

        #3 check if game over
        game_over = False
        if self._is_collision():
            game_over = True
            return game_over, self.score


        #4 place new food or just move
        if self.head == self.food:
            self.score += 1
            self._place_food()
        else:
            self.snake.pop()


        #5 update ui and clock
        self._update_ui()
        self.clock.tick(GAME_SPEED)

        #6 return game over and score
        game_over = False

        return game_over, self.score

    def _update_ui(self):
        self.display.fill(BLACK)

        for block in self.snake:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(block.x, block.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(block.x + 4, block.y + 4, 12, 12))

        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))

        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0,0]) # put in upper left
        pygame.display.flip()


    def _move(self, direction):
        x = self.head.x
        y = self.head.y
        if direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif direction == Direction.UP:
            y -= BLOCK_SIZE
        elif direction == Direction.DOWN:
            y += BLOCK_SIZE

        self.head = Point(x,y)


    def _is_collision(self):
        if self.head.x > self.width - BLOCK_SIZE or self.head.x < 0 or self.head.y > self.height - BLOCK_SIZE or self.head.y < 0:
                return True
        if self.head in self.snake[1:]:
                return True
        return False





if __name__ == "__main__":
    game = SnakeGame(1000, 1000)

    #game loop
    while True:
        game_over, score = game.play_step()

        if game_over:
            break

    print('Final Score ', score)



    pygame.quit()