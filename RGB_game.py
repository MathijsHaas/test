
from __future__ import absolute_import, division, print_function, \
    unicode_literals
try:
    from ADCPi import ADCPi
except ImportError:
    print("Failed to import ADCPi from python system path")
    print("Importing from parent folder instead")
    try:
        import sys
        sys.path.append('..')
        from ADCPi import ADCPi
    except ImportError:
        raise ImportError(
            "Failed to import library from parent folder")
import time
import random
import pygame
import opc
import multiprocessing
import buttonlayout
import ledcontrol


pygame.mixer.init()
good_sound = pygame.mixer.Sound("good_sound.ogg")
wrong_sound = pygame.mixer.Sound("wrong_sound.ogg")

# for communication with the fadecandy server
client = opc.Client('localhost:7890')
numLEDs = 35


# pins on ADC Pi Plus board
RGBslide1 = buttonlayout.RGBslide1
RGBslide2 = buttonlayout.RGBslide2
RGBslide3 = buttonlayout.RGBslide3

# PARAMETERS
marge = 0.3  # how far can they be off from the correct valeu
wait_time = 20  # amount of times it needs to be correct when checked.
level = 0
totaal_levels = 3
time_per_level = 30  # sec


r_example_value = multiprocessing.Value('i', 0)
g_example_value = multiprocessing.Value('i', 0)
b_example_value = multiprocessing.Value('i', 0)

r_play_value = multiprocessing.Value('i', 0)
g_play_value = multiprocessing.Value('i', 0)
b_play_value = multiprocessing.Value('i', 0)

game_won = multiprocessing.Value('i', 0)


adc = ADCPi(0x6C, 0x6D, 12)

# the colors that need to be machted in RGB valeus from 0 - 5V
example = (
    (78, 36, 60),
    (17, 70, 47),
    (52, 80, 17))


def control_ledstrip(r, g, b):
    """change the color of the ledstrip the player can control"""
    r_example_value.value = example[level][0]
    g_example_value.value = example[level][1]
    b_example_value.value = example[level][2]

    r_play_value.value = r * 51  # times 51 to scale the 5v to the 0-255 values of the led control
    g_play_value.value = g * 51
    b_play_value.value = b * 51


def blinkleds(r, g, b, n):
    """blinking all leds n times with rgb valeus"""
    for a in range(n):
        for i in range(numLEDs):
            pixels = [(0, 0, 0)] * numLEDs
            pixels[i] = (r, g, b)
            client.put_pixels(pixels)
            time.sleep(0.3)


def level_won():
    pygame.mixer.Sound.play(good_sound)
    blinkleds(0, 200, 0, 3)
    global level
    level += 1


def level_lost():
    pygame.mixer.Sound.play(wrong_sound)
    blinkleds(200, 0, 0, 3)
    global level
    level = 0


def checkColorValues(red, green, blue, level):
    """ read the slides and check if they are correct"""

    redtrue = red > (example[level][0] - marge) and red < (example[level][0] + marge)
    greentrue = green > (example[level][1] - marge) and green < (example[level][1] + marge)
    bluetrue = blue > (example[level][2] - marge) and blue < (example[level][2] + marge)

    return redtrue and greentrue and bluetrue  # returns only true if all three are true


def main():
    while game_won is False:
        deadline = time.time() + time_per_level
        while level < totaal_levels:
            while time.time() < deadline:
                red = adc.read_voltage(RGBslide1)
                green = adc.read_voltage(RGBslide2)
                blue = adc.read_voltage(RGBslide3)
                control_ledstrip(red, green, blue)
                if check_color_values(red, green, blue, level):  # got the right slide setting?
                    # timer to make sure its equal
                    level_won()
                    deadline += time_per_level  # add the time per level to the deadline. fast with the first level? more time for the second level.
                    break
            level_lost()
            break  # het level is weer op 0 gezet, dus er moet opnieuw een deadline gezet worden
        else:
            game_won.value = 1


if __name__ == "__main__":
    ledcontrol_process = multiprocessing.Process(target=ledcontrol.main)
    ledcontrol_process.start()
    main()
    ledcontrol_process.terminate()


# use the Color(255,255,255) function to convert the provided red, green, blue color (0-255) to a 24-bit color value.
