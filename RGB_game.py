
from __future__ import absolute_import, division, print_function, \
    unicode_literals
import time
import random
import pygame
import opc  # nog niet geinstalleerd
from neopixel import *
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

pygame.mixer.init()
good_sound = pygame.mixer.Sound("good_sound.ogg")


numLEDs = 512
client = opc.Client('localhost:7890')

def
  for i in range(numLEDs):
    pixels = [(0, 0, 0)] * numLEDs
    pixels[i] = (255, 255, 255)
    client.put_pixels(pixels)

# pins on ADC Pi Plus board
connected_pin_1 = 1
connected_pin_2 = 2
connected_pin_3 = 3

# PARAMETERS
marge = 20  # how far can they be off from the correct valeu
wait_time = 20  # amount of times it needs to be correct when checked.
level = 1
totaal_levels = 3
time_per_level = 30  # sec
v1 = 2.25
v2 = 2.5
v3 = 4.7

game_started = False
game_won = False


adc = ADCPi(0x6C, 0x6D, 12)


adc.read_voltage(connected_pin_1)

vb = ((78, 36, 60),
      (17, 70, 47),
      (52, 80, 17))

vbRed, vbBleu, vbGreen
red, green, blue

void loop() {

    # schuifjes uilezen
    adc.read_voltage(connected_pin_1)
    adc.read_voltage(connected_pin_1)
    adc.read_voltage(connected_pin_1)

    colorNa(stripNa.Color(red, green, blue));

def main():
  while level <= totaal_levels:

    // checklevels
      if (level <= totaal_levels) {
        colorVb(stripVb.Color(vb1[level - 1][0], vb1[level - 1][1], vb1[level - 1][2]))
        counter += 100

        if (checkColorValues(red, green, blue, level) == true){kleurcounter + +; }
        else {kleurcounter = 0; }
        if (kleurcounter > kleurkijktijd) {levelGehaald(); }



def checkColorValues(red, green, blue, level):
  redtrue = red > (vb1[level - 1][0] - marge) and red < (vb1[level - 1][0] + marge)
  greentrue = green > (vb1[level - 1][1] - marge) and green < (vb1[level - 1][1] + marge)
  bluetrue = blue > (vb1[level - 1][2] - marge) and blue < (vb1[level - 1][2] + marge)
  return redtrue and greentrue and bluetrue



# use Color(255,255,255) to convert the provided red, green, blue color (0-255) to a 24-bit color value.
