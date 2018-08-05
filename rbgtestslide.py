
from __future__ import absolute_import, division, print_function, \
    unicode_literals
import time
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
            "Failed to import library from parent folder")

#for communication with the fadecandy server
client = opc.Client('localhost:7890')
numLEDs = 35

game_won = False


adc = ADCPi(0x6C, 0x6D, 12)

def makecolor():
    r = adc.read_voltage(1)*50
    g = adc.read_voltage(2)*50
    b = 50
    pixels = [(r, g, b)] * numLEDs
    client.put_pixels(pixels)
    time.sleep(0.3)




def main():
    while True:
        makecolor()

import processtest
     
if __name__ == "__main__":
    main()
    print ("game won global: {}".format(game_won))


    
     
    
    
    
    
    
    
    
    
    
    
    
    

