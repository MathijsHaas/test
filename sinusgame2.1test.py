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
wave_color = pygame.Color(0, 255, 255, 0)
background_color = pygame.Color(0, 0, 0, 0)
win_color = pygame.Color(0, 150, 0, 0)


pygame.init()
# Set the window title
pygame.display.set_caption("Sine Wave")

# Make a screen to see
screen = pygame.display.set_mode((canvas_width, canvas_height))
screen.fill(background_color)
background_image = pygame.image.load("backgroundSinegame.bmp").convert()

# Make a surface to draw on
surface = pygame.Surface((canvas_width, canvas_height))


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
        if event.key == pygame.K_a and frequency > 0.1:
            frequency -= 0.05
        if event.key == pygame.K_e and translate < 400:
            translate += 10
        if event.key == pygame.K_d and translate > -400:
            translate -= 10


# punten waarom de golven gecheck worden
punt1, punt2, punt3, punt4, punt5, punt6 = 50, 100, 300, 500, 600, 700
examplePunt1, examplePunt2, examplePunt3, examplePunt4, examplePunt5, examplePunt6 = 0, 0, 0, 0, 0, 0
playerPunt1, playerPunt2, playerPunt3, playerPunt4, playerPunt5, playerPunt6 = 0, 0, 0, 0, 0, 0


def drawExampleWave():
    '''draws the example wave that needs to be matched by the player'''
    global examplePunt1, examplePunt2, examplePunt3, examplePunt4, examplePunt5, examplePunt6
    global exampleWavePeriod
    for i in range(-2 * canvas_width, canvas_width):
        j = int((canvas_height / 2) + levels[level][0] * math.sin(levels[level][1] * ((float(i) / canvas_width) * (2 * math.pi))))
        if i == punt1:
            examplePunt1 = j
        elif i == punt2:
            examplePunt2 = j
        elif i == punt3:
            examplePunt3 = j
        elif i == punt4:
            examplePunt4 = j
        elif i == punt5:
            examplePunt5 = j
        elif i == punt6:
            examplePunt6 = j
        surface.set_at(((i + levels[level][2] + exampleWavePeriod), j), wave_color)
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
    global playerPunt1, playerPunt2, playerPunt3, playerPunt4, playerPunt5, playerPunt6

    for x in range(-3 * canvas_width, 2 * canvas_width):
        y = int((canvas_height / 2) + amplitude * math.sin(frequency * ((float(x) / canvas_width) * (2 * math.pi))))
        if x == punt1:
            playerPunt1 = y
        elif x == punt2:
            playerPunt2 = y
        elif x == punt3:
            playerPunt3 = y
        elif x == punt4:
            playerPunt4 = y
        elif x == punt5:
            playerPunt5 = y
        elif x == punt6:
            playerPunt6 = y
        surface.set_at(((x + translate + playerWavePeriod), y), wave_color)
    if playerWavePeriod >= canvas_width / frequency:
        playerWavePeriod = 0
    playerWavePeriod += speed


def checkSucces():
    marge = 2

    check1 = playerPunt1 < examplePunt1 + marge and playerPunt1 > examplePunt1 - marge
    check2 = playerPunt2 < examplePunt2 + marge and playerPunt2 > examplePunt2 - marge
    check3 = playerPunt3 < examplePunt3 + marge and playerPunt3 > examplePunt3 - marge
    check4 = playerPunt4 < examplePunt4 + marge and playerPunt4 > examplePunt4 - marge
    check5 = playerPunt5 < examplePunt5 + marge and playerPunt5 > examplePunt5 - marge
    check6 = playerPunt6 < examplePunt6 + marge and playerPunt6 > examplePunt6 - marge

    if check1 and check2 and check3 and check4 and check5 and check6:
        global checkTimer
        checkTimer += 1

        if checkTimer > 30:
            # for an even start of the waves the following reset:
            global level
            level += 1
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
   # overlay()  # display shit // maar gaat vooralsnog kapot

    time.sleep(0.02)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if level < len(levels):
        # Redraw the background
        surface.fill(background_color)
        surface.blit(background_image, [0, 0])
        drawPlayerWave()
        drawExampleWave()
        control()
        if checkSucces():
            print("level won!!")
            # bb_sound.play_good_sound.value = 1
            # goedezo-jongon-animatie
            surface.fill(win_color)
            screen.blit(surface, (0, 0))
            pygame.display.flip()
            time.sleep(1)

        # Put the surface we draw on, onto the screen
        screen.blit(surface, (0, 0))
        # Show it.
        pygame.display.flip()
    if level == len(levels) - 1:
        # display Blackbox logo
        pass
