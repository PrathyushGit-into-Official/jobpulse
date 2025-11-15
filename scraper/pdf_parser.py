import io
import pdfplumber
from loguru import logger

DEFAULT_KEYWORDS = [
    "engineer",
    "developer",
    "assistant",
    "it",
    "vacancy",
    "recruitment",
]


def _iter_pages(pdf_data):
    """
    Accept either a file path or raw PDF bytes.
    """
    if isinstance(pdf_data, bytes):
        pdf = pdfplumber.open(io.BytesIO(pdf_data))
    else:
        pdf = pdfplumber.open(pdf_data)
    try:
        for page in pdf.pages:
            yield page
    finally:
        try:
            pdf.close()
        except Exception:
            pass


def parse_pdf_jobs(pdf_data, keywords=None, max_pages=50):
    keywords = keywords or DEFAULT_KEYWORDS
    jobs = []

    try:
        for page_number, page in enumerate(_iter_pages(pdf_data)):
            if page_number >= max_pages:
                break

            text = page.extract_text() or ""
            for line in text.splitlines():
                clean = line.strip()
                if not clean:
                    continue

                lower = clean.lower()
                if any(k in lower for k in keywords):
                    jobs.append({
                        "title": clean,
                        "link": str(pdf_data),
                        "company": "UNKNOWN",
                        "source": str(pdf_data)
                    })

    except Exception as e:
        logger.error("PDF parsing failed: %s", e)

    logger.info("📄 PDF parser found %d job-like lines", len(jobs))
    return jobs
