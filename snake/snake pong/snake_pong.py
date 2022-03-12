import pygame, sys, random, os, json
from pygame.math import Vector2, Vector3
from pygame import mixer

RED = (220, 20, 60)
BLUE = (30, 144, 255)

BG_RED = Vector3(230, 154, 173)
BG_BLUE = Vector3(151, 204, 230)

GRASS_RED = Vector3(222, 149, 167)
GRASS_BLUE = Vector3(146, 197, 222)

cell_size = 40
cell_number = 20

HALFWAY_POINT = (cell_size * cell_number) / 2

# Player Data
player_data = {
    'h_score' : 0,
    'sfx' : True,
    'music' : True
}

try:
    with open('player_data.txt') as data_file:
        player_data = json.load(data_file)
except:
    print("No player data file created")

class SNAKE:
    def __init__(self):
        middle = cell_number / 2
        self.body = [Vector2(middle + 1, middle), Vector2(middle, middle), Vector2(middle - 1, middle)]
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
        eat_sound.play()

    def subtract_block(self):
        self.body = self.body[:-1]
        wrong_sound.play()

    def switch_head(self):
        last_block = self.body[len(self.body) - 1]
        second_last_block = self.body[len(self.body) - 2]

        end_dir = second_last_block - last_block    # find the facing direction of the last block

        self.body.reverse() # make the opposite head the first in the array
        self.blue = not self.blue
        self.direction = end_dir * -1 # bounce back
          
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
        #sprite = pygame.image.load(os.path.join("assets/sprites/blue_fruit.png"))
        #screen.blit(sprite, fruit_rect)
        pygame.draw.rect(screen, BLUE, fruit_rect)     # Grid square

    def respawn(self):
        new_pos = Vector2(random.randint(0, cell_number -1), random.randint(0, cell_number -1))
        self.pos = new_pos

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

    def draw(self, mix_amount):
        self.draw_grass(mix_amount)
        self.red_fruit.draw_fruit()
        self.blue_fruit.draw_fruit()

        score = str(self.score)
        score_surface = score_font.render(score, True, (255, 255, 255))
        score_rect = score_surface.get_rect(topleft = (15, 10))
        screen.blit(score_surface, score_rect)

        if self.game_over: return  # if game is over, don't draw snake
        self.snake.draw_snake()

    def draw_grass(self, mix_amount):
        grass_color = GRASS_RED

        lerp = pygame.Vector3.lerp(GRASS_RED, GRASS_BLUE, mix_amount)
        grass_color = (lerp.x, lerp.y, lerp.z)

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
            wall_sound.play()
            self.end_game()

        if self.score < 0:
            self.end_game()
            self.score = 0
        
        for block in self.snake.body[1:]:
                if block == self.snake.body[0]:
                    self.end_game()
                    break

    def end_game(self):
        del self.snake  # delete the current snake
        self.game_over = True
        self.snake = SNAKE()

        if self.score > player_data["h_score"]:
            player_data["h_score"] = self.score

    def reset(self):
        self.red_fruit.respawn()
        self.blue_fruit.respawn()
        self.score = 0
        self.stopped = True
        self.game_over = False

class BUTTON:
    def __init__(self, pos, text):
        self.pos = pos
        self.text = text
        self.image = blue_button

        self.draw()

    def draw(self):
        rect = self.image.get_rect(center = self.pos)
        self.rect = rect
        screen.blit(self.image, rect)

        if self.hovering():
            self.image = red_button
        else:
            self.image = blue_button


        font = pygame.font.Font(os.path.join("assets", "fonts", "BroadwayFlat.ttf"), 50)
        text_surf = font.render(self.text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center = self.pos)
        screen.blit(text_surf, text_rect)

    def change_image(self, image):
        self.image = image

    def hovering(self):
        pos = pygame.mouse.get_pos()
        if pos[0] > self.rect.left and pos[0] < self.rect.right:
            if pos[1] > self.rect.top and pos[1] < self.rect.bottom:
                return True

        return False     

