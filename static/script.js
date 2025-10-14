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
const confettiCanvas = document.getElementById('confetti-canvas');

// Fonction pour l'animation de victoire
function handleVictory() {
  texteFinal.textContent = '🏆 Victoire ! 🎉';
  texteFinal.classList.add('win');
  texteFinal.style.transform = 'scale(1.2)';
  texteFinal.style.color = '#22c55e'; // Vert vif

  // Animation de confettis
  const myConfetti = confetti.create(confettiCanvas, {
    resize: true,
    useWorker: true
  });
  myConfetti({
    particleCount: 200,
    spread: 160,
    origin: { y: 0.6 }
  });
}

// Fonction pour l'animation de défaite
function handleDefeat() {
  texteFinal.textContent = '😢 Défaite... 😭';
  texteFinal.classList.add('lose');
  texteFinal.style.transform = 'scale(1.2)';
  texteFinal.style.color = '#ef4444'; // Rouge vif

  // Animation des pleurs (emojis)
  const tearContainer = document.body;
  for (let i = 0; i < 30; i++) {
    const tear = document.createElement('div');
    tear.innerHTML = '😢';
    tear.style.position = 'fixed';
    tear.style.left = `${Math.random() * 100}vw`;
    tear.style.top = `${-50 - Math.random() * 100}px`;
    tear.style.fontSize = `${1 + Math.random() * 1.5}rem`;
    tear.style.animation = `fall 5s linear ${Math.random() * 5}s forwards`;
    tearContainer.appendChild(tear);
  }
}

// Keyframes pour l'animation des pleurs (à ajouter au CSS ou ici via JS)
const styleSheet = document.createElement("style");
styleSheet.innerText = `
@keyframes fall {
  to {
    transform: translateY(110vh);
    opacity: 0;
  }
}
`;
document.head.appendChild(styleSheet);


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
  texteFinal.classList.remove('win', 'lose', 'draw');

  const finalScoreJoueur = parseInt(scoreJoueur.textContent, 10);
  const finalScoreOrdi = parseInt(scoreOrdi.textContent, 10);

  if (finalScoreJoueur > finalScoreOrdi) {
    handleVictory();
  } else {
    handleDefeat();
  }
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
  window.location.reload(); // Recharger la page pour une réinitialisation propre
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