''' Led control. The timer strip and the RGB led strips are controled from this file. they have multiprocessing values to read the rgb data from the rgb game and to control the timerstrip. '''

import multiprocessing
import opc


# for communication with the fadecandy server
client = opc.Client('localhost:7890')
timer_leds = 81  # amount of leds in the timer strip
example_leds = 35  # amount of leds in the RGB example strip
play_leds = 35  # amount of leds in the RGB strip the player controls

# setting up the shared list that wil be send to the strip
manager = multiprocessing.Manager()
strip = manager.list()


def list_setup(strip):
    ''' function that runs once at the start, to make a list with tuples that can be replaced
    with the processes that control the led strips'''
    for i in range(256):  # we need 4 pins with 64 leds each (4*64=256) to control all the leds
        strip.append((0, 0, 0))
    for i in range(timer_leds):
        strip[i] = (255, 255, 255)
    for i in range(example_leds):  # to control the leds from the fadecandy pin 3 (led 128 - 192)
        strip[128 + i] = (255, 255, 255)
    client.put_pixels(strip)


def set_example_color(strip, r, g, b):
    ''' control the leds from the fadecandy pin 3 (led 128 - 192) '''
    for i in range(example_leds):
        strip[128 + i] = (r, g, b)
    client.put_pixels(strip)


def set_play_color(strip, r, g, b):
    ''' control the leds from the fadecandy pin 4 (led 192 - 256) '''
    for i in range(play_leds):
        strip[192 + i] = (r, g, b)
    client.put_pixels(strip)


def main():
    while True:
        set_example_color(strip, RGB_game.r_example_value.value, RGB_game.g_example_value.value, RGB_game.b_example_value.value)
        set_play_color(strip, RGB_play.r_example_value.value, RGB_play.g_example_value.value, RGB_play.b_example_value.value)


import RGB_game
