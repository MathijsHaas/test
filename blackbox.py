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

'''
Every game is it's own process in its seperate file.
Each game has a game_won variable that is an multiprocessing value we can acces.
This game_won value turns 1 when the game is won and thus the next game can start.

Each game also has its own variable in the main loop to make sure the process only starts once.

'''


def main():
    # at the start, no games ar started.
    six_buttons_started = False
    pluggenspel_started = False
    RGB_game_started = False
    simon_says_started = False
    draaiknoppen_started = False
    sinusspel_started = False
    color_follow_started = False

    # this while loop keeps running to manage the game progression
    while True:
        # start plug game after the six buttons are pushed togheter
        if top_buttons.top_status.value == 1 and pluggenspel_started == False:
            pluggenspel_process = multiprocessing.Process(target=pluggenspel.main)
            pluggenspel_process.start()
            pluggenspel_started = True

        # Start the RGB game after all 6 plugs are connected correctly
        if pluggenspel.game_won.value == 1 and pluggenspel_started == False:
            RGB_process = multiprocessing.Process(target=RGB_game.main)
            RGB_process.start()
            pluggenspel_started = True

        # start Simon Says after all RGB game colors are machted correctly
        if RGB_game.game_won.value == 1 and simon_says_started == False:
            simon_says_process = multiprocessing.Process(target=simon_says.main)
            simon_says_process.start()
            simon_says_started = True

        if simon_says.game_won.value == 1:
            first_half = 2

        # start the big turning knobs at the same time as the plug game.
        if top_buttons.top_status.value == 1 and draaiknoppen_started == False:
            draaiknoppen_process = multiprocessing.Process(target=draaiknoppen.main)
            draaiknoppen_process.start()
            draaiknoppen_started = True

        if draaiknoppen.game_won.value == 1 and sinusspel_started == False:
            # start sinusspel
            sinusspel_started = True

        # start Color follow after dhe sinus game is won
        if sinusspel.game_won.value == 1 and draaiknoppen_started == False:
            color_follow_process = multiprocessing.Process(target=color_follow.main)
            color_follow_process.start()
            draaiknoppen_started = True

        if color_follow.game_won.value == 1:
            second_half = 2


if __name__ == "__main__":
    main()
