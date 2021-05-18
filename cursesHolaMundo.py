import curses
stdscr = curses.initscr()


def print_in_middle(win, starty, startx, width, string):
    if (win == None): win = stdscr
    y, x = curses.getwin(win)
    if (startx != 0): x = startx
    if (starty != 0): y = starty
    if (width == 0): width = 80
    length = len(string)
    temp = (width - length) / 2
    x = startx + int(temp)
    mvaddstr(y, x, string)

print_in_middle(None, 0, 0, 1, "hhol")