# JobPulse 24×7

Automated job alert system that scrapes MNC, PSU, and bank job portals 24×7 and notifies via Email + Telegram.

## Run Locally
1. `python -m venv venv`
2. `.\venv\Scripts\activate`
3. `pip install -r requirements.txt`
4. Add your `.env` with Gmail + Telegram credentials
5. Run: `python main.py`

## Automate
Use `.github/workflows/jobpulse.yml` to schedule runs every 6 hours via GitHub Actions.
