import time
import datetime
import random
from pygame import mixer
import layout
import multiprocessing


mixer.init()
bleep1 = mixer.Sound("bleep2.ogg")
bleep2 = mixer.Sound("bleep2.ogg")
bleep3 = mixer.Sound("bleep2.ogg")
bleep4 = mixer.Sound("bleep2.ogg")
wrong_sound = mixer.Sound("wrong_sound.ogg")
good_sound = mixer.Sound("good_sound.ogg")


# -------------- PARAMETERS --------------------------------
led_pins = ["led1", "led2", "led3", "led4"]
press_time = datetime.timedelta(seconds=2)  # seconds
levels = 6

game_won = multiprocessing.Value('i', 0)

# -------------- FUNCTIONS FOR IN THE GAME ---------------------


def flash_all(n):
    """flash all leds for n times"""
    for i in range(0, n):
        layout.color_follow_led1_value.value = 1
        layout.color_follow_led2_value.value = 1
        layout.color_follow_led3_value.value = 1
        layout.color_follow_led4_value.value = 1
        time.sleep(0.3)
        layout.color_follow_led1_value.value = 0
        layout.color_follow_led2_value.value = 0
        layout.color_follow_led3_value.value = 0
        layout.color_follow_led4_value.value = 0
        time.sleep(0.3)


def correct_input(value):
    """check if the input is correct within the time"""
    deadline = datetime.datetime.now() + press_time
    print("checking input")
    ledchoice = None 
    
    while datetime.datetime.now() < deadline:
        if layout.color_follow_button1_value.value == 0:
            ledchoice = "led1"
            print("led1")
            mixer.Sound.play(bleep1)
            break

        elif layout.color_follow_button2_value.value == 0:
            ledchoice = "led2"
            print("led2")
            mixer.Sound.play(bleep2)
            break

        elif layout.color_follow_button3_value.value == 0:
            ledchoice = "led3"
            print("led3")
            mixer.Sound.play(bleep3)
            break

        elif layout.color_follow_button4_value.value == 0:
            ledchoice = "led4"
            print("led4")
            mixer.Sound.play(bleep4)
            break

    if ledchoice == value:
        print ("right button!")
        return True
    else:
        return False


def put_led_on(led):
    if led == "led1":
        layout.color_follow_led1_value.value = 1
    elif led == "led2":
        layout.color_follow_led2_value.value = 1
    elif led == "led3":
        layout.color_follow_led3_value.value = 1
    elif led == "led4":
        layout.color_follow_led4_value.value = 1


def put_led_off(led):
    if led == "led1":
        layout.color_follow_led1_value.value = 0
    elif led == "led2":
        layout.color_follow_led2_value.value = 0
    elif led == "led3":
        layout.color_follow_led3_value.value = 0
    elif led == "led4":
        layout.color_follow_led4_value.value = 0

# ---------------- THE GAME -----------------------------------


def main():
    random.seed()
    count = 0
    print (count)
    while True:
        time.sleep(1)
        new_led = random.choice(led_pins)
        print(new_led)
        put_led_on(new_led)
        status = correct_input(new_led)
        put_led_off(new_led)
        if status is True:
            count += 1
            print(count)
            if count == levels:
                time.sleep(1)
                mixer.Sound.play(good_sound)
                game_won.value = 1
                print ("gewonnen")
                break
            continue
        else:
            mixer.Sound.play(wrong_sound)
            flash_all(3)
            count = 0
            print("verloren")

        # zet lampje aan
        # tijd geven om goeie knopje in te drukken
        # als goeie knopje count +1 & continieu
        # als te laat Break


if __name__ == "__main__":
    
    layout_process = multiprocessing.Process(target=layout.main)
    layout.color_follow_led1_value.value = 0
    layout.color_follow_led2_value.value = 0
    layout.color_follow_led3_value.value = 0
    layout.color_follow_led4_value.value = 0
    layout_process.start()
    main()
    layout_process.terminate()
