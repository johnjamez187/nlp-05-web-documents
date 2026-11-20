"""src/nlp/visualize_james.py - Chiefs Word Frequency Visualization.

Author: John James
Date: 2026-11

Purpose:
Visualize the ten most frequent words extracted from a Kansas
City Chiefs game recap using the custom EVTL pipeline.

Run with:
    uv run python -m nlp.visualize_james
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from nlp.config_james import PROCESSED_CSV_PATH


def main() -> None:
    """Generate a Chiefs-themed word frequency chart."""
    # Read the processed CSV.
    df = pd.read_csv(PROCESSED_CSV_PATH)

    # Extract word frequency results.
    top_words = df.loc[0, "top_10_words"]

    words = []
    counts = []

    for item in top_words.split(", "):
        word, count = item.split(": ")
        words.append(word.title())
        counts.append(int(count))

    # Configure Chiefs team colors.
    chiefs_red = "#E31837"
    chiefs_gold = "#FFB81C"

    # Create horizontal bar chart.
    fig, ax = plt.subplots(figsize=(10, 6))

    bars = ax.barh(
        words,
        counts,
        color=chiefs_red,
        edgecolor=chiefs_gold,
        linewidth=1.5,
    )

    ax.invert_yaxis()

    # Add frequency labels.
    ax.bar_label(bars, padding=5, fontsize=11)
    ax.set_xlim(0, max(counts) + 1)

    # Customize titles and labels.
    ax.set_title(
        "Kansas City Chiefs Game Recap\nTop 10 Most Frequent Words",
        fontsize=17,
        fontweight="bold",
        color=chiefs_red,
        pad=20,
    )

    ax.set_xlabel("Word Frequency")
    ax.set_ylabel("Words")

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    ax.grid(axis="x", linestyle="--", alpha=0.25)
    ax.set_axisbelow(True)

    fig.text(
        0.5,
        0.04,
        "Source: Chiefs.com | Analysis by John James",
        ha="center",
        fontsize=10,
    )

    # Create output folder.
    output_path = Path("docs/images/chiefs_word_frequency.png")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Save the visualization.
    fig.tight_layout(rect=(0, 0.07, 1, 1))
    fig.savefig(output_path, dpi=300, bbox_inches="tight")

    print(f"Visualization saved to: {output_path}")

    plt.show()


if __name__ == "__main__":
    main()
