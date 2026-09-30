import re

EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
DISPOSABLE = {"mailinator.com", "tempmail.com", "10minutemail.com", "guerrillamail.com", "yopmail.com"}
FAKE = re.compile(r"\b(test|fake|asdf|qwerty|dummy|xxx)\b", re.I)
INJ = re.compile(r"ignore (all )?(previous|prior)|system prompt|<script|drop table", re.I)
ALLOWED_ACTIONS = {"create_lead"}

def check(action, payload, session):
    """Every consequential action passes through here: returns (ALLOW | FLAG | DENY, reason)."""
    if action not in ALLOWED_ACTIONS:
        return "DENY", "Action not on the allow-list"
    missing = [f for f in ("name", "email", "need") if not payload.get(f)]
    if missing:
        return "DENY", f"Required information missing: {', '.join(missing)}"
    if not EMAIL.match(payload["email"]):
        return "DENY", "Invalid email format"
    if any(INJ.search(str(v)) for v in payload.values()):
        return "DENY", "Suspicious content in fields"
    if session.get("leads_created", 0) >= 3:
        return "DENY", "Rate limit: max 3 leads per session"
    local, domain = payload["email"].lower().split("@", 1)
    if domain in DISPOSABLE or FAKE.search(payload["name"]) or FAKE.search(local):
        return "FLAG", "Possible fake or disposable details, needs human approval"
    return "ALLOW", "All checks passed"