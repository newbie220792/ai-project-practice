from datetime import datetime

from app.config.config import ENABLE_SCHEDULE
from app.schedules import clear_no_faces_schedule, face_recognition_schedule, verify_camera_status
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()

def start():
    if ENABLE_SCHEDULE == "true":
        # scheduler.add_job(face_recognition_schedule, 'interval', seconds=60, max_instances=1)
        # scheduler.add_job(clear_no_faces_schedule, 'cron', hour=0, minute=5, max_instances=1)
        scheduler.add_job(verify_camera_status, 'interval', seconds=10, max_instances=1)
        scheduler.start()