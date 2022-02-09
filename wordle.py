import words as w

def getWord():  # get word, check length, check if word
    flag1 = True
    flag2 = True
    word = ""
    while (flag1 == True or flag2 == True) and word != "stop":
        word = input("Input the word: ")
        if len(word) == 5:
            flag1 = False
        if word in w.words[word[0]]:
            flag2 = False
        else:
            flag2 = True
        if (flag1 == True or flag2 == True) and word != "stop":
            print("That is not a 5 letter word.")
    return list(word)

def getResult():  # get result, check digits, check length
    flag1 = True
    flag2 = False
    result = ""
    while (not flag1 or not flag2) and not result == "stop":
        flag1 = True
        flag2 = False
        result = input("Input the result (GREY 0, YELLOW 1, GREEN 2): ")
        if result == "stop":
            arrResult = list("stop")
            break
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



if "__main__" == __name__:  # executes possible guesses
    cont = True
    greyLets = []  # aggregate grey letters
    yellowLets = []  # aggregate yellow letters
    yellowNums = []  # indices of yellow letters
    startLet = False  # makes more efficient if first letter is green
    greenLets = []  # aggregate green letters
    greenNums = []  # aggregate indices of green letters
    currentPossibilities = [w.allWords]  # list of all possible words (updated per iteration)
    newPossibilities = []  # refreshes per iteration, temporarily stores possibilities
    print("Enter \"stop\" at any time to stop.\n")

    while cont == True:  # runs repeatedly until word is guessed
        word = getWord()
        if word == list("stop"):
            break
        result = getResult()
        if result == list("stop"):
            break
        noGrey = []  # indices that are not to be checked for grey letters
        wordlePossibilities = []  # all possible wordle solutions, updates per iteration

        # populate greyLets
        for num, let in zip(result, word):
            if num == 0:
                greyLets += [let]  # cumulative

        # populate yellowLets and yellowNums
        i = 0
        for num, let in zip(result, word):
            if num == 1:
                yellowLets += [let]
                yellowNums += [i]
            i += 1

        # populate greenLets and greenNums, sets startLet to True if starting letter known
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
        for wordle in w.wordles:
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
                wordlePossibilities += [wordle]
        currentPossibilities = newPossibilities
        newPossibilities = []
        if len(wordlePossibilities) == 1:
            print("\nPuzzle complete! The final word was:", wordlePossibilities[0])
            break
        else:
            print("\nPossible guesses:", currentPossibilities)  # prints all current guess possibilities
            print("Possible solutions:", str(wordlePossibilities) + "\n")  # prints all current solution possibilities
