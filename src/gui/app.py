"""Interface PyGame améliorée pour le jeu Pierre-Feuille-Ciseaux."""

from __future__ import annotations

import random
from dataclasses import dataclass

import pygame

from src.logic.logic import comparer

TAILLE_FENETRE = (720, 540)

COULEUR_FOND_HAUT = (30, 34, 64)
COULEUR_FOND_BAS = (120, 80, 140)
COULEUR_CARTE = (245, 242, 240)
COULEUR_CARTE_SURVOL = (255, 248, 242)
COULEUR_CARTE_CONTOUR = (80, 60, 110)
COULEUR_TEXTE = (35, 30, 50)
COULEUR_TEXTE_SECONDAIRE = (80, 70, 110)
COULEUR_PANNEAU = (255, 255, 255, 160)

CHOIX = ["pierre", "feuille", "ciseaux"]


def _creer_fond(taille: tuple[int, int]) -> pygame.Surface:
    """Crée un simple fond en dégradé."""

    largeur, hauteur = taille
    fond = pygame.Surface(taille)
    for y in range(hauteur):
        ratio = y / max(hauteur - 1, 1)
        couleur = tuple(
            int(COULEUR_FOND_HAUT[i] * (1 - ratio) + COULEUR_FOND_BAS[i] * ratio)
            for i in range(3)
        )
        pygame.draw.line(fond, couleur, (0, y), (largeur, y))
    return fond


