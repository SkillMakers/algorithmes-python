"""Exercices 6 et 7 : trouver l'erreur. Deux versions FAUSSES, telles qu'on les ecrit souvent, et ce qu'elles font.

    python erreurs.py
"""
import random
import sys

from tris import partition, tri_rapide


def tri_bulles_faux(t):
    """ERREUR : la boucle interieure va jusqu'au dernier indice, et t[i + 1] sort de la liste."""
    n = len(t)
    for fin in range(n - 1, 0, -1):
        for i in range(n):
            if t[i] > t[i + 1]:
                t[i], t[i + 1] = t[i + 1], t[i]


def recherche_dichotomique_fausse(t, x, tours_max=1000):
    """ERREUR : bas = milieu au lieu de milieu + 1. Des que bas == milieu et t[milieu] < x, la zone ne
    retrecit plus et la boucle tourne sans fin : sur le DERNIER element, sur un absent plus grand que tout,
    et sur certains absents au milieu. tours_max sert seulement a arreter la demonstration."""
    bas, haut, tours = 0, len(t) - 1, 0
    while bas <= haut:
        tours += 1
        if tours > tours_max:
            return f"toujours en train de chercher apres {tours_max} tours (bas={bas}, haut={haut})"
        milieu = (bas + haut) // 2
        if t[milieu] == x:
            return milieu
        if t[milieu] < x:
            bas = milieu
        else:
            haut = milieu - 1
    return -1


def tri_rapide_hasard_seul(t, bas=0, haut=None):
    """Pivot au hasard, mais partition classique (plus petits a gauche, le reste a droite) : les doublons
    partent tous du meme cote."""
    if haut is None:
        haut = len(t) - 1
    if bas < haut:
        p = partition(t, bas, haut, random.randint(bas, haut))
        tri_rapide_hasard_seul(t, bas, p - 1)
        tri_rapide_hasard_seul(t, p + 1, haut)


def sort_qui_renvoie_none():
    """ERREUR : list.sort() trie sur place et renvoie None."""
    t = [14, 7, 18, 3, 11, 9]
    t = t.sort()
    return t


def main():
    print(f"Python {sys.version.split()[0]}\n")
    print("Ex 6. tri_bulles_faux([14, 7, 18, 3, 11, 9]) :")
    try:
        tri_bulles_faux([14, 7, 18, 3, 11, 9])
        print("  aucune erreur")
    except IndexError as err:
        print(f"  IndexError: {err}")

    t = [3, 7, 9, 11, 14, 18]
    print(f"\nEx 7. recherche_dichotomique_fausse dans {t} :")
    for x in (11, 3, 18, 12, 20):
        print(f"  cherche {x} -> {recherche_dichotomique_fausse(t, x)}")

    random.seed(42)
    notes = [random.randint(0, 20) for _ in range(20_000)]
    print("\nTri rapide, pivot au hasard, sur 20 000 notes entre 0 et 20 (beaucoup de doublons) :")
    try:
        tri_rapide_hasard_seul(notes.copy())
        print("  partition classique : sans erreur")
    except RecursionError as err:
        print(f"  partition classique : RecursionError: {err}")
    t2 = notes.copy()
    tri_rapide(t2)
    print(f"  partition en trois (tris.tri_rapide) : triee = {t2 == sorted(notes)}")

    print(f"\nt = t.sort() -> t vaut {sort_qui_renvoie_none()}")


if __name__ == "__main__":
    main()
