# Main control
import multiprocessing
import simon_says
import pluggenspel
import six_buttons
import draaiknoppen
import color_follow
import RGB_game

# 0 = not started yet
# 1 = started
# 2 = finished

first_half = 0
second_half = 0


def main():
    while True:

        if six_buttons.game_won is True:
            pluggenspel_process = multiprocessing.Process(target=pluggenspel.main)
            pluggenspel_process.start()
        if pluggenspel.game_won is True:
            RGB_process = multiprocessing.Process(target=RGB_game.main)
            RGB_process.start()
        if RGB_game.game_won is True:
            simon_says_process = multiprocessing.Process(target=simon_says.main)
            simon_says_process.start()           
        if simon_says.game_won is True:
            first_half = 2

        if draaiknoppen.game_won is True:
            # SINUS GAME START
            pass
        # if sinusspel.game_won is True
            color_follow_process = multiprocessing.Process(target=color_follow.main)
            color_follow_process.start()
        if color_follow.game_won is True:
            second_half = 2


if __name__ == "__main__":
    main()
