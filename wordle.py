import words as w  # "words" is where all words are stored
import random
import cProfile, pstats

# get word from user, check length, check if word
def getWord():
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


# get result from user, check digits, check length
def getResult():
    flag1 = True
    flag2 = False
    res = ""
    while (not flag1 or not flag2) and not res == "stop":
        flag1 = True
        flag2 = False
        res = input("Input the result (GREY 0, YELLOW 1, GREEN 2): ")
        if res == "stop":
            arr_result = list("stop")
            break
        arr_result = [int(a) for a in res]
        for num in arr_result:
            if num != 0 and num != 1 and num != 2:
                flag1 = False
        if not flag1:
            print("All digits must be 0, 1, or 2.")
        if len(arr_result) != 5:
            print("Result must be 5 digits.")
            continue
        else:
            flag2 = True
    return arr_result


# runs main code
if "__main__" == __name__:

    profiler = cProfile.Profile()
    profiler.enable()

    cont = True
    words_solved = 0
    all_guesses = []
    letterFreq = {
        "a": [0, 0, 0, 0, 0],
        "b": [0, 0, 0, 0, 0],
        "c": [0, 0, 0, 0, 0],
        "d": [0, 0, 0, 0, 0],
        "e": [0, 0, 0, 0, 0],
        "f": [0, 0, 0, 0, 0],
        "g": [0, 0, 0, 0, 0],
        "h": [0, 0, 0, 0, 0],
        "i": [0, 0, 0, 0, 0],
        "j": [0, 0, 0, 0, 0],
        "k": [0, 0, 0, 0, 0],
        "l": [0, 0, 0, 0, 0],
        "m": [0, 0, 0, 0, 0],
        "n": [0, 0, 0, 0, 0],
        "o": [0, 0, 0, 0, 0],
        "p": [0, 0, 0, 0, 0],
        "q": [0, 0, 0, 0, 0],
        "r": [0, 0, 0, 0, 0],
        "s": [0, 0, 0, 0, 0],
        "t": [0, 0, 0, 0, 0],
        "u": [0, 0, 0, 0, 0],
        "v": [0, 0, 0, 0, 0],
        "w": [0, 0, 0, 0, 0],
        "x": [0, 0, 0, 0, 0],
        "y": [0, 0, 0, 0, 0],
        "z": [0, 0, 0, 0, 0]
    }

    for current_word in w.wordles:  # runs with random guesses until solution is found
        greyLets = []  # aggregate grey letters
        yellowLets = []  # aggregate yellow letters
        yellowNums = []  # indices of yellow letters
        startLet = False  # makes more efficient if first letter is green
        greenLets = []  # aggregate green letters
        greenNums = []  # aggregate indices of green letters
        guesses = 0
        current_possibilities = w.allWords  # list of all possible words (updated per iteration)
        cont = True
        while cont:
            noGrey = []  # indices that are not to be checked for grey letters
            wordlePossibilities = []  # all possible wordle solutions, updates per iteration
            newPossibilities = []  # refreshes per iteration, temporarily stores possibilities
            guesses += 1
            word = list(current_possibilities[random.randrange(0, len(current_possibilities) - 1)])  # chooses random word
            current_word = list(current_word)
            # compute_result function
            result = [0, 0, 0, 0, 0]
            checked_indices = []

            i = 0
            for solution_letter, guess_letter in zip(current_word, word):
                if solution_letter == guess_letter:
                    result[i] = 2
                for result_index, current_word_letter in zip(result, current_word):
                    if result[i] == 0 and guess_letter == current_word_letter:
                        result[i] = 1
                i += 1

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
            if startLet:
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
                    if add:
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
                    if add:
                        newPossibilities.append(wordle)
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
                if add:
                    wordlePossibilities.append(wordle)
            currentPossibilities = newPossibilities

            # populates letterFreq
            for alpha in w.alphabet:
                count = 0
                for i in range(5):
                    for possibleWord in currentPossibilities:
                        if possibleWord[i] == alpha:
                            count += 1
            if len(wordlePossibilities) == 1 or len(current_possibilities) == 1:
                all_guesses.append(guesses)
                words_solved += 1
                cont = False
        if words_solved % 10 == 0:
            print(str(words_solved/2315) + "\n")
#        if words_solved > 100:
#            break
        #            letterFreq[alpha][i] = count / len(currentPossibilities)
    print("\nAverage guesses per solution:", sum(all_guesses)/len(all_guesses))

    profiler.disable()
    stats = pstats.Stats(profiler)
    stats.print_stats()

'''
Questions:
how to handle all of the variables if I am to switch to functions
how to have a prerequisite function without having to run it for every function independently, example: using result
what to leave in main
'''

# Runner that asks user for guess and result of guess
"""
print("Enter \"stop\" at any time to stop.\n")
    while cont:  # runs repeatedly until word is guessed
        word = getWord()
        if word == list("stop"):
            break
        result = getResult()
        if result == list("stop"):
            break
        noGrey = []  # indices that are not to be checked for grey letters
        wordlePossibilities = []  # all possible wordle solutions, updates per iteration
        newPossibilities = []  # refreshes per iteration, temporarily stores possibilities

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
        if startLet:
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
                if add:
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
                if add:
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
            if add:
                wordlePossibilities += [wordle]
        currentPossibilities = newPossibilities

        # populates letterFreq
        for alpha in w.alphabet:
            count = 0
            for i in range(5):
                for possibleWord in currentPossibilities:
                    if possibleWord[i] == alpha:
                        count += 1
                letterFreq[alpha][i] = count / len(currentPossibilities)

        if len(wordlePossibilities) == 1:
            print("\nPuzzle complete! The answer was:", wordlePossibilities[0])
            break
        else:
            print("\nPossible guesses:", currentPossibilities)  # prints all current guess possibilities
            print("Possible solutions:", str(wordlePossibilities) + "\n")  # prints all current solution possibilities
"""

"""
Random words average guesses per puzzle: 6.161987041036717
"""