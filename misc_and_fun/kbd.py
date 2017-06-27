import msvcrt  # built-in module


def kbfunc():
    return ord(msvcrt.getch()) if msvcrt.kbhit() else 0

if __name__ == '__main__':

    go = True

    while go:
        for n in range(10000000):
            pass
        print '.',
        k = kbfunc()
        print '\n', str(type(k)), k  # <-- Why the h... is this never printing anything but <type 'int'> 0 ???
        if k == 'q':
            go = False

