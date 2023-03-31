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

# Load the entire sprite sheet
sprite_sheet_path = "assets/Main Characters/Ninja Frog/Run (32x32).png"
sprite_sheet = pygame.image.load(sprite_sheet_path)

# Set the frame dimensions and the number of frames
frame_width = 32
frame_height = 32
num_frames = 12

# Extract individual frames from the sprite sheet
def get_frame(index):
    rect = pygame.Rect(index * frame_width, 0, frame_width, frame_height)
    frame = pygame.Surface(rect.size).convert()
    frame.blit(sprite_sheet, (0, 0), rect)
    frame.set_colorkey((0, 0, 0), pygame.RLEACCEL)
    return frame

# Scale the frames 2 times bigger
scaled_frames = []
for i in range(num_frames):
    frame = get_frame(i)
    scaled_frame = pygame.transform.scale(frame, (frame_width * 2, frame_height * 2))
    scaled_frames.append(scaled_frame)

# Set the animation loop time and initialize the timer
animation_time = 700
pygame.time.set_timer(pygame.USEREVENT, animation_time // num_frames)

# Initialize the frame indexi
frame_index = 0

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.USEREVENT:
            # Update the frame index and loop the sequence
            frame_index = (frame_index + 1) % num_frames

    # Clear the screen
    screen.fill((0, 0, 0))

    # Get the current frame and its size
    current_frame = scaled_frames[frame_index]
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
