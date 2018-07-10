#!/usr/bin/env python
from IOPi import IOPi
import time

i2c_helper = ABEHelpers()
i2c_bus = i2c_helper.get_smbus()
bus = IOPi(0x21)
bus.set_port_direction(0, 0x00)
bus.write_port(0, 0x00)
while True:
    for x in range(0,255):
        bus.write_port(0, x)
        time.sleep(0.5)
    bus.write_port(0, 0x00)
