
from __future__ import absolute_import, division, print_function, \
    unicode_literals
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

import multiprocessing
import time

#  analog shield adress
adc1 = ADCPi(0x6C, 0x6D, 12)
adc2 = ADCPi(0x6A, 0x6B, 12)

# IO PI PLUS shield setup
iobus1 = IOPi(0x20)  # bus 1 will be inputs
iobus2 = IOPi(0x21)  # bus 2 will be outputs

# inputs op bus 1
iobus1.set_port_direction(0, 0xFF)
iobus1.set_port_pullups(0, 0xFF)
iobus1.set_port_direction(1, 0xFF)
iobus1.set_port_pullups(1, 0xFF)

# Outputs op bus 2
iobus2.set_port_direction(0, 0x00)
iobus2.write_port(0, 0x00)
iobus2.set_port_direction(1, 0x00)
iobus2.write_port(1, 0x00)


# ---- test ----

game_status = multiprocessing.Value('i', 0)


# ------------------ ASSIGNING THE SHIELD PINS ---------------

''' DIGITAL INPUTS ON BUS 1 (ALL PULLUP) '''

# top buttons
top_button1 = 1
top_button2 = 3
top_button3 = 5
top_button4 = 7
top_button5 = 9
top_button6 = 11

# simon says game buttons
ss_button1 = 2
ss_button2 = 4
ss_button3 = 6
ss_button4 = 8

# Color follow buttons
color_follow_button1 = 10
color_follow_button2 = 12
color_follow_button3 = 14
color_follow_button4 = 16

# the input that reads if the the big turning knobs are in the right orientation.
big_knobs = 15

'''DIGITAL OUTPUTS ON BUS 2 '''

# top leds
top_led1 = 1
top_led2 = 3
top_led3 = 5
top_led4 = 7
top_led5 = 9
top_led6 = 11

# simon says game leds
ss_led1 = 2
ss_led2 = 4
ss_led3 = 6
ss_led4 = 8

# color follow game leds
color_follow_led1 = 10
color_follow_led2 = 12
color_follow_led3 = 14
color_follow_led4 = 16

# Relais that switches the back & bottom light on
relais = 13

'''ANALOG INPUTS ADC 1 (second shield)'''

# plugs game
plugs1 = 1
plugs2 = 2
plugs3 = 3

RGBslide1 = 6
RGBslide2 = 5
RGBslide3 = 4


'''ANALOG INPUTS ADC 2 (third (and top) shield)'''
sinusknob1 = 1
sinusknob2 = 2
sinusknob3 = 3

bypass = 4


# ------------------ MULTIPROCESSING VALUES TO WORK WITH ACROS FILES ---------------

top_button1_value = multiprocessing.Value('i', 0)
top_button2_value = multiprocessing.Value('i', 0)
top_button3_value = multiprocessing.Value('i', 0)
top_button4_value = multiprocessing.Value('i', 0)
top_button5_value = multiprocessing.Value('i', 0)
top_button6_value = multiprocessing.Value('i', 0)

# simon says game buttons
ss_button1_value = multiprocessing.Value('i', 0)
ss_button2_value = multiprocessing.Value('i', 0)
ss_button3_value = multiprocessing.Value('i', 0)
ss_button4_value = multiprocessing.Value('i', 0)

# Color follow buttons
color_follow_button1_value = multiprocessing.Value('i', 0)
color_follow_button2_value = multiprocessing.Value('i', 0)
color_follow_button3_value = multiprocessing.Value('i', 0)
color_follow_button4_value = multiprocessing.Value('i', 0)

# the input that reads if the the big turning knobs are in the right orientation.
big_knobs_value = multiprocessing.Value('i', 1)

'''DIGITAL OUTPUTS ON BUS 2 '''

# top leds
top_led1_value = multiprocessing.Value('i', 1)
top_led2_value = multiprocessing.Value('i', 1)
top_led3_value = multiprocessing.Value('i', 1)
top_led4_value = multiprocessing.Value('i', 1)
top_led5_value = multiprocessing.Value('i', 1)
top_led6_value = multiprocessing.Value('i', 1)

# simon says game leds !NIET AAPASSEN! deze worden in de code gebruikt
ss_led1_value = multiprocessing.Value('i', 0)
ss_led2_value = multiprocessing.Value('i', 0)
ss_led3_value = multiprocessing.Value('i', 0)
ss_led4_value = multiprocessing.Value('i', 0)

# color follow game leds
color_follow_led1_value = multiprocessing.Value('i', 0)
color_follow_led2_value = multiprocessing.Value('i', 0)
color_follow_led3_value = multiprocessing.Value('i', 0)
color_follow_led4_value = multiprocessing.Value('i', 0)

# Relais that switches the back & bottom light on
relais_value = multiprocessing.Value('i', 0)

'''ANALOG INPUTS ADC 1 (second shield)'''

# plugs game
plugs1_value = multiprocessing.Value('i', 0)
plugs2_value = multiprocessing.Value('i', 0)
plugs3_value = multiprocessing.Value('i', 0)

RGBslide1_value = multiprocessing.Value('i', 0)
RGBslide2_value = multiprocessing.Value('i', 0)
RGBslide3_value = multiprocessing.Value('i', 0)


'''ANALOG INPUTS ADC 2 (third (and top) shield)'''
sinusknob1_value = multiprocessing.Value('i', 0)
sinusknob2_value = multiprocessing.Value('i', 0)
sinusknob3_value = multiprocessing.Value('i', 0)

