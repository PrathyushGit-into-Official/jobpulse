# scraper/mnc_scraper.py
import time
import os
from urllib.parse import urljoin
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from bs4 import BeautifulSoup
from loguru import logger

HEADERS = {
    "User-Agent": os.getenv("JOBPULSE_USER_AGENT", "JobPulseBot/1.0")
}

REQUEST_TIMEOUT = float(os.getenv("JOBPULSE_REQUEST_TIMEOUT", "10"))
POLITE_DELAY = float(os.getenv("JOBPULSE_POLITE_DELAY", "0.6"))
MAX_RETRIES = int(os.getenv("JOBPULSE_MAX_RETRIES", "3"))
BACKOFF_FACTOR = float(os.getenv("JOBPULSE_RETRY_BACKOFF", "0.5"))

DEFAULT_URLS = {
    "TCS": "https://www.tcs.com/careers",
    "Infosys": "https://www.infosys.com/careers",
    "Tech Mahindra": "https://careers.techmahindra.com/",
    "Wipro": "https://careers.wipro.com/",
}

KEYWORDS = ["engineer", "developer", "software", "it", "trainee", "intern"]


def _build_session():
    session = requests.Session()

    retry = Retry(
        total=MAX_RETRIES,
        read=MAX_RETRIES,
        connect=MAX_RETRIES,
        backoff_factor=BACKOFF_FACTOR,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"]
    )

    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    session.headers.update(HEADERS)

    return session


def _safe_get(session, url):
    try:
        resp = session.get(url, timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()
        return resp
    except Exception as e:
        logger.warning(f"GET failed for {url} -> {e}")
        return None


def _looks_like_job_title(text):
    t = (text or "").lower()
    return any(k in t for k in KEYWORDS)


def scrape_mnc_jobs(urls=None, session=None):
    logger.info("🔍 Scraping MNC job portals...")

    jobs = []
    seen = set()

    urls = urls or DEFAULT_URLS
    session = session or _build_session()

    for company, base_url in urls.items():
        try:
            response = _safe_get(session, base_url)
            if not response:
                continue

            soup = BeautifulSoup(response.text, "html.parser")

            for a in soup.find_all("a", href=True):
                title = a.get_text(strip=True)

                if not title:
                    continue

                if not _looks_like_job_title(title):
                    continue

                link = a["href"]
                full_link = link if link.startswith("http") else urljoin(base_url, link)

                # Remove URL fragments (#something)
                full_link = full_link.split("#")[0]

                if full_link in seen:
                    continue

                seen.add(full_link)

                jobs.append({
                    "title": title,
                    "link": full_link,
                    "company": company,
                    "source": base_url,
                })

            time.sleep(POLITE_DELAY)

        except Exception as e:
            logger.exception(f"Error scraping {company}: {e}")

    logger.info(f"🔍 MNC scraper found {len(jobs)} jobs")
    return jobs
