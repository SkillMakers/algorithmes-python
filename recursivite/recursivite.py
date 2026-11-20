"""Recursivite en Python : les fonctions de la video, avec un compteur d'appels.

Chaque fonction recursive peut recevoir une liste `compteur` d'un element ; elle y ajoute 1 a
chaque appel. C'est ce compteur, et pas le chronometre, qui montre combien de fois la fonction
s'appelle : il ne depend ni de l'ordinateur ni de la version de Python.

    python demo.py       # les exercices de la video
    python mesures.py    # les temps reels (recursif contre boucle)
"""
import sys


def verifier_entier_positif(n):
    """Le cas de base est n == 0 : un n negatif ou decimal ne l'atteindrait jamais, et la fonction
    descendrait jusqu'a l'erreur de recursion. On refuse donc ces valeurs avec un message clair."""
    if not isinstance(n, int) or n < 0:
        raise ValueError(f"n doit etre un entier positif ou nul, pas {n!r}")


def compter(compteur):
    if compteur is not None:
        compteur[0] += 1


# --- Ex 1 : factorielle ---------------------------------------------------------------------

def factorielle(n, compteur=None):
    """n! = n * (n-1)!, et 0! = 1. Un appel par valeur de n a 0 : n + 1 appels."""
    verifier_entier_positif(n)
    compter(compteur)
    if n == 0:                       # cas de base : il arrete la recursion
        return 1
    return n * factorielle(n - 1, compteur)


def factorielle_trace(n, trace, niveau=0):
    """La meme factorielle, qui note la descente et la remontee dans `trace` (une ligne par etape)."""
    trace.append(f"{'  ' * niveau}factorielle({n}) appelee")
    resultat = 1 if n == 0 else n * factorielle_trace(n - 1, trace, niveau + 1)
    trace.append(f"{'  ' * niveau}factorielle({n}) renvoie {resultat}")
    return resultat


def factorielle_boucle(n):
    resultat = 1
    for k in range(2, n + 1):
        resultat *= k
    return resultat


# --- Ex 2 : somme d'une liste ---------------------------------------------------------------

def somme(t, i=0, *, compteur=None):
    """Somme de t[i:], sans copier la liste : on avance un indice. n + 1 appels."""
    compter(compteur)
    if i == len(t):                  # liste vide : la somme vaut 0
        return 0
    return t[i] + somme(t, i + 1, compteur=compteur)


def somme_tranche(t, copies=None):
    """La version des cours : somme(t[1:]). Correcte, mais t[1:] COPIE la liste a chaque appel.

    `copies` (liste d'un element) compte les elements copies : (n-1) + (n-2) + ... = n(n-1)/2.
    """
    if not t:
        return 0
    reste = t[1:]
    if copies is not None:
        copies[0] += len(reste)
    return t[0] + somme_tranche(reste, copies)


def somme_terminale(t, i=0, acc=0):
    """Recursion terminale : l'appel recursif est la toute derniere chose faite.

    Certains langages la transforment en boucle. Python non : chaque appel garde son etage dans
    la pile, et on bute sur la meme limite que la version ordinaire.
    """
    if i == len(t):
        return acc
    return somme_terminale(t, i + 1, acc + t[i])


def somme_boucle(t):
    total = 0
    for x in t:
        total += x
    return total


# --- Ex 3 : puissance -----------------------------------------------------------------------

def puissance(x, n, compteur=None):
    """x^n = x * x^(n-1) : n + 1 appels."""
    verifier_entier_positif(n)
    compter(compteur)
    if n == 0:
        return 1
    return x * puissance(x, n - 1, compteur)


