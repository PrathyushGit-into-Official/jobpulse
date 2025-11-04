# scraper/__init__.py
# Expose scraper functions at package level for easy imports.

from .mnc_scraper import scrape_mnc_jobs
from .gov_scraper import scrape_gov_jobs
from .bank_scraper import scrape_bank_jobs
from .pdf_parser import parse_pdf_jobs

__all__ = [
    "scrape_mnc_jobs",
    "scrape_gov_jobs",
    "scrape_bank_scraper",  # legacy safe name (not used broadly), keep for compatibility
    "scrape_bank_jobs",
    "parse_pdf_jobs",
]
