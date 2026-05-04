
import os
import time
from flask.cli import load_dotenv

# Run it in crontab with the following command to clear the no_faces folder every day at midnight:
# 0 0 * * * /home/rasp/venv/bin/python /media/rasp/D1/imou/clear_no_faces.py
load_dotenv()

def clear_no_faces():
    working_dir = os.getenv("WORK_DIR")
    no_faces_folder = os.path.join(working_dir, "no_faces")
    
    if os.path.exists(no_faces_folder):
        for filename in os.listdir(no_faces_folder):
            file_path = os.path.join(no_faces_folder, filename)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")
            except Exception as e:
                print(f"Error deleting {file_path}: {e}")
    else:
        print(f"No 'no_faces' folder found at: {no_faces_folder}")

if __name__ == "__main__":
    clear_no_faces()