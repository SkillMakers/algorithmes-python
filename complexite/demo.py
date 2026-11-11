"""Les exercices de la video, executes : chaque reponse est comptee par le programme.

    python demo.py
"""
import random
import sys

from complexite import (a_un_doublon_ensemble, a_un_doublon_naif, a_un_doublon_tri, dedoublonner_lent,
                        dedoublonner_lent_compte, dedoublonner_rapide, dedoublonner_rapide_compte,
                        deplacements_pop0, fib_boucle, fib_memo, fib_naif, recherche_lineaire, tours_constants,
                        tours_doublement, tours_n_log_n, tours_triangle)


def titre(texte):
    print(f"\n--- {texte}")


def main():
    print(f"Python {sys.version.split()[0]}")

    titre("Recherche lineaire dans [14, 7, 18, 3, 11, 9] : meilleur et pire cas")
    notes = [14, 7, 18, 3, 11, 9]
    for x in (14, 9, 10):
        indice, comparaisons = recherche_lineaire(notes, x)
        print(f"cherche {x:2} -> indice {indice:2}, {comparaisons} comparaison{'s' if comparaisons > 1 else ''}")

    titre("Ex 1 : f(n) = 3n^2 + 5n + 2 est en O(n^2) ? On cherche c et n0 tels que f(n) <= c * n^2")
    for n in (1, 5, 6, 10, 100, 1000):
        f = 3 * n * n + 5 * n + 2
        print(f"n = {n:4} : f(n) = {f:>9}   4n^2 = {4 * n * n:>9}   f(n) <= 4n^2 ? {f <= 4 * n * n}")
    premier = next(n for n in range(1, 100) if all(3 * k * k + 5 * k + 2 <= 4 * k * k for k in range(n, 10_000)))
    print(f"-> c = 4 marche a partir de n0 = {premier} (verifie jusqu'a 10 000)")

    titre("Ex 2 : for i in range(n): for j in range(i)  -> combien de tours ?")
    for n in (10, 100, 1000):
        print(f"n = {n:4} : {tours_triangle(n):>7} tours   n(n-1)/2 = {n * (n - 1) // 2:>7}")

    titre("Ex 3 : i = 1 ; while i < n: i *= 2  -> combien de tours ?")
    for n in (8, 1000, 1_000_000, 1_000_000_000):
        print(f"n = {n:>13,} : {tours_doublement(n):2} tours".replace(",", " "))

    titre("Ex 4 : deux boucles imbriquees ne font pas toujours n^2")
    for n in (1000, 2000):
        print(f"n = {n} : for j in range(5) -> {tours_constants(n):>6} tours   "
              f"while j < n: j *= 2 -> {tours_n_log_n(n):>6} tours")

    titre("Ex 5 : Fibonacci recursif naif, nombre d'appels")
    for n in (10, 20, 25, 30):
        compteur = [0]
        valeur = fib_naif(n, compteur)
        print(f"fib({n:2}) = {valeur:>7,}   {compteur[0]:>9,} appels".replace(",", " "))
    valeur, calcules = fib_memo(30)
    print(f"avec memoire : fib(30) = {valeur}, {calcules} valeurs calculees")
    print(f"avec une boucle : fib(30) = {fib_boucle(30)}, 30 tours")

    titre("Ex 6 : doublons dans 10 000 nombres tous differents (pire cas), operations comptees")
    aleas = random.Random(42)
    t = aleas.sample(range(10_000_000), 10_000)
    unites = {a_un_doublon_naif: "comparaisons", a_un_doublon_tri: "comparaisons", a_un_doublon_ensemble: "tests"}
    for fonction, unite in unites.items():
        trouve, operations = fonction(t)
        print(f"{fonction.__name__:22} : doublon = {trouve}, {operations:>10,} {unite}".replace(",", " "))
    print("(a_un_doublon_tri : plus le tri lui-meme, en n log n ; ensemble : un test d'appartenance au set par element)")

    titre("Ex 7 : dedoublonner en gardant l'ordre")
    t = [3, 1, 3, 2, 1]
    print(f"{t} -> lent : {dedoublonner_lent(t)}   rapide : {dedoublonner_rapide(t)}")
    t = aleas.sample(range(10_000_000), 10_000)
    _, comparaisons = dedoublonner_lent_compte(t)
    _, tests = dedoublonner_rapide_compte(t)
    print(f"10 000 elements distincts : x not in resultat (liste) -> {comparaisons:,} comparaisons cachees"
          f"   x not in vus (set) -> {tests:,} tests".replace(",", " "))
    print(f"vider 10 000 elements avec pop(0) : {deplacements_pop0(10_000):,} cases decalees".replace(",", " "))


if __name__ == "__main__":
    main()
