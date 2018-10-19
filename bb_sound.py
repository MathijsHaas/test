""" script handeling the sounds """

from pygame import mixer
import multiprocessing

# importing the differtent modules that play sound
import blackbox
import top_buttons
import plugs_game
import RGB_game
import simon_says
import sinus_game
import color_follow

mixer.init()
mixer.music.load("sound_background.ogg")
won_the_box_sound = mixer.Sound("sound_win_box.ogg")
lost_the_box_sound = mixer.Sound("sound_lost_box.ogg")
good_sound = mixer.Sound("sound_good.ogg")
wrong_sound = mixer.Sound("sound_wrong.ogg")
deep_button_sound = mixer.Sound("sound_deep_button.ogg")
bleep = mixer.Sound("sound_small_button.ogg")
simon1 = mixer.Sound("sound_simon1.ogg")
simon2 = mixer.Sound("sound_simon2.ogg")
simon3 = mixer.Sound("sound_simon3.ogg")
simon4 = mixer.Sound("sound_simon4.ogg")


play_background_sound = multiprocessing.Value('i', 0)
play_won_the_box_sound = multiprocessing.Value('i', 0)
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
    mixer.music.play(-1)
    while True:
        if play_won_the_box_sound.value == 1:
            mixer.Sound.play(won_the_box_sound)
            play_won_the_box_sound.value == 0

        if play_lost_the_box_sound.value == 1:
            mixer.Sound.play(lost_the_box_sound)
            play_lost_the_box_sound.value == 0

        if play_good_sound.value == 1:
            mixer.Sound.play(good_sound)
            play_good_sound.value == 0

        if play_wrong_sound.value == 1:
            mixer.Sound.play(wrong_sound)
            play_wrong_sound.value == 0

        if play_deep_button_sound.value == 1:
            mixer.Sound.play(deep_button_sound)
            play_deep_button_sound.value == 0

        if play_bleep.value == 1:
            mixer.Sound.play(bleep)
            play_bleep.value == 0

        if play_simon1.value == 1:
            mixer.Sound.play(simon1)
            play_simon1.value == 0

        if play_simon2.value == 1:
            mixer.Sound.play(simon2)
            play_simon2.value == 0

        if play_simon3.value == 1:
            mixer.Sound.play(simon3)
            play_simon3.value == 0

        if play_simon4.value == 1:
            mixer.Sound.play(simon4)
            play_simon4.value == 0

