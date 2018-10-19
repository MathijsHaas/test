#!/usr/bin/sh
unclutter -idle 1 &
# midori -e Fullscreen -a http://localhost:5000 &
sudo amixer set PCM -- 100%
sudo amixer cset numid=3 1
sudo /home/pi/fadecandy/bin/fcserver-rpi
python3 /home/pi/test/blackbox.py
#/usr/local/bin/processing-java --sketch=/home/pi/sinewave/sine_test --run
