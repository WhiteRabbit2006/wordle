import words as w

def getWord():  # get word, check length, check if word
    flag1 = True
    flag2 = True
    while flag1 == True or flag2 == True:
        word = input("Input the word: ")
        if len(word) == 5:
            flag1 = False
        if not word in w.words[word[0]]:
            flag2 = True
            print("word not found")
        else:
            flag2 = False
            print("word found")
        if flag1 == True or flag2 == True:
            print("That is not a 5 letter word.")
    return list(word)

def getResult():
   # get result, check digits, check length
    flag1 = True
    flag2 = False
    while not flag1 or not flag2:
        flag1 = True
        flag2 = False
        result = input("Input the result (GREY 0, YELLOW 1, GREEN 2): ")
        arrResult = [int(a) for a in result]
        for num in arrResult:
            if num != 0 and num != 1 and num != 2:
                flag1 = False
        if not flag1:
            print("All digits must be 0, 1, or 2.")
        if len(arrResult) != 5:
            print("Result must be 5 digits.")
            continue
        else:
            flag2 = True
    return arrResult

if __name__ == "__main__":
    cont = "Yes"
    greyLets = []
    yellowLets = []
    yellowNums = []
    startLet = False
    greenLets = []
    greenNums = []
    currentPossibilities = [w.allWords]
    newPossibilities = []

    while cont == "Yes" or cont == "yes":  # runs repeatedly until word is guessed
        word = getWord()
        result = getResult()
        noGrey = []

        # list grey letters (are not in solution)
        for num, let in zip(result, word):
            if num == 0:
                greyLets += [let]  # cumulative

        # format yellow letters
        i = 0
        for num, let in zip(result, word):
            if num == 1:
                yellowLets += [let]
                yellowNums += [i]
            i += 1

        # format green letters
        i = 0
        for num, let in zip(result, word):
            if num == 2:
                greenLets += [let]
                greenNums += [i]
                noGrey += [i]
            if i == 0 and num == 2:
                startLet = True
                firstLet = let
            i += 1

        # gets possible guesses
        if startLet == True:
            for wordle in w.words[firstLet[0]]:
                add = True
                i = 0
                for letter in list(wordle):
                    if letter in greyLets and not i in noGrey:
                        add = False
                    i += 1
                for yellow in yellowLets:  # check for yellow letters in word
                    if not yellow in wordle:
                        add = False
                i = 0
                for num1, let1 in zip(yellowNums, yellowLets):  # check for yellow letters at guessed indices
                    if wordle[num1] == let1:
                        add = False
                for num2, let2 in zip(greenNums, greenLets):  # check green letters
                    if not wordle[num2] == let2:
                        add = False
                if add == True:
                    newPossibilities += [wordle]
        else:
            for wordle in w.allWords:
                add = True
                i = 0
                for letter in list(wordle):
                    if letter in greyLets and not i in noGrey:
                        add = False
                    i += 1
                for yellow in yellowLets:  # check for yellow letters in word
                    if not yellow in wordle:
                        add = False
                i = 0
                for num1, let1 in zip(yellowNums, yellowLets):  # check for yellow letters at guessed indices
                    if wordle[num1] == let1:
                        add = False
                for num2, let2 in zip(greenNums, greenLets):  # check green letters
                    if not wordle[num2] == let2:
                        add = False
                if add == True:
                    newPossibilities += [wordle]
        currentPossibilities = newPossibilities
        newPossibilities = []
        print("Possible guesses:", currentPossibilities)  # prints all current possibilities
        if len(currentPossibilities) == 1:
            print("Puzzle complete!")
            break
        else:
            cont = input("Do you have another guess? (Yes or No): ")

