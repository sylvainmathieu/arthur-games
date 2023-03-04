import pygame

pygame.init()

screenWidth = 640
screenHeight = 480
surface = pygame.display.set_mode((screenWidth,screenHeight))

clock = pygame.time.Clock()

p1Colour = (251,0,0)
p2Colour = (0,0,255)

isRunning = True
while isRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
    
    surface.fill((255,255,255))

    pygame.draw.rect(surface, p1Colour, (2,100,10,80))
    pygame.draw.rect(surface, p2Colour, (screenWidth - 12,300,10,80))

    pygame.display.flip()
    pygame.display.update()

    clock.tick(60)
