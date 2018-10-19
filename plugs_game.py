from pygame import mixer
import time
import layout
import multiprocessing

mixer.init()
good_sound = mixer.Sound("sound_good.ogg")


# --------------------- PARAMETERS -----------------------------------

wait_time = 5  # amount of times it needs to be correct when checked.
margin = 50  # the accepted error
v1 = 3300
v2 = 3250
v3 = 1080

game_won = multiprocessing.Value('i', 0)

# ---------------------- THE GAME ------------------------------------


def main():
    counter = 0  # so you dont accidentally come past the right voltage
    while True:
        time.sleep(0.2)
        # print("1: ", layout.plugs1_value.value, "  2: ", layout.plugs2_value.value, "  3: ", layout.plugs3_value.value)
        if (layout.plugs1_value.value >= (v1 - margin) and layout.plugs1_value.value <= (v1 + margin) and
            layout.plugs2_value.value >= (v2 - margin) and layout.plugs2_value.value <= (v2 + margin) and
                layout.plugs3_value.value >= (v3 - margin) and layout.plugs3_value.value <= (v3 + margin)):
            counter += 1
            if counter == wait_time:
                mixer.Sound.play(good_sound)
                game_won.value = 1
                print("plugs rightly plugged")
                break
        else:
            counter = 0


if __name__ == "__main__":
    layout_process = multiprocessing.Process(target=layout.main)
    layout_process.start()
    main()
    layout_process.terminate()
