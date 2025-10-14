from flask import Flask, render_template, request, jsonify, session
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

comparer = _import_comparer()

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

afficher_regles_fn = _import_afficher_regles()

def _ensure_state():
    if "score_joueur" not in session:
        session["score_joueur"] = 0
        session["score_ordi"] = 0
        session["egalites"] = 0
        session["termine"] = False

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/state")
def state():
    _ensure_state()
    return jsonify({
        "score_joueur": session["score_joueur"],
        "score_ordi": session["score_ordi"],
        "egalites": session["egalites"],
        "termine": session["termine"]
    })

@app.route("/regles")
def regles():
    # Remplacement de l'ancienne logique pour un affichage HTML propre
    regles_html = """
        <h2> RÈGLES DU JEU </h2>
        <ul>
            <li>La pierre bat les ciseaux</li>
            <li>La feuille bat la pierre</li>
            <li>Les ciseaux battent la feuille</li>
        </ul>
        <p>Le premier joueur à <strong>3 points</strong> gagne la partie.</p>
    """
    return jsonify({"regles": regles_html})

@app.route("/play", methods=["POST"])
def play():
    _ensure_state()
    if session["termine"]:
        return jsonify({
            "erreur": "La partie est terminée. Cliquez sur Réinitialiser.",
            "termine": True,
            "score": {
                "joueur": session["score_joueur"],
                "ordi": session["score_ordi"],
                "egalites": session["egalites"]
            }
        }), 400

    data = request.get_json(silent=True) or {}
    joueur = data.get("choix")
    if joueur not in CHOIX_POSSIBLES:
        return jsonify({"erreur": "Choix invalide."}), 400

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

    return jsonify({
        "joueur": joueur,
        "ordi": ordi,
        "resultat": resultat,
        "score": {
            "joueur": session["score_joueur"],
            "ordi": session["score_ordi"],
            "egalites": session["egalites"]
        },
        "termine": session["termine"]
    })

@app.route("/reset", methods=["POST"])
def reset():
    session.clear()
    return jsonify({"ok": True})
    
if __name__ == "__main__":
    app.run(debug=True)