import collections
import enum
import random


class wordle(enum.Enum): #classe pour déterminer les lettres
    NON = 0
    PRESENT = 1
    CORRECT = 2


def filter_words(words, guess, score):
    """On filtre les mots pour avoir ceux possibles logiquement"""

    new_words = []
    for word in words:
        #compter les chars qui sont présents ou non, sans prendre en compte ceux qui sont corrects
        pool = collections.Counter(c for c, sc in zip(word, score) if sc != wordle.CORRECT)
        for char_w, char_g, sc in zip(word, guess, score):
            if sc == wordle.CORRECT and char_w != char_g:
                break  # Le mot n'a pas de char qui est correcte
            elif char_w == char_g and sc != wordle.CORRECT:
                break  # Si le choix est incorrect on ne l'ajoute pas
            elif sc == wordle.PRESENT:
                if not pool[char_g]:
                    break  #le mot n'a pas ce charactere
                pool[char_g] -= 1
            elif sc == wordle.NON and pool[char_g]:
                break  #Char absent donc on ne l'ajoute pas
        else:
            new_words.append(word)  #Si le mot est valide, on l'ajoute a new words

    return new_words


def get_random_word(words):
    print(f"Je vais prendre au hasard parmis {len(words)} mots...")
    print(f"Je réfléchis a ton mot...")
    guess = random.choice(words)
    print(f"Hmmm, essayes {guess}...")
    return guess

def play_with_computer(words):  
    mapping = {"0": wordle.NON, "1": wordle.PRESENT, "2": wordle.CORRECT}
    print(f"\nNOTE: Appuies sur 0 si la lettre est grise, sur 1 si la lettre est jaune, et 2 si la lettre est verte\n")
    while len(words) > 1:
        regle="incorrect" 
        guess = get_random_word(words)
        print("Quel est ton score ?")
        user_input = input(">>> ")
        if user_input=="non":
            while regle=="incorrect":
                with open("a_file.txt","r") as f:
                    lines=f.readlines()
                    with open("a_file.txt",'w')as fw:
                            for line in lines:
                                if line.strip('\n') != guess:
                                    fw.write(line)
                guess = get_random_word(words)
                print("Quel est ton score ?")
                user_input = input(">>> ")
                if user_input!="non":
                    regle="correct"
        sc = [mapping[char] for char in user_input if char in mapping]
        words = filter_words(words, guess, sc)
    return words
def loopdejeu():#fonction pour jouer
    with open("a_file.txt", "r") as f:#notre dico
        words = [word.strip() for word in f.readlines()]#Créer une liste a partir de notre dico
    words = play_with_computer(words)

    if not words:
        raise RuntimeError("Je ne connais pas ce mot :/")#si le mot n'est pas dans la liste
    print(f"Ton mot est {words[0]}!") # s'il reste un seul mot
    

a="true"
while a=="true": #main loop
    loopdejeu()
    a=input("Veux tu rejouer ? Entre 'o' pour oui et 'n' pour non : \n")
    if a=='n':quit()
    else:a="true"
