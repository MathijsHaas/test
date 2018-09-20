# Main control
from __future__ import absolute_import, division, print_function, \
    unicode_literals
try:
    from IOPi import IOPi
except ImportError:
    print("Failed to import IOPi from python system path")
    print("Importing from parent folder instead")
    try:
        import sys
        sys.path.append("..")
        from IOPi import IOPi
    except ImportError:
        raise ImportError(
            "Failed to import library from parent folder")
import buttonlayout  # what button is connected to what pin
import ledcontrol  # where the led strips are controled and combined to send to the fadecandy
import multiprocessing  # to spawn each game as a separate process
from pygame import mixer  # for sound
import datetime  # to keep track of the deadline
from Adafruit_LED_Backpack import SevenSegment  # for clock display

# importing the differtent seperate games
import simon_says
import plugs_game
import top_buttons
import color_follow
import RGB_game

# IO PI PLUS shield setup
iobus1 = IOPi(0x20)  # bus 1 will be inputs
iobus2 = IOPi(0x21)  # bus 2 will be outputs

# inputs op bus 1
iobus1.set_port_direction(0, 0xFF)
iobus1.set_port_pullups(0, 0xFF)
iobus1.set_port_direction(1, 0xFF)
iobus1.set_port_pullups(1, 0xFF)

# Outputs op bus 2
iobus2.set_port_direction(0, 0x00)
iobus2.write_port(0, 0x00)
iobus2.set_port_direction(1, 0x00)
iobus2.write_port(1, 0x00)

# clock via SDA/SCL
segment = SevenSegment.SevenSegment(address=0x70)

# Sound
mixer.init()
won_the_box_sound = mixer.Sound("won_the_box_sound.ogg")
lost_the_box_sound = mixer.Sound("lost_the_box_sound.ogg")
good_sound = mixer.Sound("good_sound.ogg")

game_status = multiprocessing.Value('i', 0)
# 0 = not started yet
# 1 = started
# 2 = black box won within time
# 3 = black box lost

'''
Every game is it's own process in its seperate file.
Each game has a game_won variable that is an multiprocessing value we can acces.
This game_won value turns 1 when the game is won and thus the next game can start.

Each game also has its own ..._started variable in the main loop to make sure the process only starts once.

'''

# these are set when top_buttons.top_status.value == 1 (thus the game starts)
startTime = None
deadline = None
minutesToPlay = 60
deltaMinutes = datetime.deltatime(minutes=minutesToPlay)

spy_knobs = buttonlayout.spy_knobs
relais = buttonlayout.relais


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


def blackBoxWon():
    game_status.value = 3
    showTime()
    mixer.Sound.play(won_the_box_sound)
    while true:  # the game is won, this happens till a reset
        pass


def blackBoxLost():
    game_status.value = 4
    showtime()
    mixer.Sound.play(lost_the_box_sound)
    while true:  # the game is lost, this happens till a reset
        pass


def boxStart():
    ''' what happens at the start, after the six buttons are pushed '''
    game_status.value = 1
    global startTime  # record once when the game started
    startTime = datetime.datetime.now()
    global deadline  # set the deadline for when the game must be finished
    deadline = datetime.datetime.now() + deltaMinutes
    iobus2.write_pin(relais)  # put on back- and bottomlight


def main():
    # at the start, no games ar started.
    top_buttons_started = False
    plugs_game_started = False
    RGB_game_started = False
    simon_says_started = False
    spy_knobs_started = False
    sinus_game_started = False
    color_follow_started = False

    # this while loop keeps running to manage the game progression
    while True:
        # loop background sound
        # start a process to check the top buttons
        if top_buttons.top_status.value == 0 and top_buttons_started == False:
            top_buttons_process = multiprocessing.Process(target=top_buttons.main)
            top_buttons_process.start()
            top_buttons_started = True

        # start plug game after the six buttons are pushed togheter
        if top_buttons.top_status.value == 1 and plugs_game_started == False:
            plugs_game_process = multiprocessing.Process(target=plugs_game.main)
            plugs_game_process.start()
            plugs_game_started = True
            boxStart()

        # Start the RGB game after all 6 plugs are connected correctly
        if plugs_game.game_won.value == 1 and RGB_game_started == False:
            RGB_game_process = multiprocessing.Process(target=RGB_game.main)
            RGB_game_process.start()
            RGB_game_started = True

        # start Simon Says after all RGB game colors are machted correctly
        if RGB_game.game_won.value == 1 and simon_says_started == False:
            simon_says_process = multiprocessing.Process(target=simon_says.main)
            simon_says_process.start()
            simon_says_started = True

        if simon_says.game_won.value == 1:
            top_buttons.RGB_half_status.value = 1

        # start the big turning knobs at the same time as the plug game.
        if top_buttons.top_status.value == 1 and iobus1.read_pin(spy_knobs) == 0 and spy_knobs_started == False:
            spy_knobs_process = multiprocessing.Process(target=spy_knobs.main)
            spy_knobs_process.start()
            spy_knobs_started = True

        # start the sinus game
        if spy_knobs.game_won.value == 1 and sinus_game_started == False:
            sinus_game_process = multiprocessing.Process(target=sinus_game.main)
            sinus_game_process.start()
            sinus_game_started = True

        # start Color follow after the sinus game is won
        if sinus_game.game_won.value == 1 and collor_follow_started == False:
            color_follow_process = multiprocessing.Process(target=color_follow.main)
            color_follow_process.start()
            color_follow_started = True

        if color_follow.game_won.value == 1:
            top_buttons.sinus_half_status.value = 1

        # BlackBox Lost
        if timedate.timedate.now() > deadline:
            blackBoxLost()

        # BlackBox Won
        if top_buttons.top_status.value == 2:
            blackBoxWon()


if __name__ == "__main__":
    main()
