import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv


load_dotenv()
GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")

def send_alert(to_email, predicted_value, threshold, city):
    msg = EmailMessage()
    msg["Subject"] = f"PM2.5 Alert: {predicted_value} µg/m³ forecast in {city} "
    msg["From"] = GMAIL_USER
    msg["To"] = to_email

    msg.set_content(
        f"Air quality alert for {city}\n\n"
        f"Forecast PM2.5 for the next hour: {predicted_value} µg/m³\n"
        f"Your alert threshold: {threshold}µg/m³\n\n"
        f"Consider limiting prolonged outdoor activity, and keep windows "
        f"closed if levels stay elevated.\n\n"
        f"This is a forecast from a model trained on industrial sensor data "
        f"from Ploiesti, Romania. Predictions for other regions are estimates.\n"
        f"Data by Open-Meteo.com (CC BY 4.0)\n"
    )
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=10) as server:
            server.login(GMAIL_USER, GMAIL_PASSWORD)
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"Failed to sent to {to_email}: {e}")
        return False

def send_welcome(to_email, threshold, city):
    msg = EmailMessage()
    msg["Subject"] = f"Welcome to PM2.5 Air Quality Monitor"
    msg["From"] = GMAIL_USER
    msg["To"] = to_email

    msg.set_content(
        f"Thank you for subscribing to PM2.5 Air Quality Monitor!\n\n"
        f"Location: {city}\n"
        f"Your alert threshold: {threshold} µg/m³\n\n"
        f"You'll receive an email whenever the forecast PM2.5 in your area "
        f"is predicted to exceed your threshold.\n\n"
        f"---\n"
        f"This is a forecast from a model trained on industrial sensor data "
        f"from Ploiesti, Romania. Predictions for other regions are estimates.\n"
        f"Data by Open-Meteo.com (CC BY 4.0)\n"
    )

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=10) as server:
            server.login(GMAIL_USER, GMAIL_PASSWORD)
            server.send_message(msg)
            return True
    except Exception as e:
        print(f"Failed to sent welcome email to {to_email}: {e}")
        return False