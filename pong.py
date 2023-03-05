import pygame

pygame.init()

screenWidth = 640
screenHeight = 480
surface = pygame.display.set_mode((screenWidth,screenHeight))

clock = pygame.time.Clock()

p1Colour = (251,0,0)
p2Colour = (0,0, 255)
playerHeight = 80
player1 = pygame.Rect(2, 100, 10, playerHeight)
player2 = pygame.Rect(screenWidth - 12, 300, 10, playerHeight)
ballX = screenWidth / 2
ballY = screenHeight / 2

playerSpeed = 5
ballSpeedX = 5
ballSpeedY = 5
p1Speed = 0
p2Speed = 0

isRunning = True
while isRunning:

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                p2Speed = playerSpeed * -1
            if event.key == pygame.K_DOWN:
                p2Speed = playerSpeed
            if event.key == pygame.K_w:
                p1Speed = playerSpeed * -1
            if event.key == pygame.K_s:
                p1Speed = playerSpeed
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                p2Speed = 0
            if event.key == pygame.K_DOWN:
                p2Speed = 0
            if event.key == pygame.K_w:
                p1Speed = 0
            if event.key == pygame.K_s:
                p1Speed = 0
        elif event.type == pygame.QUIT:
            isRunning = False
    
    surface.fill((255,255,255))

    player1.y += p1Speed
    player2.y += p2Speed

    if player1.y <= 3:
        player1.y = 3
    if player1.y >= screenHeight - playerHeight - 3:
        player1.y = screenHeight - playerHeight - 3

    if player2.y <= 3:
        player2.y = 3
    if player2.y >= screenHeight - playerHeight - 3:
        player2.y = screenHeight - playerHeight - 3

    ballX += ballSpeedX
    ballY += ballSpeedY

    if ballY > screenHeight:
        ballSpeedY = -5
    if ballX > screenWidth:
        ballSpeedX = -5
    if ballY < 0:
        ballSpeedY = 5
    if ballX < 0:
        ballSpeedX = 5

    pygame.draw.rect(surface, p1Colour, player1)
    pygame.draw.rect(surface, p2Colour, player2)

    pygame.draw.circle(surface, (0,0,0), (ballX, ballY), 5, 5)

    pygame.display.flip()
    pygame.display.update()

    clock.tick(60)
