import json, uuid
from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from app.graph import run
from app.db import all_leads, recent_audit

app = FastAPI(title="MarketCloud AI Advisor")
SESSIONS = {}

class ChatIn(BaseModel):
    message: str = Field(min_length=1, max_length=1000)
    session_id: str | None = None

@app.post("/api/chat")
def chat(body: ChatIn):
    sid = body.session_id or uuid.uuid4().hex
    session = SESSIONS.setdefault(sid, {})
    out = run(body.message.strip(), session)
    return {"session_id": sid, "answer": out["answer"], "sources": out.get("sources", []), "trace": out["trace"]}

@app.get("/api/leads")
def leads():
    return [dict(zip(("id", "name", "email", "company", "need", "status"), r)) for r in all_leads()]

@app.get("/api/audit")
def audit_log():
    return [dict(zip(("id", "action", "verdict", "reason"), r)) for r in recent_audit()]

@app.get("/api/evals")
def evals():
    p = Path("evals/results.json")
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}

@app.get("/")
def index():
    return FileResponse("frontend/index.html")

@app.get("/ping")
def ping():
    return {"status": "ok"}