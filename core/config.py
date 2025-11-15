import os
from pathlib import Path

SCRAPE_INTERVAL_HOURS = int(os.getenv("JOBPULSE_INTERVAL_HOURS", "6"))

DEFAULT_KEYWORDS = ["engineer", "developer", "analyst", "it", "computer"]
KEYWORDS = os.getenv("JOBPULSE_KEYWORDS", ",".join(DEFAULT_KEYWORDS)).split(",")

DATABASE_PATH = Path(os.getenv("JOBPULSE_DB_PATH", "data/jobs.db"))
LOG_FILE = Path(os.getenv("JOBPULSE_LOG_FILE", "logs/app.log"))

DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
