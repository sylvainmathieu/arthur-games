import pygame
import sys
import os

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
    "1                       1",
    "1                       1",
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

# Set the frame dimensions and the number of frames
frame_width = 32
frame_height = 32

# Extract individual frames from the sprite sheet
def get_frame(sprite_sheet, index):
    rect = pygame.Rect(index * frame_width, 0, frame_width, frame_height)
    frame = pygame.Surface(rect.size).convert()
    frame.blit(sprite_sheet, (0, 0), rect)
    frame.set_colorkey((0, 0, 0), pygame.RLEACCEL)
    return frame

def get_frames(path, num_frames, flip):
    # Load the entire sprite sheet
    sprite_sheet = pygame.image.load(path)
    if flip:
        sprite_sheet = pygame.transform.flip(sprite_sheet, True, False)
    frames = []
    for i in range(num_frames):
        frame = get_frame(sprite_sheet, i)
        scaled_frame = pygame.transform.scale(frame, (frame_width * 2, frame_height * 2))
        frames.append(scaled_frame)
    return frames

running_right_frames = get_frames("assets/Main Characters/Ninja Frog/Run (32x32).png", 12, False)
running_left_frames = get_frames("assets/Main Characters/Ninja Frog/Run (32x32).png", 12, True)
idle_right_frames = get_frames("assets/Main Characters/Ninja Frog/Idle (32x32).png", 11, False)
idle_left_frames = get_frames("assets/Main Characters/Ninja Frog/Idle (32x32).png", 11, True)
jump_right_frames = get_frames("assets/Main Characters/Ninja Frog/Jump (32x32).png", 1, False)
jump_left_frames = get_frames("assets/Main Characters/Ninja Frog/Jump (32x32).png", 1, True)
djump_right_frames = get_frames("assets/Main Characters/Ninja Frog/Double Jump (32x32).png", 6, False)
djump_left_frames = get_frames("assets/Main Characters/Ninja Frog/Double Jump (32x32).png", 6, True)

# Set the animation loop time and initialize the timer
pygame.time.set_timer(pygame.USEREVENT, 58)

# Initialize the frame index
player_frame_index = 0
player_frames = idle_right_frames

player_x = (window_width - frame_width) // 2
player_y = window_height - 64 - 32

dx = 0
current_dx = 0
vel_y = 0
player_speed = 5
player_jump_speed = 10
gravity = 0.6

is_going_right = True
is_jumping = False
is_double_jumping = False

# stone_rect = pygame.Rect(window_width // 2, window_height - 100, 48 * 2, 16 * 2)

clock = pygame.time.Clock()

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                current_dx = player_speed
                is_going_right = True
            if event.key == pygame.K_LEFT:
                current_dx = -player_speed
                is_going_right = False
            if event.key == pygame.K_UP and not is_jumping and vel_y == 0 and not is_double_jumping:
                vel_y = -player_jump_speed
                is_jumping = True
                is_double_jumping = False
            elif event.key == pygame.K_UP and is_jumping and vel_y <= 3 and not is_double_jumping:
                vel_y = -(player_jump_speed * 1.2)
                is_double_jumping = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT and current_dx > 0:
                current_dx = 0
            elif event.key == pygame.K_LEFT and current_dx < 0:
                current_dx = 0
        if event.type == pygame.USEREVENT:
            # Update the frame index and loop the sequence
            player_frame_index += 1

    dx = current_dx

    # Clear the screen
    screen.fill((0, 0, 0))

    vel_y = vel_y + gravity
    if vel_y > 10:
        vel_y = 10
    dy = vel_y

    # floor detection
    player_height = frame_height * 2
    player_top = player_y
    player_bottom = player_top + player_height

    player_collision_rect = pygame.Rect(player_x + 8, player_top + 10, player_height - 16, player_height - 10)

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
                if vel_y > 0:
                    dy = tile_rect.top - player_bottom
                    vel_y = 0
                    is_jumping = False
                    is_double_jumping = False
                else:
                    dy = tile_rect.bottom - player_top
                    vel_y = 0
                    is_jumping = True
                    is_double_jumping = False
                collided = True
            
            if collided:
                break

    player_x = player_x + dx
    player_y = player_y + dy

    # Animation logic
    if is_jumping is True:
        if is_double_jumping:
            if is_going_right == True:
                player_frames = djump_right_frames
            else:
                player_frames = djump_left_frames
        else:
            if is_going_right == True:
                player_frames = jump_right_frames
            else:
                player_frames = jump_left_frames
    else:
        if dx == 0:
            if is_going_right == True:
                player_frames = idle_right_frames
            else:
                player_frames = idle_left_frames
        elif dx > 0:
            player_frames = running_right_frames
        else:
            player_frames = running_left_frames

    player_frame_index = player_frame_index % len(player_frames)

    current_frame = player_frames[player_frame_index]

    # Draw the sprites
    for tile_y, lines in enumerate(world_map):
        for tile_x, tile in enumerate(lines):
            if tile != " ":
                screen.blit(terrain_dict[tile], (tile_x * 16 * 2, tile_y * 16 * 2))
    screen.blit(current_frame, (player_x, player_y))

    # Update the display
    pygame.display.flip()

    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
