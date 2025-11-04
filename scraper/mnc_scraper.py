# scraper/mnc_scraper.py
import time
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
from loguru import logger

HEADERS = {"User-Agent": "JobPulseBot/1.0 (+https://github.com/PrathyushGit-into-Official/jobpulse)"}
REQUEST_TIMEOUT = 10
POLITE_DELAY = 0.8  # seconds between requests

def _safe_get(url):
    try:
        resp = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()
        return resp
    except Exception as e:
        logger.error(f"Request failed for {url}: {e}")
        return None

def scrape_mnc_jobs():
    """
    Scrapes selected MNC career pages and returns a list of job dicts:
    {'title', 'link', 'company', 'source'}
    """
    logger.info("🔍 Scraping MNC job portals...")
    jobs = []

    urls = {
        "TCS": "https://www.tcs.com/careers",
        "Infosys": "https://www.infosys.com/careers",
        "Tech Mahindra": "https://careers.techmahindra.com/",
        "Wipro": "https://careers.wipro.com/",
    }

    for company, url in urls.items():
        resp = _safe_get(url)
        if not resp:
            continue

        soup = BeautifulSoup(resp.text, "html.parser")

        # Generic scan for links/titles; site-specific parsing can be added later
        for a in soup.find_all("a", href=True):
            title = a.get_text(strip=True)
            if not title:
                continue
            link = a["href"]
            # simple keyword filter
            if any(k in title.lower() for k in ["engineer", "developer", "software", "it", "trainee", "intern"]):
                full_link = link if link.startswith("http") else urljoin(url, link)
                jobs.append({
                    "title": title,
                    "link": full_link,
                    "company": company,
                    "source": url
                })

        time.sleep(POLITE_DELAY)

    logger.info(f"🔍 MNC scrapers found {len(jobs)} candidates.")
    return jobs
