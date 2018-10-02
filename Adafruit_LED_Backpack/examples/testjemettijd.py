import datetime
import time

secondsToPlay = datetime.timedelta(seconds=3)

nu = datetime.datetime.now()

deadline = datetime.datetime.now() + secondsToPlay

while datetime.datetime.now() < deadline:
    print ("playing")
    print (datetime.datetime.now() < deadline)
    time.sleep(1)
else:
    print("klaar")
