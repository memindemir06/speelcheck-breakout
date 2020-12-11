from tkinter import *
import time
import random
import json
from itertools import repeat
import math


class Game:
    """
    Game object
    """

    def __init__(self, window, username, level, score):
        self.window = window
        self.username = username
        self.level = level
        self.score = score
        clearWindow(window)
        self.canvas = Canvas(window, bg="#250826", width=500,
                             height=800, bd=0, highlightthickness=0)
        self.window.bind('<KeyPress-p>', self.pauseGame)
        self.bricks = []
        self.bricksCheck = []
        if self.level == 1 and self.score == 0:
            self.saved = False
        else:
            self.saved = True

    def display(self):
        self.canvas.pack()
        usernameText = "Player: " + self.username
        levelText = "Level: " + str(self.level)
        scoreText = "Score: " + str(self.score)
        self.usernameObj = self.canvas.create_text(20, 20, fill="white",
                                                   font="Roboto 16 bold", anchor=W, text=usernameText)
        self.levelObj = self.canvas.create_text(480, 40, fill="white",
                                                font="Roboto 16 bold", anchor=E, text=levelText)
        self.scoreObj = self.canvas.create_text(480, 20, fill="white",
                                                font="Roboto 16 bold", anchor=E, text=scoreText)
        self.paddle = Paddle(self.canvas, "#FFDF00")
        self.ball = Ball(self.window, self,  self.canvas,
                         self.paddle, self.bricks, "#FFDF00")
        self.displayBricks()
        self.paddle.move_active()
        self.ball.move_active()

    def displayBricks(self):
        if self.level == 1:
            for row in range(2, 16):
                for column in range(8, 17):
                    if row == 6 or row == 11:
                        break
                    color = "%06x" % random.randint(0, 0xFFFFFF)
                    brick = Brick(self.canvas, '#'+color,
                                  row*28, column*18)
                    brick.display()
                    self.bricks.append(brick)
        elif self.level == 2:
            pass
        elif self.level == 3:
            pass

    def pauseGame(self, event):
        """
        docstring
        """
        pause = Pause(window, self)
        pause.display()

    def saveGame(self):
        profile = {"name": self.username,
                   "level": self.level, "score": self.score}
        with open("savedgames.json", "r") as file:
            data = json.load(file)
            temp = data['userProfiles']
            temp.append(profile)
        with open("savedgames.json", "w") as file:
            json.dump(data, file)
        self.saved = True

    def setIndex(self, count):
        self.count = count

    def override(self):
        profile = {"name": self.username,
                   "level": self.level, "score": self.score}
        with open("savedgames.json", "r") as file:
            data = json.load(file)
            temp = data['userProfiles']
            if hasattr(self, "count"):
                temp.pop(self.count)
            else:
                temp.pop(len(temp)-1)
            temp.append(profile)
        with open("savedgames.json", "w") as file:
            json.dump(data, file)

    def win(self):
        if self.level < 3:
            game = Game(self.window, self.username, self.level+1, self.score)
            game.display()
        else:
            winMessage = Label(
                window, text="You won!",
                fg="white", bg="#250826", bd=0, width=40, font="Roboto 24 bold")
            winMessage.place(relx=0.5, rely=0.4, anchor=CENTER)

    def updateInfo(self):
        usernameText = "Player: " + self.username
        levelText = "Level: " + str(self.level)
        scoreText = "Score: " + str(self.score)
        self.canvas.itemconfigure(self.usernameObj, text=usernameText)
        self.canvas.itemconfigure(self.levelObj, text=levelText)
        self.canvas.itemconfigure(self.scoreObj, text=scoreText)


