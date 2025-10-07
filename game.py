import random
from logic import comparer

EMOJIS = {"pierre": "🪦", "feuille": "🧻", "ciseaux": "✂️"}

def jouer():
    choix_possibles = ["pierre", "feuille", "ciseaux"]

    print("Bienvenue dans Pierre-Feuille-Ciseaux ! (tape 'stop' pour quitter)")

    while True:
        print(f"Choisis : pierre {EMOJIS['pierre']}, feuille {EMOJIS['feuille']} ou ciseaux {EMOJIS['ciseaux']}")
        joueur = input("> ").strip().lower()

        if joueur == "stop":
            print("Fin du jeu, merci d'avoir joué !")
            break

        if joueur not in choix_possibles:
            print("Choix invalide. Tape 'pierre', 'feuille' ou 'ciseaux'.")
            continue

        ordi = random.choice(choix_possibles)
        print("L'ordinateur a choisi :", f"{ordi} {EMOJIS[ordi]}")

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
