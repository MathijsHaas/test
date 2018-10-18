

import time
import random
from pygame import mixer
import multiprocessing
import layout

# PARAMETERS
levels = 6
pattern_speed = 0.1
time_to_press = 4

game_won = multiprocessing.Value('i', 0)

# SOUND
mixer.init()
bleep1 = mixer.Sound("bleep1.ogg")
bleep2 = mixer.Sound("bleep2.ogg")
bleep3 = mixer.Sound("bleep3.ogg")
bleep4 = mixer.Sound("bleep4.ogg")
wrong_sound = mixer.Sound("wrong_sound.ogg")
good_sound = mixer.Sound("good_sound.ogg")


def flash(led, n):
    """turn led l for n seconds"""
    if led == 1:
        layout.ss_led1_value.value = 1
        time.wait(n)
        layout.ss_led1_value.value = 0
    elif led == 2:
        layout.ss_led2_value.value = 1
        time.wait(n)
        layout.ss_led2_value.value = 0
    elif led == 3:
        layout.ss_led3_value.value = 1
        time.wait(n)
        layout.ss_led3_value.value = 0
    elif led == 4:
        layout.ss_led4_value.value = 1
        time.wait(n)
        layout.ss_led4_value.value = 0


def flash_all(n):
    """flash all leds for n times"""
    for i in range(0, n):
        # de pins op het IO PI PLUS bord waar de ledjes op zijn aangesloten
        layout.ss_led1_value.value = 1
        layout.ss_led2_value.value = 1
        layout.ss_led3_value.value = 1
        layout.ss_led4_value.value = 1
        time.sleep(0.3)
        layout.ss_led1_value.value = 0
        layout.ss_led2_value.value = 0
        layout.ss_led3_value.value = 0
        layout.ss_led4_value.value = 0
        time.sleep(0.3)


def correct_input(value):
    """check if the input is correct"""
    deadline = time.time() + time_to_press
    ledchoise = 4  # to declare the ledcoise variable without it being 0-3 for the comparison at the end of the function

    while time.time() < deadline:

        if layout.ss_button1_value.value == 0:
            ledchoise = 0
            print("led1")
            mixer.Sound.play(bleep1)
            break

        elif layout.ss_button2_value.value == 0:
            ledchoise = 1
            print("led2")
            mixer.Sound.play(bleep2)
            break

        elif layout.ss_button3_value.value == 0:
            ledchoise = 2
            print("led3")
            mixer.Sound.play(bleep3)
            break

        elif layout.ss_button4_value.value == 0:
            ledchoise = 3
            print("led4")
            mixer.Sound.play(bleep4)
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


def attract_mode():
    ''' attracting the atention of the player to push a button and start the game'''
    layout.ss_led1_value.value = 1
    while True:
        # knipper met lampjes
        if layout.ss_button1_value.value == 0 or layout.ss_button2_value.value == 0 or layout.ss_button3_value.value == 0 or layout.ss_button4_value.value == 0:
            layout.ss_led1_value.value = 0
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
                    mixer.Sound.play(bleep)
                    flash(sequence[i], 0.4)
                    time.sleep(pattern_speed)
                # Letting the player repeat the sequence
                for i in range(0, len(sequence)):
                    while layout.ss_button1_value.value == 0 or layout.ss_button2_value.value == 0 or layout.ss_button3_value.value == 0 or layout.ss_button4_value.value == 0:
                        pass  # stops the program until you release the button again.
                    status = correct_input(sequence[i])
                    time.sleep(0.05)
                    if status == 1:
                        flash(sequence[i], 0.1)
                    else:
                        # LOST
                        mixer.Sound.play(wrong_sound)
                        print("Simon Says Wrong")
                        flash_all(3)
                        break
                else:
                    count += 1
                    if count == levels:
                        # WON
                        game_won.value = 1
                        mixer.Sound.play(good_sound)
                        layout.ss_led1_value.value = 1
                        layout.ss_led2_value.value = 1
                        layout.ss_led3_value.value = 1
                        layout.ss_led4_value.value = 1
                        print ("Simon Says gewonnen")
                        return True  # spel gewonnen
                        break
                    continue
                break


if __name__ == "__main__":
    main()
