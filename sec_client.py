import logging
import requests
from config import COMPANIES

logger = logging.getLogger(__name__)

# SEC EDGAR requires a User-Agent in this exact format: "Name Email"
# See: https://www.sec.gov/os/accessing-edgar-data
HEADERS = {
    "User-Agent": "Quartr puneet@quartr.com",
    "Accept-Encoding": "gzip, deflate",
}


def get_latest_10k_url(company_name: str, cik: str) -> str:
    """
    Fetches the latest 10-K filing URL for a given company using SEC EDGAR.

    Steps:
    1. Hit the submissions endpoint to get all filings for the company
    2. Find the most recent 10-K entry
    3. Build and return the URL to the primary document
    """
    submissions_url = f"https://data.sec.gov/submissions/CIK{cik}.json"
    response = requests.get(submissions_url, headers=HEADERS)
    response.raise_for_status()

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