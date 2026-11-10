"""Les algorithmes de tri du cours, et la recherche dichotomique.

Les trois tris simples (bulles, selection, insertion) trient la liste sur place et ne renvoient rien,
comme list.sort(). Le parametre facultatif `etapes` recoit une copie de la liste apres chaque passage :
c'est ce qui sert a verifier un exercice fait a la main.

Le tri fusion renvoie une nouvelle liste. Le tri rapide trie sur place.
"""
import random


def tri_bulles(t, etapes=None):
    """Compare les voisins et les echange s'ils sont dans le desordre ; le plus grand remonte a la fin."""
    n = len(t)
    for fin in range(n - 1, 0, -1):
        echange = False
        for i in range(fin):
            if t[i] > t[i + 1]:
                t[i], t[i + 1] = t[i + 1], t[i]
                echange = True
        if etapes is not None:
            etapes.append(t.copy())
        # Aucun echange pendant tout un passage : la liste est deja triee, on s'arrete
        if not echange:
            break


def tri_selection(t, etapes=None):
    """Cherche le plus petit de la partie non triee et le place au debut."""
    n = len(t)
    for debut in range(n - 1):
        mini = debut
        for i in range(debut + 1, n):
            if t[i] < t[mini]:
                mini = i
        t[debut], t[mini] = t[mini], t[debut]
        if etapes is not None:
            etapes.append(t.copy())


def tri_insertion(t, etapes=None):
    """Prend chaque element et le glisse a sa place dans la partie deja triee, a gauche."""
    for i in range(1, len(t)):
        cle = t[i]
        j = i - 1
        while j >= 0 and t[j] > cle:
            t[j + 1] = t[j]
            j -= 1
        t[j + 1] = cle
        if etapes is not None:
            etapes.append(t.copy())


def fusionner(gauche, droite):
    """Fusionne deux listes deja triees en une seule liste triee."""
    resultat = []
    i = j = 0
    while i < len(gauche) and j < len(droite):
        # <= et non < : a egalite on prend a gauche d'abord, le tri reste stable
        if gauche[i] <= droite[j]:
            resultat.append(gauche[i])
            i += 1
        else:
            resultat.append(droite[j])
            j += 1
    resultat.extend(gauche[i:])
    resultat.extend(droite[j:])
    return resultat


def tri_fusion(t):
    """Coupe en deux, trie chaque moitie (recursion), puis fusionne. Renvoie une nouvelle liste."""
    if len(t) <= 1:
        return t.copy()
    milieu = len(t) // 2
    return fusionner(tri_fusion(t[:milieu]), tri_fusion(t[milieu:]))


def partition(t, bas, haut, pivot_index):
    """Place le pivot a sa position definitive : les plus petits a gauche, les autres a droite."""
    t[pivot_index], t[haut] = t[haut], t[pivot_index]
    pivot = t[haut]
    p = bas
    for i in range(bas, haut):
        if t[i] < pivot:
            t[i], t[p] = t[p], t[i]
            p += 1
    t[p], t[haut] = t[haut], t[p]
    return p


def tri_rapide_naif(t, bas=0, haut=None):
    """Tri rapide avec le DERNIER element comme pivot, la version des cours.

    Piege : sur une liste deja triee, chaque partition ne retire qu'un element. La recursion descend
    alors aussi profond que la liste est longue, et Python s'arrete (RecursionError) vers 1 000 elements :
    la limite de recursion par defaut est 1 000 appels, ceux deja en cours compris (le seuil exact baisse
    un peu sous unittest, IDLE ou Jupyter).
    """
    if haut is None:
        haut = len(t) - 1
    if bas < haut:
        p = partition(t, bas, haut, haut)
        tri_rapide_naif(t, bas, p - 1)
        tri_rapide_naif(t, p + 1, haut)


def partition3(t, bas, haut, pivot_index):
    """Partition en trois : plus petits | egaux au pivot | plus grands. Renvoie les bornes de la zone
    des egaux. Sans elle, une liste pleine de doublons (des notes sur vingt) retombe dans le piege."""
    pivot = t[pivot_index]
    lt, i, gt = bas, bas, haut
    while i <= gt:
        if t[i] < pivot:
            t[lt], t[i] = t[i], t[lt]
            lt += 1
            i += 1
        elif t[i] > pivot:
            t[i], t[gt] = t[gt], t[i]
            gt -= 1
        else:
            i += 1
    return lt, gt


def tri_rapide(t, bas=0, haut=None):
    """Tri rapide corrige : pivot tire au hasard (plus de piege sur une liste deja triee) ET les elements
    egaux au pivot regroupes au milieu, qu'on ne trie plus (plus de piege sur une liste de doublons)."""
    if haut is None:
        haut = len(t) - 1
    if bas < haut:
        lt, gt = partition3(t, bas, haut, random.randint(bas, haut))
        tri_rapide(t, bas, lt - 1)
        tri_rapide(t, gt + 1, haut)


def recherche_dichotomique(t, x):
    """Cherche x dans la liste TRIEE t. Renvoie un indice ou se trouve x, ou -1. Chaque tour divise la zone
    par deux. Avec des doublons, ce n'est pas forcement le premier (pour le premier : bisect.bisect_left)."""
    bas, haut = 0, len(t) - 1
    while bas <= haut:
        milieu = (bas + haut) // 2
        if t[milieu] == x:
            return milieu
        if t[milieu] < x:
            bas = milieu + 1
        else:
            haut = milieu - 1
    return -1


def recherche_dichotomique_rec(t, x, bas=0, haut=None):
    """La meme recherche, en recursif."""
    if haut is None:
        haut = len(t) - 1
    if bas > haut:
        return -1
    milieu = (bas + haut) // 2
    if t[milieu] == x:
        return milieu
    if t[milieu] < x:
        return recherche_dichotomique_rec(t, x, milieu + 1, haut)
    return recherche_dichotomique_rec(t, x, bas, milieu - 1)


def nombre_de_tours(t, x):
    """Comme recherche_dichotomique, mais renvoie le nombre de tours de boucle (pour l'exercice)."""
    bas, haut, tours = 0, len(t) - 1, 0
    while bas <= haut:
        tours += 1
        milieu = (bas + haut) // 2
        if t[milieu] == x:
            return tours
        if t[milieu] < x:
            bas = milieu + 1
        else:
            haut = milieu - 1
    return tours
