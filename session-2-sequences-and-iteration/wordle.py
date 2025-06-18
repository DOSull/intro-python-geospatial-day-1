# Wordle script because 2021
# David O'Sullivan 2022

# the random module allows for randomization functions
import random

from colorama import init
# See https://pypi.org/project/colorama/ for what colorama does
init()

def get_matching_indexes(attempt:str, word:str):
    """Returns list of index positions where attempt matches word
    
    Args:
        attempt (str): the user's attempt at guessing the word.
        word (str): the word in which to find matches.
        
    Returns:
        list[int]: a list of ints for the matching positions.
    """
    return [i for i in range(5) if attempt[i] == word[i]]

def score_attempt(attempt:str, word:str, miss:str = "."):
    """Returns a string representing how well attempt matches word.
    
    By default a correct letter in the correct position is shown upper case;
    a letter in the word, but in the wrong position is shown lower case; and
    a completely incorrect letter is shown as the 'miss' character. E.g.
    
        attempt "CROAK" on word "TRAIN" --> ".Ra.."
    
    Args:
        attempt (str): the user's attempt to guess the word.
        word (str): the word they are trying to guess.
        miss(str, optional): the character to use for complete misses. Defaults
          to ".".
    
    Returns:
        str: encoded per the description above.
    """
    matches = get_matching_indexes(attempt, word)
    other_letters = [c for i, c in enumerate(word) if i not in matches]
    other_matches = []
    for i in range(5):
        if i not in matches:
            if attempt[i] in other_letters:
                other_matches.append(i)
                # only give one mark per letter in attempt
                other_letters.remove(attempt[i])
    # baseline is all letters are misses; use list because strings are immutable
    clue = [miss] * 5
    # give an upper case letter for all matches
    for i in matches:
        clue[i] = attempt[i].upper()
    # give a lower case letter for all letters in attempt that are in word
    for i in other_matches:
        clue[i] = attempt[i].lower()
    return "".join(clue)

congrats = {1: "Genius!"  , 2: "Magnificent.", 3: "Impressive.",
            4: "Splendid.", 5: "Great."      , 6: "Phew!"}

# open and read files of words
with open('wordlist.txt') as f:
    answers = f.readlines()

with open('valid_guesses.txt') as f:
    allowed_words = f.readlines()

# strip off trailing linefeed and convert to lower case
answers       = [w.strip().lower() for w in answers]
allowed_words = [w.strip().lower() for w in allowed_words] + answers

# Greet the player and tell them what to do
print("""\nI'm thinking of a 5 letter word.\n
You have 6 attempts to work it out based on clues I will give in response to
your guesses. If one of your letters matches a letter in the word and is in the
right position I will capitalise it. If it is in the word, I will show it in
lower case. If it is not in the word at all I will mark it with a '.'\n""")

# Whole program nested in infinite loop
# session (multiple games) loop
while True:
    guess_number = 1
    # select a word at random from the file
    word = random.choice(answers).lower()
    
    # game loop
    while guess_number < 7:
        # Get the next guess from the player
        attempt = input(f"Attempt {guess_number}: ")
        # handle the * case -- which indicates player wants to finish
        if attempt == "*":
            print ()
            break  # exit game loop
        if attempt == "":
            print ()
            continue  # go around again

        # convert the guess to lower case
        attempt = attempt.lower()
        # check that guesses are letters
        if not attempt.isalpha():
            print("\nYour guess should be all letters.\n")
            continue
        if attempt not in allowed_words:
            print("\nYour guess is not a word, try again.\n")
            continue
        
        # the gobbledegook here is to put the cursor back after the input prompt
        # https://gist.github.com/ConnerWill/d4b6c776b509add763e17f9f113fd25b
        print(f"\033[1A\033[{17}C -->  {score_attempt(attempt, word)}")
        if attempt == word:
            print(f"\n{congrats[guess_number]} you got it in {guess_number}.\n")
            break

        guess_number = guess_number + 1

    if guess_number == 7:
        print(f"\nBad luck! The answer was {word}.\n")
    again = input("Another game (Y/N)? ")
    if again.lower() == "y":
        print()
        continue  # go around again
    else:
        print("\nBye!\n")
        break  # exit
