
from __future__ import absolute_import, division, print_function, \
    unicode_literals
import time
import random
import pygame
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

#pygame.init()
#bleep1 = pygame.mixer.Sound("bleep1.wav")
#bleep2 = pygame.mixer.Sound("bleep2.wav")
#bleep3 = pygame.mixer.Sound("bleep3.wav")
#bleep4 = pygame.mixer.Sound("bleep4.wav")

pygame.mixer.init()
bleep1 = pygame.mixer.Sound("bleep1.ogg")
bleep2 = pygame.mixer.Sound("bleep2.ogg")
bleep3 = pygame.mixer.Sound("bleep3.ogg")
bleep4 = pygame.mixer.Sound("bleep4.ogg")
wrong_sound = pygame.mixer.Sound("wrong_sound.ogg")
good_sound = pygame.mixer.Sound("good_sound.ogg")


## IO PI PLUS shield setup

iobus1 = IOPi(0x20)  # bus 1 will be inputs
iobus2 = IOPi(0x21)  # bus 2 will be outputs

# inputs op bus 1
iobus1.set_port_direction(0, 0xFF)
iobus1.set_port_pullups(0, 0xFF)

# Outputs op bus 2
iobus2.set_port_direction(0, 0x00)
iobus2.write_port(0, 0x00)



def flash(l, n):
    """flash led l for n times"""
    iobus2.write_pin((2 + 2 * l), 1)  # deze rekensom omdat de eerste ledjes op 2,4,6,8 zitten
    time.sleep(n)
    iobus2.write_pin((2 + 2 * l), 0)
    return


def flash_all(n):
    """flash all leds for n times"""
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


def correct_input(value):
    """check if the input is correct"""
    while True:
        # hier moet nog wel een timer in
        buttonstate2 = iobus1.read_pin(2)
        buttonstate4 = iobus1.read_pin(4)
        buttonstate6 = iobus1.read_pin(6)
        buttonstate8 = iobus1.read_pin(8)

        if buttonstate2 == 0:
            ledchoise = 0
            print("led1")
            pygame.mixer.Sound.play(bleep1)
            break
        
        elif buttonstate4 == 0:
            ledchoise = 1
            print("led2")
            pygame.mixer.Sound.play(bleep2)
            break
        
        elif buttonstate6 == 0: 
            ledchoise = 2
            print("led3")
            pygame.mixer.Sound.play(bleep3)
            break
        
        elif buttonstate8 == 0:  
            ledchoise = 3
            print("led4")
            pygame.mixer.Sound.play(bleep4)
            break
         
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
    countahhh = 0 # gewoon maar even ergens tellen. gebeurd verder niet zoveel mee
    
    while True:
        time.sleep(1)
        new_value = random.randint(0, 3)
        sequence.append(new_value)
        for i in range(0, len(sequence)):
            print (sequence[i])
            if sequence[i] == 0:
                bleep = bleep1
            elif sequence[i] == 1:
                bleep = bleep2
            elif sequence[i] == 2:
                bleep = bleep3
            elif sequence[i] == 3:
                bleep = bleep4
            pygame.mixer.Sound.play(bleep)
            flash(sequence[i], 0.4)
            time.sleep(0.1)
        for i in range(0, len(sequence)):
            while iobus1.read_pin(2) == 0 or iobus1.read_pin(4) == 0 or iobus1.read_pin(6) == 0 or iobus1.read_pin(8) == 0:
                countahhh += 1 # hier kan wel iets van een timer in gezet worden die checkt of je niet te laat bent
            status = correct_input(sequence[i])  # misschien gaat hier wel iets fout, dat er te snel door het programma geskipt wordt
            time.sleep(0.05)
            if status == 1:
                flash(sequence[i], 0.1)
            else:
                pygame.mixer.Sound.play(wrong_sound)
                flash_all(3)
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
