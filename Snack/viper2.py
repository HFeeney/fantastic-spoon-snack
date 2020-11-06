import pygame as pg
import os
import random

pg.init()
random.seed()

FPS = 30
WHITE = (255, 255, 255)
COLOR = (235, 242, 230)
DIR = os.path.join(__file__, '..')
SNAKE_HEAD = pg.image.load(os.path.join(DIR, "Head.png"))
SNAKE_HEAD = pg.transform.scale(SNAKE_HEAD, (50, 50))
SNAKE_HEAD.set_colorkey(WHITE)
SNAKE_BODY = pg.image.load(os.path.join(DIR, "Body.png"))
SNAKE_BODY.set_colorkey(WHITE)
APPLE = pg.image.load(os.path.join(DIR, "apple.png"))
APPLE.set_colorkey(WHITE)
WIDTH = 900
HEIGHT = 700
TILE_WIDTH = 50
TILES_WIDE = int(WIDTH / TILE_WIDTH)
TILES_HIGH = int(HEIGHT / TILE_WIDTH)


class Snake:
    def __init__(self, xTile, yTile, length, speed):
        self.positions = []
        for i in range(length):
            self.positions.append([xTile, yTile - i])
        self.directions = [0]*length
        self.length = len(self.positions)
        self.alive = True
        self.direction = 0
        self.directionChangeCooldown = False
        self.speed = speed
        self.frames = 0
        self.ateApple = False
    
    def update(self):
        self.frames += 1
        if (self.frames % self.speed == 0):
            # set newPosition equal to head position + 1 in direction of movement
            if (self.direction == 0):
                newPosition = [self.positions[0][0], self.positions[0][1] + 1]
            elif (self.direction == 1):
                newPosition = [self.positions[0][0] + 1, self.positions[0][1]]
            elif (self.direction == 2):
                newPosition = [self.positions[0][0], self.positions[0][1] - 1]
            elif (self.direction == 3):
                newPosition = [self.positions[0][0] - 1, self.positions[0][1]]

            # if the new head will collide with rest of snake, die
            for i in self.positions[2:len(self.positions) - 1]:
                if (newPosition == i):
                    self.alive = False
            
            # if the new head will go outside of screen, die
            if (newPosition[0] == -1 or newPosition[0] == TILES_WIDE or newPosition[1] == -1 or newPosition[1] == TILES_HIGH):
                self.alive = False
            
            if (self.alive):
                # don't get rid of tail if you ate an apple
                if not self.ateApple:
                    self.directions.pop()
                    self.positions.pop()
                self.directions.insert(0, self.direction)
                self.positions.insert(0, newPosition)

            # update length of snake
            self.length = len(self.positions)
            
            # we can change direction again
            self.directionChangeCooldown = False

            self.ateApple = False
        
        if not self.directionChangeCooldown:
            self.updateDirection()
    
    def updateDirection(self):
        # get directional key input then change snake direction accordingly
        keys = pg.key.get_pressed()
        beforeDirection = self.direction
        if (keys[pg.K_DOWN] and self.direction != 2):
            self.direction = 0
        elif (keys[pg.K_RIGHT] and self.direction != 3):
            self.direction = 1
        elif (keys[pg.K_UP] and self.direction != 0):
            self.direction = 2
        elif (keys[pg.K_LEFT] and self.direction != 1):
            self.direction = 3
        if (beforeDirection != self.direction):
            self.directionChangeCooldown = True

    def draw(self, surface):
        for i in range(len(self.positions)):
            j = (len(self.positions) - 1) - i
            img = SNAKE_BODY
            increment = TILE_WIDTH / self.speed
            frame = self.frames % self.speed 
            addedPos = frame * increment - TILE_WIDTH
            if (j == 0):
                img = SNAKE_HEAD
            img = pg.transform.rotate(img, self.directions[j] * 90 + 180)
            if (self.directions[j] == 0):
                surface.blit(img, (self.positions[j][0] * TILE_WIDTH, self.positions[j][1] * TILE_WIDTH + addedPos))
            elif (self.directions[j] == 1):
                surface.blit(img, (self.positions[j][0] * TILE_WIDTH + addedPos, self.positions[j][1] * TILE_WIDTH))
            elif (self.directions[j] == 2):
                surface.blit(img, (self.positions[j][0] * TILE_WIDTH, self.positions[j][1] * TILE_WIDTH - addedPos))
            elif (self.directions[j] == 3):
                surface.blit(img, (self.positions[j][0] * TILE_WIDTH - addedPos, self.positions[j][1] * TILE_WIDTH))

class Apple:
    def __init__(self, snake):
        rX = random.randint(0, TILES_WIDE - 1)
        rY = random.randint(0, TILES_HIGH - 1)
        while self.isInSnake(rX, rY, snake.positions):
            rX = random.randint(0, TILES_WIDE - 1)
            rY = random.randint(0, TILES_HIGH - 1)
        self.xTile = rX
        self.yTile = rY

    def isInSnake(self, xTile, yTile, snakePositions):
        for position in snakePositions:
            if (position == [xTile, yTile]):
                return True
        return False
    
    def draw(self, surface):
        surface.blit(APPLE, (self.xTile * TILE_WIDTH, self.yTile * TILE_WIDTH))

class Game:
    def __init__(self):
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pg.time.Clock()
        self.running = True
        
    def new(self):
        self.snake = Snake(5, 5, 4, 7)
        self.apple = Apple(self.snake)
        self.run()

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        self.snake.update()
        if (self.snake.positions[0] == [self.apple.xTile, self.apple.yTile]):
            self.snake.ateApple = True
            self.apple = Apple(self.snake)
        if not self.snake.alive:
            self.playing = False
            
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

    def draw(self):
        # draw background
        self.screen.fill(COLOR)
        self.snake.draw(self.screen)
        self.apple.draw(self.screen)
        pg.display.flip()

g = Game()
while g.running:
    g.new()
pg.quit()