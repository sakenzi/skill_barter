import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os


load_dotenv()

async def send_email_message(to_email: str, subject: str, body: str):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = os.getenv("SMTP_USER")
    msg["To"] = to_email

    with smtplib.SMTP(os.getenv("SMTP_HOST"), os.getenv("SMTP_PORT")) as server:
        server.starttls()
        server.login(os.getenv("SMTP_USER"), os.getenv("SMTP_PASS"))
        server.sendmail(os.getenv("SMTP_USER"), to_email, msg.as_string())