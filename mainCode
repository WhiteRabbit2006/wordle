import words as w

if __name__ == "__main__":
    flag1 = True
    flag2 = True

    # get word, check length, check if word
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
    arrWord = list(word)

    # get result, check digits, check length
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

    # list grey letters (are not in solution)
    greyLets = []
    for num, let in zip(arrResult, arrWord):
        if num == 0:
            greyLets += [let]

    # format yellow letters
    yellowLets = []
    yellowNums = []
    i = 0
    for num, let in zip(arrResult, arrWord):
        if num == 1:
            yellowLets += [let]
            yellowNums += [i]
        i += 1

    # format green letters
    i = 0
    startLet = False
    greenLets = []
    greenNums = []
    for num, let in zip(arrResult, arrWord):
        if num == 2:
            greenLets += [let]
            greenNums += [i]
        if i == 0 and num == 2:
            startLet = True
            firstLet = let
        i += 1

    # gets possible guesses
    possibleGuesses = []

    if startLet == True:
        for wordle in w.words[firstLet[0]]:
            add = True
            for grey in greyLets:  # check for grey letters
                if grey in wordle:
                    add = False
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
                possibleGuesses += [wordle]
    else:
        for wordle in w.allWords:
            add = True
            for grey in greyLets:  # check for grey letters
                if grey in wordle:
                    add = False
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
                possibleGuesses += [wordle]

    print("Possible guesses:", possibleGuesses)  # prints all current possibilities
