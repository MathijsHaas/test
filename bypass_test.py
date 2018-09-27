import layout
import multiprocessing
import time
count = 0

def main():
    plug_bypass = 1
    RGB_bypass = 1
    simon_says_bypass = 1
    turning_knobs_bypass = 1
    sinus_game_bypass = 1
    color_follow_bypass = 1 
    
    global count
    bypass = 0
    margin = 100
    count_number = 100  # the amount of times it needs to check if there is a value before passing it to see what it is.

    if layout.bypass_value.value > 100 or layout.bypass_value.value < 4900:
        count += 1
    else:
        count = 0

    if count > count_number:
        if (layout.bypass_value.value <= (plug_bypass - margin) and layout.bypass_value.value >= (plug_bypass + margin)):
            bypass = 1
        elif (layout.bypass_value.value <= (RGB_bypass - margin) and layout.bypass_value.value >= (RGB_bypass + margin)):
            bypass = 2
        elif (layout.bypass_value.value <= (simon_says_bypass - margin) and layout.bypass_value.value >= (simon_says_bypass + margin)):
            bypass = 3
        elif (layout.bypass_value.value <= (turning_knobs_bypass - margin) and layout.bypass_value.value >= (turning_knobs_bypass + margin)):
            bypass = 4
        elif (layout.bypass_value.value <= (sinus_game_bypass - margin) and layout.bypass_value.value >= (sinus_game_bypass + margin)):
            bypass = 5
        elif (layout.bypass_value.value <= (color_follow_bypass - margin) and layout.bypass_value.value >= (color_follow_bypass + margin)):
            bypass = 6
            
        print(bypass)
        
if __name__ == "__main__":
    layout_process = multiprocessing.Process(target=layout.main)
    layout_process.start()
  
    while True:
        main()
        print(layout.bypass_value.value)
        time.sleep(0.2)

