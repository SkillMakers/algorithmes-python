"""Les exercices de la video, executes : chaque reponse est calculee et comptee par le programme.

    python demo.py
"""
import sys

from recursivite import (aplatir, aplatir_corrige, aplatir_piege, est_palindrome,
                         est_palindrome_sans_return, factorielle, factorielle_boucle, factorielle_trace, hanoi, hanoi_valide,
                         nombre_deplacements_hanoi, profondeur, profondeur_maximale, puissance,
                         puissance_double_appel, puissance_rapide, somme, somme_terminale, somme_tranche)


def titre(texte):
    print(f"\n--- {texte}")


def main():
    print(f"Python {sys.version.split()[0]}")

    titre("Ex 1 : factorielle(4), la descente puis la remontee")
    trace = []
    print(f"factorielle(4) = {factorielle_trace(4, trace)}")
    for ligne in trace:
        print(ligne)
    for n in (4, 10, 20):
        compteur = [0]
        valeur = factorielle(n, compteur)
        print(f"factorielle({n:2}) = {valeur:>26,}   {compteur[0]:2} appels".replace(",", " "))
    print(f"factorielle(20) recursive == boucle : {factorielle(20) == factorielle_boucle(20)}")

    titre("La pile d'appels : jusqu'ou descendre ?")
    print(f"sys.getrecursionlimit() = {sys.getrecursionlimit()}")
    print(f"descendre(n) passe jusqu'a n = {profondeur_maximale()}")
    try:
        factorielle(1000)
        print("factorielle(1000) : passe")
    except RecursionError as erreur:
        print(f"factorielle(1000) -> RecursionError: {erreur}")
    print(f"factorielle_boucle(1000) a {len(str(factorielle_boucle(1000)))} chiffres")

    titre("Ex 2 : somme d'une liste")
    notes = [14, 7, 18, 3, 11, 9]
    compteur = [0]
    print(f"somme({notes}) = {somme(notes, compteur=compteur)}   {compteur[0]} appels")
    copies = [0]
    print(f"somme_tranche({notes}) = {somme_tranche(notes, copies)}   {copies[0]} elements copies")
    for n in (10, 100, 900):
        t = list(range(n))
        copies = [0]
        somme_tranche(t, copies)
        print(f"n = {n:3} : somme_tranche copie {copies[0]:>7,} elements   n(n-1)/2 = {n * (n - 1) // 2:>7,}"
              .replace(",", " "))

    for taille in (900, 1000):
        t = list(range(taille))
        for nom, f in (("somme", somme), ("somme_terminale", somme_terminale)):
            try:
                print(f"{nom}({taille:,} nombres) = {f(t):,}".replace(",", " "))
            except RecursionError as erreur:
                print(f"{nom}({taille:,} nombres) -> RecursionError: {erreur}".replace(",", " "))

    titre("Ex 3 : 2 puissance n, nombre d'appels")
    for n in (10, 100, 900):
        c1, c2 = [0], [0]
        a, b = puissance(2, n, c1), puissance_rapide(2, n, c2)
        print(f"n = {n:3} : puissance {c1[0]:3} appels   puissance_rapide {c2[0]:2} appels   memes resultats : {a == b}")
    c = [0]
    puissance_rapide(2, 1_000_000, c)
    try:
        puissance(2, 1_000_000)
        directe = "passe"
    except RecursionError as erreur:
        directe = f"RecursionError: {erreur}"
    print(f"n = 1 000 000 : puissance_rapide {c[0]} appels   puissance -> {directe}")
    print("l'appel sur n // 2 ecrit deux fois :")
    for n in (10, 100, 900):
        c = [0]
        juste = puissance_double_appel(2, n, c) == 2 ** n
        print(f"n = {n:3} : puissance_double_appel {c[0]:>5,} appels   resultat juste : {juste}".replace(",", " "))

    titre("Ex 4 : palindrome, et la copie sans return")
    for mot in ("a", "ab", "radar", "kayak", "python", "abca"):
        juste = est_palindrome(mot)
        faux = est_palindrome_sans_return(mot)
        print(f"{mot!r:9} : est_palindrome -> {juste!s:5}   sans return -> {faux!s:5}")

    titre("Ex 5 : tours de Hanoi")
    for ligne in hanoi(3):
        print(f"disque {ligne[0]} : {ligne[1]} -> {ligne[2]}")
    for n in (3, 10, 20):
        d = hanoi(n)
        print(f"n = {n:2} : {len(d):>9,} deplacements   2^n - 1 = {2 ** n - 1:>9,}   regle respectee : {hanoi_valide(n, d)}"
              .replace(",", " "))
    print(f"n = 64 : {nombre_deplacements_hanoi(64):,} deplacements".replace(",", " "))
    secondes_par_an = 365.25 * 24 * 3600
    print(f"a un deplacement par seconde : {nombre_deplacements_hanoi(64) / secondes_par_an / 1e9:.0f} milliards d'annees")

    titre("Ex 6 : aplatir une liste imbriquee")
    donnees = [1, [2, [3, 4]], 5, [[[6]]]]
    compteur = [0]
    print(f"aplatir({donnees}) = {aplatir(donnees, compteur)}   {compteur[0]} appels, profondeur {profondeur(donnees)}")

    titre("Ex 7 : le piege de l'argument par defaut")
    print(f"aplatir_piege([1, [2]])   = {aplatir_piege([1, [2]])}")
    print(f"aplatir_piege([3, [4]])   = {aplatir_piege([3, [4]])}")
    print(f"aplatir_piege([5])        = {aplatir_piege([5])}")
    print(f"aplatir_corrige([1, [2]]) = {aplatir_corrige([1, [2]])}")
    print(f"aplatir_corrige([3, [4]]) = {aplatir_corrige([3, [4]])}")
    print(f"aplatir_corrige([5])      = {aplatir_corrige([5])}")
    print(f"valeur par defaut stockee : aplatir_piege.__defaults__ = {aplatir_piege.__defaults__}")



if __name__ == "__main__":
    main()
