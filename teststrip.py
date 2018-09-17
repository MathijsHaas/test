import time
import multiprocessingmanager
import multiprocessing

manager = multiprocessing.Manager()
shared_list = manager.list()


def main():
    manager = multiprocessing.Manager()
    print (shared_list)
