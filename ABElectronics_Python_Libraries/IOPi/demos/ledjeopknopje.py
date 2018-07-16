#!/usr/bin/env python

"""
================================================
ABElectronics IO Pi | Digital I/O Read Demo

Requires python smbus to be installed
For Python 2 install with: sudo apt-get install python-smbus
For Python 3 install with: sudo apt-get install python3-smbus

run with: python demo_ioread.py
================================================

This example reads from all 16 pins on both buses on the IO Pi.
The internal pull-up resistors are enabled so each pin will read
as 1 unless the pin is connected to ground.

"""
from __future__ import absolute_import, division, print_function, \
                                                    unicode_literals
import time
import os

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


def main():
    """
    Main program function
    """
    
    iobus2 = IOPi(0x21)

    iobus2.set_pin_direction(2, 0)
    iobus2.set_pin_direction(4, 0)
    iobus2.set_pin_direction(10, 1)
    iobus2.set_pin_direction(14, 1)
    iobus2.set_port_pullups(1, 0xFF) 
    
    while True:
        # clear the console
        
        if iobus2.read_pin(14) == 0:
            iobus2.write_pin(2, 1)
        else:
            iobus2.write_pin(2, 0)
            
        if iobus2.read_pin(10) == 0:
            iobus2.write_pin(4, 1)
        else:
            iobus2.write_pin(4, 0)

if __name__ == "__main__":
    main()
