import pygame, sys, random
from pygame.math import Vector2

class SNAKE:
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(6, 10), Vector2(7, 10)]
        self.direction = Vector2(1, 0)
    
    def draw_snake(self):
        for block in self.body:
            snake_rect = pygame.Rect(block.x * cell_size, block.y * cell_size, cell_size, cell_size)
            if block == self.body[0]:
                pygame.draw.rect(screen, (220, 20, 60), snake_rect)
            elif block == self.body[len(self.body) - 1]:
                pygame.draw.rect(screen, (30, 144, 255), snake_rect)
            else:
                pygame.draw.rect(screen, (255, 255, 255), snake_rect)

    def move_snake(self):
        body_copy = self.body[:-1]
        body_copy.insert(0, body_copy[0] + self.direction)
        self.body = body_copy

    def add_block(self):
        self.body.insert(1, self.body[1] + self.direction)

class FRUIT:
    def __init__(self,):
        self.pos = Vector2(random.randint(0, cell_number -1), random.randint(0, cell_number -1))

    def draw_fruit(self):
        fruit_rect = pygame.Rect(self.pos.x * cell_size, self.pos.y * cell_size, cell_size, cell_size)
        pygame.draw.rect(screen, (126, 166, 114), fruit_rect)

    def respawn(self):
        self.pos = Vector2(random.randint(0, cell_number -1), random.randint(0, cell_number -1))

class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()

    def update(self):
        self.snake.move_snake()
        self.collision()

    def draw(self):
        self.snake.draw_snake()
        self.fruit.draw_fruit()

    def collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.respawn()
            self.snake.add_block()

pygame.init()
cell_size = 40
cell_number = 20
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
clock = pygame.time.Clock()
pygame.display.set_caption("Snakes")

game = MAIN()

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

while True:
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                game.snake.direction = (-1, 0)
            elif event.key == pygame.K_RIGHT:
                game.snake.direction = (1, 0)
            elif event.key == pygame.K_UP:
                game.snake.direction = (0, -1)
            elif event.key == pygame.K_DOWN:
                game.snake.direction = (0, 1)
        if event.type == SCREEN_UPDATE:
            game.update()

    screen.fill((42, 45, 51))
    game.draw()

    pygame.display.update()
    clock.tick(60)