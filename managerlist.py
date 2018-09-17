import multiprocessing
import teststrip
import time

manager = multiprocessing.Manager()
strip = manager.list()

strip = [(0, 0, 0)] * 3

print (strip)

process1 = multiprocessing.Process(
    target=teststrip.rgb, args=[strip])
# process2 = multiprocessing.Process(
#     target=worker2, args=[strip])

process1.start()

process1.join()


n = 0
while n < 10:
    print(strip)
    time.sleep(0.5)
    n += 1
