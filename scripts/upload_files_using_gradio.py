import gradio as gr
import shutil
import os

UPLOAD_DIR = "/media/rasp/D/imou/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def save_file(files) -> str:
    if len(files) <= 0:
        return 'File is empty', None
    dst = ''
    for file in files:
        if _is_image(file):
            dst = os.path.join(
                UPLOAD_DIR,
                'images',
                os.path.basename(file.name)
            )
        elif _is_video(file):
            dst = os.path.join(
                UPLOAD_DIR,
                'videos',
                os.path.basename(file.name)
            )
        else:
            dst = os.path.join(
                UPLOAD_DIR,
                'documents',
                os.path.basename(file.name)
            )
        shutil.copy(file.name, dst)

    return 'Upload file success!!!', gr.File(value=None)

def _is_image(f:gr.File) -> bool:
    return f.endswith(".jpg") or f.endswith(".png")

def _is_video(f:gr.File) -> bool:
    return f.endswith(".mp4") or f.endswith(".")

def remove_file(files):
   for f in files: 
       print(f.name)
   return  gr.File(value=None)

def toggle_button(files):
    enabled = files is not None and len(files) > 0
    return gr.Button(interactive=enabled)

with gr.Blocks() as demo:
    files = gr.File(file_count="multiple")
    output = gr.Textbox()

    btn = gr.Button(value="Upload", interactive=False)
    btnRemove = gr.Button(value="Remove")

    files.change(
        fn=toggle_button,
        inputs=files,
        outputs=btn
    )
    files.clear(
        fn=toggle_button,
        inputs=files,
        outputs=[btn]
    )

    btn.click(save_file, inputs=files, outputs=[output, files], show_progress="full")
    btnRemove.click(remove_file, inputs=files, outputs=files)

demo.launch(server_port=9191, server_name="0.0.0.0", root_path='/uploads')