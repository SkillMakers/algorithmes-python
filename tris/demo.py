"""Le fil rouge de la video : la meme liste triee par chaque algorithme, puis les exercices corriges.

    python demo.py
"""
import sys

from tris import (nombre_de_tours, recherche_dichotomique, recherche_dichotomique_rec, tri_bulles,
                  tri_fusion, tri_insertion, tri_rapide_naif, tri_selection)

NOTES = [14, 7, 18, 3, 11, 9]


def montrer(nom, fonction, liste):
    t = liste.copy()
    etapes = []
    fonction(t, etapes)
    print(f"--- {nom} : {liste}")
    for k, e in enumerate(etapes, 1):
        print(f"  passage {k} : {e}")
    print(f"  resultat  : {t}")


def main():
    print(f"Python {sys.version.split()[0]}\n")
    montrer("tri a bulles", tri_bulles, NOTES)
    montrer("tri par selection", tri_selection, NOTES)
    montrer("tri par insertion", tri_insertion, NOTES)

    print(f"--- tri fusion : {NOTES}")
    print(f"  moities    : {NOTES[:3]} et {NOTES[3:]}")
    print(f"  triees     : {tri_fusion(NOTES[:3])} et {tri_fusion(NOTES[3:])}")
    print(f"  fusion     : {tri_fusion(NOTES)}")

    t = NOTES.copy()
    tri_rapide_naif(t)
    print(f"--- tri rapide (pivot = dernier) : {NOTES} -> {t}")

    triee = sorted(NOTES)
    print(f"--- recherche dichotomique dans {triee}")
    print(f"  11 -> indice {recherche_dichotomique(triee, 11)} (recursif : {recherche_dichotomique_rec(triee, 11)})")
    print(f"  10 -> indice {recherche_dichotomique(triee, 10)}")

    print("\n=== Exercices ===")
    print("Ex 1. Tri par insertion, liste apres chaque passage :")
    montrer("Ex 1", tri_insertion, [5, 2, 9, 1, 7])

    print("Ex 2. Tri a bulles : combien de passages ?")
    montrer("Ex 2", tri_bulles, [1, 2, 3, 5, 4])

    print("Ex 3. Trier les eleves par note, a note egale garder l'ordre alphabetique :")
    eleves = [("Lea", 14), ("Hugo", 11), ("Ines", 14), ("Adam", 11), ("Sami", 17)]
    par_nom = sorted(eleves)
    par_note = sorted(par_nom, key=lambda e: e[1], reverse=True)
    print(f"  par nom  : {par_nom}")
    print(f"  par note : {par_note}")

    print("Ex 4. Recherche dichotomique dans 1 000 000 de nombres tries : combien de tours au pire ?")
    grand = range(1_000_000)  # un range se lit par indice comme une liste, sans la stocker
    pire = max(nombre_de_tours(grand, x) for x in grand)
    print(f"  au pire {pire} tours sur les 1 000 000 recherches (2^20 = {2 ** 20})")

    print("Ex 5. Tri rapide naif sur une liste deja triee de 2 000 elements :")
    try:
        tri_rapide_naif(list(range(2000)))
        print("  trie sans erreur")
    except RecursionError as err:
        print(f"  RecursionError: {err}")


if __name__ == "__main__":
    main()
