# scraper/bank_scraper.py
import time
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
from loguru import logger

HEADERS = {"User-Agent": "JobPulseBot/1.0 (+https://github.com/PrathyushGit-into-Official/jobpulse)"}
REQUEST_TIMEOUT = 10
POLITE_DELAY = 0.8

def _safe_get(url):
    try:
        resp = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()
        return resp
    except Exception as e:
        logger.error(f"Request failed for {url}: {e}")
        return None

def scrape_bank_jobs():
    """
    Scrapes bank career pages for IT/technology openings.
    Returns list of dicts: {'title','link','company','source'}
    """
    logger.info("🏦 Scraping bank job portals...")
    jobs = []

    urls = {
        "SBI": "https://sbi.co.in/careers",
        "HDFC": "https://www.hdfcbank.com/personal/about-us/careers",
        "ICICI": "https://www.icicicareers.com/website/ICICI_Careers/",
    }

    for bank, url in urls.items():
        resp = _safe_get(url)
        if not resp:
            continue

        soup = BeautifulSoup(resp.text, "html.parser")
        for a in soup.find_all("a", href=True):
            title = a.get_text(strip=True)
            if not title:
                continue
            link = a["href"]
            if any(k in title.lower() for k in ["it", "developer", "analyst", "officer", "technology", "programmer"]):
                full_link = link if link.startswith("http") else urljoin(url, link)
                jobs.append({
                    "title": title,
                    "link": full_link,
                    "company": bank,
                    "source": url
                })
        time.sleep(POLITE_DELAY)

    logger.info(f"🏦 Bank scrapers found {len(jobs)} candidates.")
    return jobs
