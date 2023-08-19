import pygame
import sys

# Initialize Pygame
pygame.init()

# Set window dimensions and title
window_width = 25 * 32
window_height = 18 * 32
window_title = "2D Platformer"

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
    "1           M           1",
    "1                       1",
    "1    3 3  2  2  2    4441",
    "1           111         1",
    "1                       1",
    "1                       1",
    "1 2                     1",
    "1                       1",
    "1     2            M    1",
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

def get_frame(sprite_sheet, index, frame_width, frame_height):
    # Extract individual frames from the sprite sheet
    rect = pygame.Rect(index * frame_width, 0, frame_width, frame_height)
    frame = pygame.Surface(rect.size).convert()
    frame.blit(sprite_sheet, (0, 0), rect)
    frame.set_colorkey((0, 0, 0), pygame.RLEACCEL)
    return frame

def get_frames(path, num_frames, flip, frame_width, frame_height):
    # Load the entire sprite sheet
    sprite_sheet = pygame.image.load(path)
    if flip:
        sprite_sheet = pygame.transform.flip(sprite_sheet, True, False)
    frames = []
    for i in range(num_frames):
        if flip:
            i = num_frames - 1 - i
        frame = get_frame(sprite_sheet, i, frame_width, frame_height)
        scaled_frame = pygame.transform.scale(frame, (frame_width * 2, frame_height * 2))
        frames.append(scaled_frame)
    return frames

enemies = []

debug_mode = True

class Player:
    def __init__(self):
        self.x = (window_width - 32) // 2
        self.y = window_height - 64 - 32
        self.current_dx = 0
        self.vel_y = 0
        self.speed = 5
        self.jump_speed = 10
        self.is_going_right = True
        self.is_jumping = False
        self.is_double_jumping = False

        self.running_right_frames = get_frames("assets/Main Characters/Ninja Frog/Run (32x32).png", 12, False, 32, 32)
        self.running_left_frames = get_frames("assets/Main Characters/Ninja Frog/Run (32x32).png", 12, True, 32, 32)
        self.idle_right_frames = get_frames("assets/Main Characters/Ninja Frog/Idle (32x32).png", 11, False, 32, 32)
        self.idle_left_frames = get_frames("assets/Main Characters/Ninja Frog/Idle (32x32).png", 11, True, 32, 32)
        self.jump_right_frames = get_frames("assets/Main Characters/Ninja Frog/Jump (32x32).png", 1, False, 32, 32)
        self.jump_left_frames = get_frames("assets/Main Characters/Ninja Frog/Jump (32x32).png", 1, True, 32, 32)
        self.djump_right_frames = get_frames("assets/Main Characters/Ninja Frog/Double Jump (32x32).png", 6, False, 32, 32)
        self.djump_left_frames = get_frames("assets/Main Characters/Ninja Frog/Double Jump (32x32).png", 6, True, 32, 32)
        self.hit_right_frames = get_frames("assets/Main Characters/Ninja Frog/Hit (32x32).png", 7, False, 32, 32)
        self.hit_left_frames = get_frames("assets/Main Characters/Ninja Frog/Hit (32x32).png", 7, True, 32, 32)

        self.frame_index = 0
        self.frames = self.idle_right_frames

        self.is_dying = False
    
    def get_collision_rect(self):
        player_height = 32 * 2
        player_top = self.y
        return pygame.Rect(self.x + 18, player_top + 15, player_height - 36, player_height - 15)
    
    def start_dying(self):
        self.frame_index = 0
        self.is_dying = True
        self.dx = 0
        self.current_dx = 0
        if self.is_going_right:
            self.current_dx = -1
        else:
            self.current_dx = 1
        self.vel_y = -self.jump_speed

    def update(self, events):
        
        # React to player control inputs
        for event in events:
            if event.type == pygame.USEREVENT:
                if not self.is_dying or self.frame_index < len(self.frames) - 1:
                    self.frame_index += 1

            if self.is_dying:
                continue

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

        dx = self.current_dx

        # Apply gravity
        self.vel_y = self.vel_y + gravity
        if self.vel_y > 10:
            self.vel_y = 10
        dy = self.vel_y

        # Detect collisions 
        if not self.is_dying:
            collision_rect = self.get_collision_rect()
            for tile_y, lines in enumerate(world_map):
                for tile_x, tile in enumerate(lines):
                    if not tile.isdigit():
                        continue

                    sprite = terrain_dict[tile]
                    tile_rect = pygame.Rect(tile_x * 32, tile_y * 32, sprite.get_width(), sprite.get_height())
                    collided = False

                    # x-axis collision detection
                    if tile_rect.colliderect(collision_rect.left + dx, collision_rect.top, collision_rect.width, collision_rect.height):
                        dx = 0
                        collided = True

                    # y-axis collision detection
                    if tile_rect.colliderect(collision_rect.left, collision_rect.top + dy + 1, collision_rect.width, collision_rect.height):
                        if self.vel_y > 0:
                            dy = tile_rect.top - collision_rect.bottom
                            self.vel_y = 0
                            self.is_jumping = False
                            self.is_double_jumping = False
                        else:
                            dy = tile_rect.bottom - collision_rect.top
                            self.vel_y = 0
                            self.is_jumping = True
                            self.is_double_jumping = False
                        collided = True
                    
                    if collided:
                        break

            # Detect collisions with the enemies
            if not self.is_dying:
                for enemy in enemies:
                    if enemy.is_dying:
                        continue
                    
                    # x-axis collision detection
                    if enemy.collides(
                        collision_rect.left + dx,
                        collision_rect.top,
                        collision_rect.width,
                        collision_rect.height):
                        self.start_dying()

                    # y-axis collision detection
                    elif enemy.collides(
                        collision_rect.left,
                        collision_rect.top + dy + 1,
                        collision_rect.width,
                        collision_rect.height):
                        enemy.frame_index = 0
                        enemy.is_dying = True
                        enemy.dx = 0

        # Move the player 
        self.x = self.x + dx
        self.y = self.y + dy

        # Animation logic
        if self.is_dying:
            if self.is_going_right == True:
                self.frames = self.hit_right_frames
            else:
                self.frames = self.hit_left_frames
        elif self.is_jumping is True:
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

        if not self.is_dying:
            self.frame_index = self.frame_index % len(self.frames)

        self.current_frame = self.frames[self.frame_index]

    def draw(self):
        screen.blit(self.current_frame, (self.x, self.y))

        if debug_mode:
            if self.is_dying:
                color = (255, 0, 0)
            else:
                color = (0, 255, 0)
            pygame.draw.rect(screen, color, self.get_collision_rect(), 1)