class SavedGames:
    """
    SavedGames page.
    """

    def __init__(self, window):
        self.window = window
        clearWindow(window)
        window.config(bg="#022120")
        self.title = Label(window, text="Saved Games", fg="white",
                           bg="#022120", bd=0, width=20, font="Roboto 16 bold")
        self.hline = LabelFrame(window, bg="white")
        with open("savedgames.json", "r") as file:
            self.scores = json.load(file)
        self.saved = True
        self.returnMenu = Button(window, text="Main Menu", fg="#022120", command=self._returnmenu,
                                 bg="white", bd=0, width=20, font="Roboto 16 bold", highlightcolor="#FAFAFA",
                                 activebackground="#FAFAFA", cursor="hand2")

    def display(self):
        self.returnMenu.place(relx=0.5, rely=0.1, anchor=CENTER)
        self.title.place(relx=0.5, rely=0.2, anchor=CENTER)
        self.hline.place(relx=0.2, rely=0.25, width=300, anchor=W)

        count = len(self.scores['userProfiles'])-1
        columnCount = 0.3
        playedGames = self.scores['userProfiles']
        for i in range(len(self.scores['userProfiles'])-1, -1, -1):
            gameName = playedGames[i]['name'] + 10*" " + "Level: " + str(
                playedGames[i]['level']) + " | Score: " + str(playedGames[i]['score'])
            button = Button(window, text=gameName, fg="#022120", command=lambda count=count: self._loadgame(count),
                            bg="white", bd=0, width=30, font="Roboto 16", highlightcolor="#FAFAFA",
                            activebackground="#FAFAFA", cursor="hand2")
            button.place(relx=0.5, rely=columnCount, anchor=CENTER)
            columnCount += 0.08
            count -= 1

    def _loadgame(self, count):
        gameindex = self.scores['userProfiles'][count]
        game = Game(self.window, gameindex['name'],
                    gameindex['level'], 0)
        game.saved = True
        game.setIndex(count)
        game.display()

    def _returnmenu(self):
        main = MainMenu(window)
        main.display()


class Leaderboard:
    """
    Leader Board page.
    """

    def __init__(self, window):
        self.window = window
        clearWindow(window)
        self.window.config(bg="#022120")
        with open("savedgames.json", "r") as file:
            self.scores = json.load(file)

        self.returnMenu = Button(window, text="Main Menu", fg="#022120", command=self._returnmenu,
                                 bg="white", bd=0, width=20, font="Roboto 16 bold", highlightcolor="#FAFAFA",
                                 activebackground="#FAFAFA", cursor="hand2")

        self.labelName = Label(window, text="Name", fg="white",
                               bg="#022120", bd=0, width=20, font="Roboto 16 bold")

        self.labelScore = Label(window, text="Score", fg="white",
                                bg="#022120", bd=0, width=20, font="Roboto 16 bold")

        self.hline = LabelFrame(window, bg="white")

    def display(self):
        self.returnMenu.place(relx=0.5, rely=0.1, anchor=CENTER)
        self.labelName.place(relx=0.32, rely=0.2, anchor=CENTER)
        self.labelScore.place(relx=0.65, rely=0.2, anchor=CENTER)
        self.hline.place(relx=0.2, rely=0.25, width=300, anchor=W)
        self.scores['userProfiles'].sort(reverse=True, key=self.myFunc)
        i = 0.3
        for item in self.scores['userProfiles']:
            label1 = Label(window, text=item['name'], fg="white",
                           bg="#022120", bd=0, width=20, font="Roboto 16")
            label2 = Label(window, text=item['score'], fg="white",
                           bg="#022120", bd=0, width=20, font="Roboto 16")
            label1.place(relx=0.32, rely=i, anchor=CENTER)
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

    def __init__(self, window):
        self.window = window
        clearWindow(window)
        window.config(bg="#022120")
        self.title = Label(window, text="Controls", fg="white",
                           bg="#022120", bd=0, width=20, font="Roboto 16 bold")
        self.hline = LabelFrame(window, bg="white")
        self.labelPaddle = Label(window, text="Paddle Movement: ", fg="white",
                                 bg="#022120", bd=0, width=20, font="Roboto 12")

        self.checkPaddle1 = Checkbutton(window, text="A-S", fg="white", command=self._checkpaddle,
                                        bg="#022120", bd=0, width=20, font="Roboto 8", cursor="hand2", relief=FLAT, variable=IntVar())
        self.checkPaddle2 = Checkbutton(window, text="Left-Right Arrow", fg="white", command=self._checkpaddle,
                                        bg="#022120", bd=0, width=20, font="Roboto 8", cursor="hand2", relief=FLAT, variable=IntVar())
        self.returnMenu = Button(window, text="Main Menu", fg="#022120", command=self._returnmenu,
                                 bg="white", bd=0, width=20, font="Roboto 16 bold", highlightcolor="#FAFAFA",
                                 activebackground="#FAFAFA", cursor="hand2")

    def display(self):
        self.title.place(relx=0.5, rely=0.1, anchor=CENTER)
        self.hline.place(relx=0.2, rely=0.15, width=300, anchor=W)
        self.labelPaddle.place(relx=0.25, rely=0.25, anchor=CENTER)
        self.checkPaddle1.place(relx=0.55, rely=0.25, anchor=CENTER)
        self.checkPaddle2.place(relx=0.85, rely=0.25, anchor=CENTER)

    def _checkpaddle(self):
        """
        Determine the user prefence to move the paddle
        """
        if self.checkPaddle1['variable'] == 1:
            self.checkPaddle2.deselect()
        else:
            self.checkPaddle1.deselect()

    def _returnmenu(self):
        main = MainMenu(window)
        main.display()


