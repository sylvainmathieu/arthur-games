import pygame

pygame.init()
pygame.font.init()
my_font = pygame.font.SysFont('Annai MN Regular', 30)

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
ballRadius = 5

playerSpeed = 7
ballSpeedX = 5
ballSpeedY = 5
p1Speed = 0
p2Speed = 0

p1Score = 0
p2Score = 0

def resetBall():
    global ballX, ballY
    ballX = screenWidth / 2
    ballY = screenHeight / 2

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

    ballRect = pygame.Rect(ballX - ballRadius, ballY - ballRadius, ballRadius * 2, ballRadius * 2)

    if ballY > screenHeight:
        ballSpeedY = -5
    if ballX > screenWidth:
        p1Score += 1
        resetBall()
    if ballY < 0:
        ballSpeedY = 5
    if ballX < 0:
        p2Score += 1
        resetBall()

    if player1.colliderect(ballRect):
        ballSpeedX = 5
    if player2.colliderect(ballRect):
        ballSpeedX = -5

    pygame.draw.rect(surface, p1Colour, player1)
    pygame.draw.rect(surface, p2Colour, player2)

    pygame.draw.circle(surface, (0,0,0), (ballX, ballY), ballRadius, 5)

    p1ScoreSurface = my_font.render(str(p1Score), True, p1Colour)
    p2ScoreSurface = my_font.render(str(p2Score), True, p2Colour)
    surface.blit(p1ScoreSurface, ((screenWidth / 2) - 100, 20))
    surface.blit(p2ScoreSurface, ((screenWidth / 2) + 60, 20))

    pygame.display.flip()
    pygame.display.update()

    clock.tick(60)
