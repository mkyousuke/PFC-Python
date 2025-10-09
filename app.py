from flask import Flask, render_template, request, redirect, url_for, session
import random, io, contextlib

app = Flask(__name__)
app.secret_key = "dev"

CHOIX_POSSIBLES = ["pierre", "feuille", "ciseaux"]
OBJECTIF_VICTOIRES = 3

def _import_comparer():
    try:
        from src.logic.logic import comparer as cmp
        return cmp
    except Exception:
        try:
            from src.logic import comparer as cmp
            return cmp
        except Exception:
            from logic import comparer as cmp
            return cmp

def _import_afficher_regles():
    try:
        from src.menu import afficher_regles as ar
        return ar
    except Exception:
        try:
            from menu import afficher_regles as ar
            return ar
        except Exception:
            return None

comparer = _import_comparer()
afficher_regles_fn = _import_afficher_regles()

def _ensure_state():
    if "score_joueur" not in session:
        session["score_joueur"] = 0
        session["score_ordi"] = 0
        session["egalites"] = 0
        session["termine"] = False
        session["show_rules"] = False
        session["last_joueur"] = None
        session["last_ordi"] = None
        session["last_resultat"] = None

@app.route("/", methods=["GET"])
def index():
    _ensure_state()
    regles = None
    if session.get("show_rules"):
        if afficher_regles_fn:
            s = io.StringIO()
            with contextlib.redirect_stdout(s):
                afficher_regles_fn()
            regles = s.getvalue().strip() or None
        else:
            regles = "— RÈGLES —\n• pierre bat ciseaux\n• feuille bat pierre\n• ciseaux bat feuille"
    return render_template(
        "index.html",
        score_joueur=session["score_joueur"],
        score_ordi=session["score_ordi"],
        egalites=session["egalites"],
        termine=session["termine"],
        last_joueur=session["last_joueur"],
        last_ordi=session["last_ordi"],
        last_resultat=session["last_resultat"],
        regles=regles
    )

@app.route("/play", methods=["POST"])
def play():
    _ensure_state()
    if session["termine"]:
        return redirect(url_for("index"))
    joueur = request.form.get("choix")
    if joueur not in CHOIX_POSSIBLES:
        return redirect(url_for("index"))
    ordi = random.choice(CHOIX_POSSIBLES)
    resultat = comparer(joueur, ordi)
    if resultat == "gagne":
        session["score_joueur"] += 1
    elif resultat == "perd":
        session["score_ordi"] += 1
    else:
        session["egalites"] += 1
    if session["score_joueur"] >= OBJECTIF_VICTOIRES or session["score_ordi"] >= OBJECTIF_VICTOIRES:
        session["termine"] = True
    session["last_joueur"] = joueur
    session["last_ordi"] = ordi
    session["last_resultat"] = resultat
    return redirect(url_for("index"))

@app.route("/reset", methods=["POST"])
def reset():
    session.clear()
    return redirect(url_for("index"))

@app.route("/toggle-regles", methods=["POST"])
def toggle_regles():
    _ensure_state()
    session["show_rules"] = not session["show_rules"]
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
