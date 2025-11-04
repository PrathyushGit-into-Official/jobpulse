# tests/test_email.py
# Simple manual test script — doesn't run in CI unless env has credentials.
import os
import smtplib
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv()

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
TO_EMAIL = EMAIL_USER

def send_test_email():
    if not EMAIL_USER or not EMAIL_PASS:
        print("Email creds not set in .env — skipping.")
        return

    subject = "✅ JobPulse Email Test"
    body = "This is a test email from JobPulse — your email system works fine!"

    msg = MIMEMultipart()
    msg["From"] = EMAIL_USER
    msg["To"] = TO_EMAIL
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASS)
            server.send_message(msg)
        print("✅ Test email sent successfully!")
    except Exception as e:
        print("❌ Failed to send email:", e)

if __name__ == "__main__":
    send_test_email()
