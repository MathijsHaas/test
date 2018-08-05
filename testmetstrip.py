#!/usr/bin/env python

from __future__ import absolute_import, division, print_function, \
    unicode_literals
import opc
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
            "Failed to import ADCPi library from parent folder")
import time
import multiprocessing
import stripcontrol

game_won = False

numLEDs = 35
client = opc.Client('localhost:7890')

adc = ADCPi(0x6C, 0x6D, 12)



kleur = multiprocessing.Manager().list()
kleur[0] = adc.read_voltage(1)*50
kleur[1] = 50
kleur[2] = adc.read_voltage(2)*50

def setcolorvb():
    """blinking all leds n times with rgb valeus"""
    kleur[0] = adc.read_voltage(1)*50
    kleur[1] = 50
    kleur[2] = adc.read_voltage(2)*50

 


strip_process = multiprocessing.Process(target=stripcontrol.main)
strip_process.start()


while True:
    setcolorvb()
         
        
        
        
        
        
        
        
        
        
        
        

