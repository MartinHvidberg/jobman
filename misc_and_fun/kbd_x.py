import getche_x  # built-in module


def kbfunc():
    return ord(getche_x.getch()) ## if msvcrt.kbhit() else 0

if __name__ == '__main__':

    go = True

    while go:
        for n in range(10000000):
            pass
        print '.',
        k = kbfunc()
        print '\n', str(type(k)), k
        if k == 'q':
            go = False

