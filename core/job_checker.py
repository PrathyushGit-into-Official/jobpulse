# core/job_checker.py
from loguru import logger
from utils.db import job_exists, add_job
from utils.notifier import send_email, send_telegram

def check_and_notify(jobs):
    """
    Accepts list of job dicts {title, link, company, source}
    Stores new ones and notifies user.
    """
    if not jobs:
        logger.info("No jobs to check.")
        return

    new_jobs = []
    for job in jobs:
        link = job.get("link")
        title = job.get("title")
        company = job.get("company", "Unknown")
        source = job.get("source", "Unknown")

        if not link or not title:
            continue

        if not job_exists(link):
            add_job(title, link, company, source)
            new_jobs.append(job)

    if new_jobs:
        logger.info(f"Found {len(new_jobs)} new jobs.")
        msg = "\n\n".join([f"{j['title']}\n{j['link']}\n({j['company']})" for j in new_jobs])
        send_email("New JobPulse Alerts", msg)
        send_telegram(f"🚨 New Job Openings:\n\n{msg}")
    else:
        logger.info("No new jobs found this cycle.")
