# Pierre • Feuille • Ciseaux — Flask + HTML/CSS/JS

Version web simple de Pierre-Feuille-Ciseaux :
backend Flask (Python) + frontend HTML/CSS/JS.

---

## Arborescence (propre)

```
PFC-PYTHON/
├── src/
│   ├── game/
│   │   ├── __init__.py
│   │   └── game.py
│   ├── logic/
│   │   ├── __init__.py
│   │   └── logic.py
│   └── menu/
│       ├── __init__.py
│       └── menu.py
├── static/
│   ├── style.css
│   └── script.js
├── templates/
│   └── index.html
├── app.py
├── main.py
└── README.md
```

---

## Fonctionnement

* `app.py` : application Flask et routes (`/`, `/state`, `/play`, `/reset`, `/regles`), sessions pour stocker l’état.
* `src/` : logique Python réutilisée (comparaison des coups, règles, boucle de manche).
* `templates/index.html` : structure de la page.
* `static/script.js` : appels `fetch` vers l’API et mise à jour du DOM.
* `static/style.css` : styles (effet “verre”/glass).

---

## Prérequis

* Python 3.9+
* pip
  Conseillé : environnement virtuel.

---

## Installation

macOS / Linux:

```bash
cd PFC-PYTHON
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install flask
```

Windows (PowerShell):

```powershell
cd PFC-PYTHON
py -m venv .venv
. .venv\Scripts\Activate.ps1
py -m pip install --upgrade pip
py -m pip install flask
```

---

## Lancer

Depuis la racine du projet:

macOS / Linux:

```bash
source .venv/bin/activate
python3 app.py
```

Windows (PowerShell):

```powershell
. .venv\Scripts\Activate.ps1
py app.py
```

Ouvrir: `http://127.0.0.1:5000/`

---

## API rapide

* `GET /state` : état courant (scores, égalités, fin de partie)
* `GET /regles` : règles
* `POST /play` : body JSON `{ "choix": "pierre" | "feuille" | "ciseaux" }`
* `POST /reset` : réinitialise la partie

---

## Dépannage

* `ModuleNotFoundError: No module named 'src'`
  Vérifier que les modules sont dans `src/` et que vous lancez `app.py` depuis la racine.
* `ModuleNotFoundError: No module named 'server'`
  Lancer depuis la racine (`python3 app.py` ou `py app.py`), pas depuis `templates/` ou `static/`.
* Chemins `templates`/`static`
  `app.py` doit déclarer `template_folder="templates"` et `static_folder="static"` si nécessaire.

---

## Personnalisation

* Remplacer la clé de session de développement dans `app.py` par une clé forte en production.
* Adapter le design dans `static/style.css`.
* Étendre `src/logic/logic.py` et `src/menu/menu.py` selon vos règles.
