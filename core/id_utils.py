import hashlib

def make_lead_id(email: str, phone: str, first: str, last: str) -> str:
    base = (email or "").strip().lower()
    if not base:
        base = (phone or "").strip().lower()
    if not base:
        base = f"{(first or '').strip().lower()}|{(last or '').strip().lower()}"
    return hashlib.sha256(base.encode("utf-8")).hexdigest()[:16]

