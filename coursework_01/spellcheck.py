from difflib import SequenceMatcher
import os

print("\n\t\t\t\tWELCOME TO SPELLCHECKER!\n")

loopcheck = 1

while (loopcheck):
    words = []
    incorrectCount = 0
    addedToDictionaryCount = 0
    changedWordCount = 0
    output = []
    print("Please select one of the options:\n")
    option = input(
        " Spellcheck a sentence (1)\n Spellcheck a file (2)\n quit (0)\n\n>> ")
    if (option.isdigit()):
        option = int(option)
        if (option == 1):
            commandPromptInput = input("Please type in your sentence:\n>> ")
            words = commandPromptInput.split()
            manupilatedWords = []
            for word in words:
                manupilatedWord = ""
                for character in word:
                    if (character.isalpha()):
                        manupilatedWord += character.lower()
                manupilatedWords.append(manupilatedWord)
            for word in manupilatedWords:
                if (word == ""):
                    manupilatedWords.remove("")
            numOfWords = len(manupilatedWords)
            for word in manupilatedWords:
                suggestion = ("", 0)
                output.append(word)
                matchCheck = False
                with open("EnglishWords.txt") as file:
                    for line in file:
                        line = line.strip()
                        score = SequenceMatcher(None, line, word).ratio()
                        if (score == 1.0):
                            suggestion = ("", 0)
                            matchCheck = True
                            break
                        elif (score > 0.6 and score > suggestion[1]):
                            suggestion = (line, score)
                        else:
                            pass
                # Word did not match
                if (matchCheck == False):
                    loopcheck2 = True
                    while loopcheck2:
                        print("You incorrectly spelled \'%s\'" % word)
                        incorrectOption = input(
                            "Please select what you want to do with it:\n Ignore (1)\n Mark (2)\n Add to dictionary (3)\n Show suggestion (4)\n>> ")
                        if (incorrectOption.isdigit()):
                            incorrectOption = int(incorrectOption)
                            if (incorrectOption == 1):
                                incorrectCount += 1
                                loopcheck2 = False
                            elif (incorrectOption == 2):
                                output[len(output)-1] = "?" + word + "?"
                                incorrectCount += 1
                                loopcheck2 = False
                            elif (incorrectOption == 3):
                                addedToDictionaryCount += 1
                                break
                            elif (incorrectOption == 4):
                                if(suggestion[0] == ""):
                                    print("No suggestion found.")
                                    break
                                print("Did you mean \'%s\' instead of \'%s\'? " % (
                                    suggestion[0], word))
                                while True:
                                    correctWordOption = input(
                                        "(y) for Yes and (n) for no:\n>> ")
                                    if (correctWordOption == "y"):
                                        output[len(output)-1] = suggestion[0]
                                        changedWordCount += 1
                                        loopcheck2 = False
                                        break
                                    elif (correctWordOption == "n"):
                                        incorrectCount += 1
                                        loopcheck2 = False
                                        break
                                    else:
                                        print("Please type in a valid option!")
                            else:
                                print("Please type in a valid option!")
                        else:
                            print("\nPlease type in a valid option!")
            filename = input(
                "The spellcheck is successfully completed. What would you like the file name to be?\n>> ")
            filename += ".txt"
            with open(filename, "w") as file:
                file.write(
                    "|----------------------------SUMMARY----------------------------|\n")
                file.write("The total number of words: %d\n" % numOfWords)
                file.write("The number of words spelt correctly: %d\n" %
                           (numOfWords-incorrectCount))
                file.write("The number of words spelt incorrectly: %d\n" %
                           incorrectCount)
                file.write(
                    "The number of words added to the dictionary: %d\n" % addedToDictionaryCount)
                file.write(
                    "The number of words changed by the user accepting the suggested word: %d\n" % changedWordCount)
                file.write(
                    "|-----------------------END OF THE SUMMARY-----------------------|\n")
                file.write(
                    "\n\n\n|----------------USER INPUT----------------|\n")
                file.write(" ".join(output))
                file.write(
                    "\n|--------------END OF USER INPUT--------------|\n")
            print("The output has created at %s" % filename)
            while True:
                returnInput = input("Return to main menu (r) or quit (q):\n>> ")
                if(returnInput == "r"):
                    break
                elif (returnInput == "q"):
                    loopcheck = 0
                    break
                else:
                    print("Please type in a valid option!")
        elif (option == 2):
            print("b")
        elif (option == 0):
            loopcheck = 0
        else:
            print("Please type in a valid option!\n")
    else:
        print("Please type in a valid option!\n")
