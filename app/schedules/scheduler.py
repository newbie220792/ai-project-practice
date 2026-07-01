from datetime import datetime

from app.config.config import ENABLE_SCHEDULE
from app.schedules import *
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()

def start():
    if ENABLE_SCHEDULE == "true":
        scheduler.add_job(face_recognition_schedule, 'interval', seconds=60, max_instances=1)
        scheduler.add_job(clear_no_faces_schedule, 'cron', hour=0, minute=5, max_instances=1)
        scheduler.add_job(verify_camera_status, 'interval', hours=1, max_instances=1)
        scheduler.add_job(publish_monitoring_data, 'interval', seconds=3, max_instances=1)
        #scheduler.add_job(weather_tracking_schedule, 'interval', seconds=60, max_instances=1)
        scheduler.add_job(verify_hdd_health, 'interval', hours=24, max_instances=1)
        scheduler.start()
