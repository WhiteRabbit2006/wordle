import random
from enum import Enum

import words


class Color(Enum):
    GRAY = 0
    YELLOW = 1
    GREEN = 2


def replace_letter(word, i_letter, replacement="-"):
    return word[0:i_letter] + replacement + word[i_letter + 1:]


class Hint:
    def __init__(self, word, colors):
        self._word = word
        self._colors = colors

    @classmethod
    def from_guess(cls, guess, solution):
        colors = [Color.GRAY] * 5

        # Determine the GREEN letters by testing for exact matches.  When a
        # GREEN letter is found, replace the matching letter in the solution
        # with a "dummy" character (necessary for determining YELLOW
        # characters).
        for i_letter in range(5):
            if guess[i_letter] == solution[i_letter]:
                colors[i_letter] = Color.GREEN
                solution = replace_letter(solution, i_letter)
                # print("Letter %d (%s) is GREEN" % (i_letter, guess[i_letter]))
                # print(solution)

        # Determine the YELLOW letters by testing for "containment" within the
        # solution.  When a YELLOW letter is found, replace the first instance
        # of the "contained" letter with a "dummy" character (necessary for
        # determining additional YELLOW letters).
        for i_letter in range(5):
            if colors[i_letter] is Color.GREEN:
                continue
            if guess[i_letter] in solution:
                colors[i_letter] = Color.YELLOW
                solution = replace_letter(solution, solution.index(guess[i_letter]))
                # print("Letter %d (%s) is YELLOW" % (i_letter, guess[i_letter]))
                # print(solution)

        # Return the hint
        return Hint(guess, colors)

    def is_word_compatible(self, word):

        # Return False if any GREEN letter does not match.  Replace matching
        # GREEN letters in the word with a "dummy" character (necessary for
        # further testing YELLOW and GRAY letters).
        for i_letter in range(5):
            if self._colors[i_letter] == Color.GREEN:
                if self._word[i_letter] != word[i_letter]:
                    return False
                else:
                    word = replace_letter(word, i_letter)

        # Return False if any YELLOW letter does match, or if the word does
        # not contain a YELLOW letter.  Replace "contained" YELLOW letters
        # with a dummy character (necessay for further testing YELLOW letters).
        for i_letter in range(5):
            if self._colors[i_letter] == Color.YELLOW:
                if self._word[i_letter] == word[i_letter]:
                    return False
                elif self._word[i_letter] not in word:
                    return False
                else:
                    word = replace_letter(word, word.index(self._word[i_letter]))

        # Return False if any GRAY letter appears in the word.
        for i_letter in range(5):
            if self._colors[i_letter] == Color.GRAY:
                if self._word[i_letter] in word:
                    return False

        # All letters are compatible with the hint, return True
        return True

    def is_solution(self):
        return all(color is Color.GREEN for color in self._colors)

    def print(self):
        print(self._word)
        for i_letter in range(5):
            if self._colors[i_letter] == Color.GRAY:
                print(0, end="")
            elif self._colors[i_letter] == Color.YELLOW:
                print(1, end="")
            else:
                print(2, end="")
        print("")


def filter_words(words, hint):
    return [word for word in words if hint.is_word_compatible(word)]


class Guesser:
    def __init__(self, possible_guesses=words.allWords, possible_solutions=words.wordles, human_player=False):
        # Create a copy of the possible guesses and soutions.  These will be
        # updated during a game as hints eliminate possible guesses and
        # solutions.
        self._possible_guesses = possible_guesses.copy()
        self._possible_solutions = possible_solutions.copy()
        self._human_player = human_player

    def receive_hint(self, hint):
        # Update possible guesses and solutions
        self._possible_guesses = filter_words(self._possible_guesses, hint)
        self._possible_solutions = filter_words(self._possible_solutions, hint)

    def get_human_guess(self):
        num_solutions = len(self._possible_solutions)
        if num_solutions > 50:
            print("\nThere are %d possible solutions (too many to list):" % num_solutions)
        else:
            print("\nThere are %d possible solutions:" % num_solutions)
            for count, word in enumerate(self._possible_solutions):
                print(word.ljust(7), end="")
                if (count + 1) % 10 == 0:
                    print("")
            print("")
        valid = False
        while not valid:
            guess = input("\nEnter your guess: ")
            if len(guess) != 5 or not guess.isalpha():
                print("Your guess must be exactly 5 alphanumeric characters")
            else:
                guess = guess.lower()
                valid = True
        return guess

    def make_guess(self):
        return self.get_human_guess()


class RandomGuesser(Guesser):
    def make_guess(self):
        return random.choice(tuple(self._possible_solutions))


class RandomScrabbleGuesser(Guesser):
    scrabble_letter_score = {"a": 1, "c": 3, "b": 3, "e": 1, "d": 2, "g": 2,
                             "f": 4, "i": 1, "h": 4, "k": 5, "j": 8, "m": 3,
                             "l": 1, "o": 1, "n": 1, "q": 10, "p": 3, "s": 1,
                             "r": 1, "u": 1, "t": 1, "w": 4, "v": 4, "y": 4,
                             "x": 8, "z": 10}

    def compute_scrabble_score(self, word):
        return sum(self.scrabble_letter_score[letter] for letter in word)

    def make_guess(self):
        guesses = [(self.compute_scrabble_score(word), word)
                   for word in self._possible_solutions]
        guesses.sort()
        min_score = guesses[0][0]
        guesses = [guess[1] for guess in guesses if guess[0] == min_score]
        return random.choice(guesses)


class Game:
    def __init__(self, guesser, solution=None):
        self._guesser = guesser
        self._solution = solution
        if solution is None:
            self._solution = random.choice(tuple(words.wordles))

    def play(self, print_hint=False):
        num_guesses = 0
        solved = False
        while not solved:
            num_guesses += 1
            guess = self._guesser.make_guess()
            hint = Hint.from_guess(guess, self._solution)
            if print_hint:
                hint.print()
            if hint.is_solution():
                solved = True
            else:
                self._guesser.receive_hint(hint)
        return num_guesses


def test_guesser(guesser_class):
    total_num_guesses = 0
    num_games = len(words.wordles)
    for i_game, solution in enumerate(words.wordles):
        num_guesses = Game(guesser_class(), solution).play()
        total_num_guesses += num_guesses
        print("%d of %d, %d" % (i_game, num_games, i_game / num_games * 100))
    print("Average number of guesses =", total_num_guesses / len(words.wordles))


if "__main__" == __name__:
    # test_guesser(RandomGuesser)  # 4.08
    # test_guesser(RandomScrabbleGuesser)  # 4.03
    # Game(Guesser(), "sauna").play(print_hint=True)
    # Game(Guesser(), "cynic").play(print_hint=True)
    # Game(Guesser(), "blind").play(print_hint=True)
    # Game(Guesser()).play(print_hint=True)

# human player known solution
