# Movie Ratings Scraper & Analysis

Projet Python de scraping et visualisation de donnees — notes de films comparees entre IMDb, Rotten Tomatoes, Metacritic et Fandango.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Pandas](https://img.shields.io/badge/Pandas-2.0-green?logo=pandas)
![Matplotlib](https://img.shields.io/badge/Matplotlib-3.7-orange)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

---

## Objectif

Ce projet scrape des donnees de notation de films depuis une source publique, les nettoie avec Pandas, puis genere des visualisations pour repondre a une question concrete :

> Les plateformes de notation sont-elles toutes objectives ? Ou certaines gonflent-elles leurs notes ?

Resultat : Fandango note significativement plus haut que les autres plateformes.

---

## Visualisations generees

| Graphique | Description |
|-----------|-------------|
| `1_distributions_notes.png` | Distribution des notes RT, IMDb et Fandango |
| `2_imdb_vs_rotten_tomatoes.png` | Correlation entre critiques et popularite |
| `3_biais_fandango.png` | Comparaison des moyennes entre plateformes |
| `4_top10_films.png` | Top 10 IMDb avec overlay RT |

---

## Structure du projet

```
movie-scraper/
│
├── scraper.py        # Telechargement et nettoyage des donnees
├── analysis.py       # Visualisations avec Matplotlib et Seaborn
├── requirements.txt  # Dependances Python
│
├── data/
│   └── movies.csv    # Donnees nettoyees (146 films)
│
└── charts/
    ├── 1_distributions_notes.png
    ├── 2_imdb_vs_rotten_tomatoes.png
    ├── 3_biais_fandango.png
    └── 4_top10_films.png
```

---

## Tutoriel complet

### Etape 1 — Verifier que Python est installe

Ouvre un terminal (sur Windows : touche Windows + R, tape `cmd`, valide) et lance :

```bash
python --version
```

Si tu vois `Python 3.x.x`, c'est bon. Sinon, telecharge Python sur https://www.python.org/downloads/ et installe-le (coche "Add to PATH" pendant l'installation).

---

### Etape 2 — Recuperer le projet

**Option A : cloner depuis GitHub (recommande)**

```bash
git clone https://github.com/salma40/movie-ratings-scraper.git
cd movie-ratings-scraper
```

**Option B : telecharger le ZIP**

Clique sur le bouton vert "Code" sur GitHub, puis "Download ZIP". Extrais le dossier, puis ouvre un terminal dans ce dossier.

---

### Etape 3 — Installer les dependances

```bash
pip install -r requirements.txt
```

Cette commande installe automatiquement toutes les bibliotheques necessaires (pandas, matplotlib, seaborn, requests, beautifulsoup4).

Si tu as une erreur de permission sur Mac/Linux, utilise :

```bash
pip install -r requirements.txt --user
```

---

### Etape 4 — Scraper les donnees

```bash
python scraper.py
```

Ce que tu vas voir dans le terminal :

```
[scraper] Connexion a : https://raw.githubusercontent.com/...
[scraper] Donnees recues (14.8 Ko)
[cleaner] 146 films -> 146 apres nettoyage
[scraper] Donnees sauvegardees dans 'data/movies.csv' (146 films)
```

Un fichier `data/movies.csv` est cree avec les donnees nettoyees.

---

### Etape 5 — Generer les visualisations

```bash
python analysis.py
```

Ce que tu vas voir :

```
[analysis] 146 films charges
[chart] charts/1_distributions_notes.png
[chart] charts/2_imdb_vs_rotten_tomatoes.png
[chart] charts/3_biais_fandango.png
[chart] charts/4_top10_films.png

Films analyses    : 146
Note IMDb moy.    : 6.74/10
Note RT moy.      : 60.8/100
Note Fandango moy.: 4.09/5
```

Les 4 graphiques sont sauvegardes dans le dossier `charts/`. Ouvre-les avec n'importe quel visualiseur d'images.

---

### Problemes courants

**"ModuleNotFoundError: No module named 'pandas'"**
Lance d'abord `pip install -r requirements.txt`.

**"pip n'est pas reconnu"**
Essaie `pip3` a la place de `pip`, ou reinstalle Python en cochant "Add to PATH".

**Pas de connexion internet**
Le scraper a besoin d'internet pour telecharger les donnees. Les donnees sont aussi deja disponibles dans `data/movies.csv` si tu as clone le repo — dans ce cas tu peux passer directement a l'etape 5.

---

## Resultats cles

- 146 films analyses (sorties 2015)
- Note IMDb moyenne : 6.74/10
- Note RT Critics moyenne : 60.8/100
- Note Fandango moyenne : 4.09/5, soit 8.18/10 — clairement au-dessus des autres
- Film le plus vote : The Imitation Game (334 164 votes IMDb)

---

## Stack technique

- requests — Requetes HTTP
- BeautifulSoup4 — Parsing HTML
- Pandas — Manipulation de donnees
- Matplotlib — Graphiques
- Seaborn — Visualisations statistiques

---

## Source des donnees

Donnees originales : FiveThirtyEight — Fandango Dataset
https://github.com/fivethirtyeight/data/tree/master/fandango

---

## Licence

MIT
