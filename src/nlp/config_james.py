"""src/nlp/config_james.py - Kansas City Chiefs Web Mining Configuration.

Author: John James
Date: 2026-11

Purpose:
Configure the custom EVTL pipeline to analyze a Kansas City Chiefs
game recap article from the official Chiefs website.

Analytical Question:
What information and performance-related terms can be extracted
from a Kansas City Chiefs game recap?
"""

from pathlib import Path

# ============================================================
# WEB DOCUMENT CONFIGURATION
# ============================================================

PAGE_URL: str = (
    "https://www.chiefs.com/news/"
    "chiefs-defeat-chargers-22-6-to-move-to-5-0-on-the-season"
)

HTTP_REQUEST_HEADERS: dict = {
    "User-Agent": "Mozilla/5.0 (educational-use; web-mining-course)"
}

# ============================================================
# PATH CONFIGURATION
# ============================================================

ROOT_PATH: Path = Path.cwd()
DATA_PATH: Path = ROOT_PATH / "data"
RAW_PATH: Path = DATA_PATH / "raw"
PROCESSED_PATH: Path = DATA_PATH / "processed"

RAW_HTML_PATH: Path = RAW_PATH / "chiefs_raw.html"
PROCESSED_CSV_PATH: Path = PROCESSED_PATH / "chiefs_processed.csv"
