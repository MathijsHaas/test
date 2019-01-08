""" script handeling the sounds """

import multiprocessing

# importing the differtent modules that play sound
import blackbox
import top_buttons
import plugs_game
import RGB_game
import simon_says
import sinusgame
import color_follow

play_background_sound = multiprocessing.Value('i', 0)
play_won_the_box_sound = multiprocessing.Value('i', 0)
play_start_the_box_sound = multiprocessing.Value('i', 0)
play_lost_the_box_sound = multiprocessing.Value('i', 0)
play_good_sound = multiprocessing.Value('i', 0)
play_wrong_sound = multiprocessing.Value('i', 0)
play_deep_button_sound = multiprocessing.Value('i', 0)
play_bleep = multiprocessing.Value('i', 0)
play_simon1 = multiprocessing.Value('i', 0)
play_simon2 = multiprocessing.Value('i', 0)
play_simon3 = multiprocessing.Value('i', 0)
play_simon4 = multiprocessing.Value('i', 0)

def main():
    print("sound module started")


 