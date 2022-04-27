import collections
import enum
import random


class wordle(enum.Enum): #classe pour déterminer les lettres
    NON = 0
    PRESENT = 1
    CORRECT = 2


def score(secret, guess):
    """Scores a guess word when compared to a secret word.
    Makes sure that characters aren't over-counted when they are correct.
    For example, a careless implementation would flag the first “s”
    of “swiss” as PRESENT if the secret word were “chess”.
    However, the first “s” must be flagged as ABSENT.
    To account for this, we start by computing a pool of all the relevant characters
    and then make sure to remove them as they get used.
    """

    # All characters that are not correct go into the usable pool.
    pool = collections.Counter(s for s, g in zip(secret, guess) if s != g)
    # Create a first tentative score by comparing char by char.
    score = []
    for secret_char, guess_char in zip(secret, guess):
        if secret_char == guess_char:
            score.append(wordle.CORRECT)
        elif guess_char in secret and pool[guess_char] > 0:
            score.append(wordle.PRESENT)
            pool[guess_char] -= 1
        else:
            score.append(wordle.NON)

    return score


def filter_words(words, guess, score):
    """Filter words to only keep those that respect the score for the given guess."""

    new_words = []
    for word in words:
        # The pool of characters that account for the PRESENT ones is all the characters
        # that do not correspond to CORRECT positions.
        pool = collections.Counter(c for c, sc in zip(word, score) if sc != wordle.CORRECT)
        for char_w, char_g, sc in zip(word, guess, score):
            if sc == wordle.CORRECT and char_w != char_g:
                break  # Word doesn't have the CORRECT character.
            elif char_w == char_g and sc != wordle.CORRECT:
                break  # If the guess isn't CORRECT, no point in having equal chars.
            elif sc == wordle.PRESENT:
                if not pool[char_g]:
                    break  # Word doesn't have this PRESENT character.
                pool[char_g] -= 1
            elif sc == wordle.NON and pool[char_g]:
                break  # ABSENT character shouldn't be here.
        else:
            new_words.append(word)  # No `break` was hit, so store the word.

    return new_words


def get_random_word(words):
    print(f"Je vais prendre au hasard parmis {len(words)} mots...")
    print(f"Je réfléchis a ton mot...")
    guess = random.choice(words)
    print(f"Hmmm, essayes {guess!r}...")
    return guess

def play_with_computer(words):
    
    mapping = {"0": wordle.NON, "1": wordle.PRESENT, "2": wordle.CORRECT}
    print(f"\nNOTE: Appuies sur 0 si la lettre est grise, sur 1 si la lettre est jaune, et 2 si la lettre est verte\n")
    while len(words) > 1:
        guess = get_random_word(words)
        print("Quel est ton score ?")
        user_input = input(">>> ")
        sc = [mapping[char] for char in user_input if char in mapping]
        words = filter_words(words, guess, sc)
        print()

    return words
def loopdejeu():#fonction pour jouer
    WORD_LST = "a_file.txt"  # Dictionnaire crée auparavant

    with open(WORD_LST, "r") as f:
        words = [word.strip() for word in f.readlines()]

    words = play_with_computer(words)

    if not words:
        raise RuntimeError("Je ne connais pas ce mot :/")#si le mot n'est pas dans la liste
    print(f"Ton mot est {words[0]!r}!") # s'il reste un seul mot
    

a="true"
while a=="true": #main loop
    loopdejeu()
    a=input("Veux tu rejouer ? Entre 'o' pour oui et 'n' pour non : \n")
    if a=='n':quit()
    else:a="true"
