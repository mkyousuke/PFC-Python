# 🪦🧻✂️ Pierre • Feuille • Ciseaux (Python)

Un petit projet **débutant** en Python qui joue à *Pierre‑Feuille‑Ciseaux* dans le terminal — clair, simple, efficace.

> Nouveau : une **mini interface PyGame** avec trois gros boutons gris pour cliquer comme un vrai débutant. Pour l'essayer : `python -m src.gui.app`.

> Objectif : le **premier à 3 points** gagne. Tapez `stop` à tout moment pour quitter.

---

## Fonctionnalités
- Interface terminal soignée avec **emojis** (🪦 pierre · 🧻 feuille · ✂️ ciseaux)
- **Score en direct**, numéro de manche, et **arrêt** avec `stop`
- **Règles** intégrées via le menu
- Code **structuré** et facile à lire

---

## Arborescence
```
.
├── main.py
├── README.md
└── src/
    ├── __init__.py
    ├── game/
    │   ├── __init__.py
    │   └── game.py          # Boucle de jeu & gestion du score
    ├── gui/
    │   ├── __init__.py
    │   └── app.py           # Interface PyGame toute simple
    ├── logic/
    │   ├── __init__.py
    │   └── logic.py         # Logique: comparer les choix (gagne/perd/égalité)
    └── menu/
        ├── __init__.py
        └── menu.py          # Affichage du menu et des règles
```

---

## Lancer le projet
> Prérequis : **Python 3.10+** — installez `pygame` (`pip install pygame`) si vous testez l'interface graphique.


1. Se rendre à la racine du dossier du projet
2. Ouvrir un terminal 
3. Taper la commande suivante : 

```bash
python main.py
```
ou sur macOS
```bash
python3 main.py
```

### Lancer l'interface PyGame (optionnel)

```bash
python -m src.gui.app
```

---

## Règles (rappel)
- **pierre** bat **ciseaux**
- **feuille** bat **pierre**
- **ciseaux** bat **feuille**

---

## Astuces
- Entrez `pierre`, `feuille` ou `ciseaux` (majuscules/espaces ignorés)
- Tapez `stop` pour quitter proprement

---

## Personnalisation
- Changez l’objectif de victoires dans `src/game/game.py` (`objectif_victoires = 3`)
- Modifiez les emojis / libellés dans `src/game/game.py` (`EMOJIS = {...}`)

---

Fait par : 
Nathan Toubalem & Maxime Loprin
