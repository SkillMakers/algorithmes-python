"""Tests : chaque resultat et chaque compte d'appels cite dans la video est verifie ici.

    python -m unittest -v
"""
import math
import sys
import unittest

from recursivite import (aplatir, aplatir_corrige, aplatir_piege, est_palindrome, est_palindrome_sans_return,
                         factorielle, factorielle_boucle, factorielle_trace, hanoi, hanoi_valide,
                         nombre_deplacements_hanoi, profondeur, profondeur_maximale, puissance, puissance_double_appel,
                         puissance_rapide,
                         somme, somme_boucle, somme_terminale, somme_tranche)


class TestFactorielle(unittest.TestCase):

    def test_factorielle_egale_math_factorial_et_fait_n_plus_1_appels(self):
        """factorielle(n) = n!, avec n + 1 appels (de n jusqu'au cas de base 0)."""
        for n in (0, 1, 4, 10, 20, 500):
            with self.subTest(n=n):
                # GIVEN
                compteur = [0]
                # WHEN
                valeur = factorielle(n, compteur)
                # THEN
                self.assertEqual(valeur, math.factorial(n))
                self.assertEqual(valeur, factorielle_boucle(n))
                self.assertEqual(compteur[0], n + 1)

    def test_trace_descend_puis_remonte(self):
        """La trace de factorielle(4) : 5 appels qui descendent, puis 5 retours qui remontent."""
        # GIVEN
        trace = []
        # WHEN
        valeur = factorielle_trace(4, trace)
        # THEN
        self.assertEqual(valeur, 24)
        self.assertEqual([ligne.strip() for ligne in trace[:5]],
                         [f"factorielle({n}) appelee" for n in (4, 3, 2, 1, 0)])
        self.assertEqual(trace[5].strip(), "factorielle(0) renvoie 1")
        self.assertEqual(trace[-1], "factorielle(4) renvoie 24")


class TestPile(unittest.TestCase):
    """Ces tests fixent eux-memes la limite a 1 000 (valeur par defaut de Python) : sous Jupyter
    ou IPython, elle vaut 3 000, et les erreurs attendues n'arriveraient pas."""

    def setUp(self):
        self.limite_avant = sys.getrecursionlimit()
        sys.setrecursionlimit(1000)

    def tearDown(self):
        sys.setrecursionlimit(self.limite_avant)

    def test_limite_et_recursion_error(self):
        """Limite 1 000 : factorielle(1000) leve RecursionError, la boucle non."""
        # WHEN / THEN
        with self.assertRaises(RecursionError):
            factorielle(1000)
        self.assertEqual(len(str(factorielle_boucle(1000))), 2568)

    def test_profondeur_maximale_un_peu_sous_la_limite(self):
        """Les appels deja en cours (le test lui-meme) comptent : on descend un peu moins de 1 000 fois."""
        # WHEN
        n = profondeur_maximale()
        # THEN
        self.assertTrue(900 < n < 1000, n)

    def test_profondeur_maximale_suit_une_limite_relevee(self):
        """Limite relevee a 5 000 : la recherche ne plafonne plus a une valeur ecrite en dur."""
        # GIVEN
        sys.setrecursionlimit(5000)
        # WHEN
        n = profondeur_maximale()
        # THEN
        self.assertTrue(4900 < n < 5000, n)

    def test_recursion_terminale_bute_sur_la_meme_limite(self):
        """Python ne transforme pas la recursion terminale en boucle."""
        # GIVEN
        t = list(range(1000))
        # WHEN / THEN
        with self.assertRaises(RecursionError):
            somme_terminale(t)
        with self.assertRaises(RecursionError):
            somme(t)
        self.assertEqual(somme_terminale(list(range(900))), sum(range(900)))


