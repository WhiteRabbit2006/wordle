import words as w  # "words" is where all words are stored
import random
import cProfile, pstats


# get word from user, check length, check if word
def get_word():
    flag1 = True
    flag2 = True
    word = ""
    while (flag1 == True or flag2 == True) and word != "stop":
        word = input("Input the word: ")
        if len(word) == 5:
            flag1 = False
        if str(word) in w.words[word[0]]:
            flag2 = False
        else:
            flag2 = True
        if (flag1 == True or flag2 == True) and word != "stop":
            print("That is not a 5 letter word.")
    return list(word)


# get result from user, check digits, check length
def get_result():
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


# given guess and solution, returns result of guess
def compute_result(guess, solution):
    result = [0, 0, 0, 0, 0]
    i = 0
    for solution_letter, guess_letter in zip(solution, guess):
        if solution_letter == guess_letter:
            result[i] = 2
        for result_index, current_word_letter in zip(result, current_word):
            if result[i] == 0 and guess_letter == current_word_letter:
                result[i] = 1
        i += 1
    return result


# uses result and word to output letters and indices of different colors
def use_result(word, result):
    out = [
        [],  # grey letters in the word
        [],  # yellow letters in the word
        [],  # indices of yellow letters in the word
        [],  # green letters in the word
        []  # indices of green letters in the word
    ]
    i = 0
    for num, let in zip(result, word):
        if num == 0:
            out[0] += [let]  # cumulative
        elif num == 1:
            out[1] += [let]
            out[2] += [i]
        elif 2 == num:
            out[3] += [let]
            out[4] += [i]
        i += 1
    return out


# runs main code
if "__main__" == __name__:

    profiler = cProfile.Profile()
    profiler.enable()

    words_solved = 0
    guesses = 0
    '''    letterFreq = {
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
    }'''  # letter frequency dictionary

    for current_word in w.wordles:  # runs with random guesses until solution is found
        current_word = list(current_word)
        current_possibilities = w.allWords  # list of all possible words (updated per iteration)
        cont = True
        while cont:
            guesses += 1

            wordle_possibilities = [w.wordles]  # all possible wordle solutions, updates per iteration
            new_possibilities = []  # refreshes per iteration, temporarily stores possibilities

            word = list(random.choice(current_possibilities))  # chooses random word from current possible guesses

            result = compute_result(word, current_word)

            used_result = use_result(word, result)

            # gets possible guesses
            for wordle in current_possibilities:
                add = True
                i = 0
                for letter in list(wordle):
                    if letter in used_result[1] and not i in used_result[4]:
                        add = False
                    i += 1
                for yellow in used_result[1]:  # check for yellow letters in word
                    if not yellow in wordle:
                        add = False
                i = 0
                for num1, let1 in zip(used_result[2], used_result[1]):  # check for yellow letters at guessed indices
                    if wordle[num1] == let1:
                        add = False
                for num2, let2 in zip(used_result[4], used_result[3]):  # check green letters
                    if not wordle[num2] == let2:
                        add = False
                if add:
                    new_possibilities.append(wordle)

            current_possibilities = new_possibilities
            new_possibilities = []

            # gets possible solutions
            for wordle in wordle_possibilities:
                add = True
                i = 0
                for letter in list(wordle):
                    if letter in used_result[1] and not i in used_result[4]:
                        add = False
                    i += 1
                for yellow in used_result[1]:  # check for yellow letters in word
                    if not yellow in wordle:
                        add = False
                i = 0
                for num1, let1 in zip(used_result[2], used_result[1]):  # check for yellow letters at guessed indices
                    if list(wordle)[num1] == let1:
                        add = False
                for num2, let2 in zip(used_result[4], used_result[3]):  # check green letters
                    if not list(wordle)[num2] == let2:
                        add = False
                if add:
                    new_possibilities.append(wordle)

            wordle_possibilities = new_possibilities
            new_possibilities = []

            # populates letterFreq
            '''
            for alpha in w.alphabet:
                count = 0
                for i in range(5):
                    for possibleWord in current_possibilities:
                        if possibleWord[i] == alpha:
                            count += 1
            if len(wordle_possibilities) == 1 or len(current_possibilities) == 1:
                words_solved += 1
                cont = False

            if words_solved % 10 == 0:
                print(str(words_solved / 2315) + "\n")
            if words_solved > 100:
                break'''

    print("\nAverage guesses per solution:", guesses / words_solved)

    profiler.disable()
    stats = pstats.Stats(profiler)
    stats.print_stats()

'''
fix error with narrowing guesses
'''  # short term to-do

'''
refine runner to take a number of words to run and a frequency to print percentage
'''  # long term to-do

'''

'''  # questions

"""
print("Enter \"stop\" at any time to stop.\n")
    while cont:  # runs repeatedly until word is guessed
        word = getWord()
        if word == list("stop"):
            break
        result = getResult()
        if result == list("stop"):
            break
        used_result[4] = []  # indices that are not to be checked for grey letters
        wordlePossibilities = []  # all possible wordle solutions, updates per iteration
        newPossibilities = []  # refreshes per iteration, temporarily stores possibilities

        # populate used_result[1]
        for num, let in zip(result, word):
            if num == 0:
                used_result[1] += [let]  # cumulative

        # populate used_result[1] and used_result[2]]
        i = 0
        for num, let in zip(result, word):
            if num == 1:
                used_result[1] += [let]
                used_result[2]] += [i]
            i += 1

        # populate used_result[3] and used_result[4], sets startLet to True if starting letter known
        i = 0
        for num, let in zip(result, word):
            if num == 2:
                used_result[3] += [let]
                used_result[4] += [i]
                used_result[4] += [i]
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
                    if letter in used_result[1] and not i in used_result[4]:
                        add = False
                    i += 1
                for yellow in used_result[1]:  # check for yellow letters in word
                    if not yellow in wordle:
                        add = False
                i = 0
                for num1, let1 in zip(used_result[2], used_result[1]):  # check for yellow letters at guessed indices
                    if wordle[num1] == let1:
                        add = False
                for num2, let2 in zip(used_result[4], used_result[3]):  # check green letters
                    if not wordle[num2] == let2:
                        add = False
                if add:
                    newPossibilities += [wordle]
        else:
            for wordle in w.allWords:
                add = True
                i = 0
                for letter in list(wordle):
                    if letter in used_result[1] and not i in used_result[4]:
                        add = False
                    i += 1
                for yellow in used_result[1]:  # check for yellow letters in word
                    if not yellow in wordle:
                        add = False
                i = 0
                for num1, let1 in zip(used_result[2], used_result[1]):  # check for yellow letters at guessed indices
                    if wordle[num1] == let1:
                        add = False
                for num2, let2 in zip(used_result[4], used_result[3]):  # check green letters
                    if not wordle[num2] == let2:
                        add = False
                if add:
                    newPossibilities += [wordle]
        for wordle in w.wordles:
            add = True
            i = 0
            for letter in list(wordle):
                if letter in used_result[1] and not i in used_result[4]:
                    add = False
                i += 1
            for yellow in used_result[1]:  # check for yellow letters in word
                if not yellow in wordle:
                    add = False
            i = 0
            for num1, let1 in zip(used_result[2], used_result[1]):  # check for yellow letters at guessed indices
                if wordle[num1] == let1:
                    add = False
            for num2, let2 in zip(used_result[4], used_result[3]):  # check green letters
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
"""  # runner that asks user for guess and result of guess (not currently functional)

"""
Random words average guesses per puzzle: 6.161987041036717
"""  # average guesses for various versions
