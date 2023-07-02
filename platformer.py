import pygame
import sys

# Initialize Pygame
pygame.init()

# Set window dimensions and title
window_width = 25 * 32
window_height = 18 * 32
window_title = "Image Display"

# Create the window
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption(window_title)

# 25x18 grid
world_map = [
    "1111111111111111111111111",
    "1                       1",
    "1                       1",
    "1                       1",
    "1           3 3 3       1",
    "1  2                    1",
    "1  111                  1",
    "1                       1",
    "1                       1",
    "1    3    2  2  2    4441",
    "1           111         1",
    "1                       1",
    "1                       1",
    "1 2                     1",
    "1             4         1",
    "1     2                 1",
    "1                       1",
    "1111111111111111111111111"
]

terrain = pygame.image.load("assets/Terrain/Terrain (16x16).png") 
background = pygame.image.load("assets/Background/Yellow.png")

def get_sprite(image, x, y, w, h):
    rect = pygame.Rect(x, y, w, h)
    frame = pygame.Surface(rect.size).convert()
    frame.blit(image, (0, 0), rect)
    frame.set_colorkey((0, 0, 0), pygame.RLEACCEL)
    return pygame.transform.scale(frame, (w * 2, h * 2))

terrain_dict = {
    "1": get_sprite(terrain, 192, 16, 16, 16), # little square stone
    "2": get_sprite(terrain, 192, 0, 48, 16),  # long horizontal stone
    "3": get_sprite(terrain, 208, 16, 32, 32), # large square stone
    "4": get_sprite(terrain, 240, 0, 16, 48)   # long vertical stone
}

background_sprite = get_sprite(background, 0, 0, 64, 64)

# Set the animation loop time and initialize the timer
pygame.time.set_timer(pygame.USEREVENT, 58)

gravity = 0.6

clock = pygame.time.Clock()

