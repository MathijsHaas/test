""" script handeling the sounds """

from pygame import mixer

mixer.init()
background_sound = mixer.Sound("sound_background.ogg")
won_the_box_sound = mixer.Sound("sound_win_box.ogg")
lost_the_box_sound = mixer.Sound("sound_lost_box.ogg")
good_sound = mixer.Sound("sound_good.ogg")



# importing the differtent modules that play sound
import blackbox
import top_buttons
import plugs_game
import RGB_game
import simon_says
import sinus_game
import color_follow

