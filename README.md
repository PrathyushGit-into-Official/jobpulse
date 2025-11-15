# JobPulse 24×7 (Final Production Version)

JobPulse is an automated job-scraping + alerting engine that checks MNC, PSU/Government,
and Bank job portals every cycle and sends alerts via Email + Telegram.

## Setup
1. python -m venv venv
2. Activate venv
3. pip install -r requirements.txt
4. Copy .env.example → .env and fill credentials
5. Run: python main.py

## Automation
- GitHub Actions workflow runs every 6 hours.
- Logs + DB uploaded as artifacts.
