from tkinter import *
import time
import random
import json


class Game:
    """
    Game object
    """

    def __init__(self, window, level, score):
        self.window = window
        self.level = level
        self.score = score
        clearWindow(window)
        self.canvas = Canvas(window, bg="#071E22", width=500,
                             height=800, bd=0, highlightthickness=0)
        self.window.bind('<KeyPress-p>', self.pauseGame)
        self.bricks = []

    def display(self):
        self.canvas.pack()
        self.paddle = Paddle(self.canvas, "#2191FB")
        self.ball = Ball(self.window, self.canvas,
                         self.paddle, self.bricks, "#EF2D56")
        self.paddle.move_active()
        self.ball.move_active()

    def pauseGame(self, event):
        """
        docstring
        """
        pause = Pause(window, self)
        pause.display()


class SavedGames:
    """
    SavedGames page.
    """
    pass


class Leaderboard:
    """
    Leader Board page.
    """

    def __init__(self, window):
        self.window = window
        clearWindow(window)
        self.window.config(bg="#F2E9DC")
        with open("savedgames.json", "r") as file:
            scores = json.load(file)

        returnMenu = Button(window, text="Main Menu", fg="white", command=self._returnmenu,
                            bg="#1D7874", bd=0, width=20, font="Roboto", highlightcolor="white",
                            activebackground="white", cursor="hand2")
        returnMenu.place(relx=0.5, rely=0.1, anchor=CENTER)

        labelName = Label(window, text="Name", fg="#2A0800",
                          bg="#F2E9DC", bd=0, width=20, font="Roboto")
        labelName.place(relx=0.35, rely=0.2, anchor=CENTER)
        labelScore = Label(window, text="Score", fg="#2A0800",
                           bg="#F2E9DC", bd=0, width=20, font="Roboto")
        labelScore.place(relx=0.65, rely=0.2, anchor=CENTER)
        hline = LabelFrame(window, bg="black")
        hline.place(relx=0.2, rely=0.25, width=300, anchor=W)
        scores['userProfiles'].sort(reverse=True, key=self.myFunc)
        i = 0.3
        for item in scores['userProfiles']:
            label1 = Label(window, text=item['name'], fg="#2A0800",
                           bg="#F2E9DC", bd=0, width=20, font="Roboto")
            label2 = Label(window, text=item['score'], fg="#2A0800",
                           bg="#F2E9DC", bd=0, width=20, font="Roboto")
            label1.place(relx=0.35, rely=i, anchor=CENTER)
            label2.place(relx=0.65, rely=i, anchor=CENTER)
            i += 0.05

    def myFunc(self, e):
        return e['score']

    def _returnmenu(self):
        main = MainMenu(window)
        main.display()


class Settings:
    """
    Settings page.
    """
    pass

# TO DO: LABELS FOR ENTRIES, LABEL AFTER SAVING GAME


class Pause:
    """
    Pause screen
    """

    def __init__(self, window, game):
        self.window = window
        self.game = game
        game.ball.active = False
        game.paddle.active = False
        self.cheatEntry = Entry(self.game.canvas)
        self.cheatEntry.bind('<Return>', self.getCheatCode)
        self.continueGame = Button(self.game.canvas, text="Continue", fg="white", command=self._continuegame,
                                   bg="#1D7874", bd=0, width=20, font="Roboto", highlightcolor="white",
                                   activebackground="white", cursor="hand2")
        self.nameEntry = Entry(self.game.canvas)
        self.saveGame = Button(self.game.canvas, text="Save Game", fg="white", command=self._savegame,
                               bg="#1D7874", bd=0, width=20, font="Roboto", highlightcolor="white",
                               activebackground="white", cursor="hand2")

    def display(self):
        self.cheatEntry.place(relx=0.5, rely=0.2, anchor=CENTER)
        self.continueGame.place(relx=0.5, rely=0.4, anchor=CENTER)
        self.nameEntry.place(relx=0.5, rely=0.6, anchor=CENTER)
        self.saveGame.place(relx=0.5, rely=0.65, anchor=CENTER)

    def getCheatCode(self, event):
        cheatCode = self.cheatEntry.get()
        print(type(cheatCode))

    def _continuegame(self):
        print("PAUSE")
        self.nameEntry.destroy()
        self.cheatEntry.destroy()
        self.continueGame.destroy()
        self.saveGame.destroy()
        self.game.ball.active = True
        self.game.paddle.active = True
        self.game.ball.move_active()
        self.game.paddle.move_active()

    def _savegame(self):
        name = self.nameEntry.get()
        if name == "":
            return
        score = self.game.score
        level = self.game.level
        profile = {"name": name, "level": level, "score": score}
        with open("savedgames.json", "r") as file:
            data = json.load(file)
            temp = data['userProfiles']
            temp.append(profile)
        with open("savedgames.json", "w") as file:
            json.dump(data, file)


