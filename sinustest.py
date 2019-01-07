
import pygame
import sys
import math
import time

plotPoints = []
period = 600                # width of one wave
amplitude = 50             # hight of the wave
horizontalTranslation = 30  # where the wave starts
wavespeed = 3               # speed to the right
screenHight = 480
screenWidth = 600

pygame.init()
screen = pygame.display.set_mode([screenWidth, screenHight])

for x in range(0, screenWidth, 3):
    y = int(math.sin(x / period * 4 * math.pi) * amplitude + screenHight / 2)
    plotPoints.append([x, y])
    print(x)


while True:
    time.sleep(0.05)
    screen.fill([0, 0, 0])
    for i in range(len(plotPoints)):
        if plotPoints[i][0] == 0:
            plotPoints[i][1] = plotPoints[len(plotPoints) - 1][1]
        else:
            plotPoints[len(plotPoints) - i][1] = plotPoints[len(plotPoints) - i - 2][1]
    pygame.draw.lines(screen, [255, 255, 255], False, plotPoints, 2)
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()


def drawPlayerWave():  # the wave that the influences player
    pass


def drawGameWave():  # the wave the player needs to match
    pass