class TITLE_SCREEN:
    def __init__(self):
        self.draw()

    def draw(self):
        button_pos = Vector2(HALFWAY_POINT, HALFWAY_POINT + 50)
        self.button = BUTTON(button_pos, "Play")

        if self.button.hovering():
            screen.fill(BG_BLUE)
        else:
            screen.fill(BG_RED)

        title_surface = title_font.render("Snake Pong", True, (255, 255, 255))
        title_rect = title_surface.get_rect(center = (HALFWAY_POINT, HALFWAY_POINT - 55))
        screen.blit(title_surface, title_rect)

        self.button.draw()

class END_SCREEN:
    def __init__(self):
        pass
    
    def draw(self, score):
        text_surf = end_score_font.render(score, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center = ((HALFWAY_POINT, HALFWAY_POINT - 40)))
        screen.blit(text_surf, text_rect)

        restart_surf = end_text_font.render("Press R to restart", True, (208, 138, 158))
        restart_rect = restart_surf.get_rect(center = (HALFWAY_POINT, HALFWAY_POINT + 50))
        screen.blit(restart_surf, restart_rect)

        h_surf = end_text_font.render(f'{player_data["h_score"]}', True, (255, 201, 215))
        h_rect = h_surf.get_rect(center = (HALFWAY_POINT, HALFWAY_POINT - 140))
        screen.blit(h_surf, h_rect)

def clamp(num, min_value, max_value):
   return max(min(num, max_value), min_value)

pygame.init()
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
clock = pygame.time.Clock()
pygame.display.set_caption("Snake Pong")

# UI elements
score_font = pygame.font.Font(os.path.join("assets", "fonts", "BroadwayFlat.ttf"), 75)
title_font = pygame.font.Font(os.path.join("assets", "fonts", "BroadwayFlat.ttf"), 125)
end_score_font = pygame.font.Font(os.path.join("assets", "fonts", "BroadwayFlat.ttf"), 150)
end_text_font = pygame.font.Font(os.path.join("assets", "fonts", "BroadwayFlat.ttf"), 40)
blue_button = pygame.image.load(os.path.join("assets", "sprites", "blue_button.png"))
red_button = pygame.image.load(os.path.join("assets", "sprites", "red_button.png"))

# Sound
eat_sound = mixer.Sound(os.path.join("assets", "sounds", "eat.wav"))
wall_sound = mixer.Sound(os.path.join("assets", "sounds", "hit_wall.wav"))
wrong_sound = mixer.Sound(os.path.join("assets", "sounds", "wrong_fruit.wav"))

# Instances
game = MAIN()
menu = TITLE_SCREEN()
end_screen = END_SCREEN()

# Snake movement control
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 140)

# Background fade
COLOR_FADE = pygame.USEREVENT
fading = False
mix_amount = 0
bg_color = BG_RED

while True:
    delta = pygame.time.Clock().get_time()

    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            with open('player_data.txt', 'w') as data_file:
                json.dump(player_data, data_file)

            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if game.menu and menu.button.hovering():
                game.menu = False
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
    
    fade_speed = 0.05

    if fading:
        if game.snake.blue:
            mix_amount += fade_speed
        elif not game.snake.blue:
            mix_amount -= fade_speed
    
    mix_amount = clamp(mix_amount, 0, 1.0)

    if game.snake.blue:
        if bg_color != BG_BLUE:
            fading = True
        else:
            fading = False
            mix_amount = 1
    elif not game.snake.blue:
        if bg_color != BG_RED:
            fading = True
        elif bg_color == BG_RED:
            fading = False
            mix_amount = 0

    lerp = pygame.Vector3.lerp(BG_RED, BG_BLUE, mix_amount)
    if game.game_over:
        bg_color = BG_RED
    else:
        bg_color = (lerp.x, lerp.y, lerp.z)

    screen.fill(bg_color)

    if game.menu:
        menu.draw()
    elif game.game_over:
        end_screen.draw(str(game.score))
    else:
        game.draw(mix_amount)

    pygame.display.update()
    clock.tick(60)