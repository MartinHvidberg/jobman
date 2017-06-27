import msvcrt

while True:
    if msvcrt.kbhit():
        key = msvcrt.getch()
        print "::", key  # just to show the result