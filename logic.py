def comparer(joueur, ordi):

    if joueur == ordi:
        return "egalite"

    if (joueur == "pierre 🪦" and ordi == "ciseaux ✂️") \
       or (joueur == "feuille 🧻" and ordi == "pierre 🪦") \
       or (joueur == "ciseaux ✂️" and ordi == "feuille 🧻"):
        return "gagne"

    return "perd"
