import pygame, sys, random
from pygame.math import Vector2

red = (220, 20, 60)
blue = (30, 144, 255)

cell_size = 35
cell_number = 25

class SNAKE:
    def __init__(self):
        self.body = [Vector2(10, 10), Vector2(9, 10), Vector2(8, 10)]
        self.direction = Vector2(1, 0)
        self.blue = False
    
    def draw_snake(self):
        for block in self.body:
            snake_rect = pygame.Rect(block.x * cell_size, block.y * cell_size, cell_size, cell_size)
            color = (255, 255, 255)
            if block == self.body[0]:
                if not self.blue:
                    color = red
                else:
                    color = blue
            elif block == self.body[len(self.body) - 1]:
                if not self.blue:
                    color = blue
                else:      
                    color = red
            else:
                color = (255, 255, 255)

            pygame.draw.rect(screen, color, snake_rect)

    def move_snake(self):
        body_copy = self.body[:-1]
        body_copy.insert(0, body_copy[0] + self.direction)
        self.body = body_copy

    def add_block(self):
        self.body.insert(1, self.body[1] + self.direction)

    def subtract_block(self):
        self.body = self.body[:-1]

    def switch_head(self):
        self.body.reverse()
        self.blue = not self.blue
        self.direction *= -1
          
class RED_FRUIT:
    def __init__(self,):
        self.pos = Vector2(random.randint(0, cell_number -1), random.randint(0, cell_number -1))

    def draw_fruit(self):
        fruit_rect = pygame.Rect(self.pos.x * cell_size, self.pos.y * cell_size, cell_size, cell_size)
        pygame.draw.rect(screen, red, fruit_rect)

    def respawn(self):
        self.pos = Vector2(random.randint(0, cell_number -1), random.randint(0, cell_number -1))

class BLUE_FRUIT:
    def __init__(self,):
        self.pos = Vector2(random.randint(0, cell_number -1), random.randint(0, cell_number -1))

    def draw_fruit(self):
        fruit_rect = pygame.Rect(self.pos.x * cell_size, self.pos.y * cell_size, cell_size, cell_size)
        pygame.draw.rect(screen, blue, fruit_rect)

    def respawn(self):
        self.pos = Vector2(random.randint(0, cell_number -1), random.randint(0, cell_number -1))

class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.red_fruit = RED_FRUIT()
        self.blue_fruit = BLUE_FRUIT()

        if self.blue_fruit.pos == self.red_fruit.pos:
            self.blue_fruit.respawn()

    def update(self):
        self.snake.move_snake()
        self.collision()
        self.check_lose()

    def draw(self):
        self.snake.draw_snake()
        self.red_fruit.draw_fruit()
        self.blue_fruit.draw_fruit()

    def collect_red(self):
        self.red_fruit.respawn()
        self.snake.add_block()
        self.snake.switch_head()

    def collect_blue(self):
        self.blue_fruit.respawn()
        self.snake.add_block()
        self.snake.switch_head()
    
    def collision(self):
        if self.red_fruit.pos == self.snake.body[0]:
            if not self.snake.blue:
                self.collect_red()
            else:
                self.red_fruit.respawn()
                self.snake.subtract_block()
        if self.blue_fruit.pos == self.snake.body[0]:
            if self.snake.blue:
                self.collect_blue()
            else:
                self.blue_fruit.respawn()
                self.snake.subtract_block()

    def check_lose(self):
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.game_over()

    def game_over(self):
        pygame.quit()
        sys.exit()

pygame.init()
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
clock = pygame.time.Clock()
pygame.display.set_caption("Snakes")

game = MAIN()

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 140)

while True:
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                game.snake.direction = Vector2(-1, 0)
            elif event.key == pygame.K_RIGHT:
                game.snake.direction = Vector2(1, 0)
            elif event.key == pygame.K_UP:
                game.snake.direction = Vector2(0, -1)
            elif event.key == pygame.K_DOWN:
                game.snake.direction = Vector2(0, 1)
        if event.type == SCREEN_UPDATE:
            game.update()

    screen.fill((42, 45, 51))
    game.draw()

    pygame.display.update()
    clock.tick(60)