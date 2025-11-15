# utils/notifier.py
import os
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from loguru import logger
import requests

load_dotenv()

EMAIL = os.getenv("EMAIL_USER")
PASSWORD = os.getenv("EMAIL_PASS")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

RETRIES = int(os.getenv("NOTIFIER_RETRIES", "3"))
INITIAL_BACKOFF = float(os.getenv("NOTIFIER_BACKOFF", "1.0"))
SMTP_TIMEOUT = float(os.getenv("SMTP_TIMEOUT", "10.0"))
HTTP_TIMEOUT = float(os.getenv("HTTP_TIMEOUT", "8.0"))


def _retry_loop(fn, *args, retries=RETRIES, initial_backoff=INITIAL_BACKOFF, **kwargs):
    backoff = initial_backoff
    last_exc = None
    for attempt in range(1, retries + 1):
        try:
            result = fn(*args, **kwargs)
            return True, result
        except Exception as e:
            last_exc = e
            logger.warning(f"Attempt {attempt}/{retries} failed: {e}")
            if attempt < retries:
                time.sleep(backoff)
                backoff *= 2
    logger.error(f"All {retries} attempts failed. Last error: {last_exc}")
    return False, last_exc


def send_email(subject: str, body: str, to_email: str = None) -> bool:
    """Send an email via Gmail SMTP. Returns True on success."""
    if not EMAIL or not PASSWORD:
        logger.warning("Email credentials missing; skipping email send.")
        return False

    recipient = to_email or EMAIL

    def _send():
        msg = MIMEMultipart()
        msg["From"] = EMAIL
        msg["To"] = recipient
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP("smtp.gmail.com", 587, timeout=SMTP_TIMEOUT)
        try:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(EMAIL, PASSWORD)
            server.send_message(msg)
        finally:
            try:
                server.quit()
            except Exception:
                pass
        return True

    ok, result = _retry_loop(_send)
    if ok:
        logger.info(f"📧 Email sent successfully to {recipient}")
        return True
    else:
        logger.error(f"❌ Email failed after retries: {result}")
        return False


def _send_telegram_via_api(message: str) -> bool:
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        raise RuntimeError("Telegram credentials missing")

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    r = requests.post(url, json=payload, timeout=HTTP_TIMEOUT)
    r.raise_for_status()
    data = r.json()
    if not data.get("ok"):
        raise RuntimeError(f"Telegram API error: {data}")
    return True


def send_telegram(message: str) -> bool:
    """Send Telegram message. Returns True on success."""
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        logger.warning("Telegram credentials missing; skipping Telegram send.")
        return False

    ok, result = _retry_loop(_send_telegram_via_api, message)
    if ok:
        logger.info("💬 Telegram sent successfully.")
        return True
    else:
        logger.error(f"❌ Telegram failed after retries: {result}")
        return False


def send_notification(jobs_or_message):
    """
    Unified notifier. Accepts either a string or a list of job dicts.
    Returns {'email': bool, 'telegram': bool}
    """
    if isinstance(jobs_or_message, str):
        body = jobs_or_message
    else:
        lines = []
        for j in jobs_or_message:
            t = j.get("title", "").strip()
            l = j.get("link", "")
            c = j.get("company", "")
            lines.append(f"{t}\n{l}\n({c})")
        body = "\n\n".join(lines) if lines else "No jobs."

    # Keep telegram message length reasonable
    telegram_body = f"🚨 New JobPulse Alerts:\n\n{body[:3500]}"

    email_ok = send_email("New JobPulse Alerts", body)
    telegram_ok = send_telegram(telegram_body)

    return {"email": email_ok, "telegram": telegram_ok}