class TestSomme(unittest.TestCase):

    def test_trois_versions_meme_resultat(self):
        """somme, somme_tranche et la boucle donnent 62 sur les six notes."""
        # GIVEN
        notes = [14, 7, 18, 3, 11, 9]
        compteur = [0]
        # WHEN / THEN
        self.assertEqual(somme(notes, compteur=compteur), 62)
        self.assertEqual(compteur[0], 7)
        self.assertEqual(somme_tranche(notes), 62)
        self.assertEqual(somme_boucle(notes), 62)
        self.assertEqual(somme([]), 0)

    def test_tranche_copie_n_n_moins_1_sur_2_elements(self):
        """t[1:] a chaque appel : (n-1) + (n-2) + ... + 0 = n(n-1)/2 elements copies, 404 550 pour 900."""
        for n in (0, 1, 6, 100, 900):
            with self.subTest(n=n):
                # GIVEN
                copies = [0]
                # WHEN
                somme_tranche(list(range(n)), copies)
                # THEN
                self.assertEqual(copies[0], n * (n - 1) // 2)


class TestPuissance(unittest.TestCase):

    def test_puissance_rapide_juste_et_logarithmique(self):
        """Memes resultats ; n + 1 appels contre bit_length(n) + 1 (5, 8, 11 pour 10, 100, 900)."""
        attendus = {10: 5, 100: 8, 900: 11, 1_000_000: 21}
        for n, appels in attendus.items():
            with self.subTest(n=n):
                # GIVEN
                c = [0]
                # WHEN
                valeur = puissance_rapide(2, n, c)
                # THEN
                self.assertEqual(valeur, 2 ** n)
                self.assertEqual(c[0], appels)
                self.assertEqual(c[0], n.bit_length() + 1)
        c = [0]
        self.assertEqual(puissance(3, 900, c), 3 ** 900)
        self.assertEqual(c[0], 901)

    def test_double_appel_juste_mais_lineaire(self):
        """L'appel sur n // 2 ecrit deux fois : 31, 255, 2 047 appels pour 10, 100, 900."""
        for n, appels in {10: 31, 100: 255, 900: 2047}.items():
            with self.subTest(n=n):
                # GIVEN
                c = [0]
                # WHEN
                valeur = puissance_double_appel(2, n, c)
                # THEN
                self.assertEqual(valeur, 2 ** n)
                self.assertEqual(c[0], appels)

    def test_n_negatif_ou_decimal_refuse_avec_un_message_clair(self):
        """Sans cette verification, n ne toucherait jamais le cas de base 0 : erreur de recursion."""
        for fonction, args in ((factorielle, (-1,)), (factorielle, (2.5,)), (puissance, (2, -1)),
                               (puissance_rapide, (2, -1)), (puissance_double_appel, (2, -1))):
            with self.subTest(fonction=fonction.__name__, args=args):
                # WHEN / THEN
                with self.assertRaises(ValueError):
                    fonction(*args)


class TestPalindrome(unittest.TestCase):

    def test_palindrome(self):
        # GIVEN
        cas = {"": True, "a": True, "ab": False, "radar": True, "kayak": True, "python": False, "abba": True}
        for mot, attendu in cas.items():
            with self.subTest(mot=mot):
                # WHEN / THEN
                self.assertIs(est_palindrome(mot), attendu)

    def test_sans_return_renvoie_none_sans_erreur(self):
        """Juste sur 1 lettre et sur un faux palindrome, None (donc faux) sur radar et kayak."""
        # WHEN / THEN
        self.assertIs(est_palindrome_sans_return("a"), True)
        self.assertIs(est_palindrome_sans_return("ab"), False)
        self.assertIsNone(est_palindrome_sans_return("radar"))
        self.assertIsNone(est_palindrome_sans_return("kayak"))
        self.assertIsNone(est_palindrome_sans_return("abca"))
        self.assertFalse(bool(est_palindrome_sans_return("radar")))


class TestHanoi(unittest.TestCase):

    def test_deux_puissance_n_moins_un_deplacements_valides(self):
        """2^n - 1 deplacements, et la regle respectee a chaque deplacement (rejoue)."""
        for n in (1, 2, 3, 10, 20):
            with self.subTest(n=n):
                # WHEN
                d = hanoi(n)
                # THEN
                self.assertEqual(len(d), 2 ** n - 1)
                self.assertTrue(hanoi_valide(n, d))

    def test_trois_disques(self):
        # WHEN / THEN
        self.assertEqual(hanoi(3), [(1, "A", "C"), (2, "A", "B"), (1, "C", "B"), (3, "A", "C"),
                                    (1, "B", "A"), (2, "B", "C"), (1, "A", "C")])

    def test_soixante_quatre_disques(self):
        """18 446 744 073 709 551 615 deplacements, environ 585 milliards d'annees a un par seconde."""
        # WHEN
        d = nombre_deplacements_hanoi(64)
        # THEN
        self.assertEqual(d, 2 ** 64 - 1)
        self.assertEqual(round(d / (365.25 * 24 * 3600) / 1e9), 585)

    def test_validateur_refuse_un_grand_disque_sur_un_petit(self):
        # GIVEN
        triche = [(1, "A", "B"), (2, "A", "B")]
        # WHEN / THEN
        self.assertFalse(hanoi_valide(2, triche))

    def test_autres_noms_de_piquets(self):
        # GIVEN
        d = hanoi(4, "X", "Y", "Z")
        # WHEN / THEN
        self.assertTrue(hanoi_valide(4, d, "X", "Y", "Z"))
        self.assertTrue(hanoi_valide(2, hanoi(2, "A", "B", "C"), "A", "B", "C"))


class TestAplatir(unittest.TestCase):

    def test_aplatir(self):
        # GIVEN
        donnees = [1, [2, [3, 4]], 5, [[[6]]]]
        compteur = [0]
        # WHEN
        resultat = aplatir(donnees, compteur)
        # THEN
        self.assertEqual(resultat, [1, 2, 3, 4, 5, 6])
        self.assertEqual(compteur[0], 6)
        self.assertEqual(profondeur(donnees), 4)
        self.assertEqual(aplatir([]), [])

    def test_piege_argument_par_defaut_accumule(self):
        """Le 1er appel est juste, les suivants repartent de la liste du precedent."""
        # GIVEN : la fonction garde sa liste d'un appel a l'autre, on la vide pour un test isole
        aplatir_piege.__defaults__[0].clear()
        # WHEN
        premier = list(aplatir_piege([1, [2]]))
        deuxieme = aplatir_piege([3, [4]])
        # THEN
        self.assertEqual(premier, [1, 2])
        self.assertEqual(deuxieme, [1, 2, 3, 4])
        self.assertIs(deuxieme, aplatir_piege.__defaults__[0])

    def test_corrige_independant_d_un_appel_a_l_autre(self):
        # WHEN / THEN
        self.assertEqual(aplatir_corrige([1, [2]]), [1, 2])
        self.assertEqual(aplatir_corrige([3, [4]]), [3, 4])
        self.assertEqual(aplatir_corrige([5]), [5])


if __name__ == "__main__":
    unittest.main()
