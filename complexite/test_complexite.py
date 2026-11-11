"""Tests : chaque compte d'operations cite dans la video est verifie ici.

    python -m unittest -v
"""
import random
import unittest

from complexite import (a_un_doublon_ensemble, a_un_doublon_naif, a_un_doublon_tri, dedoublonner_lent,
                        dedoublonner_lent_compte, dedoublonner_rapide, dedoublonner_rapide_compte,
                        deplacements_pop0, fib_boucle, fib_memo, fib_naif, recherche_lineaire, tours_constants,
                        tours_doublement, tours_n_log_n, tours_triangle, vider_avec_deque, vider_avec_pop0)


def distincts(n):
    """Les memes 10 000 nombres distincts que demo.py (graine 42)."""
    return random.Random(42).sample(range(10_000_000), n)


class TestCompteurs(unittest.TestCase):

    def test_recherche_lineaire_meilleur_et_pire_cas(self):
        """1 comparaison si x est en tete, n si x est en dernier ou absent."""
        # GIVEN
        notes = [14, 7, 18, 3, 11, 9]
        # WHEN / THEN
        self.assertEqual(recherche_lineaire(notes, 14), (0, 1))
        self.assertEqual(recherche_lineaire(notes, 9), (5, 6))
        self.assertEqual(recherche_lineaire(notes, 10), (-1, 6))

    def test_triangle_fait_n_n_moins_1_sur_2_tours(self):
        """for i in range(n): for j in range(i) -> n(n-1)/2 tours, 499 500 pour n = 1 000."""
        # GIVEN
        tailles = (0, 1, 2, 10, 1000)
        for n in tailles:
            with self.subTest(n=n):
                # WHEN / THEN
                self.assertEqual(tours_triangle(n), n * (n - 1) // 2)
        self.assertEqual(tours_triangle(1000), 499_500)

    def test_doublement_fait_log2_tours(self):
        """i *= 2 tant que i < n : 10 tours pour 1 000, 20 pour un million, 30 pour un milliard."""
        # GIVEN
        attendus = {1: 0, 8: 3, 1000: 10, 1_000_000: 20, 1_000_000_000: 30}
        for n, tours in attendus.items():
            with self.subTest(n=n):
                # WHEN / THEN
                self.assertEqual(tours_doublement(n), tours)
        for n in range(1, 5000):
            with self.subTest(n=n):
                self.assertEqual(tours_doublement(n), (n - 1).bit_length())

    def test_boucle_interne_constante_reste_lineaire(self):
        """Doubler n double exactement le nombre de tours : O(n)."""
        # GIVEN
        n = 1000
        # WHEN
        a, b = tours_constants(n), tours_constants(2 * n)
        # THEN
        self.assertEqual((a, b), (5000, 10000))

    def test_boucle_interne_qui_double_fait_n_log_n(self):
        """n tours de log2(n) : 1000 x 10 et 2000 x 11."""
        # GIVEN
        n = 1000
        # WHEN
        a, b = tours_n_log_n(n), tours_n_log_n(2 * n)
        # THEN
        self.assertEqual((a, b), (10_000, 22_000))


class TestFibonacci(unittest.TestCase):

    def test_fibonacci_naif_compte_exponentiel(self):
        """Le nombre d'appels vaut 2 * fib(n + 1) - 1."""
        # GIVEN
        tailles = range(0, 26)
        for n in tailles:
            with self.subTest(n=n):
                compteur = [0]
                # WHEN
                valeur = fib_naif(n, compteur)
                # THEN
                self.assertEqual(valeur, fib_boucle(n))
                self.assertEqual(compteur[0], 2 * fib_boucle(n + 1) - 1)

    def test_fibonacci_naif_de_30_fait_2_692_537_appels(self):
        """Le chiffre de la video : fib(30) = 832 040, en 2 692 537 appels."""
        # GIVEN
        compteur = [0]
        # WHEN
        valeur = fib_naif(30, compteur)
        # THEN
        self.assertEqual((valeur, compteur[0]), (832_040, 2_692_537))

    def test_fibonacci_memo_calcule_chaque_valeur_une_fois(self):
        """Avec memoire : fib(0) a fib(30), soit 31 valeurs calculees."""
        # GIVEN
        n = 30
        # WHEN
        resultat = fib_memo(n)
        # THEN
        self.assertEqual(resultat, (832_040, 31))

    def test_fibonacci_memo_reste_recursif_et_plante_sur_un_grand_n(self):
        """Le cache rend fib lineaire, mais la recursion depasse la limite de Python ; la boucle, non."""
        # GIVEN
        n = 3000
        # WHEN / THEN
        with self.assertRaises(RecursionError):
            fib_memo(n)
        self.assertEqual(len(str(fib_boucle(n))), 627)


class TestDoublons(unittest.TestCase):

    def test_les_trois_algorithmes_donnent_la_meme_reponse(self):
        """Sur 300 listes aleatoires, avec et sans doublon, les trois fonctions sont d'accord."""
        # GIVEN
        aleas = random.Random(1)
        for _ in range(300):
            t = [aleas.randint(0, 60) for _ in range(aleas.randint(0, 40))]
            attendu = len(set(t)) != len(t)
            with self.subTest(t=t):
                # WHEN / THEN
                self.assertEqual(a_un_doublon_naif(t)[0], attendu)
                self.assertEqual(a_un_doublon_tri(t)[0], attendu)
                self.assertEqual(a_un_doublon_ensemble(t)[0], attendu)

    def test_pire_cas_operations_comptees(self):
        """Sans doublon : naif n(n-1)/2 comparaisons, tri n-1 (plus le tri), ensemble n tests."""
        # GIVEN 10 000 nombres tous differents
        t = distincts(10_000)
        # WHEN
        naif, tri, ensemble = a_un_doublon_naif(t), a_un_doublon_tri(t), a_un_doublon_ensemble(t)
        # THEN
        self.assertEqual(naif, (False, 49_995_000))
        self.assertEqual(tri, (False, 9_999))
        self.assertEqual(ensemble, (False, 10_000))


class TestPieges(unittest.TestCase):

    def test_dedoublonner_lent_et_rapide_donnent_le_meme_resultat(self):
        """Meme liste, meme ordre (premiere occurrence gardee)."""
        # GIVEN
        aleas = random.Random(2)
        for _ in range(200):
            t = [aleas.randint(0, 30) for _ in range(aleas.randint(0, 60))]
            with self.subTest(t=t):
                # WHEN / THEN
                self.assertEqual(dedoublonner_lent(t), dedoublonner_rapide(t))
                self.assertEqual(dedoublonner_rapide(t), list(dict.fromkeys(t)))
                self.assertEqual(dedoublonner_lent_compte(t)[0], dedoublonner_lent(t))
                self.assertEqual(dedoublonner_rapide_compte(t)[0], dedoublonner_rapide(t))

    def test_x_not_in_liste_cache_n_carre_comparaisons(self):
        """Une seule boucle visible, mais n(n-1)/2 comparaisons cachees ; le set fait n tests."""
        # GIVEN
        t = distincts(10_000)
        # WHEN
        _, comparaisons = dedoublonner_lent_compte(t)
        _, tests = dedoublonner_rapide_compte(t)
        # THEN
        self.assertEqual(comparaisons, 49_995_000)
        self.assertEqual(tests, 10_000)

    def test_pop0_decale_n_carre_cases(self):
        """Vider n elements avec pop(0) decale (n-1) + ... + 0 = n(n-1)/2 cases."""
        # GIVEN
        tailles = (0, 1, 2, 10, 10_000)
        for n in tailles:
            with self.subTest(n=n):
                # WHEN / THEN
                self.assertEqual(deplacements_pop0(n), n * (n - 1) // 2)

    def test_pop0_et_deque_donnent_le_meme_total(self):
        """La file videe avec pop(0) ou avec deque.popleft() donne la meme somme."""
        # GIVEN
        t = list(range(1000))
        # WHEN / THEN
        self.assertEqual(vider_avec_pop0(t), vider_avec_deque(t))
        self.assertEqual(vider_avec_pop0(t), sum(t))


if __name__ == "__main__":
    unittest.main()
