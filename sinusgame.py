import sys
import os
import pygame
from pygame.locals import *
import time
import math
import layout
import multiprocessing
import bb_sound

sinewave_game_status = multiprocessing.Value('i', 0)  # 0 = not started, 1 = started, 2 = won

# Some config width height settings
canvas_width = 800
canvas_height = 480
timing = 0
checkTimer = 0  # to not instantly win if you have the correct value match

# Just define some colors we can use
wave_color = pygame.Color(0, 255, 255, 0)
background_color = pygame.Color(0, 0, 0, 0)
win_color = pygame.Color(0, 150, 0, 0)


levels = [  # [amplitude, frequency, translate]
    [70, 1, 0],
    [100, 1.8, 80],
    [40, 0.7, 200]
]

level = 0
speed = 5
marge = 5
translate = 0
frequency = 1
amplitude = 50


def setup():
    pygame.init()
    # Set the window title
    pygame.display.set_caption("Sine Wave")
    pygame.mouse.set_visible(False)

    # Make a screen to see
    global screen
    screen = pygame.display.set_mode((canvas_width, canvas_height), pygame.FULLSCREEN)
    screen.fill(background_color)
    global background_image
    background_image = pygame.image.load("backgroundSinegame.bmp").convert()
    global logo_image
    logo_image = pygame.image.load("logo.png").convert()
    
    # display shit
    font = pygame.font.SysFont("comicsansms", 30)
    text = font.render("Hello, World", True, (0, 128, 0))
    # Make a surface to draw on
    global surface
    surface = pygame.Surface((canvas_width, canvas_height))


def mappingValues(value, leftMin, leftMax, rightMin, rightMax):
    """ mapping a value range to another value range"""
    leftSpan = leftMax - leftMin                            # Figure out how 'wide' each range is
    rightSpan = rightMax - rightMin
    valueScaled = float(value - leftMin) / float(leftSpan)  # Convert the left range into a 0-1 range (float)
    return rightMin + (valueScaled * rightSpan)             # Convert the 0-1 range into a value in the right range.


def control():
    ''' influence the values to play'''
    global amplitude
    global frequency
    global translate

    translate = mappingValues(layout.sinusknob1_value.value, 0, 500, -400, 400)
    frequency = mappingValues(layout.sinusknob2_value.value, 0, 500, 0.1, 5)
    amplitude = mappingValues(layout.sinusknob3_value.value, 0, 500, 0, 220)

#    if event.type == pygame.KEYDOWN:
#        if event.key == pygame.K_w and amplitude < 220:
#            amplitude += 10
#        if event.key == pygame.K_s and amplitude > 0:
#            amplitude -= 10
#        if event.key == pygame.K_q and frequency < 20:
#            frequency += 0.05
#        if event.key == pygame.K_a and frequency > 0.1:
#            frequency -= 0.05
#        if event.key == pygame.K_e and translate < 400:
#            translate += 10
#        if event.key == pygame.K_d and translate > -400:
#            translate -= 10


# punten waarom de golven gecheck worden
punt1, punt2, punt3, punt4, punt5, punt6, punt7 = 0, 100, 200, 300, 500, 600, 700
examplePunt1, examplePunt2, examplePunt3, examplePunt4, examplePunt5, examplePunt6, examplePunt7 = 0, 0, 0, 0, 0, 0, 0
playerPunt1, playerPunt2, playerPunt3, playerPunt4, playerPunt5, playerPunt6, playerPunt7 = 0, 0, 0, 0, 0, 0, 0


def drawExampleWave():
    '''draws the example wave that needs to be matched by the player'''
    global examplePunt1, examplePunt2, examplePunt3, examplePunt4, examplePunt5, examplePunt6, examplePunt7
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
        elif i == punt7:
            examplePunt7 = j
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
    global playerPunt1, playerPunt2, playerPunt3, playerPunt4, playerPunt5, playerPunt6, playerPunt7

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
        elif x == punt7:
            playerPunt7 = y
        surface.set_at(((int(x + translate + playerWavePeriod)), y), wave_color)
    if playerWavePeriod >= canvas_width / frequency:
        playerWavePeriod = 0
    playerWavePeriod += speed


def checkSucces():
    

    check1 = playerPunt1 < examplePunt1 + marge and playerPunt1 > examplePunt1 - marge
    check2 = playerPunt2 < examplePunt2 + marge and playerPunt2 > examplePunt2 - marge
    check3 = playerPunt3 < examplePunt3 + marge and playerPunt3 > examplePunt3 - marge
    check4 = playerPunt4 < examplePunt4 + marge and playerPunt4 > examplePunt4 - marge
    check5 = playerPunt5 < examplePunt5 + marge and playerPunt5 > examplePunt5 - marge
    check6 = playerPunt6 < examplePunt6 + marge and playerPunt6 > examplePunt6 - marge
    check7 = playerPunt7 < examplePunt7 + marge and playerPunt7 > examplePunt7 - marge

    if check1 and check2 and check3 and check4 and check5 and check6 and check7:
        global checkTimer
        checkTimer += 1

        if checkTimer > 6:
            # for an even start of the waves the following reset:
            global level
            bb_sound.play_good_sound.value = 1
            level += 1

            if level == len(levels):
                sinewave_game_status.value = 2

            return True
    else:
        checkTimer = 0


def overlay():
    surface.blit(font.render("level:" + str(level), True, (255, 0, 0)), (0, 0))
    surface.blit(font.render("Amplitude to match:" + str(levels[level][0]) + "  amplitude:" + str(amplitude), True, (255, 0, 0)), (0, 20))
    surface.blit(font.render("Frequency to match:" + str(levels[level][1]) + "frequency :" + str(frequency), True, (255, 0, 0)), (0, 40))
    surface.blit(font.render("translate to match:" + str(levels[level][2]) + "  translate:" + str(translate), True, (255, 0, 0)), (0, 60))


# Simple main loop
def main():
    setup()
    # overlay()  # display shit // maar gaat vooralsnog kapot
    while True:
        time.sleep(0.005)
        for event in pygame.event.get():
            if (event.type == QUIT):
                pygame.display.quit()
                sys.exit(0)
                return False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.display.quit()
                    sys.exit(0)
                    return False

        if sinewave_game_status.value == 0:     # keep the screen black until the game is started
            surface.fill(background_color)

        if sinewave_game_status.value == 1:     # Play the game
            # Redraw the background
            surface.blit(background_image, [0, 0])
            drawPlayerWave()
            drawExampleWave()
            control()
            if checkSucces():
                print("level won!!")
                # goedezo-jongon-animatie
                surface.fill(win_color)
                screen.blit(surface, (0, 0))
                pygame.display.flip()
                time.sleep(1)

        elif sinewave_game_status.value == 2:   # Display the logo once the game is won
            surface.blit(logo_image, [0, 0])

        # Put the surface we draw on, onto the screen
        screen.blit(surface, (0, 0))
        # Show it.
        pygame.display.flip()


if __name__ == '__main__':
    layout_process = multiprocessing.Process(target=layout.main)
    layout_process.start()
    sinewave_game_status.value = 1
    main()
    layout_process.terminate()
