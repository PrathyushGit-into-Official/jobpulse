# scraper/gov_scraper.py
import time
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
from loguru import logger

HEADERS = {"User-Agent": "JobPulseBot/1.0 (+https://github.com/PrathyushGit-into-Official/jobpulse)"}
REQUEST_TIMEOUT = 10
POLITE_DELAY = 1.0

def _safe_get(url):
    try:
        resp = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()
        return resp
    except Exception as e:
        logger.error(f"Request failed for {url}: {e}")
        return None

def scrape_gov_jobs():
    """
    Scrapes government and PSU sites for job links and returns list of job dicts.
    """
    logger.info("🏛️ Scraping government and PSU portals...")
    jobs = []

    urls = {
        "ISRO": "https://www.isro.gov.in/Careers.html",
        "DRDO": "https://www.drdo.gov.in/careers",
        "NIC": "https://www.nic.in/careers/",
        "BHEL": "https://careers.bhel.in/bhel/jsp/",
    }

    for org, url in urls.items():
        resp = _safe_get(url)
        if not resp:
            continue

        soup = BeautifulSoup(resp.text, "html.parser")

        # Generic link scan; refine per-site if needed
        for a in soup.find_all("a", href=True):
            title = a.get_text(strip=True)
            if not title:
                continue
            link = a["href"]
            if any(k in title.lower() for k in ["engineer", "recruitment", "vacancy", "it", "assistant", "scientist"]):
                full_link = link if link.startswith("http") else urljoin(url, link)
                jobs.append({
                    "title": title,
                    "link": full_link,
                    "company": org,
                    "source": url
                })

        time.sleep(POLITE_DELAY)

    logger.info(f"🏛️ Govt scrapers found {len(jobs)} candidates.")
    return jobs
