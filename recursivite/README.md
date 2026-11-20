# Récursivité en Python : cours et exercices corrigés

Vidéo : à venir (playlist [Python](https://www.youtube.com/playlist?list=PLe6-9MbhEih4iKO3s9BT_tp4VyfGJvDiB))

Chaque appel est compté par le programme, la pile d'appels est poussée jusqu'à sa limite, et les deux erreurs
silencieuses de la vidéo sont exécutées. Sept exercices corrigés.

| Fichier | Contenu |
|---|---|
| [`recursivite.py`](recursivite.py) | les fonctions de la vidéo, avec un compteur d'appels |
| [`demo.py`](demo.py) | les exercices 1 à 7, la pile d'appels et sa limite |
| [`mesures.py`](mesures.py) | récursif contre boucle (temps réels), et la limite relevée jusqu'à 10 millions |
| [`test_recursivite.py`](test_recursivite.py) | 21 tests (`unittest`) |

```
python demo.py
python mesures.py
python -m unittest -v
```

Testé avec Python 3.15.1 et 3.11.9. Les temps de `preuves/mesures.txt` ont été mesurés sur un portable Windows 11
(meilleur de 3 séries d'au moins 0,2 s) : ils changent d'une machine et d'une exécution à l'autre, l'ordre de grandeur
reste le même.

Les exercices :
1. factorielle, avec la trace de la descente et de la remontée ;
2. somme d'une liste (avec un indice, et avec la tranche `t[1:]`, qui copie n(n-1)/2 éléments) ;
3. puissance, et puissance rapide en log n appels ;
4. palindrome, et la copie sans `return` qui renvoie `None` sans erreur ;
5. tours de Hanoï : 2^n - 1 déplacements, chacun rejoué et vérifié ;
6. aplatir une liste imbriquée ;
7. le piège : `resultat=[]` comme valeur par défaut, partagée entre les appels.

Ce qui se passe quand on relève la limite avec `sys.setrecursionlimit` : depuis Python 3.11, la plupart des appels
Python ne consomment plus la pile du C, et `descendre(5 000 000)` passe avec une limite à 10 millions
(`preuves/mesures.txt`, `preuves/mesures-3.11.txt`). La documentation prévient quand même qu'une limite trop haute
peut faire planter l'interpréteur.
