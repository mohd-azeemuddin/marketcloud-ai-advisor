import os
import sqlite3, json, time
from pathlib import Path

Path("data").mkdir(exist_ok=True)
_c = sqlite3.connect(os.getenv("CRM_DB", "data/demo_crm.db"), check_same_thread=False)
_c.executescript("""
CREATE TABLE IF NOT EXISTS leads(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, email TEXT, company TEXT, need TEXT, status TEXT, created REAL);
CREATE TABLE IF NOT EXISTS audit(id INTEGER PRIMARY KEY AUTOINCREMENT, ts REAL, action TEXT, verdict TEXT, reason TEXT, payload TEXT);
""")

def add_lead(l, status):
    cur = _c.execute("INSERT INTO leads(name,email,company,need,status,created) VALUES(?,?,?,?,?,?)",
                     (l["name"], l["email"], l.get("company") or "", l["need"], status, time.time()))
    _c.commit()
    return cur.lastrowid

def audit(action, verdict, reason, payload):
    _c.execute("INSERT INTO audit(ts,action,verdict,reason,payload) VALUES(?,?,?,?,?)",
               (time.time(), action, verdict, reason, json.dumps(payload)))
    _c.commit()

def all_leads():
    return _c.execute("SELECT id,name,email,company,need,status FROM leads ORDER BY id DESC").fetchall()

def recent_audit(n=20):
    return _c.execute("SELECT id,action,verdict,reason FROM audit ORDER BY id DESC LIMIT ?", (n,)).fetchall()