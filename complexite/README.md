# Complexité algorithmique en Python : cours et exercices corrigés

Vidéo : https://youtu.be/7tY4PK9ceSc

La complexité calculée sur le code, comptée par le programme, puis vérifiée au chronomètre avec le test du
doublement. Sept exercices corrigés, dont un « trouver l'erreur ».

| Fichier | Contenu |
|---|---|
| [`complexite.py`](complexite.py) | les fonctions de la vidéo ; la plupart comptent leurs opérations (comparaisons, tours, appels) |
| [`demo.py`](demo.py) | la recherche linéaire, puis les exercices 1 à 7 avec les compteurs |
| [`mesures.py`](mesures.py) | le test du doublement : temps réels quand n double (`--fib` : Fibonacci seul) |
| [`test_complexite.py`](test_complexite.py) | 15 tests (`unittest`) |

```
python demo.py
python mesures.py          # ~20 minutes : les versions lentes vont jusqu'à près de 2 minutes par taille
python mesures.py --fib    # Fibonacci seul
python -m unittest -v
```

Testé avec Python 3.15.1 et 3.11. Les temps de `preuves/mesures.txt` ont été mesurés sur un portable Windows 11
(meilleur de 3 séries d'au moins 0,2 s, graine 42) : ils changent d'une machine à l'autre, l'ordre de grandeur reste
le même. Les rapports des mesures de quelques millisecondes restent bruités.

Le piège montré dans la vidéo : une seule boucle, et pourtant n au carré.
- `if x not in resultat` parcourt la liste : 80 000 éléments = 113,55 s, contre 38,1 ms avec un `set` ;
- `liste.pop(0)` décale toute la liste : 400 000 éléments = 88,28 s, contre 62,9 ms avec `collections.deque`.
