# Algorithmes de tri en Python : cours et exercices corrigés

Vidéo : https://youtu.be/Uk9Py1uXrfA

Les cinq tris du programme (bulles, sélection, insertion, fusion, rapide) et la recherche dichotomique, sur la même
liste de notes `[14, 7, 18, 3, 11, 9]`, avec sept exercices corrigés.

| Fichier | Contenu |
|---|---|
| [`tris.py`](tris.py) | les tris et la recherche dichotomique (en boucle et en récursif) |
| [`demo.py`](demo.py) | chaque tri passage par passage, puis les exercices 1 à 5 |
| [`erreurs.py`](erreurs.py) | exercices 6 et 7 « trouver l'erreur », et le tri rapide qui plante sur des doublons |
| [`mesures.py`](mesures.py) | les temps réels, de 1 000 à 1 000 000 de nombres |
| [`test_tris.py`](test_tris.py) | 13 tests (`unittest`) |

```
python demo.py
python erreurs.py
python mesures.py          # quelques minutes : les tris lents vont jusqu'à 10 000 éléments
python -m unittest -v
```

Testé avec Python 3.15.1 et 3.11. Les temps de `preuves/mesures.txt` ont été mesurés sur un portable Windows 11
(meilleur de 3) : ils changent d'une machine à l'autre, l'ordre de grandeur reste le même.

Deux pièges montrés dans la vidéo :
- le tri rapide « des cours » (pivot = dernier élément) plante avec `RecursionError` sur une liste **déjà triée**
  d'environ 1 000 éléments ;
- un pivot tiré au hasard ne suffit pas : sur 20 000 notes sur vingt (beaucoup de doublons), il plante aussi. La
  version de `tris.py` regroupe en plus les éléments égaux au pivot (partition en trois).
