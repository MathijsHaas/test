numLEDs = 3
pixelmoment = [1, 2, 3, 4, 5, 6, 7, 8, 9]
red = [1, 4, 7]
blue = [2, 5, 8]
green = [3, 6, 9]

pixels_list = []
numLEDs = 3
pixels = [(0, 0, 0)] * numLEDs


def make_pixel_list():
    '''neem de pixels_array die uit losse waardes bestaat en maak er een list van rgb waardes van waarbij iedere
    3 waardes een led aansturen. de pixels_list bestaan dan uit tuples van 3 waardes (rgb) in de vorm [(0,0,0),(0,0,0), .... ]'''


"""  test
    for i in numLEDs:
        a = pixelmoment.pop(0)
        b = pixelmoment.pop(0)
        c = pixelmoment.pop(0)
        global pixels_list
        pixels_list[i - 1] = (a, b, c)
"""
z = list(zip(red, blue, green))

print (pixels)
print (z)
