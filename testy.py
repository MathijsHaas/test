import multiprocessing


def kleur(red_array.array):
    p = 10
    for a in range(10):
        for arg in args:
            ledcontrol.red_array.array[arg] = p
            p += 10
            print (arg, ledcontrol.red_array.array)


import ledcontrol

if __name__ == '__main__':
    rij = multiprocessing.Array('i', 3)
    rij.array = [0] * 3
    print (rij.array)
    rij.array[2] = 6
    print (rij.array)
