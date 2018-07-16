
from __future__ import absolute_import, division, print_function, \
    unicode_literals
import time
import random
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


iobus1 = IOPi(0x20)  # bus 1 will be inputs
iobus2 = IOPi(0x21)  # bus 2 will be outputs

# inputs op bus 1
iobus1.set_port_direction(0, 0xFF)
iobus1.set_port_pullups(0, 0xFF)

# Outputs op bus 2
iobus2.set_port_direction(0, 0x00)
iobus2.write_port(0, 0x00)
# Flash a LED n seconds


def flash(l, n):
    iobus2.write_pin((2 + 2 * l), 1)  # deze rekensom omdat de eerste ledjes op 2,4,6,8 zitten
    time.sleep(n)
    iobus2.write_pin((2 + 2 * l), 0)
    return

# Flash the LEDs n times


def flash_all(n):
    for i in range(0, n):
        iobus2.write_pin(2, 1)
        iobus2.write_pin(4, 1)
        iobus2.write_pin(6, 1)
        iobus2.write_pin(8, 1)
        time.sleep(0.3)
        iobus2.write_pin(2, 0)
        iobus2.write_pin(4, 0)
        iobus2.write_pin(6, 0)
        iobus2.write_pin(8, 0)
        time.sleep(0.3)
    return


# Verify if user input matches value in expected sequence
def correct_input(value):
    # hier wellicht een aanpassing maken dat hij wel even wacht op een input voordat hij doorgaat.
    if iobus1.read_pin(2) == 0:
        ledchoise = 0
    elif iobus1.read_pin(4) == 0:
        ledchoise = 1
    elif iobus1.read_pin(6) == 0:
        ledchoise = 2
    elif iobus1.read_pin(8) == 0:
        ledchoise = 3
    else:
        return 0

    if ledchoise == value:
        return 1
    else:
        return 0

#####################################
# MAIN PROGRAM, a game of simon says#
#####################################


def main():
    random.seed()   # Different seed for every game
    count = 0  # Keeps track of player score
    sequence = []  # Will contain the sequence of light for the simon says

    while True:
        time.sleep(1)
        new_value = random.randint(0, 3)
        sequence.append(new_value)
        for i in range(0, len(sequence)):
            flash(sequence[i], 0.4)
            time.sleep(0.1)
        for i in range(0, len(sequence)):
            status = correct_input(sequence[i])  # misschien gaat hier wel iets fout, dat er te snel door het programma geskipt wordt
            if status == 1:
                flash(sequence[i], 0.1)
            else:
                flash_all(5)
                break
        else:
            count += 1
            continue
        break

    # End with lights off
    iobus2.write_pin(2, 0)
    iobus2.write_pin(4, 0)
    iobus2.write_pin(6, 0)
    iobus2.write_pin(8, 0)
    print ("Your score is", count)
    return 0


if __name__ == "__main__":
    main()
