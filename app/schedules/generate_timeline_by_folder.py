
import os
import subprocess

INPUT_DIR = "/data/photos"
OUTPUT_DIR = "/data/videos"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def get_images(folder):
    exts = (".jpg", ".jpeg", ".png")
    files = [f for f in os.listdir(folder) if f.lower().endswith(exts)]
    files.sort(key=lambda x: os.path.getmtime(os.path.join(folder, x)))
    return [os.path.join(folder, f) for f in files]


def write_concat_list(images, path):
    with open(path, "w") as f:
        for img in images:
            f.write(f"file '{img}'\n")
            f.write("duration 1.5\n")
        f.write(f"file '{images[-1]}'\n")


def build_video(folder):
    images = get_images(folder)

    if len(images) < 5:
        return

    name = os.path.basename(folder)
    list_file = f"/tmp/{name}.txt"
    output = os.path.join(OUTPUT_DIR, f"{name}.mp4")

    write_concat_list(images, list_file)

    cmd = [
        "sudo",
        "ffmpeg",
        "-framerate 1/3",
        "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", list_file,
        "-vsync", "vfr",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-r 30 ",
        "-vf", "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2",
        "-preset", "veryfast"
    ]

    subprocess.run(cmd, check=True)
    print("done:", output)


def main():
    for folder in sorted(os.listdir(INPUT_DIR)):
        path = os.path.join(INPUT_DIR, folder)
        if os.path.isdir(path):
            print("Processing:", folder)
            build_video(path)


if __name__ == "__main__":
    main()


def generate_timeline_by_folder(folder_path):
    # Placeholder for the actual implementation
    # This function would contain logic to generate a timeline based on the contents of the specified folder
    print(f"Generating timeline for folder: {folder_path}")