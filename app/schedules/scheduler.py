from app.config.config import ENABLE_SCHEDULE
from app.schedules import clear_no_faces_schedule, face_recognition_schedule
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()

def start():
    if ENABLE_SCHEDULE == "true":
        scheduler.add_job(face_recognition_schedule, 'interval', seconds=10, max_instances=1)
        # scheduler.add_job(clear_no_faces_schedule, 'interval', seconds=10)
        scheduler.start()


# def start():
#     while True:
#         face_recognition_schedule()
#         time.sleep(10)  # nghỉ sau khi chạy xong