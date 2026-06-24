import os
import logging
from playwright.sync_api import sync_playwright
from sec_client import edgar_get

logger = logging.getLogger(__name__)

OUTPUT_DIR = "output"


def save_reports_as_pdf(reports: dict[str, str]) -> dict[str, list]:
    """
    Takes a dict of {company_name: url} and converts all to PDF
    using a single browser instance.

    Downloads HTML via requests first, then renders locally
    to avoid SEC bot detection on browser requests.
    """
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    results = {"success": [], "failed": []}

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        for company_name, url in reports.items():
            try:
                filename = f"{company_name.replace(' ', '_')}_10K.pdf"
                output_path = os.path.join(OUTPUT_DIR, filename)

                # Download HTML via requests (rate-limited, already accepted by SEC)
                logger.info(f"{company_name} - Downloading filing...")
                response = edgar_get(url)

                # Save HTML temporarily
                temp_html = os.path.abspath(
                    os.path.join(OUTPUT_DIR, f"{company_name.replace(' ', '_')}_temp.html")
                )
                with open(temp_html, "w", encoding="utf-8") as f:
                    f.write(response.text)

                # Render locally and export PDF
                logger.info(f"{company_name} - Converting to PDF...")
                page.goto(f"file://{temp_html}", wait_until="networkidle", timeout=90000)
                page.pdf(path=output_path, format="A4", print_background=True)

                # Clean up temp file
                os.remove(temp_html)

                logger.info(f"{company_name} - Saved -> {output_path}")
                results["success"].append(company_name)

            except Exception as e:
                logger.error(f"{company_name} - Failed: {e}")
                results["failed"].append(company_name)

        browser.close()

    return results