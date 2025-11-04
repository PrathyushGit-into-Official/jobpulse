# utils/notifier.py
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from loguru import logger
import telebot

load_dotenv()

EMAIL = os.getenv("EMAIL_USER")
PASSWORD = os.getenv("EMAIL_PASS")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_email(subject: str, body: str, to_email: str = None):
    """Send an email via Gmail SMTP (App Password recommended)."""
    if not EMAIL or not PASSWORD:
        logger.warning("Email creds missing; skipping email send.")
        return

    recipient = to_email or EMAIL
    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL
        msg["To"] = recipient
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL, PASSWORD)
            server.send_message(msg)

        logger.info("📧 Email sent successfully.")
    except Exception as e:
        logger.error(f"❌ Email failed: {e}")

def send_telegram(message: str):
    """Send message using Telegram Bot API (if configured)."""
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        logger.warning("Telegram creds missing; skipping Telegram send.")
        return

    try:
        bot = telebot.TeleBot(TELEGRAM_TOKEN)
        bot.send_message(TELEGRAM_CHAT_ID, message)
        logger.info("💬 Telegram message sent successfully.")
    except Exception as e:
        logger.error(f"❌ Telegram failed: {e}")

def send_notification(jobs_or_message):
    """
    Unified notification helper (keeps tests and callers simple).
    Accepts either a string message or list of job dicts.
    """
    if isinstance(jobs_or_message, str):
        body = jobs_or_message
    else:
        # list of job dicts
        lines = []
        for j in jobs_or_message:
            t = j.get("title", "").strip()
            l = j.get("link", "")
            c = j.get("company", "")
            lines.append(f"{t}\n{l}\n({c})")
        body = "\n\n".join(lines) if lines else "No jobs."

    send_email("New JobPulse Alerts", body)
    send_telegram(f"🚨 New JobPulse Alerts:\n\n{body}")
