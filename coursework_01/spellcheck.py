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
    printer(" Ignore (1)", "text")
    printer(" Mark (2)", "text")
    printer(" Add to dictionary (3)", "text")
    printer(" Show suggestion (4)", "text")
    while True:
        read = input(9*" " + vline + " >> ")
        if (read.isdigit()):
            read = int(read)
            if (read == 1 or read == 2 or read == 3 or read == 4):
                return read
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
    printer(" Spellcheck a sentence (1)", "text")
    printer(" Spellcheck a file (2)", "text")
    printer(" Exit (0)", "text")
    printer("", "text")
    while True:
        read = input(9*" " + vline + " >> ")
        if (read.isdigit()):
            read = int(read)
            if (read == 1 or read == 2 or read == 0):
                return read
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

def addToDictionary(word):
    """
    Add the word to EnglishWords.txt
    """
    with open("EnglishWords.txt", "a") as file:
        file.write(word + "\n")

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
        printer("Checking '" + word + "'...", "text")
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
            printer(("'" + word + "' is spelt incorrectly."), "text")
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
                        ("Did you mean '" + suggestion[0] + "' instead of '" + word + "'?"), "text")
                    answer = getYesNoInput()
                    if (answer == "y"):
                        processedInput[len(processedInput)-1] = suggestion[0]
                        changedWordCount += 1
                    elif (answer == "n"):
                        incorrectCount += 1
                    else:
                        pass

    return [numOfWords, correctCount, incorrectCount, addedToDictionaryCount, changedWordCount]

def fileCheck():
    """
    Check whether a file exists or not until user gives up or the condition becomes true
    """
    while True:
        printer("Please enter the file name or simply drag it here:", "text")
        filename = input(9*" " + vline + " >> ")
        if(os.path.isfile(filename)):
            return filename
        else:
            printer("File not found! Do you want to try again?:", "text")
            printer("Yes (y) or return to main menu (r)", "text")
            option = input(9*" " + vline + " >> ")
            if (option == "y"):
                continue
            elif (option == "r"):
                clear()
                printer(" MAIN MENU ", "title")
                return False


def createFile(summaryList, processedInput, timediff):
    """
    Create the output file
    """
    printer("The spellcheck is successfully completed. An output file", "text")
    printer(" with a summary and spellchecked input will be created.", "text")
    printer("What would you like the file name to be?", "text")
    filename = input(9*" " + vline + " >> ")
    if (filename.find(".") == -1):
        filename += ".txt"
    with open(filename, "w") as file:
        file.write(
            "|"+"SUMMARY STATISTICS".center(80, "-") + "|\n\n")
        file.write("The total number of words: %d\n" %
                   summaryList[0])
        file.write("The number of words spelt correctly: %d\n" %
                   summaryList[1])
        file.write("The number of words spelt incorrectly: %d\n" %
                   summaryList[2])
        file.write(
            "The number of words added to the dictionary: %d\n" % summaryList[3])
        file.write(
            "The number of words changed by the user accepting the suggested word: %d\n" % summaryList[4])
        file.write("The time and day input was spellchecked: " +
                   str(datetime.now()))
        file.write("\nThe amount of time elapsed (the time it took) to spellcheck the input: " +
                   str(timediff) + " seconds\n")
        file.write(
            "\n|"+"END OF THE SUMMARY".center(80, "-") + "|\n")
        file.write(
            "\n\n" + "|"+"PROCESSED INPUT".center(80, "-") + "|\n\n")
        file.write("\n".join(processedInput) + "\n")
        file.write(
            "\n|"+"END OF THE PROCESSED INPUT".center(80, "-") + "|\n")
    printer(("The output has created at '" + str(filename) + "'"), "text")
    printer("", "hline")

# THE PROGRAM

printer(" THE SPELLCHECKER ", "title")

while True:
    # This will store the processed input to be put in the output file
    processedInput = []
    words = []
    printer("Please select one of the options:", "text")
    option = get0to2Input()
    if (option == 1):
        printer("", "hline")
        printer("Please type in your sentence:", "text")
        sentence = input(
            (9*" " + vline + " >> "))
        beginning = time.perf_counter()
        words = sentence.split()
        wordList = processWords(words)
        summaryList = spellcheck(wordList)
        end = time.perf_counter()
        createFile(summaryList, processedInput, end-beginning)
        returnOption = getReturnInput()
        if (returnOption == "r"):
            clear()
            printer(" MAIN MENU ", "title")
            continue
        elif (returnOption == "q"):
            printer("", "bottom")
            break
        else:
            pass
    elif (option == 2):
        printer("", "hline")
        filename = fileCheck()
        if (filename == False):
            continue
        else:
            beginning = time.perf_counter()
            with open(filename) as file:
                for line in file:
                    tempList = line.split(" ")
                    for word in tempList:
                        word = word.strip()
                        words.append(word)
            if (words == []):
                break
            wordList = processWords(words)
            summaryList = spellcheck(wordList)
            end = time.perf_counter()
            createFile(summaryList, processedInput, end-beginning)
            returnOption = getReturnInput()
            if (returnOption == "r"):
                clear()
                printer(" MAIN MENU ", "title")
                continue
            elif (returnOption == "q"):
                printer("", "bottom")
                break
            else:
                pass
    elif (option == 0):
        printer("", "bottom")
        break
    else:
        pass
