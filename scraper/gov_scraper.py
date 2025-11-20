# scraper/gov_scraper.py
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
    # Core Government Engineering Organizations
    "ISRO": "https://www.isro.gov.in/Careers.html",
    "DRDO": "https://www.drdo.gov.in/careers",
    "NIC": "https://www.nic.in/careers/",
    "BHEL": "https://careers.bhel.in/bhel/jsp/",

    # Space & Aviation
    "HAL (Hindustan Aeronautics Ltd)": "https://hal-india.co.in/Careers/M__206",
    "BEL (Bharat Electronics Ltd)": "https://bel-india.in/careers",
    "AAI (Airports Authority of India)": "https://www.aai.aero/en/careers/recruitment",

    # Power & Energy Sector PSUs
    "NTPC": "https://www.ntpc.co.in/careers",
    "ONGC": "https://www.ongcindia.com/wps/wcm/connect/en/career/",
    "GAIL": "https://gailonline.com/CRApplyingGail.html",
    "HPCL": "https://jobs.hpcl.co.in/Recruit_New/",
    "BPCL": "https://www.bharatpetroleum.in/careers/careers.aspx",
    "IOCL": "https://iocl.com/latest-job-opening",

    # Electronics, Technology, Telecom PSUs
    "ECIL": "https://ecil.co.in/job_openings.php",
    "C-DAC": "https://cdac.in/index.aspx?id=jobcurrent",
    "NPCIL": "https://npcil.nic.in/Content.aspx?&MenuID=24",
    "BSNL": "https://www.bsnl.co.in/opencms/bsnl/BSNL/career/index.html",

    # Railways & Transport
    "Indian Railways (RRB/RRC)": "https://indianrailways.gov.in/railwayboard/view_section.jsp?lang=0&id=0,1,304,366,558",
    "DMRC (Delhi Metro)": "https://delhimetrorail.com/careers",
    "MRVC": "https://mrvc.indianrailways.gov.in/view_section.jsp?lang=0&id=0,294,302",

    # Atomic, Research, Nuclear Engineering
    "BARC": "https://recruit.barc.gov.in/barcrecruit/",
    "ISRO IPRC / LPSC / VSSC Units": "https://www.isro.gov.in/Careers.html",  # central portal
    "DAE (Dept of Atomic Energy)": "https://dpsdae.formflix.in/",

    # Heavy Engineering & Manufacturing PSUs
    "SAIL": "https://sailcareers.com/",
    "NALCO": "https://nalcoindia.com/careers/",
    "NMDC": "https://www.nmdc.co.in/Careers",
    "HMT Machine Tools": "http://www.hmtmachinetools.com/careers.html",

    # Oil & Mining
    "Coal India": "https://www.coalindia.in/career-cil/",
    "Oil India": "https://www.oil-india.com/Current_openings",
    "NLC India": "https://www.nlcindia.in/new_website/careers/CAREERS.htm",

    # Science & Research Labs
    "CSIR": "https://www.csir.res.in/career-opportunities",
    "IISc": "https://iisc.ac.in/positions-open/",
    "IITs (Common)": "https://iitb.ac.in/en/careers"  # IIT Bombay as representative
}

KEYWORDS = ["engineer", "recruitment", "vacancy", "it", "assistant", "scientist"]


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
    session.mount("http://", adapter)
    session.mount("https://", adapter)
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


def scrape_gov_jobs(urls=None, session=None):
    logger.info("🏛️ Scraping government job portals...")

    jobs = []
    seen = set()

    urls = urls or DEFAULT_URLS
    session = session or _build_session()

    for dept, base_url in urls.items():
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
                    "company": dept,
                    "source": base_url,
                })

            time.sleep(POLITE_DELAY)

        except Exception as e:
            logger.exception(f"Error scraping {dept}: {e}")

    logger.info(f"🏛️ GOV scraper found {len(jobs)} jobs")
    return jobs
