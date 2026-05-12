import gradio as gr
import shutil
import os

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def save_file(files):
    if len(files) <= 0: 
        return
    saved = []

    for file in files:
        dst = os.path.join(
            UPLOAD_DIR,
            os.path.basename(file.name)
        )
        shutil.copy(file.name, dst)
        saved.append(dst)

    return "\n".join(saved), gr.File(value=None)

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

    btn = gr.Button(value="Upload",  interactive=False)
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

demo.launch()