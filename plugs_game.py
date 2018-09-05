
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
import pygame
import buttonlayout

pygame.mixer.init()
good_sound = pygame.mixer.Sound("good_sound.ogg")

# pins on ADC Pi Plus board
plugs1 = buttonlayout.plugs1
plugs2 = buttonlayout.plugs2
plugs3 = buttonlayout.plugs3

# PARAMETERS
wait_time = 20  # amount of times it needs to be correct when checked.
margin = 0.5  # the accepted error
v1 = 2.25
v2 = 2.5
v3 = 4.7


game_won = multiprocessing.Value('i', 0)


adc = ADCPi(0x6C, 0x6D, 12)


def main():
    counter = 0  # so you dont accidentally come past the right voltage
    while True:
        if (adc.read_voltage(plugs1) >= (v1 - margin) and adc.read_voltage(plugs1) <= (v1 + margin) and
            adc.read_voltage(plugs2) >= (v2 - margin) and adc.read_voltage(plugs2) <= (v2 + margin) and
                adc.read_voltage(plugs3) >= (v3 - margin) and adc.read_voltage(plugs3) <= (v3 + margin)):
            counter += 1
            if counter == wait_time:
                pygame.mixer.Sound.play(good_sound)
                game_won is True
                return True
            else:
                counter = 0


if __name__ == "__main__":
    main()
