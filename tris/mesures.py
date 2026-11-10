"""Temps reels des tris sur des listes aleatoires de 1 000 a 1 000 000 de nombres.

Chaque mesure est le meilleur de 3 executions (time.perf_counter), sur une copie de la meme liste
(graine fixe : tout le monde peut rejouer les memes listes). Les tris en n^2 s'arretent a 10 000 :
au-dela, ils prendraient plusieurs minutes.

    python mesures.py
"""
import platform
import random
import sys
import time

from tris import tri_bulles, tri_fusion, tri_insertion, tri_rapide, tri_rapide_naif, tri_selection


def chrono(fonction, liste, repetitions=3):
    meilleur = float("inf")
    for _ in range(repetitions):
        t = liste.copy()
        debut = time.perf_counter()
        fonction(t)
        meilleur = min(meilleur, time.perf_counter() - debut)
    return meilleur


def sorted_(t):
    t.sort()


def format_s(s):
    return f"{s * 1000:9.1f} ms" if s < 1 else f"{s:9.2f} s "


def main():
    print(f"Python {sys.version.split()[0]} · {platform.system()} {platform.release()} · {platform.processor()}")
    print("Meilleur de 3 executions, listes aleatoires (graine 42)\n")
    random.seed(42)
    tailles = [1_000, 10_000, 100_000, 1_000_000]
    listes = {n: [random.randint(0, 1_000_000) for _ in range(n)] for n in tailles}
    tris = [("bulles", tri_bulles, 10_000), ("selection", tri_selection, 10_000),
            ("insertion", tri_insertion, 10_000), ("fusion", tri_fusion, 1_000_000),
            ("rapide (corrige)", tri_rapide, 1_000_000), ("list.sort()", sorted_, 1_000_000)]
    print(f"{'tri':24}" + "".join(f"{n:>13,}".replace(",", " ") for n in tailles))
    for nom, f, maxi in tris:
        ligne = f"{nom:24}"
        for n in tailles:
            ligne += format_s(chrono(f, listes[n])).rjust(13) if n <= maxi else f"{'-':>13}"
        print(ligne, flush=True)

    print("\nListe DEJA triee de 10 000 elements :")
    deja = sorted(listes[10_000])
    for nom, f in [("bulles", tri_bulles), ("insertion", tri_insertion), ("selection", tri_selection)]:
        print(f"  {nom:12} {format_s(chrono(f, deja))}")

    print("\nTri rapide NAIF (pivot = dernier element) :")
    print(f"  liste aleatoire de 10 000 : {format_s(chrono(tri_rapide_naif, listes[10_000]))}")
    print(f"  liste deja triee de   900 : {format_s(chrono(tri_rapide_naif, list(range(900))))}")
    print(f"  liste aleatoire de    900 : {format_s(chrono(tri_rapide_naif, listes[1_000][:900]))}")
    try:
        tri_rapide_naif(list(range(1_000)))
        print("  liste deja triee de 1 000 : sans erreur")
    except RecursionError as err:
        print(f"  liste deja triee de 1 000 : RecursionError: {err}")
    print(f"  limite de recursion de Python : sys.getrecursionlimit() = {sys.getrecursionlimit()}")


if __name__ == "__main__":
    main()