class Mushroom:
    def __init__(self, x, y):
        self.idle_frames_right = get_frames("assets/Enemies/Mushroom/Idle (32x32).png", 14, True, 32, 32)
        self.idle_frames_left = get_frames("assets/Enemies/Mushroom/Idle (32x32).png", 14, False, 32, 32)
        self.running_frames_right = get_frames("assets/Enemies/Mushroom/Run (32x32).png", 16, True, 32, 32)
        self.running_frames_left = get_frames("assets/Enemies/Mushroom/Run (32x32).png", 16, False, 32, 32)

        self.frame_index = 0
        self.current_frame = self.idle_frames_right[self.frame_index]

        self.x = x
        self.y = y

        self.idle_counter = -1
        self.dx = 1
        self.next_dx = 0
        self.is_going_right = True

        self.is_dying = False

    def get_collision_rect(self):
        return pygame.Rect(self.x + self.dx + 5, self.y + 25, 64 - 10, 64 - 25)

    def update(self, events):
        for event in events:
            if event.type == pygame.USEREVENT:
                self.frame_index += 1
                self.idle_counter -= 1

        if self.dx > 0:
            self.is_going_right = True
            frames = self.running_frames_right
        elif self.dx < 0:
            self.is_going_right = False
            frames = self.running_frames_left
        else:
            if self.is_going_right == True:
                frames = self.idle_frames_right
            else:
                frames = self.idle_frames_left

        # Edge detection
        if self.dx > 0:
            self.edge_detection_rect = pygame.Rect(self.x + 64, self.y + 64 - 5, 10, 10)
        elif self.dx < 0:
            self.edge_detection_rect = pygame.Rect(self.x - 10, self.y + 64 - 5, 10, 10)
        else:
            self.edge_detection_rect = None

        if self.edge_detection_rect is not None:           
            edge_detection_collided = False
            for tile_y, lines in enumerate(world_map):
                for tile_x, tile in enumerate(lines):
                    if not tile.isdigit():
                        continue
                    sprite = terrain_dict[tile]
                    tile_rect = pygame.Rect(tile_x * 32, tile_y * 32, sprite.get_width(), sprite.get_height())
                    if self.edge_detection_rect.colliderect(tile_rect):
                        edge_detection_collided = True
                        break

            if not edge_detection_collided:
                self.idle_counter = 28
                if self.dx > 0:
                    self.next_dx = -1
                elif self.dx < 0:
                    self.next_dx = 1
                self.dx = 0
        
        # Wall detection
        collision_rect = self.get_collision_rect()
        wall_collided = False
        if self.dx != 0:
            for tile_y, lines in enumerate(world_map):
                for tile_x, tile in enumerate(lines):
                    if not tile.isdigit():
                        continue
                    sprite = terrain_dict[tile]
                    tile_rect = pygame.Rect(tile_x * 32, tile_y * 32, sprite.get_width(), sprite.get_height())
                    if collision_rect.colliderect(tile_rect):
                        wall_collided = True
                        break
            if wall_collided:
                self.idle_counter = 28
                if self.dx > 0:
                    self.next_dx = -1
                elif self.dx < 0:
                    self.next_dx = 1
                self.dx = 0

        if self.idle_counter == 0:
            self.dx = self.next_dx

        self.frame_index = self.frame_index % len(frames)
        self.current_frame = frames[self.frame_index]

        self.x += self.dx      

    def collides(self, x, y, width, height):
        rect = pygame.Rect(x + self.dx, y, width, height)
        return self.get_collision_rect().colliderect(rect)

    def draw(self):
        screen.blit(self.current_frame, (self.x, self.y))

        if debug_mode:
            if self.is_dying:
                color = (255, 0, 0)
            else:
                color = (0, 255, 0)
            pygame.draw.rect(screen, color, self.get_collision_rect(), 1)

# Creating the enemies
for tile_y, lines in enumerate(world_map):
    for tile_x, tile in enumerate(lines):
        if tile == "M":
            enemies.append(Mushroom(tile_x * 32, tile_y * 32))

player = Player()

# Main loop
running = True
while running:

    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            running = False

    player.update(events)
    for enemy in enemies:
        enemy.update(events)

    # Clear the screen
    screen.fill((0, 0, 0))

    # Background tiles
    for y in range(int(window_height / 128) + 1):
        for x in range(int(window_width / 128)):
            screen.blit(background_sprite, (x * 128, y * 128))

    # Wolrd map tiles
    for tile_y, lines in enumerate(world_map):
        for tile_x, tile in enumerate(lines):
            if tile.isdigit():
                screen.blit(terrain_dict[tile], (tile_x * 16 * 2, tile_y * 16 * 2))

    # Player sprite
    for enemy in enemies:
        enemy.draw()
    player.draw()

    # Update the display
    pygame.display.flip()

    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
