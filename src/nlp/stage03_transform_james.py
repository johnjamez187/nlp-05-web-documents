"""src/nlp/stage03_transform_james.py - Chiefs Article Transformation.

Author: John James
Date: 2026-11

Source: Validated BeautifulSoup object
Sink: Pandas DataFrame

Purpose:
Extract, clean, and analyze text from a Kansas City Chiefs
game recap article.

Analytical Questions:
- How many words and paragraphs does the article contain?
- Which meaningful words appear most frequently?
- What topics receive the most attention in the game recap?
"""

# ============================================================
# Section 1. Setup and Imports
# ============================================================

from collections import Counter
import logging
import re

from bs4 import BeautifulSoup
import pandas as pd

from nlp.config_james import PAGE_URL

# ============================================================
# Section 2. Define Stop Words
# ============================================================


STOP_WORDS = {
    "a",
    "an",
    "the",
    "and",
    "or",
    "but",
    "if",
    "in",
    "on",
    "at",
    "to",
    "for",
    "of",
    "with",
    "by",
    "from",
    "as",
    "is",
    "was",
    "were",
    "are",
    "be",
    "been",
    "being",
    "it",
    "its",
    "this",
    "that",
    "these",
    "those",
    "he",
    "she",
    "they",
    "them",
    "his",
    "her",
    "their",
    "we",
    "our",
    "you",
    "your",
    "i",
    "me",
    "my",
    "who",
    "what",
    "when",
    "where",
    "which",
    "how",
    "not",
    "no",
    "so",
    "than",
    "then",
    "there",
    "here",
    "had",
    "has",
    "have",
    "did",
    "do",
    "does",
    "will",
    "would",
    "could",
    "should",
    "can",
    "may",
    "might",
    "also",
    "just",
    "more",
    "after",
    "before",
    "into",
    "out",
    "up",
    "down",
    "over",
    "about",
    "through",
    "during",
    "all",
    "any",
    "some",
    "each",
    "other",
    "only",
    "both",
    "such",
    "while",
}


# ============================================================
# Section 3. Define Run Transform Function
# ============================================================


def run_transform(
    soup: BeautifulSoup,
    LOG: logging.Logger,
) -> pd.DataFrame:
    """Transform Chiefs article HTML into structured data."""
    LOG.info("========================")
    LOG.info("STAGE 03: TRANSFORM starting...")
    LOG.info("========================")

    # Extract the article title.
    title_tag = soup.find("title")
    title = title_tag.get_text(strip=True) if title_tag else "unknown"

    # Extract nonempty article paragraphs.
    paragraphs = [
        p.get_text(" ", strip=True)
        for p in soup.select("article p")
        if p.get_text(" ", strip=True)
    ]

    # Combine paragraphs into one text document.
    article_text = " ".join(paragraphs)

    # ========================================================
    # Calculate derived fields.
    # ========================================================

    paragraph_count = len(paragraphs)

    # Tokenize text and convert words to lowercase.
    words = re.findall(r"[a-z]+", article_text.lower())
    word_count = len(words)

    # Remove common stop words and short words.
    cleaned_words = [word for word in words if word not in STOP_WORDS and len(word) > 2]

    cleaned_word_count = len(cleaned_words)

    # Calculate word frequencies.
    word_frequencies = Counter(cleaned_words)
    top_words = word_frequencies.most_common(10)

    # ========================================================
    # Log analysis results.
    # ========================================================

    LOG.info("Article title: %s", title)
    LOG.info("Paragraph count: %s", paragraph_count)
    LOG.info("Total word count: %s", word_count)
    LOG.info("Cleaned word count: %s", cleaned_word_count)

    LOG.info("TOP 10 MOST FREQUENT WORDS:")

    for word, count in top_words:
        LOG.info("%s: %s", word, count)

    # ========================================================
    # Build structured record.
    # ========================================================

    record = {
        "title": title,
        "source_url": PAGE_URL,
        "paragraph_count": paragraph_count,
        "word_count": word_count,
        "cleaned_word_count": cleaned_word_count,
        "unique_word_count": len(word_frequencies),
        "top_10_words": ", ".join(f"{word}: {count}" for word, count in top_words),
    }

    df = pd.DataFrame([record])

    LOG.info(
        "Created DataFrame with %s row and %s columns",
        len(df),
        len(df.columns),
    )

    LOG.info("DataFrame preview:\n%s", df.head())
    LOG.info("Transformation complete.")

    return df
