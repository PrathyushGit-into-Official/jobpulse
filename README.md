.

🚀 JobPulse — Automated Job Notifier for MNCs, PSUs & Banks
A lightweight, reliable 24×7 job-monitoring system for CSE freshers.
📌 Overview

JobPulse is a Python-based automation tool that monitors selected company career pages from:

🏢 Top MNCs

🏛️ Government / PSU Organizations

🏦 Banks

The system fetches new job postings directly from official career portals, filters roles relevant to CSE/IT freshers, stores them in a SQLite database, and sends instant alerts via Email and Telegram.

It eliminates the need to manually check multiple career pages and ensures you never miss important opportunities.

🌟 Key Features
🏢 Direct Scraping From Official Career Pages

JobPulse does not use job boards like LinkedIn/Indeed.
It reads job postings directly from selected companies, ensuring accuracy and no third-party dependencies.

🎯 Designed for CSE Freshers

Detects only:

Software Engineer

Developer

Programmer

IT/Tech roles

Internships / Trainee positions

🗄️ SQLite Job Database

Stores all fetched jobs

Prevents duplicates

Maintains job history

⚡ Instant Notifications

Get alerts immediately through:

📧 Email (SMTP)

📱 Telegram Bot API

🔁 Automatic 24×7 Operation

Works continuously through:

GitHub Actions

Cron jobs

Manual execution

🧩 Modular Structure

Each company has its own scraper module inside jobboards/, making the system easy to expand.

🧱 Project Structure
jobpulse/
│
├── main.py                     # Main runner
├── config.yaml                 # Configuration (keywords, companies, settings)
├── requirements.txt            # Dependencies
│
├── data/
│   └── jobs.db                 # SQLite database
│
├── jobboards/                  # Scrapers for selected career pages
│   ├── tcs.py
│   ├── infosys.py
│   ├── isro.py
│   ├── rbi.py
│   └── ...
│
└── utils/
    ├── db.py                   # Database operations
    └── notifier.py             # Email / Telegram notifications

⚙️ How It Works

Loads settings from config.yaml (keywords, company URLs, notification preferences).

Visits each selected company’s official career page.

Extracts job details (title, link, location, etc.).

Checks SQLite to avoid duplicate entries.

Sends alerts only for newly added jobs.

Repeats automatically on a fixed schedule.

✉️ Example Alert

Email:

JobPulse — New Opening Detected!

Company: ISRO
Role: Graduate Apprentice (Computer Science)
Location: Bengaluru
Apply: https://isro.gov.in/careers/1234


Telegram:

🔔 New Job Alert
ISRO — Graduate Apprentice (CSE)
Bengaluru
Apply Now ✓

🚀 Getting Started
1️⃣ Create & activate virtual environment
python -m venv venv


Activate:

Windows

venv\Scripts\activate


Linux/Mac

source venv/bin/activate

2️⃣ Install dependencies
pip install -r requirements.txt

3️⃣ Configure environment

Copy .env.example → .env and fill:

Email SMTP credentials

Telegram bot token

Chat ID

4️⃣ Configure job settings

Edit config.yaml to set:

Target companies

Keywords (software, developer, intern…)

Notification options

5️⃣ Run JobPulse
python main.py

🔁 Automation (24×7 Mode)
🟦 GitHub Actions (Recommended)

Runs every 6 hours (configurable)

Scrapes companies and saves DB

Uploads logs & database as artifacts

🟩 Local Cron Job

Run periodically on your local system or server.

🧩 Skills Demonstrated

This project showcases strong practical engineering skills in:

Python backend development

Web scraping (official career portals)

Automation & scheduling

Database handling (SQLite)

Notification systems (SMTP, Bot APIs)

Config-driven system design

Modular architecture

Perfect for SDE, Backend, Python, Automation, and Tools Developer roles.

🔮 Future Enhancements

Add more company scrapers

Add web dashboard (React/Streamlit)

Add role/category filters

Add Docker support

Add logging and monitoring

🏁 Summary

JobPulse is a clean, reliable, production-ready job-monitoring tool built for CSE freshers.
It tracks selected MNC, PSU, and Bank career pages and alerts you instantly when relevant openings appear.
Simple to configure, easy to extend, and powerful in daily use.