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

    def subtract_block(self):
        self.body = self.body[:-1]
        sfx_channel.play(wrong_sound)

    def switch_head(self):
        last_block = self.body[len(self.body) - 1]
        second_last_block = self.body[len(self.body) - 2]

        end_dir = second_last_block - last_block    # find the facing direction of the last block

        self.body.reverse() # make the opposite head the first in the array
        self.blue = not self.blue
        self.direction = end_dir * -1 # bounce back
          
class RED_FRUIT:
    def __init__(self):
        self.pos = Vector2(random.randint(0, cell_number -1), random.randint(0, cell_number -1))

    def draw_fruit(self):
        fruit_rect = pygame.Rect(self.pos.x * cell_size, self.pos.y * cell_size, cell_size, cell_size)
        pygame.draw.rect(screen, RED, fruit_rect)

    def respawn(self, snake_body):
        new_pos = Vector2(random.randint(0, cell_number -1), random.randint(0, cell_number -1))
        for block in snake_body:
            if new_pos == block:
                new_pos = Vector2(random.randint(0, cell_number -1), random.randint(0, cell_number -1))
        self.pos = new_pos

class BLUE_FRUIT:
    def __init__(self):
        self.pos = Vector2(random.randint(0, cell_number -1), random.randint(0, cell_number -1))

    def draw_fruit(self):
        fruit_rect = pygame.Rect(self.pos.x * cell_size, self.pos.y * cell_size, cell_size, cell_size)
        #sprite = pygame.image.load(os.path.join("assets/sprites/blue_fruit.png"))
        #screen.blit(sprite, fruit_rect)
        pygame.draw.rect(screen, BLUE, fruit_rect)     # Grid square

    def respawn(self, snake_body):
        new_pos = Vector2(random.randint(0, cell_number -1), random.randint(0, cell_number -1))
        for block in snake_body:
            if new_pos == block:
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
        self.settings = False
        self.score = 0

        if self.blue_fruit.pos == self.red_fruit.pos:
            self.blue_fruit.respawn(self.snake.body)

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
        self.red_fruit.respawn(self.snake.body)
        self.snake.add_block()
        sfx_channel.play(eat_sound)

    def collect_blue(self):
        self.snake.switch_head()
        self.blue_fruit.respawn(self.snake.body)
        self.snake.add_block()
        sfx_channel.play(eat_sound2)

    def collision(self):
        if self.red_fruit.pos == self.snake.body[0]:
            if not self.snake.blue:
                self.collect_red()
                self.score += 1
            else:
                self.red_fruit.respawn(self.snake.body)
                self.snake.subtract_block()
                self.score -= 1
        if self.blue_fruit.pos == self.snake.body[0]:
            if self.snake.blue:
                self.collect_blue()
                self.score += 1
            else:
                self.blue_fruit.respawn(self.snake.body)
                self.snake.subtract_block()
                self.score -=1

    def check_lose(self):
        if self.game_over: return
        
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number: # if the snake head isn't between the display size, end the game
            sfx_channel.play(wall_sound)
            self.end_game()

        if self.score < 0:
            self.end_game()
            self.score = 0
        
        for block in self.snake.body[1:]:
                if block == self.snake.body[0]:
                    self.end_game()
                    sfx_channel.play(wrong_sound)
                    break

    def end_game(self):
        del self.snake  # delete the current snake
        self.game_over = True
        self.snake = SNAKE()

        if self.score > player_data["h_score"]:
            player_data["h_score"] = self.score

    def reset(self):
        self.red_fruit.respawn(self.snake.body)
        self.blue_fruit.respawn(self.snake.body)
        self.score = 0
        self.stopped = True
        self.game_over = False

class BUTTON:
    def __init__(self, pos, text, text_size, img, hover_img):
        self.pos = pos
        self.text = text
        self.text_size = text_size
        self.img = img
        self.hover_img = hover_img

        self.cur_img = self.img

        self.draw()

    def draw(self):
        rect = self.cur_img.get_rect(center = self.pos)
        self.rect = rect
        screen.blit(self.cur_img, rect)

        if self.hovering():
            self.cur_img = self.hover_img
        else:
            self.cur_img = self.img


        font = pygame.font.Font(os.path.join("assets", "fonts", "BroadwayFlat.ttf"), self.text_size)
        text_surf = font.render(self.text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center = self.pos)
        screen.blit(text_surf, text_rect)

    def hovering(self):
        pos = pygame.mouse.get_pos()
        if pos[0] > self.rect.left and pos[0] < self.rect.right:
            if pos[1] > self.rect.top and pos[1] < self.rect.bottom:
                return True

        return False     

