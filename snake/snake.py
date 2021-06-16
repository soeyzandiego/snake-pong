import pygame, sys, random
from pygame.math import Vector2

class FRUIT:
    def __init__(self, x, y):
        self.pos = Vector2(x, y)

    def draw_fruit(self):
        fruit_rect = pygame.Rect(self.pos.x * cell_size, self.pos.y * cell_size, cell_size, cell_size)
        pygame.draw.rect(screen, (126, 166, 114), fruit_rect)

pygame.init()
cell_size = 40
cell_number = 20
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
clock = pygame.time.Clock()
pygame.display.set_caption("Snakes")

fruit = FRUIT(random.randint(0, cell_number -1), random.randint(0, cell_number -1))
dir = Vector2(0, 0)

while True:
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                dir = (-1, 0)
            elif event.key == pygame.K_RIGHT:
                dir = (1, 0)
            elif event.key == pygame.K_UP:
                dir = (0, -1)
            elif event.key == pygame.K_DOWN:
                dir = (0, 1)

    screen.fill((42, 45, 51))
    fruit.draw_fruit()

    pygame.display.update()
    clock.tick(60)