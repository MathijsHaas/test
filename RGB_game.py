
import time
from pygame import mixer
import multiprocessing
import layout
import ledcontrol


mixer.init()
good_sound = mixer.Sound("sound_good.ogg")
wrong_sound = mixer.Sound("sound_wrong.ogg")


# -------------- PARAMETERS ------------------------------------------------------

marge = 30  # how far can they be off from the correct valeu
wait_time = 5  # amount of times it needs to be correct when checked.
level = 0
totaal_levels = 3
time_per_level = 300  # sec


game_won = multiprocessing.Value('i', 0)


# the colors that need to be machted in RGB valeus from 0 - 5V
example = (
    (160, 80, 120),
    (50, 140, 100),
    (52, 80, 17))


# -------------- FUNCTIONS FOR IN THE GAME -----------------------------------------

def control_ledstrip(r, g, b):
    """change the color of the ledstrip the player can control"""
    ledcontrol.r_example_value.value = example[level][0]
    ledcontrol.g_example_value.value = example[level][1]
    ledcontrol.b_example_value.value = example[level][2]

    ledcontrol.r_play_value.value = r
    ledcontrol.g_play_value.value = g
    ledcontrol.b_play_value.value = b


def blinkleds(r, g, b, n):
    """blinking all leds n times with rgb valeus"""
    blinkspeed = 0.2
    for i in range(n):
        ledcontrol.r_example_value.value = r
        ledcontrol.g_example_value.value = g
        ledcontrol.b_example_value.value = b

        ledcontrol.r_play_value.value = r
        ledcontrol.g_play_value.value = g
        ledcontrol.b_play_value.value = b

        time.sleep(blinkspeed)

        ledcontrol.r_example_value.value = 0
        ledcontrol.g_example_value.value = 0
        ledcontrol.b_example_value.value = 0

        ledcontrol.r_play_value.value = 0
        ledcontrol.g_play_value.value = 0
        ledcontrol.b_play_value.value = 0

        time.sleep(blinkspeed)


def level_won():
    mixer.Sound.play(good_sound)
    print("blinking")
    blinkleds(0, 200, 0, 3)
    global level
    level += 1


def level_lost():
    mixer.Sound.play(wrong_sound)
    print("blinking")
    blinkleds(200, 0, 0, 3)
    global level
    level = 0


def check_color_values(red, green, blue, level):
    """ read the slides and check if they are correct"""

    redtrue = red > (example[level][0] - marge) and red < (example[level][0] + marge)
    greentrue = green > (example[level][1] - marge) and green < (example[level][1] + marge)
    bluetrue = blue > (example[level][2] - marge) and blue < (example[level][2] + marge)

    return redtrue and greentrue and bluetrue  # returns only true if all three are true


# ---------------------- THE GAME ----------------------------------------------------------

def main():
    while game_won.value == 0:
        deadline = time.time() + time_per_level
        while level < totaal_levels:
            print ("level {}".format(level))
            while time.time() < deadline:
                red = layout.RGBslide1_value.value
                green = layout.RGBslide2_value.value
                blue = layout.RGBslide3_value.value
                control_ledstrip(layout.RGBslide1_value.value, layout.RGBslide2_value.value, layout.RGBslide3_value.value)
                # print("RGB Red: {}, Green: {}, Blue: {}".format(layout.RGBslide1_value.value, layout.RGBslide2_value.value, layout.RGBslide3_value.value))
                time.sleep(0.2)
                if check_color_values(layout.RGBslide1_value.value, layout.RGBslide2_value.value, layout.RGBslide3_value.value, level):  # got the right slide setting?
                    # timer to make sure its equal
                    print("WIN level:", level)
                    level_won()
                    deadline += time_per_level  # add the time per level to the deadline. fast with the first level? more time for the second level.
                    break
            else:
                print("LOST level:", level)
                level_lost()
            break  # het level is weer op 0 gezet, dus er moet opnieuw een deadline gezet worden
        else:
            game_won.value = 1


if __name__ == "__main__":
    ledcontrol_process = multiprocessing.Process(target=ledcontrol.main)
    layout_process = multiprocessing.Process(target=layout.main)
    layout_process.start()
    ledcontrol_process.start()
    print("start RGB_game")
    main()
    print("RGB_game stop")
    ledcontrol_process.terminate()
    layout_process.terminate()
