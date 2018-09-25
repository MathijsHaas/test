from pygame import mixer
import layout
import multiprocessing

mixer.init()
good_sound = mixer.Sound("good_sound.ogg")


# --------------------- PARAMETERS -----------------------------------

wait_time = 20  # amount of times it needs to be correct when checked.
margin = 50  # the accepted error
v1 = 350
v2 = 350
v3 = 350

game_won = multiprocessing.Value('i', 0)

# ---------------------- THE GAME ------------------------------------


def main():
    counter = 0  # so you dont accidentally come past the right voltage
    while True:
        if (layout.plugs1_value.value >= (v1 - margin) and layout.plugs1_value.value <= (v1 + margin) and
            layout.plugs2_value.value >= (v2 - margin) and layout.plugs2_value.value <= (v2 + margin) and
                layout.plugs3_value.value >= (v3 - margin) and layout.plugs3_value.value <= (v3 + margin)):
            counter += 1
            if counter == wait_time:
                mixer.Sound.play(good_sound)
                game_won is True
                return True
            else:
                counter = 0


if __name__ == "__main__":
    main()
