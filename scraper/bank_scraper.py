# scraper/bank_scraper.py
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
    # Already given
    "SBI": "https://sbi.co.in/careers",
    "HDFC": "https://www.hdfcbank.com/personal/about-us/careers",
    "ICICI": "https://www.icicicareers.com/website/ICICI_Careers/",

    # Public Sector Banks
    "Bank of Baroda": "https://www.bankofbaroda.in/career",
    "Punjab National Bank": "https://www.pnbindia.in/Recruitments.aspx",
    "Canara Bank": "https://canarabank.com/pages/careers",
    "Indian Bank": "https://www.indianbank.in/career/",
    "Bank of India": "https://bankofindia.co.in/career",
    "Union Bank of India": "https://www.unionbankofindia.co.in/english/recruitment.aspx",
    "UCO Bank": "https://www.ucobank.com/en/career",
    "Bank of Maharashtra": "https://bankofmaharashtra.in/recruitment",
    "Indian Overseas Bank": "https://www.iob.in/careers.aspx",
    "Central Bank of India": "https://centralbankofindia.co.in/en/recruitments",

    # Major Private Banks
    "Axis Bank": "https://www.axisbank.com/careers",
    "Kotak Mahindra Bank": "https://www.kotak.com/en/about-us/careers.html",
    "IndusInd Bank": "https://www.indusind.com/in/en/personal/careers.html",
    "Yes Bank": "https://www.yesbank.in/about-us/careers",
    "IDFC First Bank": "https://www.idfcfirstbank.com/careers",
    "RBL Bank": "https://www.rblbank.com/careers",
    "Federal Bank": "https://www.federalbank.co.in/careers",   # requested

    # Other Private Banks
    "South Indian Bank": "https://www.southindianbank.com/Careers",
    "Karur Vysya Bank": "https://www.kvb.co.in/careers/",
    "Tamilnad Mercantile Bank": "https://www.tmb.in/careers",
    "DCB Bank": "https://www.dcbbank.com/careers",
    "Jammu & Kashmir Bank": "https://www.jkbank.com/others/common/jobportal.php",
    "Dhanlaxmi Bank": "https://www.dhanbank.com/careers",
    "City Union Bank": "https://www.cityunionbank.com/web-page/careers",

    # Small Finance Banks (Top ones)
    "AU Small Finance Bank": "https://www.aubank.in/about/careers",
    "Equitas Small Finance Bank": "https://www.equitasbank.com/careers",
    "Ujjivan Small Finance Bank": "https://www.ujjivansfb.in/careers",
    "Jana Small Finance Bank": "https://www.janabank.com/careers"
}


KEYWORDS = ["it", "developer", "analyst", "technology", "officer", "programmer"]


def _build_session():
    session = requests.Session()
    retry = Retry(
        total=MAX_RETRIES,
        read=MAX_RETRIES,
        connect=MAX_RETRIES,
        backoff_factor=BACKOFF_FACTOR,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"],
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


def scrape_bank_jobs(urls=None, session=None):
    logger.info("🏦 Scraping bank portals...")

    jobs = []
    seen = set()

    urls = urls or DEFAULT_URLS
    session = session or _build_session()

    for bank, base_url in urls.items():
        try:
            resp = _safe_get(session, base_url)
            if not resp:
                continue

            soup = BeautifulSoup(resp.text, "html.parser")

            for a in soup.find_all("a", href=True):
                title = a.get_text(strip=True)

                if not title:
                    continue

                if not _looks_like_job_title(title):
                    continue

                link = a["href"]
                full_link = link if link.startswith("http") else urljoin(base_url, link)
                full_link = full_link.split("#")[0]

                if full_link in seen:
                    continue

                seen.add(full_link)

                jobs.append({
                    "title": title,
                    "link": full_link,
                    "company": bank,
                    "source": base_url
                })

            time.sleep(POLITE_DELAY)

        except Exception as e:
            logger.exception(f"Error scraping {bank}: {e}")

    logger.info(f"🏦 Bank scraper found {len(jobs)} jobs")
    return jobs
