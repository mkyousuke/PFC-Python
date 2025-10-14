const boutons = document.querySelectorAll('.btn[data-choix]');
const choixJoueur = document.getElementById('choix-joueur');
const choixOrdi = document.getElementById('choix-ordi');
const texteFinal = document.getElementById('texte-final');
const scoreJoueur = document.getElementById('score-joueur');
const scoreEgalite = document.getElementById('score-egalite');
const scoreOrdi = document.getElementById('score-ordi');
const btnReset = document.getElementById('btn-reset');
const btnRegles = document.getElementById('btn-regles');
const blocRegles = document.getElementById('bloc-regles');

async function syncState() {
  const r = await fetch('/state');
  const s = await r.json();
  scoreJoueur.textContent = s.score_joueur;
  scoreEgalite.textContent = s.egalites;
  scoreOrdi.textContent = s.score_ordi;
  if (s.termine) lockGame();
}

function lockGame() {
  boutons.forEach(b => b.disabled = true);
  texteFinal.textContent = '🏁 Partie terminée — cliquez sur Réinitialiser.';
  texteFinal.classList.remove('win', 'lose', 'draw');
}

function majScores(s) {
  scoreJoueur.textContent = s.joueur;
  scoreEgalite.textContent = s.egalites;
  scoreOrdi.textContent = s.ordi;
}

boutons.forEach(b => {
  b.addEventListener('click', async () => {
    const choix = b.dataset.choix;
    texteFinal.classList.remove('win', 'lose', 'draw');
    texteFinal.textContent = '...';

    try {
      const res = await fetch('/play', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ choix })
      });

      const data = await res.json();

      if (!res.ok) {
        texteFinal.textContent = data.erreur || 'Erreur.';
        if (data.termine) lockGame();
        return;
      }
      choixJoueur.textContent = data.joueur;
      choixOrdi.textContent = data.ordi;

      if (data.resultat === 'gagne') {
        texteFinal.textContent = '✅ Vous avez gagné !';
        texteFinal.classList.add('win');
      } else if (data.resultat === 'perd') {
        texteFinal.textContent = '❌ Vous avez perdu.';
        texteFinal.classList.add('lose');
      } else {
        texteFinal.textContent = '🤝 Égalité.';
        texteFinal.classList.add('draw');
      }

      majScores(data.score);

      if (data.termine) lockGame();

    } catch (e) {
      texteFinal.textContent = 'Erreur réseau.';
    }
  });
});
btnReset.addEventListener('click', async () => {
  await fetch('/reset', { method: 'POST' });
  scoreJoueur.textContent = '0';
  scoreEgalite.textContent = '0';
  scoreOrdi.textContent = '0';
  choixJoueur.textContent = '–';
  choixOrdi.textContent = '–';
  texteFinal.textContent = 'Cliquez pour jouer !';
  texteFinal.classList.remove('win', 'lose', 'draw');
  boutons.forEach(b => b.disabled = false);
});

btnRegles.addEventListener('click', async () => {
  if (!blocRegles.hasAttribute('hidden')) {
    blocRegles.setAttribute('hidden', '');
    return;
  }

  const r = await fetch('/regles');
  const d = await r.json();
  blocRegles.textContent = d.regles || '';
  blocRegles.removeAttribute('hidden');
});

syncState();
