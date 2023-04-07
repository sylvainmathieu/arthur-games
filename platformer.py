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

# Set the animation loop time and initialize the timer
pygame.time.set_timer(pygame.USEREVENT, 58)

# Initialize the frame index
player_frame_index = 0

player_frames = idle_right_frames

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                player_frames = running_right_frames
            elif event.key == pygame.K_LEFT:
                player_frames = running_left_frames
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                player_frames = idle_right_frames
            elif event.key == pygame.K_LEFT:
                player_frames = idle_left_frames
        elif event.type == pygame.USEREVENT:
            # Update the frame index and loop the sequence
            player_frame_index += 1
            
    player_frame_index = player_frame_index % len(player_frames)

    # Clear the screen
    screen.fill((0, 0, 0))

    # Get the current frame and its size    
    current_frame = player_frames[player_frame_index]
    frame_width, frame_height = current_frame.get_size()

    # Calculate the frame position
    frame_x = (window_width - frame_width) // 2
    frame_y = (window_height - frame_height) // 2

    # Draw the current frame
    screen.blit(current_frame, (frame_x, frame_y))

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
