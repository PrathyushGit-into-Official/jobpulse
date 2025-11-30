JobPulse – Automated Job Notifier for MNCs, PSUs, and Banks
A clean and reliable job-monitoring system designed for CSE freshers.

Overview
JobPulse is a Python-based automation tool that continuously checks selected company career pages, including major MNCs, Government and PSU organizations, and Banks.
It fetches job postings directly from official career portals, filters openings relevant to CSE and IT freshers, stores them in a SQLite database, and sends alerts through Email and Telegram.
The goal is to eliminate the need for manual checking and ensure that no important opportunities are missed.

Core Features

Direct Career Page Scraping
JobPulse does not rely on third-party job boards. It retrieves job listings directly from the official websites of selected companies. This ensures accuracy and avoids dependency on external job platforms.

Focus on CSE Freshers
The system is optimized to detect roles such as Software Engineer, Developer, Programmer, IT positions, internships, and trainee roles.
Only relevant CSE openings are included.

SQLite Database for Storage
Job postings are stored in a local SQLite database.
Duplicate job entries are automatically filtered out, and complete job history is maintained.

Instant Job Notifications
Whenever a new job is detected, JobPulse immediately sends alerts through both Email and Telegram, ensuring quick visibility of fresh opportunities.

Always-On Automation
JobPulse can run continuously using GitHub Actions, cron jobs, or manual execution.
It is capable of operating 24×7 without user intervention.

Modular and Maintainable Design
Each company has its own scraper module located inside the jobboards directory.
Adding support for new companies requires only one new scraper file, making the system easy to extend.

Project Structure
The project contains:

main.py: The main execution script.

config.yaml: Contains keywords, company URLs, preferences, and notification settings.

requirements.txt: List of dependencies.

data/jobs.db: The SQLite job database.

jobboards/: A directory containing individual scraper files for each selected company.

utils/db.py: Handles database operations.

utils/notifier.py: Handles email and telegram notifications.

Process Flow

Load settings from config.yaml.

Visit each company’s official career page.

Extract job title, location, apply link, and related fields.

Check if the job already exists in the database.

Save new jobs and send alerts.

Repeat at the next scheduled interval.

Notification Examples
Email notification includes job title, company name, location, and the official apply link.
Telegram notification provides a concise job alert with the apply link.

How to Use

Create and activate a virtual environment.

Install required dependencies.

Copy the .env.example file to .env and fill in the SMTP details, Telegram bot token, and chat ID.

Update config.yaml to specify the companies to monitor, role keywords, and notification preferences.

Run the application using python main.py.

Automation Options
GitHub Actions can run the tool automatically at fixed intervals, typically every six hours.
Alternatively, the tool can be run periodically using a local cron job or Task Scheduler.

Technical Skills Demonstrated
This project reflects skills in Python backend development, career-page web scraping, automation and scheduling, SQLite database operations, email and telegram notifications, structured configuration using YAML, and modular software design.
It demonstrates the ability to build practical and production-ready automation tools.

Future Improvements
Possible enhancements include adding more company scrapers, adding a dashboard (using Streamlit or React), Docker support, advanced job filtering, and integrated logging and monitoring.

Summary
JobPulse is a practical and production-ready job monitoring system tailored for CSE freshers.
It keeps track of selected MNC, PSU, and Bank career pages and immediately alerts users when fresh job postings are released.
It is easy to configure, extend, and operate, making it a powerful tool for job seekers.