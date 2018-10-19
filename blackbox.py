
from Adafruit_LED_Backpack import SevenSegment


# Main control
import ledcontrol  # where the led strips are controled and combined to send to the fadecandy
import multiprocessing  # to spawn each game as a separate process
from pygame import mixer  # for sound
import datetime  # to keep track of the deadline
import layout
import time

# importing the differtent seperate games
import top_buttons
import plugs_game
import RGB_game
import simon_says
import sinus_game
import color_follow


# -------------- SETUP ------------------------------------------------------------------

# clock via SDA/SCL
segment = SevenSegment.SevenSegment(address=0x70)

# Sound
mixer.init()
background_sound = mixer.Sound("sound_background.ogg")
won_the_box_sound = mixer.Sound("sound_win_box.ogg")
lost_the_box_sound = mixer.Sound("sound_lost_box.ogg")
good_sound = mixer.Sound("sound_good.ogg")

game_status = multiprocessing.Value('i', 0)
# 0 = not started yet
# 1 = started
# 2 = black box won within time
# 3 = black box lost

top_buttons_started = False
plugs_game_started = False
RGB_game_started = False
simon_says_started = False
sinus_game_started = False
color_follow_started = False

# the voltages needed to be measured to bypass the game (remember the multiprocessing.value is * 1000)
plug_bypass = 1000
RGB_bypass = 1500
simon_says_bypass = 2000
turning_knobs_bypass = 2500
sinus_game_bypass = 3000
color_follow_bypass = 3500

'''
Every game is it's own process in its seperate file.
Each game has a game_won variable that is
 an multiprocessing value we can acces.
This game_won value turns 1 when the game is won and thus the next game can start.

Each game also has its own ..._started variable in the main loop to make sure the process only starts once.

'''
# -------------- PARAMETERS ------------------------------------------------------------------

# these are set when top_buttons.top_status.value == 1 (thus the game starts)
startTime = None
deadline = None
minutesToPlay = 60
deltaMinutes = datetime.timedelta(minutes=minutesToPlay)

# ------------- FUNCTIONS FOR IN THE GAME ------------------------------------------------------


def showTime():
    ''' Show the time on the clock on top of the box'''
    segment.begin()

    stopTime = datetime.datetime.now()
    timePlayed = str(stopTime - startTime)

    tensOfMinutes = timePlayed[2]
    onesOfMinutes = timePlayed[3]
    tensOfSeconds = timePlayed[5]
    onesOfSeconds = timePlayed[6]

    print ("played in: ", tensOfMinutes, onesOfMinutes, tensOfSeconds, onesOfSeconds)

    # setting the time as induvidual caracters to send to the clock display
    segment.set_digit(0, tensOfMinutes)
    segment.set_digit(1, onesOfMinutes)
    segment.set_digit(2, tensOfSeconds)
    segment.set_digit(3, onesOfSeconds)
    segment.set_colon(True)  # Toggle colon

    # update the display LEDs.
    segment.write_display()


def blackBoxWon():
    game_status.value = 3
    mixer.Sound.play(won_the_box_sound)
    while True:  # the game is won, this happens till a reset
        pass


def blackBoxLost():
    game_status.value = 4
    mixer.Sound.play(lost_the_box_sound)
    while True:  # the game is lost, this happens till a reset
        pass


def boxStart():
    ''' what happens at the start, after the six buttons are pushed '''
    layout.game_status.value = 1
    global startTime  # record once when the game started
    startTime = datetime.datetime.now()
    print("start time: ", startTime)
    global deadline  # set the deadline for when the game must be finished
    deadline = datetime.datetime.now() + deltaMinutes
    layout.relais_value.value = 1  # put on back- and bottomlight

# -------------- BYPASS ------------------------------------------------------------------


