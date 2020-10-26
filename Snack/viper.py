import pygame as pg
import random

pg.init()
random.seed()

FPS = 30
WHITE = (255, 255, 255)
COLOR = (235, 242, 230)
TILE_WIDTH = 50
SNAKE_HEAD = pg.image.load("D:\Robotics\FRC\Code\Python\Snack\Head.png")
SNAKE_HEAD = pg.transform.scale(SNAKE_HEAD, (50, 50))
SNAKE_HEAD.set_colorkey(WHITE)
SNAKE_BODY = pg.image.load("D:\Robotics\FRC\Code\Python\Snack\Body.png")
SNAKE_BODY.set_colorkey(WHITE)
APPLE = pg.image.load("D:\Robotics\FRC\Code\Python\Snack/apple.png")
APPLE.set_colorkey(WHITE)
WIDTH = 500
HEIGHT = 500

class Apple:
    def __init__(self, snake):
        x = random.randrange(0, 10)
        y = random.randrange(0, 10)
        while self.inSnake(x, y, snake): 
            x = random.randrange(0, 10)
            y = random.randrange(0, 10)

        self.position = [x, y]

    def inSnake(self, x, y, snake):
        for position in snake.positions:
            if x == position[0] and y == position[1]:
                return True
        return False

    def draw(self, surface):
        surface.blit(APPLE, (self.position[0] * TILE_WIDTH, self.position[1] * TILE_WIDTH))

class Snake:
    def __init__(self):
        self.direction = 0
        self.positions = [[0, 1], [0, 0]]
        self.frames = 0
        self.canChangeDirection = True
        self.alive = True
        self.ateApple = False

    def update(self):
        self.frames += 1

        if self.canChangeDirection:
            keys = pg.key.get_pressed()
            if (keys[pg.K_DOWN] and self.direction != 2):
                self.direction = 0
            if (keys[pg.K_RIGHT] and self.direction != 3):
                self.direction = 1
            if (keys[pg.K_UP] and self.direction != 0):
                self.direction = 2
            if (keys[pg.K_LEFT] and self.direction != 1):
                self.direction = 3
            self.canChangeDirection = False
        

        if (self.frames % 10 == 0):
            if (self.direction == 0):
                newPosition = [self.positions[0][0], self.positions[0][1] + 1]
            elif (self.direction == 1):
                newPosition = [self.positions[0][0] + 1, self.positions[0][1]]
            elif (self.direction == 2):
                newPosition = [self.positions[0][0], self.positions[0][1] - 1]
            elif (self.direction == 3):
                newPosition = [self.positions[0][0] - 1, self.positions[0][1]]

            if (self.positions[0][0] == -1 or self.positions[0][0] == 10 or self.positions[0][1] == -1 or self.positions[0][1] == 10):
                self.alive = False
            
            if not self.ateApple:
                self.positions.pop()
            self.positions.insert(0, newPosition)

            self.canChangeDirection = True
            self.ateApple = False        

    def draw(self, surface):
        for i in range(len(self.positions)):
            img = SNAKE_BODY
            if (i == 0):
                img = SNAKE_HEAD
                img = pg.transform.rotate(img, 90 * self.direction)
            surface.blit(img, (self.positions[i][0] * TILE_WIDTH, self.positions[i][1] * TILE_WIDTH))

class Game:
    def __init__(self):
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.screen.fill(COLOR)
        self.clock = pg.time.Clock()
        self.running = True
        
    def new(self):
        self.snake = Snake()
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
        if not self.snake.alive:
            self.playing = False
        if self.apple.position == self.snake.positions[0]:
            self.snake.ateApple = True
            self.apple = Apple(self.snake)
            
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

    def draw(self):
        self.screen.fill(COLOR)
        self.snake.draw(self.screen)
        self.apple.draw(self.screen)
        pg.display.flip()

g = Game()
while g.running:
    g.new()
pg.quit()