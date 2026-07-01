import os
import shutil

UPLOAD_DIR = "/media/rasp/D1/imou/uploads"

def _move_file():
    try:
        files = sorted([
            f for f in os.listdir(UPLOAD_DIR)
        ])

        total_files = len(files)
        if total_files == 0:
            print("No images to process.")
            return
        dst = ''
        for index, file_name in enumerate(files, start=1):
            if not file_name.__contains__('.'):
                continue
            remaining = total_files - index

            if _is_image(file_name):
                dst = os.path.join(
                    UPLOAD_DIR,
                    'images'
                )
            elif _is_video(file_name):
                dst = os.path.join(
                    UPLOAD_DIR,
                    'videos'
                )
            else: 
                dst = os.path.join(
                    UPLOAD_DIR,
                    'documents'
                )

            print(
                f"Processing image: {file_name} "
                f"({index}/{total_files}) - Remaining: {remaining}"
            )
            
            source_path = f"{UPLOAD_DIR}/{file_name}"
            destination_path = f"{dst}/{file_name}"

            shutil.move(source_path, destination_path)

    except FileNotFoundError:
        print(f"File not found: {source_path}")

    except Exception as e:
        print(f"Move failed: {e}")

def _is_image(f) -> bool:
    return f.endswith(".jpg") or f.endswith(".png")

def _is_video(f) -> bool:
    return f.endswith(".mp4")

_move_file()