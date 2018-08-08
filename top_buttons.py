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
import time

# top_status keeps track of the top buttons and what they have to do.
# 0 = not started, 1 = started, 2 = ended
top_status = multiprocessing.Value('i', 0)

# becomes one when either of the halves of the box is completed.
RGB_half_status = multiprocessing.Value('i', 0)
Sinus_half_status = multiprocessing.Value('i', 0)

# PARAMETERS
presstime = 1  # seconds to press
buttons_to_win = 5

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

    bs = [
        iobus1.read_pin(button1),
        iobus1.read_pin(button2),
        iobus1.read_pin(button3),
        iobus1.read_pin(button4),
        iobus1.read_pin(button5),
        iobus1.read_pin(button6),
    ]

    buttonpressed = []  # gets filled with ones if all buttons are pressed
    count = []  # keeps track of how long the buttons are pressed

    while sum(buttonpressed) < buttons_to_win:
        for i in range(6):
            if bs[i] == 0 and count[i] == 0:
                count[i] = time.time()
                buttonpressed[i] = 1
            elif bs[i] == 0 and time.time() < count[i] + presstime:
                buttonpressed[i] = 1
            elif bs[i] == 0 and time.time() >= count[i] + presstime:
                buttonpressed[i] = 0
            else:
                count[i] = 0
                buttonpressed[i] = 0

    # put out the leds after you press the correc number togheter
    iobus2.write_pin(top_led123, 0)
    iobus2.write_pin(top_led456, 0)
    top_status.value = 1  # started the game


def main():
    while top_status.value < 2:  # when the game is ended you exit this loop.
        if top_status.value == 0:
            pushtogheter()

        if top_status.value == 1:
            # start timer
            # put on backlight
            # start sound

        if RGB_half_status.value == 1 and Sinus_half_status.value == 1:  # meaning both sides are completed
            top_status.value = 2
