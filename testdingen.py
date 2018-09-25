import layout
import time
import multiprocessing

layout_process = multiprocessing.Process(target=layout.main)
layout_process.start()


time.sleep(1)

print ("slides:", layout.RGBslide1_value.value, layout.RGBslide2_value.value, layout.RGBslide3_value.value)

red = layout.RGBslide1_value.value + 100 
green = layout.RGBslide2_value.value + 100

print ("red and green: ", red, green)

layout_process.terminate()