def check_bypass():
    global top_buttons_started
    global plugs_game_started
    global RGB_game_started
    global simon_says_started
    global sinus_game_started
    global color_follow_started

    bypass = 0
    margin = 100
    count_number = 100  # the amount of times it needs to check if there is a value before passing it to see what it is.

    if bypass_value.value > 100 or bypass_value.value < 4900:
        count += 1
    else:
        count = 0

    if count > count_number:
        if (bypass_value.value <= (plug_bypass - margin) and bypass_value.value >= (plug_bypass + margin)):
            bypass = 1
        elif (bypass_value.value <= (RGB_bypass - margin) and bypass_value.value >= (RGB_bypass + margin)):
            bypass = 2
        elif (bypass_value.value <= (simon_says_bypass - margin) and bypass_value.value >= (simon_says_bypass + margin)):
            bypass = 3
        elif (bypass_value.value <= (turning_knobs_bypass - margin) and bypass_value.value >= (turning_knobs_bypass + margin)):
            bypass = 4
        elif (bypass_value.value <= (sinus_game_bypass - margin) and bypass_value.value >= (sinus_game_bypass + margin)):
            bypass = 5
        elif (bypass_value.value <= (color_follow_bypass - margin) and bypass_value.value >= (color_follow_bypass + margin)):
            bypass = 6

        # bypass the plugs to start the rgb game
        if bypass == 1 and RGB_game_started is False:
            RGB_game_process = multiprocessing.Process(target=RGB_game.main)
            RGB_game_process.start()
            RGB_game_started = True

        # bypass the rgb game to start simon says
        if bypass == 2 and simon_says_started is False:
            simon_says_process = multiprocessing.Process(target=simon_says.main)
            simon_says_process.start()
            simon_says_started = True

        # bypass simon says to turn on the three top leds
        if bypass == 3:
            top_buttons.RGB_half_status.value = 1

        # bypass the turning knobs and start the sinus game
        if bypass == 4 and sinus_game_started is False:
            print ('spy knobs correctly oriëntated')  # spyknobs becomes 0 when connected correctly
            mixer.Sound.play(good_sound)
            sinus_game_process = multiprocessing.Process(target=sinus_game.main)
            sinus_game_process.start()
            sinus_game_started = True

        # bypass the sinus game and start the color follow
        if bypass == 5 and color_follow_started is False:
            color_follow_process = multiprocessing.Process(target=color_follow.main)
            color_follow_process.start()
            color_follow_started = True

        # bypass the color follow game and turn on the three top leds
        if bypass == 6:
            top_buttons.sinus_half_status.value = 1

# -------------- THE GAME ------------------------------------------------------------------


def main():
    print("Black Box started")
    # at the start, no games ar started.
    global top_buttons_started
    global plugs_game_started
    global RGB_game_started
    global simon_says_started
    global sinus_game_started
    global color_follow_started

    # this while loop keeps running to manage the game progression
    while True:
        
        # test
        if top_buttons.sinus_half_status.value == 1:
            showTime()
            while True:
                pass
        
        # loop background sound
        # start a process to check the top buttons
        if top_buttons.top_status.value == 0 and top_buttons_started is False:
            top_buttons_process = multiprocessing.Process(target=top_buttons.main)
            top_buttons_process.start()
            print("top_buttons process started")
            top_buttons_started = True

        # start plug game after the six buttons are pushed togheter
        if top_buttons.top_status.value == 1 and plugs_game_started is False:
            plugs_game_process = multiprocessing.Process(target=plugs_game.main)
            plugs_game_process.start()
            print("plugs process started")
            plugs_game_started = True
            print("game start")
            boxStart()
            print("gamestatus ", game_status.value)

        # Start the RGB game after all 6 plugs are connected correctly
        if plugs_game.game_won.value == 1 and RGB_game_started is False:
            RGB_game_process = multiprocessing.Process(target=RGB_game.main)
            RGB_game_process.start()
            print("rgb process started")
            RGB_game_started = True

        # start Simon Says after all RGB game colors are machted correctly
        if RGB_game.game_won.value == 1 and simon_says_started is False:
            simon_says_process = multiprocessing.Process(target=simon_says.main)
            simon_says_process.start()
            print("simon says process started")
            simon_says_started = True

        if simon_says.game_won.value == 1:
            top_buttons.RGB_half_status.value = 1

        # start the sinus game
        if layout.big_knobs_value.value == 0 and sinus_game_started is False:
            print ('spy knobs correctly oriëntated')  # spyknobs becomes 0 when connected correctly
            mixer.Sound.play(good_sound)
            sinus_game_process = multiprocessing.Process(target=sinus_game.main)
            sinus_game_process.start()
            print("sinus_game process started")
            sinus_game_started = True

        # start Color follow after the sinus game is won
        if sinus_game.game_won.value == 1 and color_follow_started is False:
            color_follow_process = multiprocessing.Process(target=color_follow.main)
            color_follow_process.start()
            print("color_follow process started")
            color_follow_started = True

        if color_follow.game_won.value == 1:
            top_buttons.sinus_half_status.value = 1

        # BlackBox Lost
        if game_status.value == 1 and datetime.datetime.now() > deadline:
            blackBoxLost()

        # BlackBox Won
        if game_status.value == 1 and top_buttons.top_status.value == 2:
            blackBoxWon()


if __name__ == "__main__":
    layout_process = multiprocessing.Process(target=layout.main)
    ledcontrol_process = multiprocessing.Process(target=ledcontrol.main)
    layout_process.start()
    time.sleep(2)
    ledcontrol_process.start()
    main()
    layout_process.terminate()
    ledcontrol_process.terminate()
