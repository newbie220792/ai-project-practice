from app.config.config import WORKING_DIR
import os
import datetime

# Run it in crontab with the following command to clear the no_faces folder every day at midnight:
# 0 0 * * * /home/rasp/venv/bin/python /media/rasp/D1/imou/clear_no_faces.py

def _is_previous_day(file_path):
    try:
        mtime = os.path.getmtime(file_path)
    except OSError:
        return False

    file_date = datetime.date.fromtimestamp(mtime)
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    return file_date == yesterday

def _clear_no_faces():
    no_faces_folder = os.path.join(WORKING_DIR, "no_faces")
    
    if os.path.exists(no_faces_folder):
        for filename in os.listdir(no_faces_folder):
            file_path = os.path.join(no_faces_folder, filename)
            try:
                if os.path.isfile(file_path) and _is_previous_day(file_path):
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")
            except Exception as e:
                print(f"Error deleting {file_path}: {e}")
    else:
        print(f"No 'no_faces' folder found at: {no_faces_folder}")

def _clear_captured_images():
    captured_images_folder = os.path.join(WORKING_DIR, "capture_imou")
    
    if os.path.exists(captured_images_folder):
        for filename in os.listdir(captured_images_folder):
            file_path = os.path.join(captured_images_folder, filename)
            try:
                if os.path.isfile(file_path) and _is_previous_day(file_path):
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")
            except Exception as e:
                print(f"Error deleting {file_path}: {e}")
    else:
        print(f"No 'capture_imou' folder found at: {captured_images_folder}")


def run_scheduler():
    _clear_no_faces()
    _clear_captured_images()