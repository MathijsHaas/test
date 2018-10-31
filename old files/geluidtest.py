from pygame import mixer
import bb_sound

mixer.init()
mixer.music.load("sound_background.ogg")
won_the_box_sound = mixer.Sound("sound_win_box.ogg")
lost_the_box_sound = mixer.Sound("sound_lost_box.ogg")
start_the_box_sound = mixer.Sound("sound_start_box.ogg")
good_sound = mixer.Sound("sound_good.ogg")
wrong_sound = mixer.Sound("sound_wrong.ogg")
deep_button_sound = mixer.Sound("sound_deep_button.ogg")
bleep = mixer.Sound("sound_small_button.ogg")
simon1 = mixer.Sound("sound_simon1.ogg")
simon2 = mixer.Sound("sound_simon2.ogg")
simon3 = mixer.Sound("sound_simon3.ogg")
simon4 = mixer.Sound("sound_simon4.ogg")

while True:
    if bb_sound.play_start_the_box_sound.value == 1:
        mixer.Sound.play(start_the_box_sound)
        bb_sound.play_start_the_box_sound.value = 0
    
    if bb_sound.play_won_the_box_sound.value == 1:
        mixer.Sound.play(won_the_box_sound)
        bb_sound.play_won_the_box_sound.value = 0

    if bb_sound.play_lost_the_box_sound.value == 1:
        mixer.Sound.play(lost_the_box_sound)
        bb_sound.play_lost_the_box_sound.value = 0

    if bb_sound.play_good_sound.value == 1:
        mixer.Sound.play(good_sound)
        bb_sound.play_good_sound.value = 0

    if bb_sound.play_wrong_sound.value == 1:
        mixer.Sound.play(wrong_sound)
        bb_sound.play_wrong_sound.value = 0

    if bb_sound.play_deep_button_sound.value == 1:
        mixer.Sound.play(deep_button_sound)
        bb_sound.play_deep_button_sound.value = 0

    if bb_sound.play_bleep.value == 1:
        mixer.Sound.play(bleep)
        bb_sound.play_bleep.value = 0

    if bb_sound.play_simon1.value == 1:
        mixer.Sound.play(simon1)
        bb_sound.play_simon1.value = 0

    if bb_sound.play_simon2.value == 1:
        mixer.Sound.play(simon2)
        bb_sound.play_simon2.value = 0

    if bb_sound.play_simon3.value == 1:
        mixer.Sound.play(simon3)
        bb_sound.play_simon3.value = 0

    if bb_sound.play_simon4.value == 1:
        mixer.Sound.play(simon4)
        bb_sound.play_simon4.value = 0