class Pause:
    """
    Pause screen
    """

    def __init__(self, window, game):
        self.window = window
        self.game = game
        game.ball.active = False
        game.paddle.active = False
        self.cheatLabelTop = Label(
            window, text="Wanna cheat?",
            fg="white", bg="#250826", bd=0, width=40, font="Roboto 16")
        self.cheatEntry = Entry(self.game.canvas, width=20, font="Roboto 14")
        self.cheatLabelBottom = Label(
            window, text="(Hint: See the beginning of source code.)",
            fg="white", bg="#250826", bd=0, width=40, font="Roboto 10 italic")
        self.cheatEntry.bind('<Return>', self.getCheatCode)
        self.continueGame = Button(self.game.canvas, text="Continue", fg="#250826", command=self._continuegame,
                                   bg="white", bd=0, width=20, font="Roboto 16 bold", highlightcolor="#FAFAFA",
                                   activebackground="#FAFAFA", cursor="hand2")
        self.saveGame = Button(self.game.canvas, text="Save Game", fg="#250826", command=self._savegame,
                               bg="white", bd=0, width=20, font="Roboto 16 bold", highlightcolor="#FAFAFA",
                               activebackground="#FAFAFA", cursor="hand2")

    def display(self):

        self.cheatLabelTop.place(relx=0.5, rely=0.4, anchor=CENTER)
        self.cheatEntry.place(relx=0.5, rely=0.45, anchor=CENTER)
        self.cheatLabelBottom.place(relx=0.5, rely=0.48, anchor=CENTER)
        self.continueGame.place(relx=0.5, rely=0.53, anchor=CENTER)
        self.saveGame.place(relx=0.5, rely=0.58, anchor=CENTER)

    def getCheatCode(self, event):
        cheatCode = self.cheatEntry.get()

    def _continuegame(self):
        self.cheatLabelTop.destroy()
        self.cheatLabelBottom.destroy()
        self.cheatEntry.destroy()
        self.continueGame.destroy()
        self.saveGame.destroy()
        self.game.ball.active = True
        self.game.paddle.active = True
        self.game.ball.move_active()
        self.game.paddle.move_active()

    def _savegame(self):
        name = self.game.username
        score = self.game.score
        level = self.game.level
        bricksCheck = self.game.bricksCheck
        profile = {"name": name, "level": level,
                   "score": score, "bricks": bricksCheck}
        with open("savedgames.json", "r") as file:
            data = json.load(file)
            temp = data['userProfiles']
            if self.game.saved == True:
                temp.pop(len(temp)-1)
            temp.append(profile)
        with open("savedgames.json", "w") as file:
            json.dump(data, file)
        self.game.saved = True