class TITLE_SCREEN:
    def __init__(self):
        self.draw()

        if player_data["music"]:
            mixer.music.play(-1)
        else:
            mixer.music.stop()
        if player_data["sfx"]:
            sfx_channel.set_volume(1)
        else:
            sfx_channel.set_volume(0)

    def draw(self):
        button_pos = Vector2(HALFWAY_POINT, HALFWAY_POINT + 25)
        self.button = BUTTON(button_pos, "Play", 50, blue_button, red_button)

        self.s_button = BUTTON(button_pos + (0, 80), "Settings", 35, small_button, small_button_h)

        if self.button.hovering():
            screen.fill(BG_BLUE)
        else:
            screen.fill(BG_RED)

        title_surface = title_font.render("Snake Pong", True, (255, 255, 255))
        title_rect = title_surface.get_rect(center = (HALFWAY_POINT, HALFWAY_POINT - 75))
        screen.blit(title_surface, title_rect)

        self.button.draw()
        self.s_button.draw()

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

        menu_surf = end_text_font.render("Enter to return to menu", True, (208, 138, 158))
        menu_rect = menu_surf.get_rect(center = (HALFWAY_POINT, HALFWAY_POINT + 100))
        screen.blit(menu_surf, menu_rect)

        h_surf = end_text_font.render(f'{player_data["h_score"]}', True, (255, 201, 215))
        h_rect = h_surf.get_rect(center = (HALFWAY_POINT, HALFWAY_POINT - 140))
        screen.blit(h_surf, h_rect)

class SETTINGS:
    def __init__(self):
        pass

    def draw(self):
        button_pos = Vector2(HALFWAY_POINT, HALFWAY_POINT - 85)
        music_txt = f'Music: {self.bool_to_text(player_data["music"])}'
        self.m_button = BUTTON(button_pos, music_txt, 50, blue_button, blue_button_h)
        self.m_button.draw()

        sfx_text = f'SFX: {self.bool_to_text(player_data["sfx"])}'
        self.fx_button = BUTTON(button_pos + (0, 100), sfx_text, 50, blue_button, blue_button_h)
        self.fx_button.draw()

        self.b_button = BUTTON(button_pos + (0, 300), "Back", 35, small_button, small_button_h)
        self.b_button.draw()

    def bool_to_text(self, bool):
        if bool:
            return "On"
        else:
            return "Off"

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
blue_button_h = pygame.image.load(os.path.join("assets", "sprites", "blue_button_h.png"))
small_button = pygame.image.load(os.path.join("assets", "sprites", "small_button.png"))
small_button_h = pygame.image.load(os.path.join("assets", "sprites", "small_button_h.png"))

# Sound
eat_sound = mixer.Sound(os.path.join("assets", "sounds", "eat.wav"))
eat_sound2 = mixer.Sound(os.path.join("assets", "sounds", "eat2.wav"))
wall_sound = mixer.Sound(os.path.join("assets", "sounds", "hit_wall.wav"))
wrong_sound = mixer.Sound(os.path.join("assets", "sounds", "wrong_fruit.wav"))
mixer.music.load(os.path.join("assets", "sounds", "snake_pong_theme.wav"))
sfx_channel = mixer.Channel(0)

# Instances
game = MAIN()
menu = TITLE_SCREEN()
end_screen = END_SCREEN()
settings = SETTINGS()

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
            if game.settings:
                if settings.m_button.hovering():
                    if player_data["music"]:
                        mixer.music.stop()
                        player_data["music"] = False
                    else:
                        mixer.music.play(-1)
                        player_data["music"] = True
                if settings.fx_button.hovering():
                    if player_data["sfx"]:
                        sfx_channel.set_volume(0)
                        player_data["sfx"] = False
                    else:
                        sfx_channel.set_volume(1)
                        player_data["sfx"] = True
                if settings.b_button.hovering():
                    game.menu = True
                    game.settings = False
            if game.menu:
                if menu.button.hovering():
                    game.menu = False
                elif menu.s_button.hovering():
                    game.settings = True
                    game.menu = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and game.game_over:
                game.reset()
            if event.key == pygame.K_RETURN:
                if game.menu:
                    game.menu = False
                elif game.game_over:
                    game.reset()
                    game.menu = True
                    game.game_over = False
                elif game.stopped:
                    game.stopped = False

            if not game.game_over:   # if the game isn't finished, take the snake input
                if event.key == pygame.K_LEFT and game.snake.direction.x != 1:
                    game.snake.direction = Vector2(-1, 0)
                elif event.key == pygame.K_RIGHT and game.snake.direction.x != -1:
                    game.snake.direction = Vector2(1, 0)
                elif event.key == pygame.K_UP and game.snake.direction.y != 1:
                    game.snake.direction = Vector2(0, -1)
                elif event.key == pygame.K_DOWN and game.snake.direction.y != -1:
                    game.snake.direction = Vector2(0, 1)
            

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
    elif game.settings:
        settings.draw()
    elif game.game_over:
        end_screen.draw(str(game.score))
    else:
        game.draw(mix_amount)

    pygame.display.update()
    clock.tick(60)