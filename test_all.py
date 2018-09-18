''' This script is to test everything. All the buttons will give a sound. all the leds wil turn on. '''


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
            "Failed to import library from parent folder")
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

from pygame import mixer

# for communication with the fadecandy server
client = opc.Client('localhost:7890')
numLEDs = 512

adc1 = ADCPi(0x6C, 0x6D, 12)
adc2 = ADCPi(0x6A, 0x6B, 12)

# SOUND
mixer.init()
deep_button_sound = mixer.Sound("deep_button_sound.ogg")

# IO PI PLUS shield setup

iobus1 = IOPi(0x20)  # bus 1 will be inputs
iobus2 = IOPi(0x21)  # bus 2 will be outputs

# inputs op bus 1
iobus1.set_port_direction(0, 0xFF)
iobus1.set_port_pullups(0, 0xFF)

# Outputs op bus 2
iobus2.set_port_direction(0, 0x00)
iobus2.write_port(0, 0x00)

t = 0


def test_ledstrips():
    ''' control all ledstrips with the rgb slides'''
    r = adc1.read_voltage(4) * 50
    g = adc1.read_voltage(5) * 50
    b = adc1.read_voltage(6) * 50
    pixels = [(r, g, b)] * numLEDs
    client.put_pixels(pixels)


def test_buttons():
    for i in range(1, 17):
        if iobus1.read_pin(i) == 0:
            mixer.Sound.play(deep_button_sound)


def test_leds():
    for i in range(1, 17):
        iobus2.write_pin(i, 1)


def topknobquit():
    ''' if two buttons are pushed at the same time testing ends'''
    topknobs = [0] * 6
    for i in topknobs:
        topknobs[i] = iobus1[1 + 2 * i]
    return sum(topknobs)


def main():
    test_leds()
    while topknobquit() != 2:
        test_ledstrips()
        test_buttons()
    else:
        for i in range(1, 17):
            iobus2.write_pin(i, 0)
        pixels = [(0, 0, 0)] * numLEDs
        client.put_pixels(pixels)


if __name__ == '__main__':
    main()
