import pygame
import random

pygame.init()
surface = pygame.display.set_mode((400,400))

x = 2
y = 1
dx = 0
dy = 0
fx = random.randint(0,19)
fy = random.randint(0,19)

clock = pygame.time.Clock()
isRunning = True
while isRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                dx = 0
                dy = -1
            if event.key == pygame.K_DOWN:
                dx = 0
                dy = 1
            if event.key == pygame.K_LEFT:
                dx = -1
                dy = 0
            if event.key == pygame.K_RIGHT:
                dx = 1
                dy = 0

    surface.fill((0,0,0))

    x = x + dx
    y = y + dy

    if x >= 20:
        x = 0
    if y >= 20:
        y = 0
    if x < 0:
        x = 19
    if y < 0:
        y = 19

    if x == fx and y == fy:
        fx = random.randint(0,19)
        fy = random.randint(0,19)
   
    pygame.draw.rect(surface, (50,150,255), (x * 20,y * 20,20,20))
    pygame.draw.rect(surface, (254,1,1), (fx * 20,fy * 20,20,20))

    pygame.display.flip()
    pygame.display.update()

    clock.tick(5)

print("I'm done!")
