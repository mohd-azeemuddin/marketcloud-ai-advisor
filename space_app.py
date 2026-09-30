import spaces  # must be imported before torch / sentence-transformers
import os
from pathlib import Path
import uvicorn

@spaces.GPU
def _gpu_probe():
    # Not used by the app. It only satisfies ZeroGPU's startup check.
    return 1

if not Path("data/chroma/chroma.sqlite3").exists():
    from app import ingest
    ingest.main()

from app.server import app

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", "7860")))
