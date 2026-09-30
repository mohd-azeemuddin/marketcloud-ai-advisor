import json
from groq import Groq
from app.config import GROQ_MODEL

_client = Groq()

def chat(system, user, json_mode=False, temperature=0.2):
    kw = {"response_format": {"type": "json_object"}} if json_mode else {}
    r = _client.chat.completions.create(
        model=GROQ_MODEL, temperature=temperature,
        messages=[{"role": "system", "content": system}, {"role": "user", "content": user}], **kw)
    out = r.choices[0].message.content
    return json.loads(out) if json_mode else out