class Boss:
    """
    Boss screen
    """
    pass


class MainMenu:

    def __init__(self, window):
        self.window = window
        clearWindow(window)

        self.window.config(bg="black")

        self.canvas = Canvas(window, width=350, height=100)

        self.newGame = Button(window, text="New Game", fg="white", command=self._newgame,
                              bg="black", bd=0, width=20, font="Roboto", highlightcolor="white", activebackground="white", cursor="hand2")

        self.loadGame = Button(window, text="Load Game", fg="white", command=self._savedgames,
                               bg="black", bd=0, width=20, font="Roboto", highlightcolor="white", activebackground="white", cursor="hand2")

        self.leaderboard = Button(window, text="Leaderboard", fg="white", command=self._board,
                                  bg="black", bd=0, width=20, font="Roboto", highlightcolor="white", activebackground="white", cursor="hand2")

        self.settings = Button(window, text="Settings", fg="white", command=self._settings,
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

    def _newgame(self):
        """
        Load game when the button is clicked.
        """
        game = Game(self.window, 1, 0)
        game.display()

    def _savedgames(self):
        """
        Display the saved games.
        """
        # savedGamesObject = SavedGames(self.window)
        # savedGamesObject.display()
        pass

    def _board(self):
        """
        Display leaderboard.
        """
        leaderboardObject = Leaderboard(self.window)
        # leaderboardObject.display()
        pass

    def _settings(self):
        """
        Settings
        """
        # settingsObject = Settings(self.window)
        # settingsObject.display()
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
        self.active = True

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
            self.x = -9

    def go_right(self, event):
        pos = self.canvas.coords(self.id)
        if(not(pos[2] > 500)):
            self.x = 9

    def move_active(self):
        if self.active == True:
            self.draw()
            window.after(30, self.move_active)


class Ball:
    """
    A mighty ball
    """

    def __init__(self, window, canvas, paddle, bricks, color):
        """
        Initialize the ball object
        """
        self.window = window
        self.canvas = canvas
        self.paddle = paddle
        self.bricks = bricks
        self.id = canvas.create_oval(0, 0, 10, 10, fill=color)
        self.canvas.move(self.id, 245, 750)
        self.start_direction = [-9, -8, -7, -6, 6, 7, 8, 9]
        random.shuffle(self.start_direction)
        self.x = self.start_direction[0]
        self.y = -9
        self.active = True
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
            self.active = False
            self.paddle.active = False
            leaderboard = Leaderboard(self.window)
            # leaderboard.display()
            # Game Over TO DO
        if self.hit_paddle(pos) == True:
            self.y = -self.y
            random.shuffle(self.start_direction)
            self.x = self.start_direction[2]

    def move_active(self):
        if self.active == True:
            self.draw()
            window.after(30, self.move_active)


class Brick:
    """
    The brick object
    """

    def __init__(self, canvas, color, x, y):
        self.canvas = canvas
        self.id = canvas.create_rectangle(x, y, x+10, y+5, fill=color)
        self.broken = False


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
        item.destroy()


window = createWindow(500, 800)
logo = PhotoImage(file="gamelogo.gif")
main = MainMenu(window)
main.display()
window.mainloop()
