"""Interface PyGame très simple pour le jeu Pierre-Feuille-Ciseaux."""

import random
import pygame

from src.logic.logic import comparer

COULEUR_FOND = (200, 200, 200)
COULEUR_TEXTE = (20, 20, 20)
COULEUR_BOUTON = (160, 160, 160)
COULEUR_BOUTON_SELECTION = (190, 190, 190)
TAILLE_FENETRE = (640, 480)

CHOIX = ["pierre", "feuille", "ciseaux"]


class Bouton:
    """Un bouton très basique : un rectangle et un texte."""

    def __init__(self, etiquette: str, rect: pygame.Rect):
        self.etiquette = etiquette
        self.rect = rect

    def dessiner(self, ecran: pygame.Surface, police: pygame.font.Font, survol: bool) -> None:
        couleur = COULEUR_BOUTON_SELECTION if survol else COULEUR_BOUTON
        pygame.draw.rect(ecran, couleur, self.rect)
        pygame.draw.rect(ecran, COULEUR_TEXTE, self.rect, 2)
        texte = police.render(self.etiquette, True, COULEUR_TEXTE)
        texte_rect = texte.get_rect(center=self.rect.center)
        ecran.blit(texte, texte_rect)

    def contient(self, position) -> bool:
        return self.rect.collidepoint(position)


def _afficher_lignes(ecran: pygame.Surface, police: pygame.font.Font, lignes, point_depart: tuple[int, int]) -> None:
    """Affiche des lignes de texte espacées."""
    x, y = point_depart
    for ligne in lignes:
        rendu = police.render(ligne, True, COULEUR_TEXTE)
        ecran.blit(rendu, (x, y))
        y += police.get_linesize()


def lancer_interface() -> None:
    """Démarre la petite interface PyGame."""
    pygame.init()
    ecran = pygame.display.set_mode(TAILLE_FENETRE)
    pygame.display.set_caption("PFC (version débutant)")

    police = pygame.font.Font(None, 36)
    petite_police = pygame.font.Font(None, 28)

    boutons = [
        Bouton("Pierre", pygame.Rect(60, 320, 150, 60)),
        Bouton("Feuille", pygame.Rect(245, 320, 150, 60)),
        Bouton("Ciseaux", pygame.Rect(430, 320, 150, 60)),
    ]

    clock = pygame.time.Clock()
    message = "Clique sur un bouton pour jouer."
    dernier_choix = ""
    scores = {"joueur": 0, "ordi": 0, "egalite": 0}

    en_cours = True
    while en_cours:
        for evenement in pygame.event.get():
            if evenement.type == pygame.QUIT:
                en_cours = False
            elif evenement.type == pygame.MOUSEBUTTONDOWN and evenement.button == 1:
                for bouton in boutons:
                    if bouton.contient(evenement.pos):
                        joueur = bouton.etiquette.lower()
                        ordi = random.choice(CHOIX)
                        resultat = comparer(joueur, ordi)
                        dernier_choix = f"Toi : {joueur} / Ordi : {ordi}"
                        if resultat == "gagne":
                            message = "Tu as gagné cette manche."
                            scores["joueur"] += 1
                        elif resultat == "perd":
                            message = "L'ordi marque un point."
                            scores["ordi"] += 1
                        else:
                            message = "Égalité... on recommence ?"
                            scores["egalite"] += 1

        ecran.fill(COULEUR_FOND)

        titre = police.render("Pierre - Feuille - Ciseaux", True, COULEUR_TEXTE)
        ecran.blit(titre, titre.get_rect(center=(TAILLE_FENETRE[0] // 2, 80)))

        _afficher_lignes(
            ecran,
            petite_police,
            [
                "Version super simple (style débutant)",
                "Clique sur l'un des trois gros boutons gris.",
                "Le score s'affiche juste en dessous.",
            ],
            (60, 140),
        )

        score_lignes = [
            f"Ton score : {scores['joueur']}",
            f"Score ordi : {scores['ordi']}",
            f"Égalités : {scores['egalite']}",
        ]
        _afficher_lignes(ecran, petite_police, score_lignes, (60, 220))

        if dernier_choix:
            _afficher_lignes(ecran, petite_police, [dernier_choix, message], (60, 260))
        else:
            _afficher_lignes(ecran, petite_police, [message], (60, 260))

        position_souris = pygame.mouse.get_pos()
        for bouton in boutons:
            bouton.dessiner(ecran, police, bouton.contient(position_souris))

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()


if __name__ == "__main__":
    lancer_interface()
