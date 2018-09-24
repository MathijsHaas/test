
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
from pygame import mixer
import layout
import multiprocessing

button1 = buttonlayout.color_follow_button1
button2 = buttonlayout.color_follow_button2
button3 = buttonlayout.color_follow_button3
button4 = buttonlayout.color_follow_button4

led1 = buttonlayout.color_follow_led1
led2 = buttonlayout.color_follow_led2
led3 = buttonlayout.color_follow_led3
led4 = buttonlayout.color_follow_led4


mixer.init()
bleep1 = mixer.Sound("bleep2.ogg")
bleep2 = mixer.Sound("bleep2.ogg")
bleep3 = mixer.Sound("bleep2.ogg")
bleep4 = mixer.Sound("bleep2.ogg")
wrong_sound = mixer.Sound("wrong_sound.ogg")
good_sound = mixer.Sound("good_sound.ogg")

# IO PI PLUS shield setup

iobus1 = IOPi(0x20)  # bus 1 will be inputs
iobus2 = IOPi(0x21)  # bus 2 will be outputs

# inputs op bus 1
iobus1.set_port_direction(0, 0xFF)
iobus1.set_port_pullups(0, 0xFF)
iobus1.set_port_direction(1, 0xFF)
iobus1.set_port_pullups(1, 0xFF)

# Outputs op bus 2
iobus2.set_port_direction(0, 0x00)
iobus2.write_port(0, 0x00)
iobus2.set_port_direction(1, 0x00)
iobus2.write_port(1, 0x00)

# PARAMETERS
led_pins = [layout.color_follow_led1_value.value,
            layout.color_follow_led2_value.value,
            layout.color_follow_led3_value.value,
            layout.color_follow_led4_value.value]
press_time = 2  # seconds
levels = 6

game_won = multiprocessing.Value('i', 0)


def flash_all(n):
    """flash all leds for n times"""
    for i in range(0, n):
        for i in led_pins:  # de pins op het IO PI PLUS bord waar de ledjes op zijn aangesloten
            i = 1
        time.sleep(0.3)
        for i in led_pins:
            i = 0
        time.sleep(0.3)
    return


def correct_input(value):
    """check if the input is correct within the time"""
    deadline = time.time() + press_time
    while time.time() < deadline:

        if layout.color_follow_button1_value.value == 0:
            ledchoise = led1
            print("led1")
            mixer.Sound.play(bleep1)
            break

        elif layout.color_follow_button2_value.value == 0:
            ledchoise = led2
            print("led2")
            mixer.Sound.play(bleep2)
            break

        elif layout.color_follow_button3_value.value == 0:
            ledchoise = led3
            print("led3")
            mixer.Sound.play(bleep3)
            break

        elif layout.color_follow_button4_value.value == 0:
            ledchoise = led4
            print("led4")
            mixer.Sound.play(bleep4)
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
                mixer.Sound.play(good_sound)
                game_won = True
                print ("gewonnen")
                break
            continue
        else:
            mixer.Sound.play(wrong_sound)
            flash_all(3)
            print("verloren")
        break

        # zet lampje aan
        # tijd geven om goeie knopje in te drukken
        # als goeie knopje count +1 & continieu
        # als te laat Break


if __name__ == "__main__":
    layout_process = multiprocessing.Process(target=layout.main)
    layout_process.start()
    main()
    layout_process.terminate()
