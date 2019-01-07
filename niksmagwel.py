import pygame
import time
import math


# Some config width height settings
canvas_width = 640
canvas_height = 480

# Just define some colors we can use
color = pygame.Color(255, 255, 0, 0)
background_color = pygame.Color(0, 0, 0, 0)


pygame.init()
# Set the window title
pygame.display.set_caption("Sine Wave")

# Make a screen to see
screen = pygame.display.set_mode((canvas_width, canvas_height))
screen.fill(background_color)

# Make a surface to draw on
surface = pygame.Surface((canvas_width, canvas_height))
surface.fill(background_color)

translate = 1
# Simple main loop
running = True
while running:
    time.sleep(0.02)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Redraw the background
    surface.fill(background_color)

    # Update sine wave
    frequency = 1
    amplitude1 = 50  # in px
    speed = 1
    amplitude = int((canvas_height / 2) + amplitude1 * math.sin(frequency * ((3 / canvas_width) * (2 * math.pi) + (speed * time.time()))))

    for x in range(-canvas_width, canvas_width):
        y = int((canvas_height / 2) + amplitude * math.sin(frequency * ((float(x) / canvas_width) * (2 * math.pi) + (speed * time.time()))))
        surface.set_at((x + translate, y), color)

    translate = int((canvas_height / 2) + amplitude * math.sin(frequency * ((float(x) / canvas_width) * (2 * math.pi) + (3 * time.time()))))

    amplitude = int((canvas_height / 2) + amplitude * math.sin(frequency * ((float(x) / canvas_width) * (2 * math.pi) + (speed * time.time()))))

    for i in range(0, canvas_width):
        j = int((canvas_height / 2) + 40 * math.sin(2 * ((float(i) / canvas_width) * (2 * math.pi) + (speed * time.time()))))
        surface.set_at((i, j), color)

    # Put the surface we draw on, onto the screen
    screen.blit(surface, (0, 0))

    # Show it.
    pygame.display.flip()
