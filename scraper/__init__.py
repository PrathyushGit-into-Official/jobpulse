from loguru import logger

def _empty(*args, **kwargs):
    return []

try:
    from .mnc_scraper import scrape_mnc_jobs
except Exception as e:
    logger.warning("Failed to load MNC scraper: %s", e)
    scrape_mnc_jobs = _empty

try:
    from .gov_scraper import scrape_gov_jobs
except Exception as e:
    logger.warning("Failed to load GOV scraper: %s", e)
    scrape_gov_jobs = _empty

try:
    from .bank_scraper import scrape_bank_jobs
except Exception as e:
    logger.warning("Failed to load BANK scraper: %s", e)
    scrape_bank_jobs = _empty

try:
    from .pdf_parser import parse_pdf_jobs
except Exception as e:
    logger.warning("Failed to load PDF parser: %s", e)
    parse_pdf_jobs = _empty

__all__ = [
    "scrape_mnc_jobs",
    "scrape_gov_jobs",
    "scrape_bank_jobs",
    "parse_pdf_jobs",
]
