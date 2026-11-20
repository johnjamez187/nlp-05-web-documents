"""Automated tests for the Kansas City Chiefs EVTL pipeline.

Author: John James
Date: 2026-11
"""

import logging

import pytest

from nlp.stage02_validate_james import run_validate
from nlp.stage03_transform_james import run_transform

LOG = logging.getLogger(__name__)

SAMPLE_HTML = """
<html>
    <head>
        <title>Chiefs Game Recap</title>
    </head>
    <body>
        <article>
            <p>The Chiefs played strong defensive football.</p>
            <p>The Chiefs won the game.</p>
        </article>
    </body>
</html>
"""


def test_chiefs_validate():
    """Verify successful HTML validation."""
    soup = run_validate(SAMPLE_HTML, LOG)

    title = soup.find("title")
    assert title is not None
    assert title.get_text(strip=True) == "Chiefs Game Recap"
    assert len(soup.select("article p")) == 2


def test_chiefs_invalid_html():
    """Verify that invalid HTML is rejected."""
    invalid_html = "<html><body>No article</body></html>"

    with pytest.raises(ValueError, match="Required elements missing"):
        run_validate(invalid_html, LOG)


def test_chiefs_transform():
    """Verify article transformation and word frequencies."""
    soup = run_validate(SAMPLE_HTML, LOG)
    df = run_transform(soup, LOG)

    assert df.shape == (1, 7)

    record = df.iloc[0]

    assert record["title"] == "Chiefs Game Recap"
    assert record["paragraph_count"] == 2
    assert record["word_count"] == 11
    assert record["cleaned_word_count"] == 8
    assert record["unique_word_count"] == 7
    assert "chiefs: 2" in record["top_10_words"]
    assert "the:" not in record["top_10_words"]
