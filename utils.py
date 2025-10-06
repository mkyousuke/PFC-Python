def afficher_menu():
    print("=== Pierre Feuille Ciseaux ===")
    print("Tape 'STOP' pour quitter le jeu.")

def demander_choix():    
    choix = input("Choisis : pierre, feuille ou ciseaux → ")
    return choix.lower()

def afficher_resultat(resultat):
    if resultat == "gagne":
        print("Tu gagnes ! 🎉")
    elif resultat == "perd":
        print("Tu perds... 😢")
    else:
        print("Égalité 🤝")
        
        

