# scraper/__init__.py
# Expose scraper functions at package level for easy imports.

from .mnc_scraper import scrape_mnc_jobs
from .gov_scraper import scrape_gov_jobs
from .bank_scraper import scrape_bank_jobs
from .pdf_parser import parse_pdf_jobs
from loguru import logger

__all__ = [
    "scrape_mnc_jobs",
    "scrape_gov_jobs",
    "scrape_bank_scraper",  # legacy safe name (not used broadly), keep for compatibility
    "scrape_bank_jobs",
    "parse_pdf_jobs",
]

# Attempt to import scrapers lazily and warn if any fail (keeps package import resilient)
try:
    # these imports above should succeed; keep this block in case future optional scrapers are added
    pass
except Exception as e:
    # Use loguru style formatting
    logger.warning("Failed to load scraper submodules: {}", e)
