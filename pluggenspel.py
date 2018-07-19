
from __future__ import absolute_import, division, print_function, \
    unicode_literals
import time
import random
import pygame
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

pygame.mixer.init()
good_sound = pygame.mixer.Sound("good_sound.ogg")

################### pins on ADC Pi Plus board
connected_pin_1 = 1
connected_pin_2 = 2
connected_pin_3 = 3
################### PARAMETERS
wait_time = 20 #amount of times it needs to be correct when checked.
v1 = 2.25
v2 = 2.5
v3 = 4.7

game_won = False


adc = ADCPi(0x6C, 0x6D, 12)

def main():
    counter = 0 #so you dont accidentally come past the right voltage
    while True:
        if (adc.read_voltage(connected_pin_1) >= (v1 - 0.5) and adc.read_voltage(connected_pin_1) <= (v1 + 0.5) and
            adc.read_voltage(connected_pin_2) >= (v2 - 0.5) and adc.read_voltage(connected_pin_2) <= (v2 + 0.5) and
             adc.read_voltage(connected_pin_3) >= (v3 - 0.5) and adc.read_voltage(connected_pin_3) <= (v3 + 0.5)):
            counter += 1
            if counter == wait_time:
               pygame.mixer.Sound.play(good_sound)
               game_won is True
            else:
                counter = 0
        


if __name__ == "__main__":
    main()