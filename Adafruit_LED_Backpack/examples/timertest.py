import datetime
import time


startTime = datetime.datetime.now()

time.sleep(1)

stopTime = datetime.datetime.now()
timePlayed = str(stopTime - startTime)


tensOfMinutes = timePlayed[2]
onesOfMinutes = timePlayed[3]
tensOfSeconds = timePlayed[5]
OnesOfSeconds = timePlayed[6]

print (tensOfMinutes, OnesOfMinutes, tensOfSeconds, OnesOfSeconds)


# setting the time as induvidual caracters to send to the clock display
segment.set_digit(0, tensOfMinutes)
segment.set_digit(1, onesOfMinutes)
segment.set_digit(2, tensOfSeconds)
segment.set_digit(3, OnesOfSeconds)
segment.set_colon(True)                       # Toggle colon

# update the display LEDs.
segment.write_display()
