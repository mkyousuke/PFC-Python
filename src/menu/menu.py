def afficher_menu():
    """Affiche le titre ASCII et les trois options."""
    print("\n")
    print(r"""
╔══════════════════════════════════════════════╗
║        Bienvenue sur le jeu PFC  🪦 🧻 ✂️     ║
╚══════════════════════════════════════════════╝
""")
    print("1) Jouer")
    print("2) Voir les règles")
    print("3) Quitter\n")


def afficher_regles():
    """Affiche les règles puis attend Entrée pour revenir au menu."""
    print("\n— RÈGLES —")
    print("• pierre bat ciseaux")
    print("• feuille bat pierre")
    print("• ciseaux bat feuille")
    print("\nPendant la partie : tape 'stop' pour quitter.\n")
    input("Appuie sur Entrée pour revenir au menu... ")
    print()


def lire_choix():
    """Lit le choix et renvoie 'jouer'/'regles'/'quitter'."""
    while True:
        choix = input("> ").strip().lower()
        if choix in ("1", "j", "jouer"):
            return "jouer"
        elif choix in ("2", "r", "regles", "règles"):
            return "regles"
        elif choix in ("3", "q", "quitter"):
            return "quitter"
        else:
            print("Choix invalide. Tape 1, 2 ou 3 (ou j/r/q).\n")


