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

def spellcheck(wordList):
    """
    Spellcheck the given list via SequenceMatcher and return the list with summary statistics
    """
    numOfWords = len(wordList)
    correctCount = 0
    incorrectCount = 0
    addedToDictionaryCount = 0
    changedWordCount = 0
    for word in wordList:
        suggestion = ("", 0)   # Current suggestion for incorrect word
        processedInput.append(word)
        matchCheck = False
        with open("EnglishWords.txt") as file:
            for line in file:
                line = line.strip()
                score = SequenceMatcher(None, line, word).ratio()
                if (score == 1.0):    # If the word is spelt correctly
                    suggestion = ("", 0)
                    correctCount += 1
                    matchCheck = True
                    break
                elif (score > 0.6 and score > suggestion[1]):
                    # Looking for the best suggestion although it does not give the desired output most of the time :D
                    suggestion = (line, score)
                else:
                    pass
        if (matchCheck == False):     # If the word is spelt incorrectly
            printer(("You incorrectly spelled '" + word + "'"), "text")
            printer("Please select what you want to do with it:", "text")
            decision = get1to4Input()
            if (decision == 1):
                incorrectCount += 1
            if (decision == 2):
                processedInput[len(processedInput)-1] = "?" + word + "?"
                incorrectCount += 1
            if (decision == 3):
                addToDictionary(word)
                addedToDictionaryCount += 1
            if (decision == 4):
                if (suggestion[0] == ""):
                    printer("No suggestion found.", "text")
                else:
                    printer(
                        ("Did you mean '" + suggestion[0] + "' instead of '" + word + "'"), "text")
                    answer = getYesNoInput()
                    if (answer == "y"):
                        processedInput[len(processedInput)-1] = suggestion[0]
                        changedWordCount += 1
                    elif (answer == "n"):
                        incorrectCount += 1
                    else:
                        pass

    return [numOfWords, correctCount, incorrectCount, addedToDictionaryCount, changedWordCount]
