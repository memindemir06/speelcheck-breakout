from tkinter import *
import time
import random

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


def clearWindow(window):
    _list = window.winfo_children()

    for item in _list:
        if item.winfo_children():
            _list.extend(item.winfo_children())

    for item in _list:
        item.pack_forget()


class mainMenu:

    def __init__(self, window):
        self.window = window
        clearWindow(window)

        self.window.config(bg="black")

        self.canvas = Canvas(window, width=350, height=100)

        self.newGame = Button(window, text="New Game", fg="white", command=self.lgame,
                              bg="black", bd=0, width=20, font="Roboto", highlightcolor="white", activebackground="white", cursor="hand2")

        self.loadGame = Button(window, text="Load Game", fg="white",
                               bg="black", bd=0, width=20, font="Roboto", highlightcolor="white", activebackground="white", cursor="hand2")

        self.leaderboard = Button(window, text="Leaderboard", fg="white", command=self.lboard,
                                  bg="black", bd=0, width=20, font="Roboto", highlightcolor="white", activebackground="white", cursor="hand2")

        self.settings = Button(window, text="Settings", fg="white",
                               bg="black", bd=0, width=20, font="Roboto", highlightcolor="white", activebackground="white", cursor="hand2")

    def display(self):
        """
        Displays the main menu.
        """
        self.canvas.place(relx=0.5, rely=0.2, anchor=CENTER)
        self.canvas.create_image(0, 0, anchor=NW, image=logo)
        self.newGame.place(relx=0.5, rely=0.4, anchor=CENTER)
        self.loadGame.place(relx=0.5, rely=0.45, anchor=CENTER)
        self.leaderboard.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.settings.place(relx=0.5, rely=0.55, anchor=CENTER)

    def lgame(self):
        """
        Load game when the button is clicked.
        """
        game(self.window)

    def lboard(self):
        """
        Display leaderboard.
        """
        pass


def game(window):
    """
    Starts a new game or loads a saved one.
    """
    clearWindow(window)
    canvas = Canvas(window, bg="black", width=500,
                    height=800, bd=0, highlightthickness=0)
    canvas.pack()
    paddle = Paddle(canvas, "red")
    ball = Ball(canvas, paddle, "yellow")
    while True:
        ball.draw()
        paddle.draw()
        time.sleep(0.01)
        window.update_idletasks()
        window.update()


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


class Paddle:
    """
    Paddle to redirect the ball
    """

    def __init__(self, canvas, color):
        self.canvas = canvas
        self.id = canvas.create_rectangle(225, 760, 275, 770, fill=color)
        self.x = 0
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()
        self.canvas.bind_all('<KeyPress-Left>', self.go_left)
        self.canvas.bind_all('<KeyPress-Right>', self.go_right)
        self.canvas.bind_all('<KeyRelease-Left>', self.stop)
        self.canvas.bind_all('<KeyRelease-Right>', self.stop)

    def draw(self):
        """
        docstring
        """
        self.canvas.move(self.id, self.x, 0)
        pos = self.canvas.coords(self.id)
        if(pos[0] < 0 or pos[2] > 500):
            self.x = 0

    def stop(self, event):
        """
        Stops the paddle
        """
        pos = self.canvas.coords(self.id)
        if((pos[0] > 0 or pos[2] < 500) and self.x != 0):
            self.x = 0

    def go_left(self, event):
        pos = self.canvas.coords(self.id)
        if(not(pos[0] < 0)):
            self.x = -3

    def go_right(self, event):
        pos = self.canvas.coords(self.id)
        if(not(pos[2] > 500)):
            self.x = 3


class Ball:
    """
    A mighty ball
    """

    def __init__(self, canvas, paddle, color):
        """
        Initialize the ball object
        """
        self.canvas = canvas
        self.paddle = paddle
        self.id = canvas.create_oval(0, 0, 10, 10, fill=color)
        self.canvas.move(self.id, 245, 750)
        start_direction = [-3, -2, 2, 3]
        random.shuffle(start_direction)
        self.x = start_direction[0]
        self.y = -2
        self.game_over = False

    def hit_paddle(self, pos):
        """
        Collision check between the ball and the paddle
        """
        paddle_pos = self.canvas.coords(self.paddle.id)
        if (pos[0] < paddle_pos[2] and pos[2] > paddle_pos[0] and pos[1] < paddle_pos[3] and pos[3] > paddle_pos[1]):
            return True
        return False

    def draw(self):
        """
        Render the ball
        """
        self.canvas.move(self.id, self.x, self.y)
        pos = self.canvas.coords(self.id)
        if (pos[0] < 0 or pos[2] > 500):
            self.x = -self.x
        if pos[1] <= 0:
            self.y = -self.y
        if pos[3] >= 800:
            self.y = -2
        if self.hit_paddle(pos) == True:
            self.y = -self.y
            if self.paddle.x * self.x < 0:
                if self.x < 0 and self.x > -5:
                    self.x -= 1
                elif self.x > 0 and self.x < 5:
                    self.x += 1


class Brick:
    """
    The brick object
    """
    pass


# MAIN
window = createWindow(500, 800)
logo = PhotoImage(file="gamelogo.gif")
main = mainMenu(window)
main.display()
window.mainloop()
