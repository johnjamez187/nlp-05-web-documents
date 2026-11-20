"""src/nlp/stage02_validate_james.py - Chiefs HTML Validation.

Author: John James
Date: 2026-11

Source: Raw HTML string
Sink: Validated BeautifulSoup object

Purpose:
Validate the HTML structure of a Kansas City Chiefs game recap
before extracting article content for analysis.
"""

# ============================================================
# Section 1. Setup and Imports
# ============================================================

import logging

from bs4 import BeautifulSoup

# ============================================================
# Section 2. Define Run Validate Function
# ============================================================


def run_validate(
    html_content: str,
    LOG: logging.Logger,
) -> BeautifulSoup:
    """Inspect and validate Chiefs article HTML."""
    LOG.info("========================")
    LOG.info("STAGE 02: VALIDATE starting...")
    LOG.info("========================")

    # Parse the HTML document.
    soup = BeautifulSoup(html_content, "html.parser")

    LOG.info("HTML STRUCTURE INSPECTION:")
    LOG.info(f"Top-level type: {type(soup).__name__}")

    LOG.info(
        f"Top-level elements: "
        f"{[element.name for element in soup.find_all(recursive=False)]}"
    )

    # Identify required HTML elements.
    title = soup.find("title")
    article = soup.find("article")

    paragraphs = [
        p.get_text(" ", strip=True)
        for p in soup.select("article p")
        if p.get_text(" ", strip=True)
    ]

    # Log validation results.
    LOG.info("VALIDATE: Title found: %s", title is not None)
    LOG.info("VALIDATE: Article found: %s", article is not None)
    LOG.info("VALIDATE: Nonempty paragraphs found: %s", len(paragraphs))

    # Check for missing required content.
    missing = []

    if title is None or not title.get_text(strip=True):
        missing.append("title")

    if article is None:
        missing.append("article")

    if not paragraphs:
        missing.append("article paragraphs")

    if missing:
        raise ValueError(
            f"VALIDATE: Required elements missing: {missing}. "
            "Chiefs page structure may have changed."
        )

    LOG.info("VALIDATE: Chiefs article HTML structure is valid.")
    LOG.info("Sink: validated BeautifulSoup object")

    return soup
