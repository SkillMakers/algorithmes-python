"""Tests des tris et de la recherche dichotomique.

    python -m unittest -v
"""
import random
import unittest

from erreurs import recherche_dichotomique_fausse, tri_bulles_faux, tri_rapide_hasard_seul
from tris import (fusionner, recherche_dichotomique, recherche_dichotomique_rec, tri_bulles, tri_fusion,
                  tri_insertion, tri_rapide, tri_rapide_naif, tri_selection)

SUR_PLACE = [tri_bulles, tri_selection, tri_insertion, tri_rapide, tri_rapide_naif]


class TestTris(unittest.TestCase):

    def test_chaque_tri_donne_le_meme_resultat_que_sorted(self):
        """Sur 200 listes aleatoires (vides, doublons, negatifs), chaque tri donne sorted()."""
        # GIVEN des listes aleatoires de 0 a 50 elements
        aleas = random.Random(1)
        listes = [[aleas.randint(-20, 20) for _ in range(aleas.randint(0, 50))] for _ in range(200)]
        for liste in listes:
            for tri in SUR_PLACE:
                with self.subTest(tri=tri.__name__, liste=liste):
                    t = liste.copy()
                    # WHEN
                    tri(t)
                    # THEN
                    self.assertEqual(t, sorted(liste))
            with self.subTest(tri="tri_fusion", liste=liste):
                # WHEN / THEN
                self.assertEqual(tri_fusion(liste), sorted(liste))

    def test_tri_fusion_ne_modifie_pas_la_liste_de_depart(self):
        """Le tri fusion renvoie une nouvelle liste."""
        # GIVEN
        notes = [14, 7, 18, 3, 11, 9]
        # WHEN
        triee = tri_fusion(notes)
        # THEN
        self.assertEqual(notes, [14, 7, 18, 3, 11, 9])
        self.assertEqual(triee, [3, 7, 9, 11, 14, 18])

    def test_fusion_stable_a_egalite_prend_a_gauche(self):
        """A egalite, fusionner prend d'abord l'element de gauche (tri stable)."""
        # GIVEN deux listes triees qui contiennent des valeurs egales mais distinctes (float et int)
        gauche, droite = [1, 2.0], [2, 3]
        # WHEN
        resultat = fusionner(gauche, droite)
        # THEN le 2.0 de gauche passe avant le 2 de droite
        self.assertEqual(resultat, [1, 2.0, 2, 3])
        self.assertIsInstance(resultat[1], float)

    def test_bulles_s_arrete_quand_aucun_echange(self):
        """Sur une liste presque triee, le tri a bulles s'arrete apres 2 passages."""
        # GIVEN
        t, etapes = [1, 2, 3, 5, 4], []
        # WHEN
        tri_bulles(t, etapes)
        # THEN
        self.assertEqual(len(etapes), 2)
        self.assertEqual(t, [1, 2, 3, 4, 5])

    def test_insertion_etapes_de_l_exercice(self):
        """Les etapes de l'exercice 1, telles qu'elles se font a la main."""
        # GIVEN
        t, etapes = [5, 2, 9, 1, 7], []
        # WHEN
        tri_insertion(t, etapes)
        # THEN
        self.assertEqual(etapes, [[2, 5, 9, 1, 7], [2, 5, 9, 1, 7], [1, 2, 5, 9, 7], [1, 2, 5, 7, 9]])

    def test_tri_rapide_naif_plante_sur_une_liste_deja_triee(self):
        """Le piege : pivot = dernier element, liste deja triee de 2 000 elements -> RecursionError."""
        # GIVEN
        deja_triee = list(range(2000))
        # WHEN / THEN
        with self.assertRaises(RecursionError):
            tri_rapide_naif(deja_triee)

    def test_tri_rapide_corrige_passe_sur_des_doublons(self):
        """Pivot au hasard + partition en trois : 2 000 valeurs identiques et 20 000 notes sur vingt passent."""
        # GIVEN
        aleas = random.Random(42)
        identiques = [7] * 2000
        notes = [aleas.randint(0, 20) for _ in range(20_000)]
        attendu = sorted(notes)
        # WHEN
        tri_rapide(identiques)
        tri_rapide(notes)
        # THEN
        self.assertEqual(identiques, [7] * 2000)
        self.assertEqual(notes, attendu)

    def test_tri_rapide_pivot_au_hasard_passe_sur_une_liste_deja_triee(self):
        """Avec un pivot tire au hasard, la meme liste se trie sans erreur."""
        # GIVEN
        t = list(range(2000))
        # WHEN
        tri_rapide(t)
        # THEN
        self.assertEqual(t, list(range(2000)))


class TestRechercheDichotomique(unittest.TestCase):

    def test_trouve_chaque_element_et_rejette_les_absents(self):
        """Iteratif et recursif : chaque element est trouve a son indice, les absents donnent -1."""
        # GIVEN
        t = [3, 7, 9, 11, 14, 18]
        for recherche in (recherche_dichotomique, recherche_dichotomique_rec):
            for i, x in enumerate(t):
                with self.subTest(recherche=recherche.__name__, x=x):
                    # WHEN / THEN
                    self.assertEqual(recherche(t, x), i)
            for absent in (0, 10, 20):
                with self.subTest(recherche=recherche.__name__, absent=absent):
                    # WHEN / THEN
                    self.assertEqual(recherche(t, absent), -1)

    def test_liste_vide(self):
        """Dans une liste vide, rien n'est trouve."""
        # GIVEN
        vide = []
        # WHEN / THEN
        self.assertEqual(recherche_dichotomique(vide, 5), -1)
        self.assertEqual(recherche_dichotomique_rec(vide, 5), -1)


class TestErreursDesExercices(unittest.TestCase):
    """Exercices 6 et 7 : les versions fausses font bien ce que la video montre."""

    def test_bulles_avec_range_n_sort_de_la_liste(self):
        """for i in range(n) : t[i + 1] depasse la fin de la liste -> IndexError."""
        # GIVEN
        notes = [14, 7, 18, 3, 11, 9]
        # WHEN / THEN
        with self.assertRaises(IndexError):
            tri_bulles_faux(notes)

    def test_dichotomie_avec_bas_egal_milieu_ne_s_arrete_pas(self):
        """bas = milieu : trouve 11 et 3, mais tourne sans fin sur le dernier element (18), sur un absent
        au milieu (12) et sur un absent plus grand que tout (20)."""
        # GIVEN
        t = [3, 7, 9, 11, 14, 18]
        # WHEN
        trouves = [recherche_dichotomique_fausse(t, x) for x in (11, 3)]
        bloques = [recherche_dichotomique_fausse(t, x, tours_max=1000) for x in (18, 12, 20)]
        # THEN
        self.assertEqual(trouves, [3, 0])
        for resultat in bloques:
            self.assertIn("toujours en train de chercher", resultat)

    def test_pivot_au_hasard_seul_plante_sur_des_doublons(self):
        """Pivot au hasard mais partition classique : 2 000 valeurs identiques -> RecursionError."""
        # GIVEN
        identiques = [7] * 2000
        # WHEN / THEN
        with self.assertRaises(RecursionError):
            tri_rapide_hasard_seul(identiques)


if __name__ == "__main__":
    unittest.main()
