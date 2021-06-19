import pygame, sys, random, os
from pygame.math import Vector2, Vector3

RED = (220, 20, 60)
BLUE = (30, 144, 255)

BG_RED = Vector3(230, 154, 173)
BG_BLUE = Vector3(151, 204, 230)

GRASS_RED = (222, 149, 167)
GRASS_BLUE = (146, 197, 222)

cell_size = 40
cell_number = 20

class SNAKE:
    def __init__(self):
        self.body = [Vector2(14, 12), Vector2(13, 12), Vector2(12, 12)]
        self.direction = Vector2(1, 0)
        self.blue = False
    
    def draw_snake(self):
        for block in self.body:
            snake_rect = pygame.Rect(block.x * cell_size, block.y * cell_size, cell_size, cell_size)
            color = (255, 255, 255)
            if block == self.body[0]:
                if not self.blue:
                    color = RED
                else:
                    color = BLUE
            elif block == self.body[len(self.body) - 1]:
                if not self.blue:
                    color = BLUE
                else:      
                    color = RED
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

        end_dir = second_last_block - last_block    # find the facing direction of the last block

        self.body.reverse() # make the opposite head the first in the array
        self.blue = not self.blue
        self.direction = end_dir * -1
          
class RED_FRUIT:
    def __init__(self,):
        self.pos = Vector2(random.randint(0, cell_number -1), random.randint(0, cell_number -1))

    def draw_fruit(self):
        fruit_rect = pygame.Rect(self.pos.x * cell_size, self.pos.y * cell_size, cell_size, cell_size)
        pygame.draw.rect(screen, RED, fruit_rect)

    def respawn(self):
        self.pos = Vector2(random.randint(0, cell_number -1), random.randint(0, cell_number -1))

class BLUE_FRUIT:
    def __init__(self,):
        self.pos = Vector2(random.randint(0, cell_number -1), random.randint(0, cell_number -1))

    def draw_fruit(self):
        fruit_rect = pygame.Rect(self.pos.x * cell_size, self.pos.y * cell_size, cell_size, cell_size)
        sprite = pygame.image.load(os.path.join("assets/sprites/blue_fruit.png"))
        screen.blit(sprite, fruit_rect)
        #pygame.draw.rect(screen, BLUE, fruit_rect)     Grid square

    def respawn(self):
        self.pos = Vector2(random.randint(0, cell_number -1), random.randint(0, cell_number -1))

class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.red_fruit = RED_FRUIT()
        self.blue_fruit = BLUE_FRUIT()
        self.game_over = False
        self.stopped = True
        self.menu = True
        self.score = 0

        if self.blue_fruit.pos == self.red_fruit.pos:
            self.blue_fruit.respawn()

    def update(self):
        if self.game_over: return  # if game is over, don't update

        self.collision()
        self.check_lose()
        self.snake.move_snake()

    def draw(self):
        self.draw_grass()
        self.red_fruit.draw_fruit()
        self.blue_fruit.draw_fruit()

        score = str(self.score)
        score_surface = score_font.render(score, True, (255, 255, 255))
        score_rect = score_surface.get_rect(topleft = (15, 10))
        screen.blit(score_surface, score_rect)

        if self.game_over: return  # if game is over, don't draw snake
        self.snake.draw_snake()

    def draw_grass(self):
        grass_color = GRASS_RED

        if self.snake.blue:
            grass_color = GRASS_BLUE
        else:
            grass_color = GRASS_RED

        for row in range(cell_number):
            if row % 2 == 0:
                for col in range(cell_number):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)
            else:
                for col in range(cell_number):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)

    def collect_red(self):
        self.snake.switch_head()
        self.red_fruit.respawn()
        self.snake.add_block()

    def collect_blue(self):
        self.snake.switch_head()
        self.blue_fruit.respawn()
        self.snake.add_block()
    
    def collision(self):
        if self.red_fruit.pos == self.snake.body[0]:
            if not self.snake.blue:
                self.collect_red()
                self.score += 1
            else:
                self.red_fruit.respawn()
                self.snake.subtract_block()
                self.score -= 1
        if self.blue_fruit.pos == self.snake.body[0]:
            if self.snake.blue:
                self.collect_blue()
                self.score += 1
            else:
                self.blue_fruit.respawn()
                self.snake.subtract_block()
                self.score -=1

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
        self.score = 0
        self.stopped = True
        self.game_over = False

pygame.init()
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
clock = pygame.time.Clock()
pygame.display.set_caption("Snake Pong")

# UI elements
score_font = pygame.font.Font(os.path.join("assets", "fonts", "BroadwayFlat.ttf"), 75)
title_font = pygame.font.Font(os.path.join("assets", "fonts", "BroadwayFlat.ttf"), 125)

game = MAIN()

# snake movement control
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 140)

def title_screen():
    title_surface = title_font.render("Snake Pong", True, (255, 255, 255))
    title_rect = title_surface.get_rect(center = (437.5, 400))
    screen.blit(title_surface, title_rect)


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
            
            if event.key == pygame.K_RETURN:
                if game.menu:
                    game.menu = False
                elif game.stopped:
                    game.stopped = False

        if event.type == SCREEN_UPDATE and not game.stopped:
            game.update()

    
    fade_speed = 0.01
    mix_amount = 1
    if mix_amount <= 0:
        mix_amount += fade_speed
    if mix_amount >= 1:
        mix_amount -= fade_speed
    
    bg_color = BG_RED
    if game.snake.blue:
        lerp = pygame.Vector3.lerp(BG_RED, BG_BLUE, mix_amount)
        bg_color = (lerp.x, lerp.y, lerp.z)
    else:
        lerp = pygame.Vector3.lerp(BG_BLUE, BG_RED, mix_amount)
        bg_color = (lerp.x, lerp.y, lerp.z)

    screen.fill(bg_color)

    if game.menu:
        title_screen()     
    else:
        game.draw()    

    pygame.display.update()
    clock.tick(60)