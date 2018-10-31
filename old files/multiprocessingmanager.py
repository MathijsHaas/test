import multiprocessing
manager = multiprocessing.Manager()
shared_list = manager.list()
import time
import teststrip


def worker1(l):
    d = 1
    for n in range(10):
        l.append((d, 3, 4))
        d += 1


def worker2(l):
    for n in range(10):
        l[n] = (234, 3, 2)


def main():
    process1 = multiprocessing.Process(
        target=worker1, args=[shared_list])
    process2 = multiprocessing.Process(
        target=worker2, args=[shared_list])

    process1.start()
    process1.join()
    print (shared_list)
    process2.start()
    process2.join()
    print (shared_list)
    print ("strip: ")
    teststrip.main()


if __name__ == '__main__':
    main()
