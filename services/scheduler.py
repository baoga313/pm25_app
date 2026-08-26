from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler

from services.db import get_subscribers, mark_alerted
from services.predictor import predict_pm25
from services.geocode import get_city_name
from services.email_service import send_alert

COOLDOWN_HOURS = 12


def check_and_alert():
    subscribers = get_subscribers()
    print(f"[scheduler] Checking {len(subscribers)} subscribers")

    for sub in subscribers:
        email = sub["email"]
        lat = sub["lat"]
        lon = sub["lon"]
        threshold= float(sub["threshold"])
        last_alerted = sub["last_alerted"]
        # cooldown check
        if last_alerted is not None:
            elapsed = datetime.now() - last_alerted
            if elapsed < timedelta(hours = COOLDOWN_HOURS):
                continue
        # predict, compare and sent
        try:
            prediction = predict_pm25(lat, lon)
        except Exception as e:
            print(f"[Scheduler] Prediction failed for {email}: {e}")
            continue

        if prediction > threshold:
            city =  get_city_name(lat, lon)
            if send_alert(email, prediction, threshold, city):
                mark_alerted(email)
                print(f"[Scheduler] Alerted {email}: {prediction} > {threshold}")
        


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(check_and_alert, "interval", hours=1)
    scheduler.start()
    print("[Scheduler] Started - checking hourly")