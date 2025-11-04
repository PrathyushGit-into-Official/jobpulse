# utils/db.py
import sqlite3
from loguru import logger
from pathlib import Path

DB_PATH = Path("data/jobs.db")

def init_db(db_path: Path = DB_PATH):
    """Initialize DB and ensure folder exists."""
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            link TEXT UNIQUE,
            company TEXT,
            source TEXT
        );
    """)
    conn.commit()
    conn.close()
    logger.info(f"✅ Database initialized at {db_path}.")

def job_exists(link: str, db_path: Path = DB_PATH) -> bool:
    conn = sqlite3.connect(db_path)
    cur = conn.execute("SELECT 1 FROM jobs WHERE link = ?", (link,))
    exists = cur.fetchone() is not None
    conn.close()
    return exists

def add_job(title: str, link: str, company: str, source: str, db_path: Path = DB_PATH):
    try:
        conn = sqlite3.connect(db_path)
        conn.execute(
            "INSERT OR IGNORE INTO jobs (title, link, company, source) VALUES (?, ?, ?, ?)",
            (title, link, company, source),
        )
        conn.commit()
        conn.close()
        logger.info(f"🆕 Job saved: {title} ({company})")
    except Exception as e:
        logger.error(f"❌ Failed to save job '{title}': {e}")

def save_job_if_new(job, db_path: Path = DB_PATH):
    """
    Compatibility function for tests:
    Accepts either dict with keys (title, link, company, last_date/source) or positional-like.
    Returns True if inserted, False if already exists.
    """
    if isinstance(job, dict):
        title = job.get("title")
        link = job.get("link")
        company = job.get("company", "")
        source = job.get("source", job.get("link", ""))
    else:
        # fallback - not expected
        logger.warning("save_job_if_new received non-dict job")
        return False

    if not link:
        logger.warning("save_job_if_new: job missing link")
        return False

    if job_exists(link, db_path):
        return False

    add_job(title, link, company, source, db_path=db_path)
    return True
