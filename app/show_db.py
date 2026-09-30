from app.db import all_leads, recent_audit
print("LEADS"); [print(" ", r) for r in all_leads()]
print("AUDIT"); [print(" ", r) for r in recent_audit()]