bypass_value = multiprocessing.Value("i", 0)


def main():
    ''' the loop that controls the input's and output's from the shields'''
    print ("reading and writing the pins")
    for i in range(1, 17): # put out every lamp that might still be on
            iobus2.write_pin(i, 0)
            
    while True:
        time.sleep(0.01)

        # ------------------'''DIGITAL INPUTS ON BUS 1 '''--------------------------

        top_button1_value.value = iobus1.read_pin(top_button1)
        top_button2_value.value = iobus1.read_pin(top_button2)
        top_button3_value.value = iobus1.read_pin(top_button3)
        top_button4_value.value = iobus1.read_pin(top_button4)
        top_button5_value.value = iobus1.read_pin(top_button5)
        top_button6_value.value = iobus1.read_pin(top_button6)

        # simon says game buttons
        ss_button1_value.value = iobus1.read_pin(ss_button1)
        ss_button2_value.value = iobus1.read_pin(ss_button2)
        ss_button3_value.value = iobus1.read_pin(ss_button3)
        ss_button4_value.value = iobus1.read_pin(ss_button4)

        # Color follow buttons
        color_follow_button1_value.value = iobus1.read_pin(color_follow_button1)
        color_follow_button2_value.value = iobus1.read_pin(color_follow_button2)
        color_follow_button3_value.value = iobus1.read_pin(color_follow_button3)
        color_follow_button4_value.value = iobus1.read_pin(color_follow_button4)

        # the input that reads if the the big turning knobs are in the right orientation.
        big_knobs_value.value = iobus1.read_pin(big_knobs)

# ------------------'''DIGITAL OUTPUTS ON BUS 2 '''------------------

        # ------------------ top leds ------------------------------------
        if top_led1_value.value == 1:
            iobus2.write_pin(top_led1, 1)
        else:
            iobus2.write_pin(top_led1, 0)

        if top_led2_value.value == 1:
            iobus2.write_pin(top_led2, 1)
        else:
            iobus2.write_pin(top_led2, 0)

        if top_led3_value.value == 1:
            iobus2.write_pin(top_led3, 1)
        else:
            iobus2.write_pin(top_led3, 0)

        if top_led4_value.value == 1:
            iobus2.write_pin(top_led4, 1)
        else:
            iobus2.write_pin(top_led4, 0)

        if top_led5_value.value == 1:
            iobus2.write_pin(top_led5, 1)
        else:
            iobus2.write_pin(top_led5, 0)

        if top_led6_value.value == 1:
            iobus2.write_pin(top_led6, 1)
        else:
            iobus2.write_pin(top_led6, 0)

        # ------------------ simon says game leds -----------------------------------------
        if ss_led1_value.value == 1:
            iobus2.write_pin(ss_led1, 1)
        else:
            iobus2.write_pin(ss_led1, 0)

        if ss_led2_value.value == 1:
            iobus2.write_pin(ss_led2, 1)
        else:
            iobus2.write_pin(ss_led2, 0)

        if ss_led3_value.value == 1:
            iobus2.write_pin(ss_led3, 1)
        else:
            iobus2.write_pin(ss_led3, 0)

        if ss_led4_value.value == 1:
            iobus2.write_pin(ss_led4, 1)
        else:
            iobus2.write_pin(ss_led4, 0)

        # ------------------ color follow game leds ------------------------------------
        if color_follow_led1_value.value == 1:
            iobus2.write_pin(color_follow_button1, 1)
        else:
            iobus2.write_pin(color_follow_button1, 0)

        if color_follow_led2_value.value == 1:
            iobus2.write_pin(color_follow_button2, 1)
        else:
            iobus2.write_pin(color_follow_button2, 0)

        if color_follow_led3_value.value == 1:
            iobus2.write_pin(color_follow_button3, 1)
        else:
            iobus2.write_pin(color_follow_button3, 0)

        if color_follow_led4_value.value == 1:
            iobus2.write_pin(color_follow_button4, 1)
        else:
            iobus2.write_pin(color_follow_button4, 0)

        # Relais that switches the back & bottom light on
        if relais_value.value == 1:
            iobus2.write_pin(relais, 1)
        else:
            iobus2.write_pin(relais, 0)

# ------------------ ANALOG INPUTS ADC 1 (second shield)------------------

        # plugs game
        plugs1_value.value = int(adc1.read_voltage(plugs1) * 1000)
        plugs2_value.value = int(adc1.read_voltage(plugs2) * 1000)
        plugs3_value.value = int(adc1.read_voltage(plugs3) * 1000)

        RGBslide1_value.value = int(adc1.read_voltage(RGBslide1) * 35)  # to become a 0-255 value for the RGB led strips
        RGBslide2_value.value = int(adc1.read_voltage(RGBslide2) * 35)
        RGBslide3_value.value = int(adc1.read_voltage(RGBslide3) * 35)

# -------------ANALOG INPUTS ADC 2 (third (and top) shield)---------------

        sinusknob1_value.value = int(adc2.read_voltage(sinusknob1) * 100)
        sinusknob2_value.value = int(adc2.read_voltage(sinusknob2) * 100)
        sinusknob3_value.value = int(adc2.read_voltage(sinusknob3) * 100)

        # a 0 - 5 voltage to measure resistors
        bypass_value.value = int(adc2.read_voltage(bypass) * 1000)


if __name__ == "__main__":
    main()
