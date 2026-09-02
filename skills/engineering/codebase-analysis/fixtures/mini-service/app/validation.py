REQUIRED_FIELDS = {"customer_id", "amount"}


def validate_request(payload: dict) -> tuple[bool, str]:
    missing = sorted(REQUIRED_FIELDS - set(payload))
    if missing:
        return False, f"missing: {','.join(missing)}"
    if payload["amount"] <= 0:
        return False, "amount_must_be_positive"
    return True, "ok"
