
from Adafruit_LED_Backpack import SevenSegment


# Main control
import ledcontrol  # where the led strips are controled and combined to send to the fadecandy
import multiprocessing  # to spawn each game as a separate process
import bb_sound  # sound control
import datetime  # to keep track of the deadline
import layout
import time
from pygame import mixer

# importing the differtent seperate games
import top_buttons
import plugs_game
import RGB_game
import simon_says
import sinusgame
import color_follow


# -------------- SETUP ------------------------------------------------------------------

# clock via SDA/SCL
segment = SevenSegment.SevenSegment(address=0x70)

# 0 = not started yet
# 1 = started
# 2 = black box won within time
# 3 = black box lost

top_buttons_started = False
plugs_game_started = False
RGB_game_started = False
simon_says_started = False
sinusgame_started = False
color_follow_started = False
first_half_finished = False
second_half_finished = False
# the voltages needed to be measured to bypass the game (remember the multiprocessing.value is * 1000)
plug_bypass = 3456
RGB_bypass = 3187
simon_says_bypass = 3857
turning_knobs_bypass = 2396
sinus_game_bypass = 1077
color_follow_bypass = 88

bypass_count = 0


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

# -------------- SOUND ------------------------------------------------------------------

mixer.pre_init(44100, -16, 2, 2048)  # somehow makes the sound react quicker
mixer.init()
mixer.music.load("sound_background.ogg")
won_the_box_sound = mixer.Sound("sound_win_box.ogg")
lost_the_box_sound = mixer.Sound("sound_lost_box.ogg")
start_the_box_sound = mixer.Sound("sound_start_box.ogg")
good_sound = mixer.Sound("sound_good.ogg")
wrong_sound = mixer.Sound("sound_wrong.ogg")
deep_button_sound = mixer.Sound("sound_deep_button.ogg")
bleep = mixer.Sound("sound_small_button.ogg")
simon1 = mixer.Sound("sound_simon1.ogg")
simon2 = mixer.Sound("sound_simon2.ogg")
simon3 = mixer.Sound("sound_simon3.ogg")
simon4 = mixer.Sound("sound_simon4.ogg")


def sound():

    if bb_sound.play_start_the_box_sound.value == 1:
        mixer.Sound.play(start_the_box_sound)
        bb_sound.play_start_the_box_sound.value = 0

    if bb_sound.play_won_the_box_sound.value == 1:
        mixer.Sound.play(won_the_box_sound)
        bb_sound.play_won_the_box_sound.value = 0

    if bb_sound.play_lost_the_box_sound.value == 1:
        mixer.Sound.play(lost_the_box_sound)
        bb_sound.play_lost_the_box_sound.value = 0

    if bb_sound.play_good_sound.value == 1:
        mixer.Sound.play(good_sound)
        bb_sound.play_good_sound.value = 0

    if bb_sound.play_wrong_sound.value == 1:
        mixer.Sound.play(wrong_sound)
        bb_sound.play_wrong_sound.value = 0

    if bb_sound.play_deep_button_sound.value == 1:
        mixer.Sound.play(deep_button_sound)
        bb_sound.play_deep_button_sound.value = 0

    if bb_sound.play_bleep.value == 1:
        mixer.Sound.play(bleep)
        bb_sound.play_bleep.value = 0

    if bb_sound.play_simon1.value == 1:
        mixer.Channel(1).play(mixer.Sound.play(simon1))
        bb_sound.play_simon1.value = 0

    if bb_sound.play_simon2.value == 1:
        mixer.Channel(2).play(mixer.Sound.play(simon2))
        bb_sound.play_simon2.value = 0

    if bb_sound.play_simon3.value == 1:
        mixer.Channel(3).play(mixer.Sound.play(simon3))
        bb_sound.play_simon3.value = 0

    if bb_sound.play_simon4.value == 1:
        mixer.Channel(4).play(mixer.Sound.play(simon4))
        bb_sound.play_simon4.value = 0

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
    showTime()
    layout.game_status.value = 2
    bb_sound.play_won_the_box_sound.value = 1
    ledcontrol.win_or_lose.value = 1
    while True:  # the game is won, this happens till a reset
        sound()


def blackBoxLost():
    showTime()
    layout.game_status.value = 3
    mixer.music.stop()
    bb_sound.play_lost_the_box_sound.value = 1
    time.sleep(0.2)
    ledcontrol.win_or_lose.value = 2
    layout.relais_value.value = 0
    while True:  # the game is lost, this happens till a reset
        sound()


def boxStart():
    ''' what happens at the start, after the six buttons are pushed '''

    # update the display LEDs.
    segment.write_display()
    layout.game_status.value = 1
    bb_sound.play_start_the_box_sound.value = 1
    global startTime  # record once when the game started
    startTime = datetime.datetime.now()
    print("start time: ", startTime)
    global deadline  # set the deadline for when the game must be finished
    deadline = datetime.datetime.now() + deltaMinutes
    layout.relais_value.value = 1  # put on back- and bottomlight
    layout.game_status.value = 1

# -------------- BYPASS ------------------------------------------------------------------


