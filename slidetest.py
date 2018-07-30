
from __future__ import absolute_import, division, print_function, \
    unicode_literals
import time
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

# pins on ADC Pi Plus board
connected_pin_1 = 1


game_won = False


adc = ADCPi(0x6C, 0x6D, 12)


def main():
    print ("we beginnen met schuiven")
    while True:
        if adc.read_voltage(connected_pin_1) > 5:
            time.sleep(1)
            print("schuifding gaat uit")
            processtest.slidetest_won = True #trying to set a boolean either here or in processtest.py
            global game_won
            game_won = True
            print ("game_won in slidetest: {}".format(game_won))
            print ("slidetest_won in processtest: {}".format(processtest.slidetest_won))
            break

import processtest
     
if __name__ == "__main__":
    main()
    print ("game won global: {}".format(game_won))


    
     
    
    
    
    
    
    
    
    
    
    
    
    
