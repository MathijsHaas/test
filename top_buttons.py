# The six buttons on the top of the box
import multiprocessing
import layout
import datetime
import time
from pygame import mixer

# SOUND
mixer.init()
deep_button_sound = mixer.Sound("deep_button_sound.ogg")

# top_status keeps track of the top buttons and what they have to do.
# 0 = not started, 1 = started, 2 = end game
top_status = multiprocessing.Value('i', 0)

# becomes one when either of the halves of the box is completed.
RGB_half_status = multiprocessing.Value('i', 0)
sinus_half_status = multiprocessing.Value('i', 0)

# PARAMETERS
presstime = 50000  # microseconds to press. 1.000.000 microseconds per second
buttons_to_win = 3

# ---------------- FUNCTIONS FOR IN THE GAME -----------------------------------------


def pushtogheter():
    ''' put all the lights on and wait until all buttons are pressed. then start the game. (only 5 buttons are needed to start) '''
    # put all six lights on
    layout.top_led1_value.value = 1
    layout.top_led2_value.value = 1
    layout.top_led3_value.value = 1
    layout.top_led4_value.value = 1
    layout.top_led5_value.value = 1
    layout.top_led6_value.value = 1

    pt = datetime.timedelta(microseconds=presstime)
    bs = [0, 0, 0, 0, 0, 0]
    buttonpressed = [0, 0, 0, 0, 0, 0]  # gets filled with ones if all buttons are pressed
    count = [0, 0, 0, 0, 0, 0]  # keeps track of when the buttons are pressed

    while sum(buttonpressed) < buttons_to_win:
        bs[0] = top_button1_value.value
        bs[1] = top_button2_value.value
        bs[2] = top_button3_value.value
        bs[3] = top_button4_value.value
        bs[4] = top_button5_value.value
        bs[5] = top_button6_value.value
        for i in range(6):
            if bs[i] == 0 and count[i] == 0:
                print ("start time", i)
                mixer.Sound.play(deep_button_sound)
                count[i] = datetime.datetime.now()
                buttonpressed[i] = 1
            elif bs[i] == 0 and datetime.datetime.now() < count[i] + pt:
                buttonpressed[i] = 1
            elif bs[i] == 0 and datetime.datetime.now() >= count[i] + pt:
                buttonpressed[i] = 0
                # count keeps going
            else:
                count[i] = 0
                buttonpressed[i] = 0

    # put out the leds after you press the correc number togheter
    layout.top_led1_value.value = 0
    layout.top_led2_value.value = 0
    layout.top_led3_value.value = 0
    layout.top_led4_value.value = 0
    layout.top_led5_value.value = 0
    layout.top_led6_value.value = 0

    top_status.value += 1  # 0 to 1 to start game. 1 to 2 to end the game

#---------------------- THE GAME ---------------------------------------------------


def main():
    while top_status.value < 1:  # when the game is ended you exit this loop.
        if top_status.value == 0:
            pushtogheter()

        if top_status.value == 1:
            print ("we zijn los hoor")
            pass

        if RGB_half_status.value == 1:
            # helft 1 animatie
            mixer.Sound.play(deep_button_sound)
            layout.top_led1_value.value = 1
            time.sleep(1)
            mixer.Sound.play(deep_button_sound)
            layout.top_led2_value.value = 1
            time.sleep(1)
            mixer.Sound.play(deep_button_sound)
            layout.top_led3_value.value = 1
            RGB_half_status.value = 2

        if sinus_half_status.value == 1:
            # helft 2 animatie
            mixer.Sound.play(deep_button_sound)
            layout.top_led4_value.value = 1
            time.sleep(1)
            mixer.Sound.play(deep_button_sound)
            layout.top_led5_value.value = 1
            time.sleep(1)
            mixer.Sound.play(deep_button_sound)
            layout.top_led6_value.value = 1
            sinus_half_status.value = 2

        if RGB_half_status.value == 2 and Sinus_half_status.value == 2:
            # meaning both sides are completed.
            # The
            pushtogheter()
            # win animation?


if __name__ == "__main__":
    layout_process = multiprocessing.Process(target=layout.main)
    layout_process.start()
    main()
    layout_process.terminate()
