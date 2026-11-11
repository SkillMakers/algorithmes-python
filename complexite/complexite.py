"""Complexite algorithmique : les fonctions de la video, avec un compteur d'operations.

La plupart des fonctions comptent leurs operations elementaires (comparaisons, tests, tours de
boucle ou appels) et renvoient ce compteur. C'est lui, et pas le chronometre, qui montre la
complexite : il ne depend ni de l'ordinateur ni de la version de Python. Les fonctions sans
compteur (dedoublonner_*, vider_*) ont une version *_compte qui compte le travail cache.

    python demo.py       # les exercices de la video
    python mesures.py    # les temps reels (test du doublement)
"""
from collections import deque
from functools import lru_cache


# --- Recherche lineaire : meilleur cas, pire cas -------------------------------------------

def recherche_lineaire(t, x):
    """Renvoie (indice de x ou -1, nombre de comparaisons)."""
    comparaisons = 0
    for i, v in enumerate(t):
        comparaisons += 1
        if v == x:
            return i, comparaisons
    return -1, comparaisons


# --- Doublons : trois algorithmes, trois complexites ---------------------------------------

def a_un_doublon_naif(t):
    """Compare chaque paire une fois : n(n-1)/2 comparaisons au pire, O(n^2).

    Renvoie (True/False, nombre de comparaisons).
    """
    comparaisons = 0
    n = len(t)
    for i in range(n):
        for j in range(i + 1, n):
            comparaisons += 1
            if t[i] == t[j]:
                return True, comparaisons
    return False, comparaisons


def a_un_doublon_tri(t):
    """Trie une copie (O(n log n)), puis compare les voisins (n - 1 comparaisons).

    Les doublons sont forcement cote a cote une fois la liste triee.
    """
    s = sorted(t)
    comparaisons = 0
    for i in range(len(s) - 1):
        comparaisons += 1
        if s[i] == s[i + 1]:
            return True, comparaisons
    return False, comparaisons


def a_un_doublon_ensemble(t):
    """Un seul passage avec un ensemble (set) : O(n) en moyenne.

    `x in vus` sur un set coute O(1) en moyenne (table de hachage), contre O(n) sur une liste.
    """
    vus = set()
    tests = 0
    for x in t:
        tests += 1
        if x in vus:
            return True, tests
        vus.add(x)
    return False, tests


# --- Compter les tours de boucle ------------------------------------------------------------

def tours_constants(n):
    """for i in range(n): for j in range(5) -> 5n tours : O(n), pas O(n^2)."""
    tours = 0
    for _ in range(n):
        for _ in range(5):
            tours += 1
    return tours


def tours_triangle(n):
    """for i in range(n): for j in range(i) -> 0 + 1 + ... + (n-1) = n(n-1)/2 tours : O(n^2)."""
    tours = 0
    for i in range(n):
        for _ in range(i):
            tours += 1
    return tours


def tours_doublement(n):
    """i = 1, puis i *= 2 tant que i < n -> pour n >= 1, nombre de chiffres de n-1 en binaire : O(log n)."""
    tours = 0
    i = 1
    while i < n:
        i *= 2
        tours += 1
    return tours


def tours_n_log_n(n):
    """Une boucle de n tours qui contient une boucle qui double : O(n log n)."""
    tours = 0
    for _ in range(n):
        j = 1
        while j < n:
            j *= 2
            tours += 1
    return tours


# --- Recursivite : compter les appels -------------------------------------------------------

def fib_naif(n, compteur):
    """Fibonacci recursif sans memoire. compteur est une liste [appels], modifiee sur place.

    Chaque appel en lance deux autres : le nombre d'appels grandit comme 1,618^n (exponentiel).
    """
    compteur[0] += 1
    if n < 2:
        return n
    return fib_naif(n - 1, compteur) + fib_naif(n - 2, compteur)


def fib_memo(n):
    """Fibonacci avec memoire : chaque valeur n'est calculee qu'une fois, O(n) en temps et en memoire.

    Renvoie (valeur, nombre de valeurs calculees).
    Attention : la fonction reste recursive. Vers n = 1000, elle depasse la limite de recursion
    de Python (RecursionError), comme le tri rapide sur une liste triee. fib_boucle n'a pas cette limite.
    """
    @lru_cache(maxsize=None)
    def f(k):
        if k < 2:
            return k
        return f(k - 1) + f(k - 2)
    valeur = f(n)
    return valeur, f.cache_info().currsize


def fib_boucle(n):
    """Fibonacci avec une boucle : n tours, deux variables, O(n) en temps et O(1) en memoire."""
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


# --- Le piege : une boucle simple qui est en n au carre --------------------------------------

def dedoublonner_lent(t):
    """Garde la premiere occurrence de chaque valeur, dans l'ordre.

    Une seule boucle visible, mais `x not in resultat` parcourt la liste resultat a chaque tour :
    O(n^2) au pire (quand il y a peu de doublons).
    """
    resultat = []
    for x in t:
        if x not in resultat:
            resultat.append(x)
    return resultat


def dedoublonner_rapide(t):
    """Meme resultat, meme ordre, mais le test se fait dans un set : O(n) en moyenne."""
    vus = set()
    resultat = []
    for x in t:
        if x not in vus:
            vus.add(x)
            resultat.append(x)
    return resultat


def dedoublonner_lent_compte(t):
    """dedoublonner_lent, en comptant les comparaisons que fait `x not in resultat`.

    Sans doublon, chaque test parcourt tout resultat : 0 + 1 + ... + (n-1) = n(n-1)/2 comparaisons.
    Renvoie (resultat, comparaisons).
    """
    resultat = []
    comparaisons = 0
    for x in t:
        trouve = False
        for y in resultat:
            comparaisons += 1
            if y == x:
                trouve = True
                break
        if not trouve:
            resultat.append(x)
    return resultat, comparaisons


def dedoublonner_rapide_compte(t):
    """dedoublonner_rapide, en comptant les tests d'appartenance au set : n tests.

    Renvoie (resultat, tests).
    """
    vus = set()
    resultat = []
    tests = 0
    for x in t:
        tests += 1
        if x not in vus:
            vus.add(x)
            resultat.append(x)
    return resultat, tests


def deplacements_pop0(n):
    """Nombre de cases decalees pour vider une liste de n elements avec pop(0).

    Chaque pop(0) decale tous les elements restants d'une case : (n-1) + (n-2) + ... + 0 = n(n-1)/2.
    """
    deplacements = 0
    taille = n
    while taille:
        taille -= 1
        deplacements += taille
    return deplacements


def vider_avec_pop0(t):
    """Traite une file avec list.pop(0) : chaque pop(0) decale tout le reste, O(n^2) au total."""
    t = list(t)
    total = 0
    while t:
        total += t.pop(0)
    return total


def vider_avec_deque(t):
    """Meme traitement avec collections.deque.popleft() : O(1) par retrait, O(n) au total."""
    d = deque(t)
    total = 0
    while d:
        total += d.popleft()
    return total
