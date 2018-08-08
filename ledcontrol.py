import multiprocessing
import opc
import testy

numLEDs = 4
client = opc.Client('localhost:7890')

red_array = multiprocessing.Array('i', numLEDs)
red_array.array = [0, ] * numLEDs
green_array = multiprocessing.Array('i', numLEDs)
green_array.array = [0, ] * numLEDs
blue_array = multiprocessing.Array('i', numLEDs)
blue_array.array = [0, ] * numLEDs

# pixel_moment = list(zip(red_array, blue_array, green_array))


def make_pixel_list(r, g, b):
    '''neem de pixels_array die uit losse waardes bestaat en maak er een list van rgb waardes van waarbij iedere
    3 waardes een led aansturen. de pixels_list bestaan dan uit tuples van 3 waardes (rgb) in de vorm [(0,0,0),(0,0,0), .... ]'''
    pixel_moment = list(zip(r, g, b))
    return pixel_moment


def update_led():
    for i in range(1, 11):
        print (red_array.array)
        client.put_pixels(make_pixel_list(red_array.array, green_array.array, blue_array.array))
        print (i, make_pixel_list(red_array.array, green_array.array, blue_array.array))


def main():
    print("start main")
    p = multiprocessing.Process(target=testy.kleur, args=(red_array.array))
    p.daemon = True  # makes it a background process that quits when the main program quits
    print("start process")
    p.start()
    print("start update")
    update_led()
    print("stop update")


if __name__ == "__main__":
    main()
