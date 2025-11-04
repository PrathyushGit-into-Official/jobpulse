# core/scheduler.py
from apscheduler.schedulers.blocking import BlockingScheduler
from loguru import logger
from core.config import SCRAPE_INTERVAL_HOURS

def _get_runner():
    """
    Import the run_cycle function lazily to avoid circular imports
    (main imports scheduler; scheduler should not import main at module load).
    """
    try:
        from main import run_cycle
        return run_cycle
    except Exception as e:
        logger.error(f"Could not import run_cycle from main: {e}")
        return None

def start_scheduler():
    """
    Start a blocking scheduler that runs run_cycle() every SCRAPE_INTERVAL_HOURS.
    Use lazy import to avoid circular imports when this module is imported.
    """
    runner = _get_runner()
    if not runner:
        logger.error("Scheduler cannot start: runner not available.")
        return

    scheduler = BlockingScheduler()
    scheduler.add_job(runner, "interval", hours=SCRAPE_INTERVAL_HOURS)
    logger.info(f"🔁 Scheduler started: runs every {SCRAPE_INTERVAL_HOURS} hours.")
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logger.info("Scheduler stopped by user.")
    except Exception as e:
        logger.error(f"Scheduler error: {e}")
