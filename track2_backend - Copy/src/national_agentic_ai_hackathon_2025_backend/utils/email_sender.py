import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from national_agentic_ai_hackathon_2025_backend.config import Config
from national_agentic_ai_hackathon_2025_backend._debug import Logger
from typing import List, Optional

def send_email(receiver_email: str, subject: str, body: str) -> bool:
    """Send an email using Gmail SMTP with an app password."""

    # Load credentials from config or env
    sender_email = Config.sender_email
    app_password = Config.app_password

    # Validate inputs
    if not receiver_email:
        raise ValueError("Receiver email is required.")
    if not subject:
        raise ValueError("Email subject is required.")
    if not body:
        raise ValueError("Email body is required.")

    # Build the email
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))
    Logger.debug(f"Raw email data - To: {receiver_email}, Subject: {subject}, Body: {body}")

    # Send the email
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, app_password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        Logger.success("✅ Email sent successfully!")
        return True
    except Exception as e:
        Logger.error(f"❌ Error sending email: {e}")
        return False
