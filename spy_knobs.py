from __future__ import absolute_import, division, print_function, \
    unicode_literals
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
import buttonlayout
import multiprocessing
from pygame import mixer

# SOUND
mixer.init()
good_sound = mixer.Sound("good_sound.ogg")

# IO PI PLUS shield setup
iobus1 = IOPi(0x20)  # bus 1 will be inputs

# inputs op bus 1
iobus1.set_port_direction(0, 0xFF)
iobus1.set_port_pullups(0, 0xFF)

spy_knobs = buttonlayout.spy_knobs

game_won = multiprocessing.Value('i', 0)

def main():
    if spy_knobs == 0:
        print ('spy knobs correctly oriëntated')
        game_won.value = 1

if __name__ == '__main__':
    main()