class MainMenu:

    def __init__(self, window):
        self.window = window
        clearWindow(window)

        self.window.config(bg="#252857")

        self.canvas = Canvas(window, width=350, height=100, bg="#252857", bd=0)

        self.usernameLabel = Label(window, text="Username:",
                                   fg="#FAFAFA", bg="#252857", bd=0, width=40, font="Roboto 16 bold")
        self.entry = Entry(window, width=14, font="Roboto 14")

        self.newGame = Button(window, text="Play!", fg="#252857", command=self._newgame,
                              bg="#FAFAFA", bd=0, width=22, font="Roboto 16 bold", highlightcolor="white", activebackground="white", cursor="hand2")

        self.loadGame = Button(window, text="Load Game", fg="#FAFAFA", command=self._savedgames,
                               bg="#252857", bd=0, width=20, font="Roboto 16 bold", highlightcolor="white", activebackground="white", cursor="hand2")

        self.leaderboard = Button(window, text="Leaderboard", fg="#FAFAFA", command=self._board,
                                  bg="#252857", bd=0, width=20, font="Roboto 16 bold", highlightcolor="white", activebackground="white", cursor="hand2")

        self.settings = Button(window, text="Settings", fg="#FAFAFA", command=self._settings,
                               bg="#252857", bd=0, width=20, font="Roboto 16 bold", highlightcolor="white", activebackground="white", cursor="hand2")

    def display(self):
        """
        Displays the main menu.
        """
        self.canvas.place(relx=0.5, rely=0.2, anchor=CENTER)
        self.canvas.create_image(0, 0, anchor=NW, image=logo)
        self.usernameLabel.place(relx=0.34, rely=0.35, anchor=CENTER)
        self.entry.place(relx=0.64, rely=0.35, anchor=CENTER)
        self.newGame.place(relx=0.5, rely=0.4, anchor=CENTER)
        self.loadGame.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.leaderboard.place(relx=0.5, rely=0.55, anchor=CENTER)
        self.settings.place(relx=0.5, rely=0.6, anchor=CENTER)

    def _newgame(self):
        """
        Load game when the button is clicked.
        """
        username = self.entry.get()
        if username == "" or len(username) > 10:
            return
        game = Game(self.window, username, 1, 0)
        game.display()

    def _savedgames(self):
        """
        Display the saved games.
        """
        savedGamesObject = SavedGames(self.window)
        savedGamesObject.display()
        pass

    def _board(self):
        """
        Display leaderboard.
        """
        leaderboardObject = Leaderboard(self.window)
        leaderboardObject.display()
        pass

    def _settings(self):
        """
        Settings
        """
        settingsObject = Settings(self.window)
        settingsObject.display()
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

    def __init__(self, window, game, canvas, paddle, bricks, color):
        """
        Initialize the ball object
        """
        self.window = window
        self.game = game
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

    def hit_brick(self, pos, brick_pos):
        """
        Collision check between the ball and a brick
        """
        if (pos[0] < brick_pos[2] and pos[2] > brick_pos[0] and pos[1] < brick_pos[3] and pos[3] > brick_pos[1]):
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
            self.paddle.canvas.unbind_all("<KeyPress-Left>")
            self.paddle.canvas.unbind_all("<KeyPress-Right>")
            self.paddle.canvas.unbind_all("<KeyRelease-Left>")
            self.paddle.canvas.unbind_all("<KeyRelease-Right>")
            if self.game.saved == False:
                self.game.saveGame()
            else:
                self.game.override()
            leaderboard = Leaderboard(self.window)
            leaderboard.display()
        if self.hit_paddle(pos) == True:
            self.y = -self.y
            random.shuffle(self.start_direction)
            self.x = self.start_direction[2]
        if not self.game.bricks:
            self.game.win()
        for i in range(len(self.game.bricks)):
            if self.hit_brick(pos, [self.game.bricks[i].x, self.game.bricks[i].y, self.game.bricks[i].x+25, self.game.bricks[i].y+15]) == True:

                ballHalfW = (pos[2]-pos[0])/2
                ballHalfH = (pos[3]-pos[1])/2
                brickHalfW = 12.5
                brickHalfH = 7.5
                ballCenterX = pos[0] + (pos[2]-pos[0])/2
                ballCenterY = pos[1] + (pos[3]-pos[1])/2
                brickCenterX = self.game.bricks[i].x + 12.5
                brickCenterY = self.game.bricks[i].y + 7.5

                # Difference between centers
                diffX = ballCenterX - brickCenterX
                diffY = ballCenterY - brickCenterY

                # Minimum distance to separate along X and Y
                minXDist = ballHalfW + brickHalfW
                minYDist = ballHalfH + brickHalfH

                # Depth of the collision for both axis
                depthX = (minXDist - diffX) if diffX > 0 else (-minXDist - diffX)
                depthY = (minYDist - diffY) if diffY > 0 else (-minYDist - diffY)

                # Decide which side from the collision happened

                if (depthX != 0 and depthY != 0):
                    if (abs(depthX) < abs(depthY)):
                        self.x = -self.x
                        self.game.bricks[i].delete()
                        self.game.bricks.pop(i)
                        self.game.score += 50
                        self.game.updateInfo()
                        break
                    else:
                        self.y = -self.y
                        self.game.bricks[i].delete()
                        self.game.bricks.pop(i)
                        self.game.score += 50
                        self.game.updateInfo()
                        break

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
        self.color = color
        self.x = x
        self.y = y

    def display(self):
        self.id = self.canvas.create_rectangle(
            self.x, self.y, self.x+25, self.y+15, fill=self.color)

    def delete(self):
        self.canvas.delete(self.id)


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
    y = (hs/2) - (h/2) - 20

    window.geometry('%dx%d+%d+%d' % (w, h, x, y))
    return window


def clearWindow(window):
    _list = window.winfo_children()

    for item in _list:
        if item.winfo_children():
            _list.extend(item.winfo_children())

    for item in _list:
        item.destroy()


def toggleBoss(event):
    check = False
    for item in window.winfo_children():
        if item.winfo_class() == "Label" and item['bg'] == "#888888":
            item.destroy()
            check = True
            break
    if check == False:
        img = Label(window, image=boss, bg="#888888")
        img.place(x=0, y=0)


window = createWindow(500, 800)
logo = PhotoImage(file="breakout.gif")
boss = PhotoImage(file="boss.gif")
main = MainMenu(window)
main.display()
window.bind("<b>", toggleBoss)
window.mainloop()
