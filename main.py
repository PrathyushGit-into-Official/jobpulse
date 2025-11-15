# main.py
import os
import sys
from datetime import datetime, timezone
from loguru import logger

from core.config import LOG_FILE
from utils.db import init_db, record_run
from scraper import scrape_mnc_jobs, scrape_gov_jobs, scrape_bank_jobs
from core.job_checker import check_and_notify

os.makedirs(os.path.dirname(str(LOG_FILE)), exist_ok=True)

logger.remove()
logger.add(str(LOG_FILE), rotation="5 MB", retention="14 days", enqueue=True)
logger.add(sys.stdout, level="INFO", enqueue=True)

def run_cycle():
    start_ts = datetime.now(timezone.utc)
    logger.info(f"🚀 JobPulse cycle started at {start_ts.isoformat()}")

    init_db()

    all_jobs = []
    for scraper, name in [
        (scrape_mnc_jobs, "MNC"),
        (scrape_gov_jobs, "GOV"),
        (scrape_bank_jobs, "BANK"),
    ]:
        try:
            results = scraper() or []
            logger.info(f"Scraper {name} returned {len(results)} items")
            all_jobs.extend(results)
        except Exception as e:
            logger.exception(f"Error during {name} scraping: {e}")

    try:
        summary = check_and_notify(all_jobs)
        success = True
    except Exception as e:
        logger.exception(f"check_and_notify failed: {e}")
        summary = None
        success = False

    try:
        record_run(
            started_at=start_ts,
            finished_at=datetime.now(timezone.utc),
            success=success,
            jobs_count=len(all_jobs),
        )
    except Exception as e:
        logger.exception(f"Run record failed: {e}")

    logger.info("Cycle finished.")
    return summary


if __name__ == '__main__':
    try:
        run_cycle()
    except Exception as e:
        logger.exception(f"Fatal error in main: {e}")
        sys.exit(1)
