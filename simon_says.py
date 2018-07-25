
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


# PARAMETERS
levels = 2
pattern_speed = 0.1
time_to_press = 4

game_won = False

pygame.mixer.init()
bleep1 = pygame.mixer.Sound("bleep1.ogg")
bleep2 = pygame.mixer.Sound("bleep2.ogg")
bleep3 = pygame.mixer.Sound("bleep3.ogg")
bleep4 = pygame.mixer.Sound("bleep4.ogg")
wrong_sound = pygame.mixer.Sound("wrong_sound.ogg")
good_sound = pygame.mixer.Sound("good_sound.ogg")


# IO PI PLUS shield setup

iobus1 = IOPi(0x20)  # bus 1 will be inputs
iobus2 = IOPi(0x21)  # bus 2 will be outputs

# inputs op bus 1
iobus1.set_port_direction(0, 0xFF)
iobus1.set_port_pullups(0, 0xFF)

# Outputs op bus 2
iobus2.set_port_direction(0, 0x00)
iobus2.write_port(0, 0x00)


def flash(l, n):
    """flash led l for n times"""
    iobus2.write_pin((2 + 2 * l), 1)  # deze rekensom omdat de eerste ledjes op 2,4,6,8 zitten
    time.sleep(n)
    iobus2.write_pin((2 + 2 * l), 0)
    return


def flash_all(n):
    """flash all leds for n times"""
    for i in range(0, n):
        for i in [2, 4, 6, 8]:  # de pins op het IO PI PLUS bord waar de ledjes op zijn aangesloten
            iobus2.write_pin(i, 1)
        time.sleep(0.3)
        for i in [2, 4, 6, 8]:
            iobus2.write_pin(i, 0)
        time.sleep(0.3)
    return


def correct_input(value):
    """check if the input is correct"""
    deadline = time.time() + time_to_press
    ledchoise = 4  # to declare the ledcoise variable without it being 0-3 for the comparison at the end of the function

    while time.time() < deadline:

        buttonstate2 = iobus1.read_pin(2)
        buttonstate4 = iobus1.read_pin(4)
        buttonstate6 = iobus1.read_pin(6)
        buttonstate8 = iobus1.read_pin(8)

        if buttonstate2 == 0:
            ledchoise = 0
            print("led1")
            pygame.mixer.Sound.play(bleep1)
            break

        elif buttonstate4 == 0:
            ledchoise = 1
            print("led2")
            pygame.mixer.Sound.play(bleep2)
            break

        elif buttonstate6 == 0:
            ledchoise = 2
            print("led3")
            pygame.mixer.Sound.play(bleep3)
            break

        elif buttonstate8 == 0:
            ledchoise = 3
            print("led4")
            pygame.mixer.Sound.play(bleep4)
            break

    if ledchoise == value:
        return 1
    else:
        return 0


def chose_sound(i):
    """plays the right sound with the sequence"""
    if i == 0:
        return bleep1
    elif i == 1:
        return bleep2
    elif i == 2:
        return bleep3
    elif i == 3:
        return bleep4

############
# The Game #
############


def attract_mode():
    ''' attracting the atention of the player to push a button and start the game'''
    while True:
        # knipper met lampjes
        if iobus1.read_pin(2) == 0 or iobus1.read_pin(4) == 0 or iobus1.read_pin(6) == 0 or iobus1.read_pin(8) == 0:
            return True  # start the game


def main():
    while True:
        if attract_mode():

            random.seed()   # Different seed for every game
            count = 0  # Keeps track of player score
            sequence = []  # Will contain the sequence of light for the simon says

            while True:
                time.sleep(1)
                new_value = random.randint(0, 3)
                sequence.append(new_value)
                # Running through the example sequence
                for i in range(0, len(sequence)):
                    print (sequence[i])
                    bleep = chose_sound(sequence[i])
                    pygame.mixer.Sound.play(bleep)
                    flash(sequence[i], 0.4)
                    time.sleep(pattern_speed)
                # Letting the player repeat the sequence
                for i in range(0, len(sequence)):
                    while iobus1.read_pin(2) == 0 or iobus1.read_pin(4) == 0 or iobus1.read_pin(6) == 0 or iobus1.read_pin(8) == 0:
                        pass  # stops the program until you release the button again.
                    status = correct_input(sequence[i])
                    time.sleep(0.05)
                    if status == 1:
                        flash(sequence[i], 0.1)
                    else:
                        # LOST
                        pygame.mixer.Sound.play(wrong_sound)
                        flash_all(3)
                        break
                else:
                    count += 1
                    if count == levels:
                        # WON
                        game_won = True
                        pygame.mixer.Sound.play(good_sound)
                        for i in [2, 4, 6, 8]:
                            iobus2.write_pin(i, 1)
                        time.sleep(3)  # TIJDELIJK, mag uiteindelijk weg, maar is nu zodat de lampjes niet aan blijven staan
                        for i in [2, 4, 6, 8]:
                            iobus2.write_pin(i, 0)
                        print ("you won")
                        return True  # spel gewonnen
                        break
                    continue
                break


if __name__ == "__main__":
    main()
