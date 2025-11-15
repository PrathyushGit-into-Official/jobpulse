# Deployment Guide — JobPulse 24×7

This guide covers three recommended deployment approaches: GitHub Actions (CI), Docker (VPS/host), and systemd (VM). Use the one that best fits your needs.

---

## Prerequisites
- Python 3.9+ (3.10 recommended)
- Create `.env` from `.env.example` and fill required secrets:
  - `EMAIL_USER` (Gmail address)
  - `EMAIL_PASS` (Gmail App Password)
  - `TELEGRAM_TOKEN`
  - `TELEGRAM_CHAT_ID`

---

## Option A — GitHub Actions (scheduled)
1. Add secrets to your GitHub repository:
   - `EMAIL_USER`, `EMAIL_PASS`, `TELEGRAM_TOKEN`, `TELEGRAM_CHAT_ID`
2. Push repo; workflow `.github/workflows/jobpulse.yml` runs every 6 hours.
3. Inspect artifacts (logs/app.log, data/jobs.db) in action run details when needed.

Pros: zero server maintenance.  
Cons: ephemeral runner; DB only persisted via artifacts (downloaded manually).

---

## Option B — Docker (recommended for always-on)
1. Build image:
   ```bash
   docker build -t jobpulse:latest .
