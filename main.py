import time
import logging
from config import COMPANIES
from sec_client import get_latest_10k_url
from pdf_converter import save_reports_as_pdf

# Configure logging once at the entry point
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)


def main():
    logger.info("Starting 10-K report fetcher")

    # Step 1: Collect all 10-K URLs
    reports = {}
    for company_name, cik in COMPANIES.items():
        try:
            url = get_latest_10k_url(company_name, cik)
            reports[company_name] = url
        except Exception as e:
            logger.error(f"{company_name} - Failed to get URL: {e}")
        time.sleep(1)

    # Step 2: Convert all to PDF in one browser session
    logger.info(f"Converting {len(reports)} reports to PDF")
    results = save_reports_as_pdf(reports)

    # Summary
    logger.info(f"Done - Success: {len(results['success'])}, Failed: {len(results['failed'])}")
    if results["failed"]:
        logger.warning(f"Failed companies: {', '.join(results['failed'])}")


if __name__ == "__main__":
    main()