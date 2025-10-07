# 🪦🧻✂️ Pierre • Feuille • Ciseaux (Python)

Un petit projet **débutant** en Python qui joue à *Pierre‑Feuille‑Ciseaux* dans le terminal — clair, simple, efficace.

> 🎯 Objectif : le **premier à 3 points** gagne. Tapez `stop` à tout moment pour quitter.

---

## ✨ Fonctionnalités
- Interface terminal soignée avec **emojis** (🪦 pierre · 🧻 feuille · ✂️ ciseaux)
- **Score en direct**, numéro de manche, et **arrêt** avec `stop`
- **Règles** intégrées via le menu
- Code **structuré** et facile à lire

---

## 🗂️ Arborescence
```
.
├── main.py         # Point d’entrée (menu + navigation)
├── menu.py         # Affichage du menu et des règles
├── game.py         # Boucle de jeu & gestion du score
└── logic.py        # Logique: comparer les choix (gagne/perd/égalité)
```

---

## 🚀 Lancer le projet
> Prérequis : **Python 3.10+** — aucune dépendance externe.

```bash
python -m venv .venv
source .venv/bin/activate
python main.py
```

---

## 📜 Règles (rappel)
- **pierre** bat **ciseaux**
- **feuille** bat **pierre**
- **ciseaux** bat **feuille**

---

## 💡 Astuces
- Entrez `pierre`, `feuille` ou `ciseaux` (majuscules/espaces ignorés)
- Tapez `stop` pour quitter proprement

---

## 🧰 Personnalisation
- Changez l’objectif de victoires dans `game.py` (`objectif_victoires = 3`)
- Modifiez les emojis / libellés dans `game.py` (`EMOJIS = {...}`)

---

Fait avec ❤️ pour apprendre, s’amuser et progresser en Python.
