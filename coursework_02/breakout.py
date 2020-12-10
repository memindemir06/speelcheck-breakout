from tkinter import Tk, Canvas


# GLOBAL METHODS

def createWindow(w, h):
    """
    docstring
    """
    window = Tk()
    window.title("Breakout!")
    window.resizable(0, 0)
    window.wm_attributes("-topmost", 1)
    ws = window.winfo_screenwidth()
    hs = window.winfo_screenheight()

    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)

    window.geometry('%dx%d+%d+%d' % (w, h, x, y))
    return window


def mainMenu(window):
    """
    Displays the main menu.
    """
    pass


def game(window):
    """
    Starts a new game or loads a saved one.
    """
    pass


def leaderboard(window):
    """
    Displays the leaderboard
    """
    pass


def settings(window):
    """
    Displays the settings menu.
    """
    pass

# GAME OBJECTS


class Ball:
    """
    The ball object
    """
    pass


class Brick:
    """
    The brick object
    """
    pass


class Paddle:
    """
    The paddle object
    """
    pass


# MAIN
window = createWindow(500, 800)

window.mainloop()
