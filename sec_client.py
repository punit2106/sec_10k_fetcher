import logging
import time
import requests

logger = logging.getLogger(__name__)

# SEC EDGAR requires a User-Agent in this exact format: "Name Email"
# See: https://www.sec.gov/os/accessing-edgar-data
HEADERS = {
    "User-Agent": "Quartr puneet@quartr.com",
    "Accept-Encoding": "gzip, deflate",
}

# EDGAR rate limit: 10 requests/second. Space requests and retry on 429.
_REQUEST_DELAY = 0.15  # 150 ms between requests ~ 6-7/sec, safely under the limit
_MAX_RETRIES = 3


def edgar_get(url: str) -> requests.Response:
    """
    Wrapper around requests.get that:
    - Enforces a minimum delay between calls to stay under EDGAR's 10 req/sec limit
    - Retries with exponential backoff on 429 Too Many Requests or 503
    """
    for attempt in range(1, _MAX_RETRIES + 1):
        time.sleep(_REQUEST_DELAY)
        response = requests.get(url, headers=HEADERS)
        if response.status_code in (429, 503):
            wait = 2 ** attempt  # 2s, 4s, 8s
            logger.warning(
                f"EDGAR returned {response.status_code} (attempt {attempt}/{_MAX_RETRIES}). "
                f"Retrying in {wait}s..."
            )
            time.sleep(wait)
            continue
        response.raise_for_status()
        return response
    # Final attempt — let raise_for_status propagate the error
    response.raise_for_status()
    return response  # unreachable, satisfies type checkers


def get_latest_10k_url(company_name: str, cik: str) -> str:
    """
    Fetches the latest 10-K filing URL for a given company using SEC EDGAR.

    Steps:
    1. Hit the submissions endpoint to get all filings for the company
    2. Find the most recent 10-K entry
    3. Build and return the URL to the primary document
    """
    submissions_url = f"https://data.sec.gov/submissions/CIK{cik}.json"
    response = edgar_get(submissions_url)

    data = response.json()
    filings = data["filings"]["recent"]

    # Walk through filings and find the first (latest) 10-K
    for i, form_type in enumerate(filings["form"]):
        if form_type == "10-K":
            accession_number = filings["accessionNumber"][i].replace("-", "")
            primary_doc = filings["primaryDocument"][i]

            # CIK without leading zeros for the URL path
            cik_stripped = str(int(cik))

            doc_url = (
                f"https://www.sec.gov/Archives/edgar/data/"
                f"{cik_stripped}/{accession_number}/{primary_doc}"
            )

            logger.info(f"{company_name} - Latest 10-K: {doc_url}")
            return doc_url

    raise ValueError(f"No 10-K filing found for {company_name} (CIK: {cik})")