def check_bypass():
    global top_buttons_started
    global plugs_game_started
    global RGB_game_started
    global simon_says_started
    global sinusgame_started
    global color_follow_started
    global bypass_count
    global first_half_finished
    global second_half_finished

    bypass = 0
    margin = 80
    count_number = 4  # the amount of times it needs to check if there is a value before passing it to see what it is.

    # print(layout.bypass_value.value)

    if layout.bypass_value.value > 100 or layout.bypass_value.value < 4900:
        bypass_count += 1
        # print(layout.bypass_value.value)
    else:
        bypass_count = 0

    if bypass_count > count_number:
        if (layout.bypass_value.value >= (plug_bypass - margin) and layout.bypass_value.value <= (plug_bypass + margin)):
            bypass = 1
            # print("bypass 1")
        elif (layout.bypass_value.value >= (RGB_bypass - margin) and layout.bypass_value.value <= (RGB_bypass + margin)):
            bypass = 2
            # print("bypass 2")
        elif (layout.bypass_value.value >= (simon_says_bypass - margin) and layout.bypass_value.value <= (simon_says_bypass + margin)):
            bypass = 3
            # print("bypass 3")
        elif (layout.bypass_value.value >= (turning_knobs_bypass - margin) and layout.bypass_value.value <= (turning_knobs_bypass + margin)):
            bypass = 4
            # print("bypass 4")
        elif (layout.bypass_value.value >= (sinus_game_bypass - margin) and layout.bypass_value.value <= (sinus_game_bypass + margin)):
            bypass = 5
            # print("bypass 5")
        elif (layout.bypass_value.value >= (color_follow_bypass - margin) and layout.bypass_value.value <= (color_follow_bypass + margin)):
            bypass = 6
            # print("bypass 6")

        # bypass the plugs to start the rgb game
        if bypass == 1 and RGB_game_started is False:
            print("plugs bypassed, rgb started")
            RGB_game_process = multiprocessing.Process(target=RGB_game.main)
            RGB_game_process.start()
            RGB_game_started = True

        # bypass the rgb game to start simon says
        if bypass == 2 and simon_says_started is False:
            print("rgb bypassed, simon says started")
            simon_says_process = multiprocessing.Process(target=simon_says.main)
            simon_says_process.start()
            simon_says_started = True

        # bypass simon says to turn on the three top leds
        if bypass == 3 and first_half_finished is False:
            print("SS bypassed, first half finished")
            top_buttons.RGB_half_status.value = 1
            first_half_finished = True

        # bypass the turning knobs and start the sinus game
        if bypass == 4 and sinusgame_started is False:
            print ('spy knobs bypassed, sinus started')  # spyknobs becomes 0 when connected correctly
            sinusgame.sinewave_game_status.value = 1
            sinusgame_started = True

        # bypass the sinus game and start the color follow
        if bypass == 5 and color_follow_started is False:
            print("sinus bypass, color follow started")
            color_follow_process = multiprocessing.Process(target=color_follow.main)
            color_follow_process.start()
            color_follow_started = True

        # bypass the color follow game and turn on the three top leds
        if bypass == 6 and second_half_finished is False:
            print("color follow bypass, second half finisched")
            top_buttons.sinus_half_status.value = 1
            second_half_finished = True

# -------------- THE GAME ------------------------------------------------------------------


def main():
    print("Black Box started")

    # at the start, no games ar started.
    global top_buttons_started
    global plugs_game_started
    global RGB_game_started
    global simon_says_started
    global sinusgame_started
    global color_follow_started
    global first_half_finished
    global second_half_finished

    mixer.music.play(-1)  # start looping background music

    # this while loop keeps running to manage the game progression
    while True:
        time.sleep(0.03)
        sound()
        check_bypass()
        sound()  # check and play the sounds

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
            print("gamestatus ", layout.game_status.value)

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

        if simon_says.game_won.value == 1 and first_half_finished is False:
            top_buttons.RGB_half_status.value = 1
            first_half_finished = True

        # start the sinus game
        if layout.big_knobs_value.value == 0 and sinusgame_started is False:
            print ('spy knobs correctly oriëntated')  # spyknobs becomes 0 when connected correctly
            bb_sound.play_good_sound.value = 1
            sinusgame.sinewave_game_status.value = 1
            print("sinusgame process started")
            sinusgame_started = True

        # start Color follow after the sinusgame is won
        if sinusgame.sinewave_game_status.value == 2 and color_follow_started is False:
            color_follow_process = multiprocessing.Process(target=color_follow.main)
            color_follow_process.start()
            print("color_follow process started")
            color_follow_started = True

        if color_follow.game_won.value == 1 and second_half_finished is False:
            top_buttons.sinus_half_status.value = 1
            second_half_finished = True

        # BlackBox Lost
        if layout.game_status.value == 1 and datetime.datetime.now() > deadline:
            print("BLACKBOX LOST")
            blackBoxLost()

        # BlackBox Won
        if layout.game_status.value == 1 and top_buttons.top_status.value == 2:
            print("BLACKBOX WON")
            blackBoxWon()


if __name__ == "__main__":
    layout_process = multiprocessing.Process(target=layout.main)
    ledcontrol_process = multiprocessing.Process(target=ledcontrol.main)
    sound_process = multiprocessing.Process(target=bb_sound.main)
    sinusgame_process = multiprocessing.Process(target=sinusgame.main)
    layout_process.start()
    time.sleep(1)
    ledcontrol_process.start()
    sound_process.start()
    sinusgame_process.start()  # to turn the screen black at the start
    main()
