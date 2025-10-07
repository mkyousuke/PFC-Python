# main.py — boucle menu + jeu (débutant)
from game import play_game
from menu import afficher_menu, lire_choix, afficher_regles

def main():
    while True:
        afficher_menu()
        action = lire_choix()

        if action == "jouer":
            play_game()  
        elif action == "regles":
            afficher_regles() 
        else: 
            print("\nÀ bientôt !\n")
            break

if __name__ == "__main__":
    main()
