"""src/nlp/pipeline_web_html_james.py - Chiefs EVTL Pipeline.

Author: John James
Date: 2026-11

Purpose:
Orchestrate a customized EVTL pipeline for analyzing
a Kansas City Chiefs game recap article.

Analytical Questions:
- How can we extract HTML from the official Chiefs website?
- How can we validate the article structure?
- Which meaningful words occur most frequently?
- How can we export the analysis into a structured CSV file?

Run from the root project folder with:

    uv run python -m nlp.pipeline_web_html_james
"""

# ============================================================
# Section 1. Setup and Imports
# ============================================================

import logging

from datafun_toolkit.logger import get_logger, log_header, log_path

from nlp.config_james import (
    DATA_PATH,
    HTTP_REQUEST_HEADERS,
    PAGE_URL,
    PROCESSED_CSV_PATH,
    PROCESSED_PATH,
    RAW_HTML_PATH,
    RAW_PATH,
    ROOT_PATH,
)
from nlp.stage01_extract import run_extract
from nlp.stage02_validate_james import run_validate
from nlp.stage03_transform_james import run_transform
from nlp.stage04_load import run_load

# ============================================================
# Section 2. Configure Logging
# ============================================================

LOG: logging.Logger = get_logger("CI", level="DEBUG")

# ============================================================
# Section 3. Define Main Pipeline Function
# ============================================================


def main() -> None:
    """Run the customized Kansas City Chiefs EVTL pipeline."""
    log_header(LOG, "Module 5: Kansas City Chiefs Game Recap Analysis")
    LOG.info("START CHIEFS PIPELINE")

    RAW_PATH.mkdir(parents=True, exist_ok=True)
    PROCESSED_PATH.mkdir(parents=True, exist_ok=True)

    log_path(LOG, "ROOT_PATH", ROOT_PATH)
    log_path(LOG, "DATA_PATH", DATA_PATH)
    log_path(LOG, "RAW_PATH", RAW_PATH)
    log_path(LOG, "PROCESSED_PATH", PROCESSED_PATH)

    # STAGE 01: EXTRACT
    html_content = run_extract(
        source_url=PAGE_URL,
        http_request_headers=HTTP_REQUEST_HEADERS,
        raw_html_path=RAW_HTML_PATH,
        LOG=LOG,
    )

    # STAGE 02: VALIDATE
    validated_soup = run_validate(
        html_content=html_content,
        LOG=LOG,
    )

    # STAGE 03: TRANSFORM
    df = run_transform(
        soup=validated_soup,
        LOG=LOG,
    )

    # STAGE 04: LOAD
    run_load(
        df=df,
        processed_csv_path=PROCESSED_CSV_PATH,
        LOG=LOG,
    )

    LOG.info("========================")
    LOG.info("Chiefs pipeline executed successfully!")
    LOG.info("========================")


# ============================================================
# Section 4. Run Main Function
# ============================================================

if __name__ == "__main__":
    main()
