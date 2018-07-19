#!/usr/bin/env python
"""
================================================
ABElectronics ADC Pi 8-Channel ADC data-logger demo

Requires python smbus to be installed
run with: python demo_logvoltage.py
================================================

Initialise the ADC device using the default addresses and sample rate, change
this value if you have changed the address selection jumpers

Sample rate can be 12,14, 16 or 18
"""

from __future__ import absolute_import, division, print_function, \
                                                    unicode_literals
import time
import datetime

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


def writetofile(texttowrtite):
    '''
    Open the log file, write the value and close the file.
    '''
    file = open('adclog.txt', 'a')
    file.write(str(datetime.datetime.now()) + " " + texttowrtite)
    file.close()


def main():
    '''
    Main program function
    '''

    adc = ADCPi(0x6C, 0x6D, 12)

    print("Logging...")

    while True:

        # read from adc channels and write to the log file
        writetofile("Channel 1: %02f\n" % adc.read_voltage(1))
        # wait 1 second before reading the pins again
        time.sleep(1)

if __name__ == "__main__":
    main()