class Player:
    def __init__(self):
        self.frame_width = 32
        self.frame_height = 32

        self.x = (window_width - self.frame_width) // 2
        self.y = window_height - 64 - self.frame_height
        self.current_dx = 0
        self.vel_y = 0
        self.speed = 5
        self.jump_speed = 10
        self.is_going_right = True
        self.is_jumping = False
        self.is_double_jumping = False

        self.running_right_frames = self.get_frames("assets/Main Characters/Ninja Frog/Run (32x32).png", 12, False)
        self.running_left_frames = self.get_frames("assets/Main Characters/Ninja Frog/Run (32x32).png", 12, True)
        self.idle_right_frames = self.get_frames("assets/Main Characters/Ninja Frog/Idle (32x32).png", 11, False)
        self.idle_left_frames = self.get_frames("assets/Main Characters/Ninja Frog/Idle (32x32).png", 11, True)
        self.jump_right_frames = self.get_frames("assets/Main Characters/Ninja Frog/Jump (32x32).png", 1, False)
        self.jump_left_frames = self.get_frames("assets/Main Characters/Ninja Frog/Jump (32x32).png", 1, True)
        self.djump_right_frames = self.get_frames("assets/Main Characters/Ninja Frog/Double Jump (32x32).png", 6, False)
        self.djump_left_frames = self.get_frames("assets/Main Characters/Ninja Frog/Double Jump (32x32).png", 6, True)

        self.frame_index = 0
        self.frames = self.idle_right_frames
        
    def get_frame(self, sprite_sheet, index):
        # Extract individual frames from the sprite sheet
        rect = pygame.Rect(index * self.frame_width, 0, self.frame_width, self.frame_height)
        frame = pygame.Surface(rect.size).convert()
        frame.blit(sprite_sheet, (0, 0), rect)
        frame.set_colorkey((0, 0, 0), pygame.RLEACCEL)
        return frame

    def get_frames(self, path, num_frames, flip):
        # Load the entire sprite sheet
        sprite_sheet = pygame.image.load(path)
        if flip:
            sprite_sheet = pygame.transform.flip(sprite_sheet, True, False)
        frames = []
        for i in range(num_frames):
            frame = self.get_frame(sprite_sheet, i)
            scaled_frame = pygame.transform.scale(frame, (self.frame_width * 2, self.frame_height * 2))
            frames.append(scaled_frame)
        return frames
        
    def update(self, events):
        
        # React to player control inputs
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.current_dx = self.speed
                    self.is_going_right = True
                if event.key == pygame.K_LEFT:
                    self.current_dx = -self.speed
                    self.is_going_right = False
                if event.key == pygame.K_SPACE and not self.is_jumping and self.vel_y == 0 and not self.is_double_jumping:
                    self.vel_y = -self.jump_speed
                    self.is_jumping = True
                    self.is_double_jumping = False
                elif event.key == pygame.K_SPACE and self.is_jumping and self.vel_y <= 3 and not self.is_double_jumping:
                    self.vel_y = -(self.jump_speed * 1.2)
                    self.is_double_jumping = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT and self.current_dx > 0:
                    self.current_dx = 0
                elif event.key == pygame.K_LEFT and self.current_dx < 0:
                    self.current_dx = 0
            if event.type == pygame.USEREVENT:
                # Update the frame index and loop the sequence
                self.frame_index += 1

        dx = self.current_dx

        # Apply gravity
        self.vel_y = self.vel_y + gravity
        if self.vel_y > 10:
            self.vel_y = 10
        dy = self.vel_y

        # Detect collisions 
        player_height = self.frame_height * 2
        player_top = self.y
        player_bottom = player_top + player_height
        player_collision_rect = pygame.Rect(self.x + 18, player_top + 15, player_height - 36, player_height - 15)
        for tile_y, lines in enumerate(world_map):
            for tile_x, tile in enumerate(lines):
                if tile == " ":
                    continue

                sprite = terrain_dict[tile]
                tile_rect = pygame.Rect(tile_x * 32, tile_y * 32, sprite.get_width(), sprite.get_height())
                collided = False

                # x-axis collision detection
                if tile_rect.colliderect(player_collision_rect.left + dx, player_collision_rect.top, player_collision_rect.width, player_collision_rect.height):
                    dx = 0
                    collided = True

                # y-axis collision detection
                if tile_rect.colliderect(player_collision_rect.left, player_collision_rect.top + dy + 1, player_collision_rect.width, player_collision_rect.height):
                    if self.vel_y > 0:
                        dy = tile_rect.top - player_bottom
                        self.vel_y = 0
                        self.is_jumping = False
                        self.is_double_jumping = False
                    else:
                        dy = tile_rect.bottom - player_top
                        self.vel_y = 0
                        self.is_jumping = True
                        self.is_double_jumping = False
                    collided = True
                
                if collided:
                    break

        # Move the player 
        self.x = self.x + dx
        self.y = self.y + dy

        # Animation logic
        if self.is_jumping is True:
            if self.is_double_jumping:
                if self.is_going_right == True:
                    self.frames = self.djump_right_frames
                else:
                    self.frames = self.djump_left_frames
            else:
                if self.is_going_right == True:
                    self.frames = self.jump_right_frames
                else:
                    self.frames = self.jump_left_frames
        else:
            if dx == 0:
                if self.is_going_right == True:
                    self.frames = self.idle_right_frames
                else:
                    self.frames = self.idle_left_frames
            elif dx > 0:
                self.frames = self.running_right_frames
            else:
                self.frames = self.running_left_frames

        self.frame_index = self.frame_index % len(self.frames)

        self.current_frame = self.frames[self.frame_index]

    def draw(self):
        screen.blit(self.current_frame, (self.x, self.y))

player = Player()

# Main loop
running = True
while running:

    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            running = False

    player.update(events)

    # Clear the screen
    screen.fill((0, 0, 0))

    # Background tiles
    for y in range(int(window_height / 128) + 1):
        for x in range(int(window_width / 128)):
            screen.blit(background_sprite, (x * 128, y * 128))

    # Wolrd map tiles
    for tile_y, lines in enumerate(world_map):
        for tile_x, tile in enumerate(lines):
            if tile != " ":
                screen.blit(terrain_dict[tile], (tile_x * 16 * 2, tile_y * 16 * 2))

    # Player sprite
    player.draw()

    # Update the display
    pygame.display.flip()

    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
