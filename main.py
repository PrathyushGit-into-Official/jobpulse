# main.py
import os
from loguru import logger
from scraper import scrape_mnc_jobs, scrape_gov_jobs, scrape_bank_jobs
from utils.db import init_db
from core.job_checker import check_and_notify
from core.config import LOG_FILE

# Ensure logs folder exists and configure logger
os.makedirs("logs", exist_ok=True)
logger.add(LOG_FILE, rotation="5 MB", retention="14 days", level="INFO")

def run_cycle():
    logger.info("🚀 JobPulse cycle started.")
    init_db()

    all_jobs = []
    all_jobs += scrape_mnc_jobs()
    all_jobs += scrape_gov_jobs()
    all_jobs += scrape_bank_jobs()

    check_and_notify(all_jobs)
    logger.info("✅ Cycle completed successfully.")

if __name__ == "__main__":
    run_cycle()
