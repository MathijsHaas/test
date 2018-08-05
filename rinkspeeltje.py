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

game_won = False

numLEDs = 35
client = opc.Client('localhost:7890')

adc = ADCPi(0x6C, 0x6D, 12)

def main():
    print("stripcontrol main loop start")
    while True:
        for i in range(numLEDs):
            speed = adc.read_voltage(1)/100
            pixels = [ (0,0,0) ] * numLEDs
            pixels[i] = (255, 255, 255)
            client.put_pixels(pixels)
            time.sleep(speed)
		
		
if __name__ == "__main__":
    main()