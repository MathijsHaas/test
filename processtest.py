import multiprocessing
# import simon_says
# import slidetest
import time
import threading


slidetest_won = False


def main():
    slidetest_begonnen = False
    simon_says_begonnen = False

    while True:
        if slidetest_begonnen is False:
            slidetest_process = multiprocessing.Process(target=slidetest.main)
            slidetest_process.start()
            slidetest_begonnen = True
        if slidetest.game_won.value == 1 and simon_says_begonnen == False:
            print("ss start")
            '''
            simon_says_process = multiprocessing.Process(target=simon_says.main)
            simon_says_process.start()
            simon_says_begonnen = True
            '''


if __name__ == "__main__":
    ledcontrol_process = multiprocessing.Process(target=ledcontrol.main)
    ledcontrol_process.start()
    main()
