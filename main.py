from src.menu.menu import afficher_menu, afficher_regles, lire_choix
from src.game.game import jouer as play_game  

def main():
    while True:
        afficher_menu()
        action = lire_choix()
        if action == "jouer":
            play_game()  
        elif action == "regles":
            afficher_regles()
        elif action == "quitter":
            print("À bientôt ! 👋")
            break

if __name__ == "__main__":
    main()
