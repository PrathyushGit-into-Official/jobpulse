import signal
import sys
from loguru import logger
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

from core.config import SCRAPE_INTERVAL_HOURS, DATABASE_PATH

def _get_runner():
    try:
        from main import run_cycle
        return run_cycle
    except Exception as e:
        logger.error("Failed to import run_cycle: %s", e)
        return None

def _make_jobstore_url(db_path):
    return f"sqlite:///{str(db_path)}"

def start_scheduler():
    runner = _get_runner()
    if not runner:
        logger.error("Scheduler cannot start — run_cycle missing.")
        return

    jobstores = {
        "default": SQLAlchemyJobStore(
            url=_make_jobstore_url(DATABASE_PATH)
        )
    }

    scheduler = BlockingScheduler(jobstores=jobstores)

    scheduler.add_job(
        runner,
        "interval",
        hours=SCRAPE_INTERVAL_HOURS,
        id="jobpulse_cycle",
        replace_existing=True,
        max_instances=1,
        coalesce=True,
    )

    def shutdown(_sig, _frame):
        logger.info("Scheduler shutting down.")
        try:
            scheduler.shutdown(wait=False)
        finally:
            sys.exit(0)

    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    logger.info("⏱️ Scheduler started (every %s hours).", SCRAPE_INTERVAL_HOURS)

    scheduler.start()
