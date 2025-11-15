# utils/db.py
import os
import sqlite3
import datetime
from pathlib import Path
from loguru import logger

DEFAULT_DB_PATH = Path(os.getenv("JOBPULSE_DB_PATH", "data/jobs.db"))
DB_TIMEOUT_SECONDS = int(os.getenv("JOBPULSE_DB_TIMEOUT", "30"))


def _resolve_path(p: Path) -> Path:
    p = Path(p)
    if not p.is_absolute():
        p = Path.cwd() / p
    p.parent.mkdir(parents=True, exist_ok=True)
    return p


def _get_connection(db_path: Path = DEFAULT_DB_PATH) -> sqlite3.Connection:
    db_path = _resolve_path(db_path)
    conn = sqlite3.connect(str(db_path), timeout=DB_TIMEOUT_SECONDS, detect_types=sqlite3.PARSE_DECLTYPES)
    try:
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA synchronous=NORMAL;")
    except Exception:
        logger.debug("Could not set PRAGMA on SQLite (non-fatal).")
    return conn


def init_db(db_path: Path = DEFAULT_DB_PATH):
    db_path = _resolve_path(db_path)
    conn = _get_connection(db_path)
    try:
        with conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS jobs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT,
                    link TEXT UNIQUE,
                    company TEXT,
                    source TEXT
                );
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS runs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    started_at TIMESTAMP,
                    finished_at TIMESTAMP,
                    success INTEGER,
                    jobs_count INTEGER
                );
                """
            )
        logger.info(f"✅ Database initialized at {db_path}")
    except Exception as e:
        logger.exception(f"Failed to initialize DB at {db_path}: {e}")
    finally:
        conn.close()


def job_exists(link: str, db_path: Path = DEFAULT_DB_PATH) -> bool:
    db_path = _resolve_path(db_path)
    conn = _get_connection(db_path)
    try:
        cur = conn.execute("SELECT 1 FROM jobs WHERE link = ? LIMIT 1", (link,))
        return cur.fetchone() is not None
    except Exception as e:
        logger.error(f"Error checking job existence for {link}: {e}")
        return False
    finally:
        conn.close()


def add_job(title: str, link: str, company: str, source: str, db_path: Path = DEFAULT_DB_PATH) -> bool:
    db_path = _resolve_path(db_path)
    conn = _get_connection(db_path)
    try:
        with conn:
            cur = conn.execute(
                "INSERT OR IGNORE INTO jobs (title, link, company, source) VALUES (?, ?, ?, ?)",
                (title, link, company, source),
            )
            inserted = cur.rowcount > 0
            if inserted:
                logger.info(f"🆕 Job saved: {title} ({company})")
            else:
                logger.debug(f"Job already exists (ignored): {link}")
            return inserted
    except sqlite3.IntegrityError as e:
        logger.debug(f"IntegrityError when adding job {link}: {e}")
        return False
    except Exception as e:
        logger.exception(f"Failed to save job {title}: {e}")
        return False
    finally:
        conn.close()


def save_job_if_new(job, db_path: Path = DEFAULT_DB_PATH) -> bool:
    """
    Compatibility helper used by tests and external callers.
    Accepts dict with keys 'title','link','company','source' and inserts if new.
    """
    if not isinstance(job, dict):
        logger.warning("save_job_if_new received non-dict input.")
        return False

    title = job.get("title")
    link = job.get("link")
    company = job.get("company", "")
    source = job.get("source", job.get("link", ""))

    if not link:
        logger.warning("save_job_if_new: job missing link")
        return False

    if job_exists(link, db_path=db_path):
        return False

    return add_job(title, link, company, source, db_path=db_path)


def record_run(started_at=None, finished_at=None, success=True, jobs_count=0, db_path: Path = DEFAULT_DB_PATH):
    started_at = started_at or datetime.datetime.utcnow()
    finished_at = finished_at or datetime.datetime.utcnow()
    db_path = _resolve_path(db_path)
    conn = _get_connection(db_path)
    try:
        with conn:
            conn.execute(
                "INSERT INTO runs (started_at, finished_at, success, jobs_count) VALUES (?, ?, ?, ?)",
                (started_at, finished_at, int(bool(success)), int(jobs_count)),
            )
    except Exception as e:
        logger.exception(f"Failed to record run: {e}")
    finally:
        conn.close()


def get_last_run(db_path: Path = DEFAULT_DB_PATH):
    db_path = _resolve_path(db_path)
    conn = _get_connection(db_path)
    try:
        cur = conn.execute(
            "SELECT id, started_at, finished_at, success, jobs_count FROM runs ORDER BY id DESC LIMIT 1"
        )
        row = cur.fetchone()
        if not row:
            return None
        return {
            "id": row[0],
            "started_at": row[1],
            "finished_at": row[2],
            "success": bool(row[3]),
            "jobs_count": row[4],
        }
    except Exception as e:
        logger.exception(f"Failed to fetch last run: {e}")
        return None
    finally:
        conn.close()
