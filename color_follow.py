
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
import time
import random
import pygame
import multiprocessing


pygame.mixer.init()
bleep1 = pygame.mixer.Sound("bleep2.ogg")
bleep2 = pygame.mixer.Sound("bleep2.ogg")
bleep3 = pygame.mixer.Sound("bleep2.ogg")
bleep4 = pygame.mixer.Sound("bleep2.ogg")
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

# PARAMETERS
led_pins = [2, 4, 6, 8]  # van bus 2
press_time = 2  # seconds
levels = 6

game_won = multiprocessing.Value('i', 0)


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
    """check if the input is correct within the time"""
    deadline = time.time() + press_time
    while time.time() < deadline:
        buttonstate2 = iobus1.read_pin(2)
        buttonstate4 = iobus1.read_pin(4)
        buttonstate6 = iobus1.read_pin(6)
        buttonstate8 = iobus1.read_pin(8)

        if buttonstate2 == 0:
            ledchoise = 2
            print("led1")
            pygame.mixer.Sound.play(bleep1)
            break

        elif buttonstate4 == 0:
            ledchoise = 4
            print("led2")
            pygame.mixer.Sound.play(bleep2)
            break

        elif buttonstate6 == 0:
            ledchoise = 6
            print("led3")
            pygame.mixer.Sound.play(bleep3)
            break

        elif buttonstate8 == 0:
            ledchoise = 8
            print("led4")
            pygame.mixer.Sound.play(bleep4)
            break

    if ledchoise == value:
        return True
    else:
        return False


def main():
    random.seed()
    count = 0

    while True:
        time.sleep(1)
        new_led = random.choice(led_pins)
        iobus2.write_pin(new_led, 1)  # zet lampje aan
        status = correct_input(new_led)
        iobus2.write_pin(new_led, 0)
        if status == True:
            count += 1
            if count == levels:
                time.sleep(1)
                pygame.mixer.Sound.play(good_sound)
                game_won = True
                print ("gewonnen")
                break
            continue
        else:
            pygame.mixer.Sound.play(wrong_sound)
            flash_all(3)
            print("verloren")
        break

        # zet lampje aan
        # tijd geven om goeie knopje in te drukken
        # als goeie knopje count +1 & continieu
        # als te laat Break


if __name__ == "__main__":
    main()
