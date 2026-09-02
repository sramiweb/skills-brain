from app.validation import validate_request
from app.flags import is_enabled


def handle_request(payload: dict) -> dict:
    if not is_enabled("strict-validation"):
        return {"accepted": True, "mode": "legacy"}
    valid, reason = validate_request(payload)
    return {"accepted": valid, "reason": reason, "mode": "strict"}
