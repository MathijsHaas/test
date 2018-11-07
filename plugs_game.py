import time
import layout
import multiprocessing
import bb_sound


# --------------------- PARAMETERS -----------------------------------

wait_time = 5  # amount of times it needs to be correct when checked.
margin = 80  # the accepted error
v1 = 3232
v2 = 3230
v3 = 1092

game_won = multiprocessing.Value('i', 0)

# ---------------------- THE GAME ------------------------------------


def main():
    counter = 0  # so you dont accidentally come past the right voltage
    while game_won.value == 0:
        time.sleep(0.2)
##        print("1: ", layout.plugs1_value.value, "  2: ", layout.plugs2_value.value, "  3: ", layout.plugs3_value.value)
        if (layout.plugs1_value.value >= (v1 - margin) and layout.plugs1_value.value <= (v1 + margin) and
            layout.plugs2_value.value >= (v2 - margin) and layout.plugs2_value.value <= (v2 + margin) and
                layout.plugs3_value.value >= (v3 - margin) and layout.plugs3_value.value <= (v3 + margin)):
            counter += 1
            if counter == wait_time:
                bb_sound.play_good_sound.value = 1
                game_won.value = 1
                break
        else:
            counter = 0
    print("plugs rightly plugged")


if __name__ == "__main__":
    layout_process = multiprocessing.Process(target=layout.main)
    layout_process.start()
    main()
    layout_process.terminate()
