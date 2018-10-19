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
background_sound = mixer.Sound("sound_background.ogg")
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
    background_start = False
    while True:
        if blackbox.sound_background == 1 and background is False:
            #loop
            mixer.Sound.play(background_sound)
            background_start = True
        if plugs_game.good_sound == 1 or RGB_game.good_sound == 1 or simon_says.good_sound == 1 or color_follow.good_sound == 1:
            mixer.Sound.play(good_sound)
            
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
        
        


# importing the differtent modules that play sound