def puissance_rapide(x, n, compteur=None):
    """x^n = (x^(n//2))^2, fois x si n est impair : n est divise par 2 a chaque appel.

    Environ log2(n) appels. Le resultat de l'appel est garde dans une variable : appeler deux
    fois puissance_rapide(x, n // 2) referait tout le travail, et on retomberait a n appels.
    """
    verifier_entier_positif(n)
    compter(compteur)
    if n == 0:
        return 1
    moitie = puissance_rapide(x, n // 2, compteur)
    if n % 2 == 0:
        return moitie * moitie
    return moitie * moitie * x


def puissance_double_appel(x, n, compteur=None):
    """L'erreur a ne pas faire : l'appel sur n // 2 ecrit deux fois. Juste, mais chaque appel en
    lance deux : environ 2n appels au lieu de log2(n)."""
    verifier_entier_positif(n)
    compter(compteur)
    if n == 0:
        return 1
    carre = (puissance_double_appel(x, n // 2, compteur)
             * puissance_double_appel(x, n // 2, compteur))
    return carre if n % 2 == 0 else carre * x


# --- Ex 4 : palindrome, et l'erreur du return oublie ----------------------------------------

def est_palindrome(s):
    """Un mot est un palindrome si sa premiere et sa derniere lettre sont egales, et si le
    milieu est un palindrome. Un mot de 0 ou 1 lettre en est un."""
    if len(s) <= 1:
        return True
    if s[0] != s[-1]:
        return False
    return est_palindrome(s[1:-1])


def est_palindrome_sans_return(s):
    """LA COPIE A CORRIGER : le dernier appel n'a pas de return.

    La valeur de l'appel recursif est calculee, puis jetee ; la fonction arrive a sa fin et
    renvoie None. Aucune erreur : None est simplement faux dans un if.
    """
    if len(s) <= 1:
        return True
    if s[0] != s[-1]:
        return False
    est_palindrome_sans_return(s[1:-1])


# --- Ex 5 : tours de Hanoi ------------------------------------------------------------------

def hanoi(n, depart="A", arrivee="C", intermediaire="B", deplacements=None):
    """Deplace n disques de depart vers arrivee. Renvoie la liste des deplacements.

    Pour n disques : n-1 disques sur l'intermediaire, le plus grand sur l'arrivee, puis les
    n-1 disques par-dessus. Nombre de deplacements : 2^n - 1.
    """
    if deplacements is None:
        deplacements = []
    if n == 0:
        return deplacements
    hanoi(n - 1, depart, intermediaire, arrivee, deplacements)
    deplacements.append((n, depart, arrivee))
    hanoi(n - 1, intermediaire, arrivee, depart, deplacements)
    return deplacements


def nombre_deplacements_hanoi(n):
    """Meme recursion, sans stocker les deplacements : d(n) = 2 d(n-1) + 1."""
    if n == 0:
        return 0
    return 2 * nombre_deplacements_hanoi(n - 1) + 1


def hanoi_valide(n, deplacements, depart="A", arrivee="C", intermediaire="B"):
    """Rejoue les deplacements et verifie la regle : jamais un disque sur un plus petit.
    Les noms des piquets sont ceux passes a hanoi()."""
    tours = {depart: list(range(n, 0, -1)), intermediaire: [], arrivee: []}
    for disque, de, vers in deplacements:
        if de not in tours or vers not in tours or not tours[de] or tours[de][-1] != disque:
            return False
        if tours[vers] and tours[vers][-1] < disque:
            return False
        tours[vers].append(tours[de].pop())
    return tours[arrivee] == list(range(n, 0, -1))


# --- Ex 6 : aplatir une liste imbriquee -----------------------------------------------------

def aplatir(liste, compteur=None):
    """[1, [2, [3, 4]], 5] -> [1, 2, 3, 4, 5], quelle que soit la profondeur.

    Un appel par liste rencontree. La structure est elle-meme recursive (une liste peut contenir
    des listes) : c'est le cas ou la recursivite est le bon outil.
    """
    compter(compteur)
    resultat = []
    for element in liste:
        if isinstance(element, list):
            resultat.extend(aplatir(element, compteur))
        else:
            resultat.append(element)
    return resultat


def profondeur(liste):
    """Nombre de niveaux de listes : [1, 2] -> 1, [1, [2]] -> 2, [] -> 1."""
    return 1 + max((profondeur(e) for e in liste if isinstance(e, list)), default=0)


# --- Ex 7 : le piege, l'argument par defaut mutable -----------------------------------------

def aplatir_piege(liste, resultat=[]):
    """LA COPIE A CORRIGER : resultat=[] est cree UNE SEULE FOIS, a la definition de la fonction.

    Le premier appel est juste. Le deuxieme repart de la liste laissee par le premier.
    """
    for element in liste:
        if isinstance(element, list):
            aplatir_piege(element, resultat)
        else:
            resultat.append(element)
    return resultat


def aplatir_corrige(liste, resultat=None):
    """La correction : None par defaut, et une nouvelle liste creee a chaque appel de premier niveau."""
    if resultat is None:
        resultat = []
    for element in liste:
        if isinstance(element, list):
            aplatir_corrige(element, resultat)
        else:
            resultat.append(element)
    return resultat


# --- La pile d'appels : jusqu'ou peut-on descendre ? -----------------------------------------

def descendre(n):
    """Fonction minimale : s'appelle n fois. Sert a trouver la profondeur maximale."""
    if n == 0:
        return 0
    return 1 + descendre(n - 1)


def profondeur_maximale():
    """Le plus grand n tel que descendre(n) passe, avec la limite actuelle de Python.

    descendre(n) fait n + 1 appels. Le resultat est un peu sous la limite : les fonctions deja en
    cours (celle qui appelle, le programme principal) occupent aussi des etages."""
    bas, haut = 0, sys.getrecursionlimit()
    while bas < haut:
        milieu = (bas + haut + 1) // 2
        try:
            descendre(milieu)
            bas = milieu
        except RecursionError:
            haut = milieu - 1
    return bas
