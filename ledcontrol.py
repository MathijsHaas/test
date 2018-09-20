''' Led control. The timer strip and the RGB led strips are controled from this file. they have multiprocessing values to read the rgb data from the rgb game and to control the timerstrip. '''

import multiprocessing
import opc
import RGB_game
import datetime
import time


# for communication with the fadecandy server
client = opc.Client('localhost:7890')
timer_leds = 81  # amount of leds in the timer strip
example_leds = 32  # amount of leds in the RGB example strip
play_leds = 32  # amount of leds in the RGB strip the player controls
startled = 128  # at what led does the RGB game start (first led of Fadecandy pin 3)

# setting up the shared list that wil be send to the strip
manager = multiprocessing.Manager()
strip = manager.list()

def timerstrip_running(strip):
    shutdown_led = 0
    newledout = datetime.datetime.now()
    while blackbox.game_status.value == 0:  # not started
        pass
    while blackbox.game_status.value == 1:  # timer strip running
        if datetime.datetime.now() > newledout:
            strip[timer_leds - shutdown_led] = (0,0,0)
            shutdown_led += 1
            newledout = datetime.datetime.now() + datetime.deltatime(seconds=44.5)
    while blackbox.game_status.value == 2:  # game won: timer strip flashing green
        colorflash(strip, 230, 0, 0)
    while blackbox.game_status.value == 3:  #game won: timer strip flashing red
        colorflash(strip, 0, 230, 0)

def timertest(strip): #mag weg
    while True: # timer strip running
        if datetime.datetime.now() > newledout:
            strip[timer_leds - shutdown_led] = (0,0,0)
            shutdown_led += 1
            newledout = datetime.datetime.now() + datetime.deltatime(seconds=2)
            client.put_pixels(strip)
        
def colorflash(strip, r, g, b):
        for i in range(timer_leds):
            strip[i] = (r,g,b)
            time.sleep(0.03)
        for i in range(timer_leds):
            strip[i] = (0,0,0)
            time.sleep(0.03)     
    

def timerstrip_setup(strip):
    ''' timerstrip setup that runs the timerstrip from green to red'''
    for i in range(timer_leds): # timerstrip setup
        r = 255-(255/timer_leds*i)
        g = 255/timer_leds*i 
        b = 0
        strip[i] = (r,g,b)


def list_setup(strip):
    ''' function that runs once at the start, to make a list with tuples that can be replaced
    with the processes that control the led strips'''
    for i in range(256):  # we need 4 pins with 64 leds each (4*64=256) to control all the leds
        strip.append((0, 0, 0))


def set_example_color(strip, r, g, b):
    ''' control the leds from the fadecandy pin 3 (led 128 - 192) '''
    print(r, g, b)
    for i in range(example_leds):
        strip[startled + i] = (r, g, b)


def set_play_color(strip, r, g, b):
    ''' control the leds from the fadecandy pin 4 (led 192 - 256) '''
    for i in range(play_leds):
        strip[startled + example_leds + i] = (r, g, b)

def main():
    list_setup(strip)
    timerstrip_setup(strip)
    timertest(strip)
    '''
    print (strip)
    list_setup(strip)
    timerstrip_setup(strip)
    print (strip)
    RGB_game.control_ledstrip(3,0,0)
    set_example_color(strip, RGB_game.r_example_value.value, RGB_game.g_example_value.value, RGB_game.b_example_value.value)
    print (strip)
    set_play_color(strip, RGB_game.r_play_value.value, RGB_game.g_play_value.value, RGB_game.b_play_value.value)
    client.put_pixels(strip)
    print (strip)
    '''
    # Process that does the timerstrip countdown
    # process that controls the two ledstrips
    

if __name__ == "__main__":
    main()

import RGB_game
import blackbox
