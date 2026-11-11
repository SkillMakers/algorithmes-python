"""Le test du doublement : on double n, et on regarde par combien le temps est multiplie.

x2 -> O(n) · un peu plus de x2 -> O(n log n) · x4 -> O(n^2) · x11 a chaque +5 sur n -> exponentiel (1,618^5).

Chaque temps est le meilleur de 3 series. Une serie repete l'appel jusqu'a durer au moins 0,2 s
(comme timeit.Timer.autorange), et on divise par le nombre d'appels : sans ca, une mesure de
quelques millisecondes est surtout du bruit, et ses rapports ne veulent rien dire. Graine fixe (42).

    python mesures.py          # tout (~20 min : les versions en n^2 sont lentes, c'est le sujet)
    python mesures.py --fib    # Fibonacci seul
"""
import platform
import random
import sys
import time

from complexite import (a_un_doublon_ensemble, a_un_doublon_naif, a_un_doublon_tri, dedoublonner_lent,
                        dedoublonner_rapide, fib_naif, vider_avec_deque, vider_avec_pop0)

DUREE_MINIMALE = 0.2


def chrono(fonction, args, series=3):
    """Meilleur temps d'un appel, sur 3 series d'au moins DUREE_MINIMALE secondes chacune."""
    # Nombre d'appels par serie : on double jusqu'a depasser la duree minimale.
    appels = 1
    while True:
        debut = time.perf_counter()
        for _ in range(appels):
            fonction(*args)
        duree = time.perf_counter() - debut
        if duree >= DUREE_MINIMALE:
            break
        appels *= 2
    meilleur = duree / appels
    for _ in range(series - 1):
        debut = time.perf_counter()
        for _ in range(appels):
            fonction(*args)
        meilleur = min(meilleur, (time.perf_counter() - debut) / appels)
    return meilleur


def format_s(s):
    if s < 0.001:
        return f"{s * 1_000_000:8.0f} µs"
    return f"{s * 1000:8.1f} ms" if s < 1 else f"{s:8.2f} s "


def ligne(nom, fonction, tailles, arguments, etiquette=lambda n: f"{n:>9,}".replace(",", " ")):
    """Une ligne du tableau : le temps pour chaque taille, et le rapport avec la taille d'avant."""
    precedent = None
    morceaux = []
    for n in tailles:
        s = chrono(fonction, arguments(n))
        rapport = f"(x{s / precedent:.1f})" if precedent is not None and precedent > 0 else ""
        morceaux.append(f"{etiquette(n)} : {format_s(s)} {rapport:>7}")
        precedent = s
    print(f"{nom:24}" + " | ".join(morceaux), flush=True)


def distincts(n):
    """n nombres tous differents (pire cas des doublons : il faut tout regarder)."""
    return (random.Random(42).sample(range(100_000_000), n),)


def fibonacci():
    print("Fibonacci recursif naif (exponentiel) : n augmente de 5 a chaque colonne (theorie : x11)")
    ligne("fib_naif", fib_naif, [20, 25, 30, 35], lambda n: (n, [0]), etiquette=lambda n: f"fib({n})")


def main():
    print(f"Python {sys.version.split()[0]} · {platform.system()} {platform.release()} · {platform.processor()}")
    print("Meilleur de 3 series d'au moins 0,2 s, graine 42. "
          "Entre parentheses : le temps divise par celui de la taille d'avant.\n")

    print("Doublons, n nombres tous differents")
    petites = [2_500, 5_000, 10_000, 20_000]
    ligne("a_un_doublon_naif", a_un_doublon_naif, petites, distincts)
    ligne("a_un_doublon_tri", a_un_doublon_tri, petites, distincts)
    ligne("a_un_doublon_ensemble", a_un_doublon_ensemble, petites, distincts)
    grandes = [250_000, 500_000, 1_000_000, 2_000_000]
    ligne("a_un_doublon_tri", a_un_doublon_tri, grandes, distincts)
    ligne("a_un_doublon_ensemble", a_un_doublon_ensemble, grandes, distincts)

    print("\nLe piege : une seule boucle visible")
    moyennes = [10_000, 20_000, 40_000, 80_000]
    ligne("dedoublonner_lent", dedoublonner_lent, moyennes, distincts)
    ligne("dedoublonner_rapide", dedoublonner_rapide, moyennes, distincts)
    files = [50_000, 100_000, 200_000, 400_000]
    ligne("vider_avec_pop0", vider_avec_pop0, files, distincts)
    ligne("vider_avec_deque", vider_avec_deque, files, distincts)

    print()
    fibonacci()


if __name__ == "__main__":
    if "--fib" in sys.argv:
        fibonacci()
    else:
        main()
