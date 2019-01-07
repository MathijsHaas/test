import pygame
import time
import math

import multiprocessing


# Some config width height settings
canvas_width = 800
canvas_height = 480
timing = 0
checkTimer = 0  # to not instantly win if you have the correct value match

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

levels = [  # [amplitude, frequency, translate]
    [70, 1, 0],
    [100, 1.8, 80],
    [40, 0.7, 200]
]

# display shit
font = pygame.font.SysFont("comicsansms", 30)
text = font.render("Hello, World", True, (0, 128, 0))

level = 0
speed = 5
translate = 0
frequency = 1
amplitude = 50


def control():
    ''' influence the values to play'''
    global amplitude
    global frequency
    global translate

    # translate = sinusknob1_value.value
    # frequency = sinusknob2_value.value
    # amplitude = sinusknob3_value.value

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_w and amplitude < 220:
            amplitude += 10
        if event.key == pygame.K_s and amplitude > 0:
            amplitude -= 10
        if event.key == pygame.K_q and frequency < 20:
            frequency += 0.05
        if event.key == pygame.K_a and frequency > 0:
            frequency -= 0.05
        if event.key == pygame.K_e and translate < 400:
            translate += 10
        if event.key == pygame.K_d and translate > -400:
            translate -= 10


def drawExampleWave():
    '''draws the example wave that needs to be matched by the player'''
    global exampleWavePeriod
    for i in range(-2 * canvas_width, canvas_width):
        j = int((canvas_height / 2) + levels[level][0] * math.sin(levels[level][1] * ((float(i) / canvas_width) * (2 * math.pi))))
        surface.set_at(((i + levels[level][2] + exampleWavePeriod), j), color)
    if exampleWavePeriod >= canvas_width / levels[level][1]:
        exampleWavePeriod = 0
    exampleWavePeriod += speed


playerWavePeriod = 0
exampleWavePeriod = 0


def drawPlayerWave():
    ''' draw the wave the player controls'''
    global timing
    global playerWavePeriod
    global translate

    for x in range(-2 * canvas_width, 2 * canvas_width):
        y = int((canvas_height / 2) + amplitude * math.sin(frequency * ((float(x) / canvas_width) * (2 * math.pi))))
        surface.set_at(((x + translate + playerWavePeriod), y), color)
    if playerWavePeriod >= canvas_width / frequency:
        playerWavePeriod = 0
    playerWavePeriod += speed


def checkSucces():
    amplitudeMarge = 3
    frequencyMarge = 0.3
    translateMarge = 5
    global translate
    global playerWavePeriod
    global exampleWavePeriod
    '''check if the playerwave is close enough to the example wave to win the level'''
    amplitudeCheck = amplitude < levels[level][0] + amplitudeMarge and amplitude > levels[level][0] - amplitudeMarge
    frequencyCheck = frequency < levels[level][1] + frequencyMarge and frequency > levels[level][1] - frequencyMarge
    translateCheck = translate < levels[level][2] + translateMarge and translate > levels[level][2] - translateMarge

    if amplitudeCheck and frequencyCheck and translateCheck:
        global checkTimer
        checkTimer += 1
        if checkTimer > 20:
            # for an even start of the waves the following reset:
            translate = 0
            playerWavePeriod = 0
            exampleWavePeriod = 0
            return True
    else:
        checkTimer = 0


def overlay():
    screen.blit(font.render("level:" + str(level), True, (255, 0, 0)), (0, 0))
    screen.blit(font.render("Amplitude to match:" + str(levels[level][0]) + "  amplitude:" + str(amplitude), True, (255, 0, 0)), (0, 20))
    screen.blit(font.render("Frequency to match:" + str(levels[level][1]) + "frequency :" + str(frequency), True, (255, 0, 0)), (0, 40))
    screen.blit(font.render("translate to match:" + str(levels[level][2]) + "  translate:" + str(translate), True, (255, 0, 0)), (0, 60))
    pygame.display.update()


# Simple main loop
running = True
while running:
    overlay()  # display shit
    time.sleep(0.02)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Redraw the background
    surface.fill(background_color)

    if level < len(levels):
        drawPlayerWave()
        drawExampleWave()
        control()
        if checkSucces():
            print("level won!!")
            level += 1
            # bb_sound.play_good_sound.value = 1
            # goedezo-jongon-animatie

        # Put the surface we draw on, onto the screen
        screen.blit(surface, (0, 0))
        # Show it.
        pygame.display.flip()
    if level == len(levels) - 1:
        # display Blackbox logo
        pass
