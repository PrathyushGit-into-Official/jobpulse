# scraper/pdf_parser.py
import pdfplumber
from loguru import logger

def parse_pdf_jobs(pdf_path, keywords=None):
    """
    Extracts lines from a PDF that look like job titles/announcements.
    Returns a list of job-like dicts:
      {'title': <line>, 'link': pdf_path, 'company': 'UNKNOWN', 'source': pdf_path}
    """
    if keywords is None:
        keywords = ["engineer", "developer", "assistant", "it", "vacancy", "recruitment"]

    jobs = []
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if not text:
                    continue
                for line in text.splitlines():
                    clean = line.strip()
                    if not clean:
                        continue
                    lower = clean.lower()
                    if any(k in lower for k in keywords):
                        jobs.append({
                            "title": clean,
                            "link": pdf_path,
                            "company": "UNKNOWN",
                            "source": pdf_path
                        })
    except Exception as e:
        logger.error(f"PDF parsing failed for {pdf_path}: {e}")

    logger.info(f"📄 PDF parser found {len(jobs)} potential job lines in {pdf_path}.")
    return jobs
