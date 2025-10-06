import random
from logic import comparer

def jouer():
    
    choix_possibles = ["pierre", "feuille", "ciseaux"]

    print("Bienvenue dans Pierre-Feuille-Ciseaux ! (tape 'stop' pour quitter)")

    while True:
        print("Choisis : pierre, feuille ou ciseaux")
        joueur = input("> ").strip().lower()

        if joueur == "stop":
            print("Fin du jeu, merci d'avoir joué !")
            break

        if joueur not in choix_possibles:
            print("Choix invalide. Essayez encore.")
            continue

        ordi = random.choice(choix_possibles)
        print("L'ordinateur a choisi :", ordi)

        resultat = comparer(joueur, ordi)
        if resultat == "egalite":
            print("Égalité !")
        elif resultat == "gagne":
            print("Tu gagnes !")
        else:
            print("Tu perds !")


def play_game():
    jouer()

if __name__ == "__main__":
    play_game()
