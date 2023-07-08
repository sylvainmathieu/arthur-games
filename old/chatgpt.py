import pygame

# Initialize Pygame
pygame.init()

# Set up the window
win_width = 800
win_height = 600
win = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("2D Side Scroller")

# Set up the game clock
clock = pygame.time.Clock()

# Define the Player class
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, vel, jump_vel):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel = vel
        self.jump_vel = jump_vel
        self.jump = False
        self.jump_count = 0

    def update(self):
        # Handle player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.vel
        if keys[pygame.K_RIGHT] and self.rect.x < win_width - self.rect.width:
            self.rect.x += self.vel
        if self.jump:
            if self.jump_count < 15:
                self.rect.y -= self.jump_vel
                self.jump_count += 1
            else:
                self.jump = False
                self.jump_count = 0
        else:
            if self.rect.colliderect(platform.rect) and self.rect.bottom < platform.rect.bottom:
                self.rect.bottom = platform.rect.top
                self.jump_count = 0
            elif self.rect.bottom < win_height - 10:
                self.rect.y += self.vel

# Define the Platform class
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Create the player and platform
player = Player(win_width/2 - 25, win_height - 110, 50, 100, 7, 15)
platform = Platform(win_width/2 - 100, win_height - 70, 200, 20)

# Create a sprite group for the player and platform
all_sprites = pygame.sprite.Group()
all_sprites.add(player, platform)

# Game loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not player.jump:
                player.jump = True

        # Update all sprites
        all_sprites.update()

        # Draw the screen
        win.fill((255, 255, 255))
        all_sprites.draw(win)
        pygame.display.update()

        # Limit the frame rate
        clock.tick(60)