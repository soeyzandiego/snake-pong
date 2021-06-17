import pygame, sys, random
from pygame.math import Vector2

red = (220, 20, 60)
blue = (30, 144, 255)

cell_size = 35
cell_number = 25

class SNAKE:
    def __init__(self):
        self.body = [Vector2(14, 13), Vector2(13, 13), Vector2(12, 13)]
        self.direction = Vector2(1, 0)
        self.blue = False
        self.length = 0
    
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
        self.length += 1

    def subtract_block(self):
        self.body = self.body[:-1]
        self.length -= 1

    def switch_head(self):
        last_block = self.body[len(self.body) - 1]
        second_last_block = self.body[len(self.body) - 2]

        end_dir = second_last_block - last_block    # find the facing direction of the last block

        self.body.reverse() # make the opposite head the first in the array
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
        self.game_over = False
        self.running = False

        if self.blue_fruit.pos == self.red_fruit.pos:
            self.blue_fruit.respawn()

    def update(self):
        if self.game_over: return  # if game is over, don't update

        self.snake.move_snake()
        self.collision()
        self.check_lose()

    def draw(self):
        self.red_fruit.draw_fruit()
        self.blue_fruit.draw_fruit()
        if self.game_over: return  # if game is over, don't draw snake
        self.snake.draw_snake()

        score = str(self.snake.length)
        score_surface = score_font.render(score, True, (255, 255, 255))
        score_rect = score_surface.get_rect(topleft = (15, 10))
        screen.blit(score_surface, score_rect)

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
        if self.game_over: return
        
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number: # if the snake head isn't between the display size, end the game
            self.end_game()
            
        for block in self.snake.body[1:]:
                if block == self.snake.body[0]:
                    self.end_game()
                    break

    def end_game(self):
        del self.snake  # delete the current snake
        self.game_over = True
        self.snake = SNAKE()

    def reset(self):
        self.red_fruit.respawn()
        self.blue_fruit.respawn()
        self.game_over = False

pygame.init()
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
clock = pygame.time.Clock()
pygame.display.set_caption("Snakes")

score_font = pygame.font.Font(None, 50)

game = MAIN()

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 140)

while True:
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and game.game_over:
                game.reset()

            if not game.game_over:   # if the game isn't finished, take the snake input
                if event.key == pygame.K_LEFT and game.snake.direction.x != 1:
                    game.snake.direction = Vector2(-1, 0)
                elif event.key == pygame.K_RIGHT and game.snake.direction.x != -1:
                    game.snake.direction = Vector2(1, 0)
                elif event.key == pygame.K_UP and game.snake.direction.y != 1:
                    game.snake.direction = Vector2(0, -1)
                elif event.key == pygame.K_DOWN and game.snake.direction.y != -1:
                    game.snake.direction = Vector2(0, 1)
            
            if not game.running and event.key == pygame.K_RETURN:
                game.running = True

        if event.type == SCREEN_UPDATE and game.running:
            game.update()

    bg_color = (255, 154, 173)
    if game.snake.blue:
        bg_color = (151, 204, 255)
    else:
        bg_color = (255, 154, 173)

    screen.fill(bg_color)
    game.draw()

    pygame.display.update()
    clock.tick(60)