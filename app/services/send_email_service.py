import os
import smtplib

from flask import json
from app import logger

def send_email(subject, body, to):
    # Implement your email sending logic here using smtplib or any email service provider API
    # Example using smtplib:
    with open("email_info.json", "r") as f:
        email_config = json.load(f)
    
    sender_email = email_config["email"]
    sender_password = email_config["password"]
    message = f"Subject: {subject}\n\n{body}"
    try:
        with smtplib.SMTP(email_config["smtp_server"], email_config["smtp_port"]) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, to, message)
            logger.info(f"Email sent to {to} with subject: {subject}")
    except Exception as e:
        logger.error(f"Failed to send email: {e}") 