import time
import datetime
import random
import layout
import multiprocessing
import bb_sound


# -------------- PARAMETERS --------------------------------
led_pins = ["led1", "led2", "led3", "led4"]
press_time = datetime.timedelta(seconds=2)  # seconds
levels = 10

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
        time.sleep(0.02)
        if layout.color_follow_button1_value.value == 0:
            ledchoice = "led1"
            print("led1")
            bb_sound.play_bleep.value = 1
            break

        elif layout.color_follow_button2_value.value == 0:
            ledchoice = "led2"
            print("led2")
            bb_sound.play_bleep.value = 1
            break

        elif layout.color_follow_button3_value.value == 0:
            ledchoice = "led3"
            print("led3")
            bb_sound.play_bleep.value = 1
            break

        elif layout.color_follow_button4_value.value == 0:
            ledchoice = "led4"
            print("led4")
            bb_sound.play_bleep.value = 1
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
    while game_won.value == 0:
        time.sleep(0.02)
        new_led = random.choice(led_pins)
        print(new_led)
        put_led_on(new_led)
        status = correct_input(new_led)
        put_led_off(new_led)
        while layout.color_follow_button1_value.value == 0 or layout.color_follow_button2_value.value == 0 or layout.color_follow_button3_value.value == 0 or layout.color_follow_button4_value.value == 0:
            time.sleep(0.01)
            pass  # stops the program until you release the button again.
        if status is True:
            count += 1
            print(count)
            if count == levels:
                time.sleep(1)
                bb_sound.play_good_sound.value = 1
                game_won.value = 1
                print ("gewonnen")
                break
            continue
        else:
            bb_sound.play_wrong_sound.value = 1
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
