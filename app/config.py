import os
from dotenv import load_dotenv
load_dotenv()
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
MIN_SCORE = float(os.getenv("MIN_SCORE", "0.40"))