import pygame
import sys
import os

# Initialize Pygame
pygame.init()

# Set window dimensions and title
window_width = 800
window_height = 600
window_title = "Image Display"

# Create the window
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption(window_title)

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

terrain = pygame.image.load("assets/Terrain/Terrain (16x16).png") 

def get_sprite(image, x, y, w, h):
    rect = pygame.Rect(x, y, w, h)
    frame = pygame.Surface(rect.size).convert()
    frame.blit(image, (0, 0), rect)
    frame.set_colorkey((0, 0, 0), pygame.RLEACCEL)
    return pygame.transform.scale(frame, (w * 2, h * 2))

horizontal_brown_stone = get_sprite(terrain, 192, 0, 48, 16)

# Set the animation loop time and initialize the timer
pygame.time.set_timer(pygame.USEREVENT, 58)

# Initialize the frame index
player_frame_index = 0
player_frames = idle_right_frames

player_x = (window_width - frame_width) // 2
player_y = window_height - 64

dx = 0
vel_y = 0
player_speed = 5
player_jump_speed = 10
gravity = 0.5

is_going_right = True
is_jumping = False
is_double_jumping = False

stone_rect = pygame.Rect(window_width // 2, window_height - 100, 48 * 2, 16 * 2)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                dx = player_speed
                is_going_right = True
            elif event.key == pygame.K_LEFT:
                dx = -player_speed
                is_going_right = False
            elif event.key == pygame.K_SPACE and vel_y == 0:
                vel_y = -player_jump_speed
                is_jumping = True
            elif event.key == pygame.K_SPACE and is_jumping and not is_double_jumping:
                vel_y = -player_jump_speed
                is_double_jumping = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                dx = 0
            elif event.key == pygame.K_LEFT:
                dx = 0
        elif event.type == pygame.USEREVENT:
            # Update the frame index and loop the sequence
            player_frame_index += 1

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
    if player_bottom + dy >= window_height:
        player_y = window_height - player_height
        vel_y = 0
        is_jumping = False
        is_double_jumping = False

    # x-axis collision detection
    if stone_rect.colliderect(player_x + dx, player_y, frame_width * 2, frame_height * 2):
        dx = 0

    # y-axis collision detection
    if stone_rect.colliderect(player_x, player_y + dy, frame_width * 2, frame_height * 2):
        if vel_y > 0:
            dy = stone_rect.top - player_bottom
            vel_y = 0
            is_jumping = False
            is_double_jumping = False
        else:
            dy = stone_rect.bottom - player_top
            vel_y = 0
            is_jumping = True
            is_double_jumping = False

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
    screen.blit(horizontal_brown_stone, (stone_rect.x, stone_rect.y))
    screen.blit(current_frame, (player_x, player_y))

    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(player_x, player_top, player_height, player_height), 1)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
