from msvcrt import getch
while True:
    key = ord(getch())
    if key == 27: #ESC
        break
    elif key == 13: #Enter
        select()
    elif key == 224: #Special keys (arrows, f keys, ins, del, etc.)
        key = ord(getch())
        if key == 80: #Down arrow
            moveDown()
        elif key == 72: #Up arrow
            moveUp()