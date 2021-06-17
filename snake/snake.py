import pygame, sys, random
from pygame.math import Vector2

red = (220, 20, 60)
blue = (30, 144, 255)

cell_size = 35
cell_number = 25

class SNAKE:
    def __init__(self):
        self.body = [Vector2(14, 10), Vector2(13, 10), Vector2(12, 10)]
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
        self.body.insert(0, self.body[0] + self.direction)

    def subtract_block(self):
        self.body = self.body[:-1]

    def switch_head(self):
        last_block = self.body[len(self.body) - 1]
        second_last_block = self.body[len(self.body) - 2]

        end_dir = second_last_block - last_block

        self.body.reverse()
        self.blue = not self.blue
        self.direction = end_dir * -1
          
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
        self.game_fin = False

        if self.blue_fruit.pos == self.red_fruit.pos:
            self.blue_fruit.respawn()

    def update(self):
        if self.game_fin: return  # if game is over, don't update

        self.snake.move_snake()
        self.collision()
        self.check_lose()

    def draw(self):
        self.red_fruit.draw_fruit()
        self.blue_fruit.draw_fruit()
        if self.game_fin: return  # if game is over, don't draw snake
        self.snake.draw_snake()

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
        if self.game_fin:
            return
        elif not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number: # if the snake head isn't between the display size, end the game
            self.game_over()
        else:
            for block in self.snake.body[1:]:
                if block == self.snake.body[0]:
                    self.game_over()

    def game_over(self):
        del self.snake  # delete the current snake
        self.game_fin = True

    def reset(self):
        self.snake = SNAKE()
        self.red_fruit.respawn()
        self.blue_fruit.respawn()
        self.game_fin = False

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
            if event.key == pygame.K_LEFT and game.snake.direction.x != 1:
                game.snake.direction = Vector2(-1, 0)
            elif event.key == pygame.K_RIGHT and game.snake.direction.x != -1:
                game.snake.direction = Vector2(1, 0)
            elif event.key == pygame.K_UP and game.snake.direction.y != 1:
                    game.snake.direction = Vector2(0, -1)
            elif event.key == pygame.K_DOWN and game.snake.direction.y != -1:
                game.snake.direction = Vector2(0, 1)

            if event.key == pygame.K_r and game.game_fin:
                game.reset()
        if event.type == SCREEN_UPDATE:
            game.update()

    screen.fill((42, 45, 51))
    game.draw()

    pygame.display.update()
    clock.tick(60)