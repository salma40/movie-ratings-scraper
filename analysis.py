"""
analysis.py — Analyse et visualisations des données films scrapées
Génère 4 graphiques sauvegardés dans le dossier charts/
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
import os

# ── Style global ──────────────────────────────────────────────────────────────

plt.rcParams.update({
    "font.family":    "DejaVu Sans",
    "axes.spines.top":    False,
    "axes.spines.right":  False,
    "axes.grid":          True,
    "grid.alpha":         0.3,
    "grid.linestyle":     "--",
})

PALETTE  = ["#E63946", "#457B9D", "#2A9D8F", "#E9C46A", "#F4A261"]
OUTPUT   = "charts"


# ── Helpers ───────────────────────────────────────────────────────────────────

def load_data(path: str = "data/movies.csv") -> pd.DataFrame:
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"'{path}' introuvable. Lance d'abord : python scraper.py"
        )
    return pd.read_csv(path)


def save(fig: plt.Figure, filename: str):
    os.makedirs(OUTPUT, exist_ok=True)
    path = os.path.join(OUTPUT, filename)
    fig.savefig(path, dpi=150, bbox_inches="tight")
    print(f"[chart] ✓ {path}")
    plt.close(fig)


# ── Graphique 1 : Distribution des notes par plateforme ──────────────────────

def plot_score_distributions(df: pd.DataFrame):
    fig, axes = plt.subplots(1, 3, figsize=(14, 5))
    fig.suptitle("Distribution des notes par plateforme", fontsize=16, fontweight="bold", y=1.02)

    platforms = [
        ("rt_critics",  "Rotten Tomatoes\n(Critiques)",  PALETTE[0]),
        ("imdb",        "IMDb",                          PALETTE[1]),
        ("fandango_stars", "Fandango",                   PALETTE[2]),
    ]

    for ax, (col, label, color) in zip(axes, platforms):
        data = df[col].dropna()
        ax.hist(data, bins=20, color=color, edgecolor="white", alpha=0.85)
        ax.axvline(data.mean(), color="black", linestyle="--", linewidth=1.5,
                   label=f"Moyenne : {data.mean():.1f}")
        ax.set_title(label, fontweight="bold")
        ax.set_xlabel("Note")
        ax.set_ylabel("Nombre de films")
        ax.legend(fontsize=9)

    fig.tight_layout()
    save(fig, "1_distributions_notes.png")


# ── Graphique 2 : Corrélation IMDb vs Rotten Tomatoes ────────────────────────

def plot_imdb_vs_rt(df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(9, 6))

    scatter = ax.scatter(
        df["rt_critics"], df["imdb"],
        c=df["imdb_votes"], cmap="YlOrRd",
        alpha=0.7, s=60, edgecolors="white", linewidths=0.5
    )

    # Ligne de tendance
    sns.regplot(
        x="rt_critics", y="imdb", data=df, ax=ax,
        scatter=False, line_kws={"color": PALETTE[1], "linewidth": 2}
    )

    cbar = fig.colorbar(scatter, ax=ax)
    cbar.set_label("Nombre de votes IMDb", rotation=270, labelpad=15)

    ax.set_xlabel("Note Rotten Tomatoes (Critiques)", fontsize=12)
    ax.set_ylabel("Note IMDb", fontsize=12)
    ax.set_title("Corrélation : IMDb vs Rotten Tomatoes\n(couleur = popularité sur IMDb)",
                 fontsize=14, fontweight="bold")

    # Annoter quelques films extrêmes
    for _, row in df.nlargest(3, "imdb_votes").iterrows():
        ax.annotate(
            row["title"],
            (row["rt_critics"], row["imdb"]),
            textcoords="offset points", xytext=(8, 4),
            fontsize=7.5, color="#333"
        )

    fig.tight_layout()
    save(fig, "2_imdb_vs_rotten_tomatoes.png")


# ── Graphique 3 : Fandango vs autres plateformes (biais) ─────────────────────

def plot_fandango_bias(df: pd.DataFrame):
    """
    FiveThirtyEight a découvert que Fandango gonflait ses notes.
    Ce graphique le visualise clairement.
    """
    # Normaliser toutes les notes sur /5 pour comparaison équitable
    compare = pd.DataFrame({
        "Fandango":        df["fandango_stars"],
        "IMDb":            df["imdb"],
        "RT Critiques":    df["rt_critics"] / 20,   # /100 → /5
        "Metacritic":      df["metacritic_critics"] / 20,
    })

    fig, ax = plt.subplots(figsize=(10, 6))

    means = compare.mean().sort_values(ascending=False)
    colors = [PALETTE[0] if i == 0 else "#AAAAAA" for i in range(len(means))]

    bars = ax.bar(means.index, means.values, color=colors, edgecolor="white",
                  width=0.6, zorder=3)

    for bar, val in zip(bars, means.values):
        ax.text(bar.get_x() + bar.get_width() / 2, val + 0.03,
                f"{val:.2f}", ha="center", va="bottom", fontweight="bold")

    ax.set_ylim(0, 5.5)
    ax.set_ylabel("Note moyenne (sur 5)", fontsize=12)
    ax.set_title("Fandango note-t-il plus généreusement ?\n(toutes notes ramenées sur /5)",
                 fontsize=14, fontweight="bold")
    ax.axhline(compare.mean().mean(), color="black", linestyle=":", linewidth=1.2,
               label=f"Moyenne globale : {compare.mean().mean():.2f}")
    ax.legend()

    fig.tight_layout()
    save(fig, "3_biais_fandango.png")


# ── Graphique 4 : Top 10 films les mieux notés (IMDb) ────────────────────────

def plot_top10(df: pd.DataFrame):
    top10 = df.nlargest(10, "imdb")[["title", "imdb", "rt_critics"]].copy()
    top10 = top10.sort_values("imdb")

    fig, ax = plt.subplots(figsize=(10, 7))

    bars = ax.barh(top10["title"], top10["imdb"],
                   color=PALETTE[1], alpha=0.85, edgecolor="white", height=0.6)

    # Superposer la note RT (normalisée /10)
    ax.scatter(top10["rt_critics"] / 10, top10["title"],
               color=PALETTE[0], s=80, zorder=5, label="RT Critiques (/10)")

    for bar, val in zip(bars, top10["imdb"]):
        ax.text(val + 0.02, bar.get_y() + bar.get_height() / 2,
                f"{val:.1f}", va="center", fontsize=9, fontweight="bold")

    ax.set_xlim(0, 10)
    ax.set_xlabel("Note IMDb", fontsize=12)
    ax.set_title("Top 10 films les mieux notés sur IMDb\n(avec note Rotten Tomatoes en overlay)",
                 fontsize=14, fontweight="bold")
    ax.legend(loc="lower right")

    fig.tight_layout()
    save(fig, "4_top10_films.png")


# ── Pipeline principal ────────────────────────────────────────────────────────

def run():
    print("[analysis] Chargement des données...")
    df = load_data()
    print(f"[analysis] {len(df)} films chargés\n")

    print("[analysis] Génération des graphiques...")
    plot_score_distributions(df)
    plot_imdb_vs_rt(df)
    plot_fandango_bias(df)
    plot_top10(df)

    print(f"\n[analysis] ✓ 4 graphiques sauvegardés dans '{OUTPUT}/'")

    # Stats résumées dans le terminal
    print("\n── Statistiques clés ──────────────────────────────")
    print(f"Films analysés    : {len(df)}")
    print(f"Note IMDb moy.    : {df['imdb'].mean():.2f}/10")
    print(f"Note RT moy.      : {df['rt_critics'].mean():.1f}/100")
    print(f"Note Fandango moy.: {df['fandango_stars'].mean():.2f}/5")
    print(f"Film le + voté    : {df.loc[df['imdb_votes'].idxmax(), 'title']} "
          f"({df['imdb_votes'].max():,} votes)")


if __name__ == "__main__":
    run()