def _icone_pierre(taille: int) -> pygame.Surface:
    icone = pygame.Surface((taille, taille), pygame.SRCALPHA)
    centre = taille // 2
    rayon = int(taille * 0.38)
    pygame.draw.circle(icone, (170, 170, 180), (centre, centre), rayon)
    pygame.draw.circle(icone, (200, 200, 210), (centre - rayon // 4, centre - rayon // 4), rayon // 2)
    pygame.draw.circle(icone, (140, 140, 150), (centre + rayon // 5, centre + rayon // 6), rayon // 2, 3)
    return icone


def _icone_feuille(taille: int) -> pygame.Surface:
    icone = pygame.Surface((taille, taille), pygame.SRCALPHA)
    centre = taille // 2
    hauteur = int(taille * 0.75)
    largeur = int(taille * 0.55)
    points = [
        (centre, centre - hauteur // 2),
        (centre + largeur // 2, centre),
        (centre, centre + hauteur // 2),
        (centre - largeur // 2, centre),
    ]
    pygame.draw.polygon(icone, (90, 180, 110), points)
    pygame.draw.polygon(icone, (60, 120, 80), points, 4)
    pygame.draw.line(icone, (60, 120, 80), (centre, centre - hauteur // 2), (centre, centre + hauteur // 2), 4)
    pygame.draw.line(icone, (60, 120, 80), (centre, centre), (centre + largeur // 4, centre - hauteur // 6), 3)
    pygame.draw.line(icone, (60, 120, 80), (centre, centre + hauteur // 6), (centre - largeur // 4, centre - hauteur // 10), 3)
    return icone


def _icone_ciseaux(taille: int) -> pygame.Surface:
    icone = pygame.Surface((taille, taille), pygame.SRCALPHA)
    centre = taille // 2
    longueur = int(taille * 0.8)
    # Lames
    pygame.draw.polygon(
        icone,
        (210, 210, 220),
        [
            (centre - longueur // 2, centre - 12),
            (centre + longueur // 2, centre - 4),
            (centre + longueur // 2 - 20, centre + 4),
            (centre - longueur // 2 + 20, centre - 4),
        ],
    )
    pygame.draw.polygon(
        icone,
        (210, 210, 220),
        [
            (centre - longueur // 2, centre + 12),
            (centre + longueur // 2, centre + 4),
            (centre + longueur // 2 - 20, centre - 4),
            (centre - longueur // 2 + 20, centre + 4),
        ],
    )
    # Poignées
    pygame.draw.circle(icone, (200, 120, 120), (centre - 25, centre + 24), 20, 6)
    pygame.draw.circle(icone, (200, 120, 120), (centre + 5, centre + 32), 16, 6)
    pygame.draw.circle(icone, (160, 90, 100), (centre - 10, centre + 10), 8)
    return icone


def _creer_icones(taille: int) -> dict[str, pygame.Surface]:
    return {
        "pierre": _icone_pierre(taille),
        "feuille": _icone_feuille(taille),
        "ciseaux": _icone_ciseaux(taille),
    }


@dataclass
class CarteChoix:
    etiquette: str
    rect: pygame.Rect
    icone: pygame.Surface

    def contient(self, position: tuple[int, int]) -> bool:
        return self.rect.collidepoint(position)

    def dessiner(
        self,
        ecran: pygame.Surface,
        police: pygame.font.Font,
        petite_police: pygame.font.Font,
        survol: bool,
    ) -> None:
        couleur = COULEUR_CARTE_SURVOL if survol else COULEUR_CARTE
        pygame.draw.rect(ecran, couleur, self.rect, border_radius=18)
        pygame.draw.rect(ecran, COULEUR_CARTE_CONTOUR, self.rect, width=3, border_radius=18)

        icone_rect = self.icone.get_rect(center=(self.rect.centerx, self.rect.centery - 30))
        ecran.blit(self.icone, icone_rect)

        etiquette = police.render(self.etiquette.capitalize(), True, COULEUR_TEXTE)
        etiquette_rect = etiquette.get_rect(center=(self.rect.centerx, self.rect.bottom - 45))
        ecran.blit(etiquette, etiquette_rect)

        sous_titre = petite_police.render("Clique pour jouer", True, COULEUR_TEXTE_SECONDAIRE)
        sous_rect = sous_titre.get_rect(center=(self.rect.centerx, self.rect.bottom - 20))
        ecran.blit(sous_titre, sous_rect)


def _afficher_scores(
    ecran: pygame.Surface,
    police: pygame.font.Font,
    scores: dict[str, int],
    position: pygame.Rect,
) -> None:
    panneau = pygame.Surface(position.size, pygame.SRCALPHA)
    panneau.fill(COULEUR_PANNEAU)
    ecran.blit(panneau, position.topleft)

    titres = ["Toi", "Ordi", "Égalités"]
    valeurs = [scores["joueur"], scores["ordi"], scores["egalite"]]
    largeur_colonne = position.width // 3
    for idx, (titre, valeur) in enumerate(zip(titres, valeurs)):
        x = position.left + idx * largeur_colonne + largeur_colonne // 2
        titre_rendu = police.render(titre, True, COULEUR_TEXTE_SECONDAIRE)
        valeur_rendu = police.render(str(valeur), True, COULEUR_TEXTE)
        ecran.blit(titre_rendu, titre_rendu.get_rect(center=(x, position.centery - 20)))
        ecran.blit(valeur_rendu, valeur_rendu.get_rect(center=(x, position.centery + 15)))


def _afficher_messages(
    ecran: pygame.Surface,
    police: pygame.font.Font,
    messages: list[str],
    rect: pygame.Rect,
) -> None:
    panneau = pygame.Surface(rect.size, pygame.SRCALPHA)
    panneau.fill((255, 255, 255, 200))
    ecran.blit(panneau, rect.topleft)
    y = rect.top + 12
    for message in messages:
        rendu = police.render(message, True, COULEUR_TEXTE)
        ecran.blit(rendu, (rect.left + 18, y))
        y += police.get_linesize() + 4


def lancer_interface() -> None:
    """Démarre la version améliorée de l'interface PyGame."""

    pygame.init()
    ecran = pygame.display.set_mode(TAILLE_FENETRE)
    pygame.display.set_caption("Pierre - Feuille - Ciseaux")

    fond = _creer_fond(TAILLE_FENETRE)
    icones = _creer_icones(120)

    police_titre = pygame.font.Font(None, 64)
    police = pygame.font.Font(None, 42)
    petite_police = pygame.font.Font(None, 28)

    largeur_carte = 180
    hauteur_carte = 220
    espace = 30
    total_largeur = largeur_carte * 3 + espace * 2
    depart_x = (TAILLE_FENETRE[0] - total_largeur) // 2
    rects = [
        pygame.Rect(depart_x + (largeur_carte + espace) * i, 200, largeur_carte, hauteur_carte)
        for i in range(3)
    ]

    cartes = [
        CarteChoix(choix, rect, icones[choix]) for choix, rect in zip(CHOIX, rects)
    ]

    zone_scores = pygame.Rect(60, 120, TAILLE_FENETRE[0] - 120, 90)
    zone_messages = pygame.Rect(60, 440, TAILLE_FENETRE[0] - 120, 80)

    clock = pygame.time.Clock()
    message = "Clique sur une carte pour lancer la manche."
    dernier_choix = ""
    scores = {"joueur": 0, "ordi": 0, "egalite": 0}

    en_cours = True
    while en_cours:
        for evenement in pygame.event.get():
            if evenement.type == pygame.QUIT:
                en_cours = False
            elif evenement.type == pygame.MOUSEBUTTONDOWN and evenement.button == 1:
                for carte in cartes:
                    if carte.contient(evenement.pos):
                        joueur = carte.etiquette
                        ordi = random.choice(CHOIX)
                        resultat = comparer(joueur, ordi)
                        dernier_choix = f"Tu joues {joueur.capitalize()} | Ordi : {ordi.capitalize()}"
                        if resultat == "gagne":
                            message = "Bravo ! Tu remportes la manche."
                            scores["joueur"] += 1
                        elif resultat == "perd":
                            message = "Aïe, l'ordinateur marque ce point."
                            scores["ordi"] += 1
                        else:
                            message = "Égalité parfaite. Rejouez !"
                            scores["egalite"] += 1

        ecran.blit(fond, (0, 0))

        titre = police_titre.render("Pierre • Feuille • Ciseaux", True, (240, 235, 255))
        ecran.blit(titre, titre.get_rect(center=(TAILLE_FENETRE[0] // 2, 70)))

        sous_titre = petite_police.render(
            "Choisis ton coup préféré, le reste se charge tout seul !",
            True,
            (220, 210, 255),
        )
        ecran.blit(sous_titre, sous_titre.get_rect(center=(TAILLE_FENETRE[0] // 2, 110)))

        _afficher_scores(ecran, petite_police, scores, zone_scores)

        position_souris = pygame.mouse.get_pos()
        for carte in cartes:
            carte.dessiner(
                ecran,
                police,
                petite_police,
                carte.contient(position_souris),
            )

        messages = [message]
        if dernier_choix:
            messages.insert(0, dernier_choix)
        _afficher_messages(ecran, petite_police, messages, zone_messages)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    lancer_interface()
