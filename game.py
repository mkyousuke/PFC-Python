import random
from logic import comparer

RESET  = "\033[0m"
VERT   = "\033[38;5;46m"    
ROUGE  = "\033[38;5;196m"  
ORANGE = "\033[38;5;208m"   

EMOJIS = {"pierre": "🪦", "feuille": "🧻", "ciseaux": "✂️"}


def jouer():
    """
    Jeu de Pierre-Feuille-Ciseaux : le premier à 3 victoires gagne.
    Affiche les émojis, le numéro de manche et le score en direct.
    """
    choix_possibles = ["pierre", "feuille", "ciseaux"]

    score_joueur = 0
    score_ordi = 0
    egalites = 0
    manches_jouees = 0
    objectif_victoires = 3  # premier à 3

    print("\nBienvenue dans Pierre-Feuille-Ciseaux ! 🎮 (premier à 3 points)")
    print("Tape 'stop' à tout moment pour quitter.\n")

    while score_joueur < objectif_victoires and score_ordi < objectif_victoires:
        manches_jouees += 1
        print(f"=== Manche {manches_jouees} ===")
        print(f"Choisis : pierre {EMOJIS['pierre']}, feuille {EMOJIS['feuille']} ou ciseaux {EMOJIS['ciseaux']}")

        joueur = input("> ").strip().lower()

        if joueur == "stop":
            print("\nPartie interrompue par le joueur.\n")
            break

        if joueur not in choix_possibles:
            print("Choix invalide. Tape 'pierre', 'feuille' ou 'ciseaux'.\n")
            continue

        ordi = random.choice(choix_possibles)
        print(f"L'ordinateur a choisi : {ordi} {EMOJIS[ordi]}")

        resultat = comparer(joueur, ordi)
        if resultat == "egalite":
            print(ORANGE + "\nÉgalité 🤝" + RESET)
            egalites += 1
        elif resultat == "gagne":
            print(VERT + "\nTu gagnes cette manche ! 🎉" + RESET)
            score_joueur += 1
        else:
            print(ROUGE + "\nTu perds cette manche 😢" + RESET)
            score_ordi += 1

        print(f"\nScore → Toi {score_joueur} - Ordi {score_ordi} | Égalités : {egalites}\n")

    print("=== Fin de la partie ===")
    print(f"Résultat final : Toi {score_joueur} - Ordi {score_ordi} | Égalités : {egalites}")

    if score_joueur >= objectif_victoires:
        print(VERT + "🎉 Bravo, tu remportes la partie !" + RESET)
    elif score_ordi >= objectif_victoires:
        print(ROUGE + "🤖 L'ordinateur gagne la partie !\n😢 Bien joué quand même !" + RESET)
    else:
        print(ORANGE + "Partie interrompue avant la fin." + RESET)


def play_game():
    jouer()


if __name__ == "__main__":
    play_game()
