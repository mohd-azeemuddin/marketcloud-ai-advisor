import spaces  # must come before torch / sentence-transformers
import os
from pathlib import Path
import gradio as gr

@spaces.GPU
def _gpu_probe():
    return "ok"  # unused; satisfies ZeroGPU's startup check

if not Path("data/chroma/chroma.sqlite3").exists():
    from app import ingest
    ingest.main()

from app.server import app as advisor_app

with gr.Blocks(css="footer{display:none!important} .gradio-container{padding:0!important;max-width:100%!important}") as demo:
    gr.HTML('<iframe src="/advisor/" style="width:100%;height:96vh;border:0"></iframe>')
    btn = gr.Button("probe", visible=False)
    btn.click(_gpu_probe, None, gr.Textbox(visible=False), api_name="probe")

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=int(os.getenv("PORT", "7860")), prevent_thread_lock=True)
    demo.app.mount("/advisor", advisor_app)
    demo.block_thread()
