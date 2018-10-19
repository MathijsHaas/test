#!/bin/sh
unclutter -idle 1 &
# midori -e Fullscreen -a http://localhost:5000 &
terminal -e command
sudo amixer set PCM -- 100%
sudo amixer cset numid=3 1
echo "starting the blackbox"
python3 /home/pi/test/blackbox.py &
echo "starting the sinewave" 
/usr/local/bin/processing-java --sketch=/home/pi/sinewave/sine_test --force --run &
echo "fadecandy server setup"
sudo /home/pi/fadecandy/bin/fcserver-rpi &
echo "everything run"