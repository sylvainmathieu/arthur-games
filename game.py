import pygame
import random

def is_on_the_snake(snake,x,y):
    for gh in snake:
        sx,sy = gh
        if sx == x and sy == y:
            return True
    return False

pygame.init()
surface = pygame.display.set_mode((400,400))

x = random.randint(0,19)
y = random.randint(0,19)
dx = 1
dy = 0
fx = random.randint(0,19)
fy = random.randint(0,19)
snakeColour = (50,150,255)
foodColour = (254,1,1)

snake = [(x,y)]

clock = pygame.time.Clock()
isRunning = True
gameOver = False
while isRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and dy == 0:
                dx = 0
                dy = -1
            if event.key == pygame.K_DOWN and dy == 0:
                dx = 0
                dy = 1
            if event.key == pygame.K_LEFT and dx == 0:
                dx = -1
                dy = 0
            if event.key == pygame.K_RIGHT and dx == 0:
                dx = 1
                dy = 0

    if not gameOver:
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

        if is_on_the_snake(snake,x,y):
            gameOver = True
            snakeColour = (150, 100, 30)
            foodColour = (150, 100, 30)

        snake.append((x,y))

        if x == fx and y == fy:
            fx = random.randint(0,19)
            fy = random.randint(0,19)
        else:
            # deleting the last square of the snake
            snake = snake[1:]

    surface.fill((0,0,0))

    for element in snake:
        ex, ey = element
        pygame.draw.rect(surface, snakeColour, (ex * 20,ey * 20,20,20))

    pygame.draw.rect(surface, foodColour, (fx * 20,fy * 20,20,20))

    pygame.display.flip()
    pygame.display.update()

    clock.tick(5)

print("I'm done!")
