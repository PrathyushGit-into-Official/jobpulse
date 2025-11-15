# core/job_checker.py
from datetime import datetime
from loguru import logger
from utils import db as _db
from utils import notifier as _notifier

def _safe_notify(new_jobs):
    try:
        return _notifier.send_notification(new_jobs) or {}
    except Exception as e:
        logger.exception(f"Notification sending failed: {e}")
        return {"email": False, "telegram": False}

def check_and_notify(jobs):
    started_at = datetime.utcnow()
    total = len(jobs) if jobs else 0
    logger.info(f"Checking {total} jobs...")

    if not jobs:
        logger.info("No jobs scraped.")
        return {
            "new_jobs": 0,
            "stored": 0,
            "notified": False,
            "notifications": {},
            "started_at": started_at.isoformat(),
            "finished_at": datetime.utcnow().isoformat(),
        }

    new_jobs = []
    stored_count = 0

    for job in jobs:
        try:
            link = job.get("link")
            title = job.get("title")

            if not link or not title:
                continue

            if not _db.job_exists(link):
                inserted = _db.add_job(
                    title,
                    link,
                    job.get("company", "Unknown"),
                    job.get("source", "Unknown"),
                )
                if inserted:
                    new_jobs.append(job)
                    stored_count += 1

        except Exception as e:
            logger.exception(f"Job processing failed: {e}")

    notified = False
    notifications = {}

    if new_jobs:
        logger.info(f"Found {len(new_jobs)} new jobs.")
        notifications = _safe_notify(new_jobs)
        notified = bool(notifications.get("email") or notifications.get("telegram"))
    else:
        logger.info("No new jobs found this cycle.")

    finished_at = datetime.utcnow()

    summary = {
        "new_jobs": len(new_jobs),
        "stored": stored_count,
        "notified": notified,
        "notifications": notifications,
        "started_at": started_at.isoformat(),
        "finished_at": finished_at.isoformat(),
    }

    logger.info(f"Summary: {summary}")
    return summary
