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

import multiprocessing
import buttonlayout
import datetime
from pygame import mixer

# SOUND
pygame.mixer.init()
deep_button_sound = pygame.mixer.Sound("deep_button_sound.ogg")

# top_status keeps track of the top buttons and what they have to do.
# 0 = not started, 1 = started, 2 = ended
top_status = multiprocessing.Value('i', 0)

# becomes one when either of the halves of the box is completed.
RGB_half_status = multiprocessing.Value('i', 0)
sinus_half_status = multiprocessing.Value('i', 0)

# PARAMETERS
presstime = 50000  # microseconds to press. 1.000.000 microseconds per second
buttons_to_win = 3

# check in de layout welke knop of led bij welke pin hoort.
button1 = buttonlayout.top_button1
button2 = buttonlayout.top_button2
button3 = buttonlayout.top_button3
button4 = buttonlayout.top_button4
button5 = buttonlayout.top_button5
button6 = buttonlayout.top_button6

top_led123 = buttonlayout.top_led123
top_led456 = buttonlayout.top_led456

# IO PI PLUS shield setup

iobus1 = IOPi(0x20)  # bus 1 will be inputs
iobus2 = IOPi(0x21)  # bus 2 will be outputs

# inputs op bus 1
iobus1.set_port_direction(0, 0xFF)
iobus1.set_port_pullups(0, 0xFF)

# Outputs op bus 2
iobus2.set_port_direction(0, 0x00)
iobus2.write_port(0, 0x00)


def pushtogheter():
    ''' put all the lights on and wait until all buttons are pressed. then start the game. (only 5 buttons are needed to start) '''
    # put all six lights on
    iobus2.write_pin(top_led123, 1)
    iobus2.write_pin(top_led456, 1)

    pt = datetime.timedelta(microseconds=presstime)
    bs = [0, 0, 0, 0, 0, 0]
    buttonpressed = [0, 0, 0, 0, 0, 0]  # gets filled with ones if all buttons are pressed
    count = [0, 0, 0, 0, 0, 0]  # keeps track of when the buttons are pressed

    while sum(buttonpressed) < buttons_to_win:
        bs[0] = iobus1.read_pin(button1)
        bs[1] = iobus1.read_pin(button2)
        bs[2] = iobus1.read_pin(button3)
        bs[3] = iobus1.read_pin(button4)
        bs[4] = iobus1.read_pin(button5)
        bs[5] = iobus1.read_pin(button6)
        for i in range(6):
            if bs[i] == 0 and count[i] == 0:
                print ("start time", i)
                pygame.mixer.Sound.play(deep_button_sound)
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
    iobus2.write_pin(top_led123, 0)
    iobus2.write_pin(top_led456, 0)
    top_status.value += 1  # turns 1 from 0 to start the game. turns 2 from 1 to end the game


def main():
    while top_status.value < 1:  # when the game is ended you exit this loop.
        if top_status.value == 0:
            pushtogheter()

        if top_status.value == 1:
            print ("we zijn los hoor")
            pass

        if RGB_half_status.value == 1:
            iobus2.write_pin(top_led123, 1)
            # helft 1 geluidje
            RGB_half_status.value = 2

        if sinus_half_status.value == 1:
            # helft 2 geluidje
            iobus2.write_pin(top_led456, 1)
            sinus_half_status.value = 2

        if RGB_half_status.value == 2 and Sinus_half_status.value == 2:  # meaning both sides are completed
            top_status.value = 2
            pushtogheter()
            # win animation?
            # stop timer
            # play win sound


if __name__ == "__main__":
    main()
