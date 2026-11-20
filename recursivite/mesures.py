"""Recursif contre boucle : les temps reels, et ce qui se passe quand on releve la limite.

Chaque temps est le meilleur de 3 series. Une serie repete l'appel jusqu'a durer au moins 0,2 s
(comme timeit.Timer.autorange), et on divise par le nombre d'appels.

    python mesures.py
"""
import platform
import subprocess
import sys
import time

from recursivite import factorielle, factorielle_boucle, somme, somme_boucle, somme_tranche

DUREE_MINIMALE = 0.2


def chrono(fonction, args, series=3):
    """Meilleur temps d'un appel, sur 3 series d'au moins DUREE_MINIMALE secondes chacune."""
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
    return f"{s * 1_000_000:8.1f} µs"


# Le script lance dans un processus a part : s'il plante, la mesure continue.
SCRIPT_PILE = """
import sys
sys.setrecursionlimit({limite})
def descendre(n):
    if n == 0:
        return 0
    return 1 + descendre(n - 1)
try:
    print(descendre({n}))
except RecursionError as e:
    print("RecursionError:", e)
"""


def essai_pile(limite, n):
    resultat = subprocess.run([sys.executable, "-c", SCRIPT_PILE.format(limite=limite, n=n)],
                              capture_output=True, text=True)
    sortie = (resultat.stdout.strip() or resultat.stderr.strip().splitlines()[-1:] or [""])
    if isinstance(sortie, list):
        sortie = sortie[0] if sortie else ""
    return resultat.returncode, sortie


def main():
    print(f"Python {sys.version.split()[0]} · {platform.system()} {platform.release()} · {platform.machine()}")
    print("meilleur de 3 series d'au moins 0,2 s\n")

    n = 900
    t = list(range(n))
    print(f"--- Somme de {n} nombres (sous la limite de 1 000 appels)")
    for nom, fonction, args in (("somme recursive (indice)", somme, (t,)),
                                ("somme recursive t[1:]", somme_tranche, (t,)),
                                ("somme avec une boucle", somme_boucle, (t,)),
                                ("sum(t), la fonction de Python", sum, (t,))):
        print(f"{nom:32}{format_s(chrono(fonction, args))}", flush=True)

    print(f"\n--- Factorielle de {n}")
    for nom, fonction in (("factorielle recursive", factorielle), ("factorielle avec une boucle", factorielle_boucle)):
        print(f"{nom:32}{format_s(chrono(fonction, (n,)))}", flush=True)

    print("\n--- Relever la limite : sys.setrecursionlimit(limite), puis descendre(n)")
    for limite, profondeur in ((1_000, 2_000), (100_000, 50_000), (1_000_000, 500_000), (10_000_000, 5_000_000)):
        code, sortie = essai_pile(limite, profondeur)
        print(f"limite {limite:>10,}, n = {profondeur:>9,} : code de sortie {code} · {sortie[:90]}".replace(",", " "),
              flush=True)


if __name__ == "__main__":
    main()
