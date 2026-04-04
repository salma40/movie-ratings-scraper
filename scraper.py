"""
scraper.py — Récupération des données films depuis GitHub (FiveThirtyEight)
Source : https://github.com/fivethirtyeight/data/tree/master/fandango
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

# ── Configuration ────────────────────────────────────────────────────────────

DATA_URL = (
    "https://raw.githubusercontent.com/fivethirtyeight/data/master/"
    "fandango/fandango_score_comparison.csv"
)
OUTPUT_FILE = "data/movies.csv"


# ── Scraping ─────────────────────────────────────────────────────────────────

def fetch_raw_csv(url: str) -> str:
    """Télécharge le fichier CSV brut depuis l'URL."""
    print(f"[scraper] Connexion à : {url}")
    headers = {"User-Agent": "Mozilla/5.0 (movie-scraper-cv-project/1.0)"}
    response = requests.get(url, headers=headers, timeout=15)
    response.raise_for_status()
    print(f"[scraper] ✓ Données reçues ({len(response.content) / 1024:.1f} Ko)")
    return response.text


def parse_movie_title(raw_title: str) -> tuple[str, int]:
    """Extrait le titre propre et l'année depuis 'Avengers: Age of Ultron (2015)'."""
    if "(" in raw_title and raw_title.endswith(")"):
        title = raw_title[:raw_title.rfind("(")].strip()
        year = int(raw_title[raw_title.rfind("(") + 1 : -1])
    else:
        title, year = raw_title.strip(), None
    return title, year


def clean_dataframe(raw_csv: str) -> pd.DataFrame:
    """
    Nettoie et restructure le CSV brut.
    On garde les colonnes utiles et on renomme pour plus de clarté.
    """
    from io import StringIO

    df = pd.read_csv(StringIO(raw_csv))

    # Extraire titre + année
    parsed = df["FILM"].apply(parse_movie_title)
    df["title"] = [p[0] for p in parsed]
    df["year"]  = [p[1] for p in parsed]

    # Sélection et renommage des colonnes pertinentes
    df = df.rename(columns={
        "RottenTomatoes":      "rt_critics",
        "RottenTomatoes_User": "rt_users",
        "Metacritic":          "metacritic_critics",
        "Metacritic_User":     "metacritic_users",
        "IMDB":                "imdb",
        "Fandango_Stars":      "fandango_stars",
        "IMDB_user_vote_count": "imdb_votes",
        "Fandango_votes":      "fandango_votes",
    })

    cols = [
        "title", "year",
        "rt_critics", "rt_users",
        "metacritic_critics", "metacritic_users",
        "imdb", "fandango_stars",
        "imdb_votes", "fandango_votes",
    ]
    df = df[cols].copy()

    # Nettoyage : suppression des lignes avec trop de valeurs manquantes
    before = len(df)
    df = df.dropna(subset=["title", "imdb", "rt_critics"])
    print(f"[cleaner] {before} films → {len(df)} après nettoyage")

    return df.reset_index(drop=True)


# ── Pipeline principal ────────────────────────────────────────────────────────

def run():
    os.makedirs("data", exist_ok=True)

    # 1. Scraping
    raw = fetch_raw_csv(DATA_URL)

    # 2. Nettoyage
    df = clean_dataframe(raw)

    # 3. Sauvegarde
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"[scraper] ✓ Données sauvegardées dans '{OUTPUT_FILE}' ({len(df)} films)\n")

    # 4. Aperçu rapide
    print(df.head(5).to_string(index=False))
    return df


if __name__ == "__main__":
    run()
