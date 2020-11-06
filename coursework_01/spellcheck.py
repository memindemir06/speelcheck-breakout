from difflib import SequenceMatcher
import os
import time
from datetime import datetime

# UNICODE BORDER VARIABLES
hline = '\u2550'  # horizontal line
vline = '\u2551'  # vertical line
tlcor = '\u2554'  # top left corner
trcor = '\u2557'  # top right corner
blcor = '\u255A'  # bottom left corner
brcor = '\u255D'  # bottom right corner

# FUNCTIONS


def clear():
    """
    Clear lines in terminal
    I am using it as it makes the output look nicer.
    """
    if os.name == 'nt':     # Windows
        os.system('cls')
    else:                   # OS X and Linux
        os.system('clear')


def printer(str, type):
    """
    Decorated printing with appropriate borders
    """
    if type == "title":
        res = '\u2554' + \
            str.center(60, u'\u2550') + '\u2557'
    elif type == "text":
        res = '\u2551' + \
            str.center(60) + '\u2551'
    elif type == "bottom":
        res = '\u255A' + \
            "".center(60,  u'\u2550') + '\u255D'
    elif type == "hline":
        res = '\u2551' + \
            str.center(60,  u'\u2550') + '\u2551'
    else:
        return
    print(res.center(80))

def get1to4Input():
    """
    Get input when a word spelt incorrectly
    """
    while True:
        printer(" Ignore (1)", "text")
        printer(" Mark (2)", "text")
        printer(" Add to dictionary (3)", "text")
        printer(" Show suggestion (4)", "text")
        read = input(9*" " + vline + " >> ")
        if (read.isdigit()):
            read = int(read)
            if (read == 1 or read == 2 or read == 3 or read == 4):
                return read
        clear()
        printer("", "title")
        printer("Please type in a valid option!", "text")


def getYesNoInput():
    """
    Answer for program's suggestion for incorrectly spelt word
    """
    while True:
        printer("(y) for Yes and (n) for No:", "text")
        read = input(9*" " + vline + " >> ")
        if (read == "y" or read == "n"):
            return read
        else:
            printer("Please type in a valid option!", "text")


def get0to2Input():
    """
    Ask if the user ant to spellcheck a file or a sentence
    """
    while True:
        printer(" Spellcheck a sentence (1)", "text")
        printer(" Spellcheck a file (2)", "text")
        printer(" Exit (0)", "text")
        printer("", "text")
        read = input(9*" " + vline + " >> ")
        if (read.isdigit()):
            read = int(read)
            if (read == 1 or read == 2 or read == 0):
                return read
        clear()
        printer("", "title")
        printer("Please type in a valid option!", "text")


def getReturnInput():
    """
    Return to main menu or quit
    """
    while True:
        printer("Return to main menu (r) or quit (q): ", "text")
        read = input(9*" " + vline + " >> ")
        if (read == "r" or read == "q"):
            return read
        else:
            printer("Please type in a valid option!", "text")

def processWords(words):
    """
    Process the raw input
    """
    wordList = []
    for word in words:
        temp = ""
        if (word != ""):
            for character in word:
                if (character.isalpha()):
                    temp += character.lower()
            wordList.append(temp)
    wordList = list(filter(None, wordList))
    return wordList
