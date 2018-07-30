
from __future__ import absolute_import, division, print_function, \
    unicode_literals
import time
import random
import pygame
import opc  # nog niet geinstalleerd
from neopixel import *
try:
    from ADCPi import ADCPi
except ImportError:
    print("Failed to import ADCPi from python system path")
    print("Importing from parent folder instead")
    try:
        import sys
        sys.path.append('..')
        from ADCPi import ADCPi
    except ImportError:
        raise ImportError(
            "Failed to import library from parent folder")

pygame.mixer.init()
good_sound = pygame.mixer.Sound("good_sound.ogg")
wrong_sound = pygame.mixer.Sound("wrong_sound.ogg")

numLEDs = 512
client = opc.Client('localhost:7890')



# pins on ADC Pi Plus board
connected_pin_1 = 1
connected_pin_2 = 2
connected_pin_3 = 3

# PARAMETERS
marge = 0.3  # how far can they be off from the correct valeu
wait_time = 20  # amount of times it needs to be correct when checked.
level = 0
totaal_levels = 3 
time_per_level = 30  # sec
v1 = 2.25
v2 = 2.5
v3 = 4.7


game_won = False


adc = ADCPi(0x6C, 0x6D, 12)

#the colors that need to be machted in RGB valeus from 0 - 255
vb = ((78, 36, 60),
      (17, 70, 47),
      (52, 80, 17))

def control_ledstrip():
    """change the color of the ledstrip the player can control"""
    pass
    

def blinkleds(r, g, b, n):
    """blinking all leds n times with rgb valeus"""
    for a in range n:
        for i in range(numLEDs):
            pixels = [(0, 0, 0)] * numLEDs
            pixels[i] = (r, g, b)
            client.put_pixels(pixels)
            time.sleep(0.3)


def level_won():
    pygame.mixer.Sound.play(good_sound)
    blinkleds(0, 200, 0, 3)
    global level
    level += 1


def level_lost():
    pygame.mixer.Sound.play(wrong_sound)
    blinkleds(200, 0, 0, 3)
    global level
    level = 0


def checkColorValues(red, green, blue, level):
    """ read the slides and check if they are correct"""
    
    red = adc.read_voltage(connected_pin_1)
    green = adc.read_voltage(connected_pin_2)
    blue = adc.read_voltage(connected_pin_3)
    
    redtrue = red > (vb[level][0] - marge) and red < (vb[level][0] + marge)
    greentrue = green > (vb[level][1] - marge) and green < (vb[level][1] + marge)
    bluetrue = blue > (vb[level][2] - marge) and blue < (vb[level][2] + marge)
    
    return redtrue and greentrue and bluetrue #returns only true if all three are true


def main():
    while game_won is False:
        deadline = time.time() + time_per_level
        while level < totaal_levels:
            while time.time() < deadline:
                control_ledstrip()
                if check_color_values(red, green, blue, level): # got the right slide setting?
                    ### timer to make sure its equal
                    level_won()
                    deadline += time_per_level #add the time per level to the deadline. fast with the first level? more time for the second level.
                    break
            level_lost()
            break # het level is weer op 0 gezet, dus er moet opnieuw een deadline gezet worden
        else:
            global game_won
            game_won = True
      
if __name__ == "__main__":
    main()







# use the Color(255,255,255) function to convert the provided red, green, blue color (0-255) to a 24-bit color value.
