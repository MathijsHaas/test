

import time
import random
import multiprocessing
import layout
import bb_sound

# PARAMETERS
levels = 10
pattern_speed = 0.2
time_to_press = 4

game_won = multiprocessing.Value('i', 0)


def flash(led, n):
    """turn led l for n seconds"""
    if led == 0:
        layout.ss_led1_value.value = 1
        time.sleep(n)
        layout.ss_led1_value.value = 0
    elif led == 1:
        layout.ss_led2_value.value = 1
        time.sleep(n)
        layout.ss_led2_value.value = 0
    elif led == 2:
        layout.ss_led3_value.value = 1
        time.sleep(n)
        layout.ss_led3_value.value = 0
    elif led == 3:
        layout.ss_led4_value.value = 1
        time.sleep(n)
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
##    print("value", value)

    while time.time() < deadline:
        time.sleep(0.02)
        if layout.ss_button1_value.value == 0:
            ledchoise = 0
# print("led1")
            bb_sound.play_simon1.value = 1  # play the sound
            while layout.ss_button1_value.value == 0:  # keep the light on till button release
                layout.ss_led1_value.value = 1
                time.sleep(0.05)
            layout.ss_led1_value.value = 0  # light out after button release
            break  # break the loop to compare the coise to the correct anwser

        elif layout.ss_button2_value.value == 0:
            ledchoise = 1
# print("led2")
            bb_sound.play_simon2.value = 1
            while layout.ss_button2_value.value == 0:
                layout.ss_led2_value.value = 1
                time.sleep(0.05)
            layout.ss_led2_value.value = 0
            break

        elif layout.ss_button3_value.value == 0:
            ledchoise = 2
# print("led3")
            bb_sound.play_simon3.value = 1
            while layout.ss_button3_value.value == 0:
                layout.ss_led3_value.value = 1
                time.sleep(0.05)
            layout.ss_led3_value.value = 0
            break

        elif layout.ss_button4_value.value == 0:
            ledchoise = 3
# print("led4")
            bb_sound.play_simon4.value = 1
            while layout.ss_button4_value.value == 0:
                layout.ss_led4_value.value = 1
                time.sleep(0.05)
            layout.ss_led4_value.value = 0
            break

        else:
            ledchoise = 5  # to declare the ledcoise variable without it being 0-3 for the comparison at the end of the function

    if ledchoise == value:

        ##        print(ledchoise, "goeie keuze")
        return 1

    else:
        ##        print(ledchoise, "slechte keuze")
        return 0


def chose_sound(i):
    """plays the right sound with the sequence"""
    if i == 0:
        bb_sound.play_simon1.value = 1
    elif i == 1:
        bb_sound.play_simon2.value = 1
    elif i == 2:
        bb_sound.play_simon3.value = 1
    elif i == 3:
        bb_sound.play_simon4.value = 1


def attract_mode():
    ''' attracting the atention of the player to push a button and start the game'''
    layout.ss_led3_value.value = 1
    while True:
        time.sleep(0.04)
        # knipper met lampjes
        if layout.ss_button1_value.value == 0 or layout.ss_button2_value.value == 0 or layout.ss_button3_value.value == 0 or layout.ss_button4_value.value == 0:
            layout.ss_led1_value.value = 0
            layout.ss_led2_value.value = 0
            layout.ss_led3_value.value = 0
            layout.ss_led4_value.value = 0
            return True  # start the game


def main():
    while game_won.value == 0:
        if attract_mode():

            random.seed()   # Different seed for every game
            count = 0  # Keeps track of player score
            sequence = []  # Will contain the sequence of light for the simon says

            while True:
                time.sleep(1)  # test
                new_value = random.randint(0, 3)
                sequence.append(new_value)
                # Running through the example sequence
                for i in range(0, len(sequence)):
                    chose_sound(sequence[i])
                    flash(sequence[i], 0.15)
                    time.sleep(pattern_speed)
                # Letting the player repeat the sequence
                for i in range(0, len(sequence)):
                    status = correct_input(sequence[i])
                    if status != 1:  # thus not correct
                        bb_sound.play_wrong_sound.value = 1
                        print("Simon Says Wrong")
                        flash_all(3)
                        break
                else:
                    count += 1
                    if count == levels:
                        # WON
                        game_won.value = 1
                        bb_sound.play_good_sound.value = 1
                        print ("Simon Says gewonnen")
                        layout.ss_led1_value.value = 1
                        layout.ss_led2_value.value = 1
                        layout.ss_led3_value.value = 1
                        layout.ss_led4_value.value = 1
                        return True  # spel gewonnen
                        break
                    continue
                break


if __name__ == "__main__":
    layout_process = multiprocessing.Process(target=layout.main)
    layout_process.start()
    main()
    layout_process.terminate()
