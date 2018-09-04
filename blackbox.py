# Main control

# importing the differtent seperate games
import multiprocessing
import simon_says
import pluggenspel
import six_buttons
import draaiknoppen
import color_follow
import RGB_game

import pygame  # for music
import datetime  # to keep track of the deadline
from Adafruit_LED_Backpack import SevenSegment  # for clock display

# clock via SDA/SCL
segment = SevenSegment.SevenSegment(address=0x70)

# geluid
pygame.mixer.init()
won_the_box_sound = pygame.mixer.Sound("won_the_box_sound.ogg")
lost_the_box_sound = pygame.mixer.Sound("lost_the_box_sound.ogg")

# 0 = not started yet
# 1 = started
# 2 = finished

'''
Every game is it's own process in its seperate file.
Each game has a game_won variable that is an multiprocessing value we can acces.
This game_won value turns 1 when the game is won and thus the next game can start.

Each game also has its own variable in the main loop to make sure the process only starts once.

'''

# set when top_buttons.top_status.value == 1 (thus the game starts)
startTime = None
deadline = None
minutesToPlay = datetime.deltatime(minutes=60)


def showTime():
    ''' Show the time on the clock on top of the box'''
    segment.begin()

    stopTime = datetime.datetime.now()
    timePlayed = str(stopTime - startTime)

    tensOfMinutes = timePlayed[2]
    onesOfMinutes = timePlayed[3]
    tensOfSeconds = timePlayed[5]
    OnesOfSeconds = timePlayed[6]

    print ("played in: ", tensOfMinutes, OnesOfMinutes, tensOfSeconds, OnesOfSeconds)

    # setting the time as induvidual caracters to send to the clock display
    segment.set_digit(0, tensOfMinutes)
    segment.set_digit(1, onesOfMinutes)
    segment.set_digit(2, tensOfSeconds)
    segment.set_digit(3, OnesOfSeconds)
    segment.set_colon(True)  # Toggle colon

    # update the display LEDs.
    segment.write_display()


def BlackBoxWon():
    showTime()
    pygame.mixer.Sound.play(won_the_box_sound)
    # Timerstrip op groene wave


def BlackboxLost():
    showtime()
    pygame.mixer.Sound.play(lost_the_box_sound)
    # Timerstrip op rode wave


def main():
    # at the start, no games ar started.
    six_buttons_started = False
    pluggenspel_started = False
    RGB_game_started = False
    simon_says_started = False
    draaiknoppen_started = False
    sinusspel_started = False
    color_follow_started = False

    # this while loop keeps running to manage the game progression
    while True:
        # start plug game after the six buttons are pushed togheter
        if top_buttons.top_status.value == 1 and pluggenspel_started == False:
            pluggenspel_process = multiprocessing.Process(target=pluggenspel.main)
            pluggenspel_process.start()
            pluggenspel_started = True
            global startTime  # record once when the game started
            startTime = datetime.datetime.now()
            global deadline  # set the deadline for when the game must be finished
            deadline = datetime.datetime.now() + minutesToPlay
            # TURN ON BACKLIGHT

        # Start the RGB game after all 6 plugs are connected correctly
        if pluggenspel.game_won.value == 1 and pluggenspel_started == False:
            RGB_process = multiprocessing.Process(target=RGB_game.main)
            RGB_process.start()
            pluggenspel_started = True

        # start Simon Says after all RGB game colors are machted correctly
        if RGB_game.game_won.value == 1 and simon_says_started == False:
            simon_says_process = multiprocessing.Process(target=simon_says.main)
            simon_says_process.start()
            simon_says_started = True

        if simon_says.game_won.value == 1:
            top_buttons.RGB_half_status.value = 1

        # start the big turning knobs at the same time as the plug game.
        if top_buttons.top_status.value == 1 and draaiknoppen_started == False:
            draaiknoppen_process = multiprocessing.Process(target=draaiknoppen.main)
            draaiknoppen_process.start()
            draaiknoppen_started = True

        if draaiknoppen.game_won.value == 1 and sinusspel_started == False:
            # start sinusspel
            sinusspel_started = True

        # start Color follow after dhe sinus game is won
        if sinusspel.game_won.value == 1 and draaiknoppen_started == False:
            color_follow_process = multiprocessing.Process(target=color_follow.main)
            color_follow_process.start()
            draaiknoppen_started = True

        if color_follow.game_won.value == 1:
            top_buttons.sinus_half_status.value = 1

        # BlackBox Lost
        if timedate.timedate.now() > deadline:
            BlackBoxLost()

        # BlackBox Won
        if Won:
            BlackBoxWon()


if __name__ == "__main__":
    main()
