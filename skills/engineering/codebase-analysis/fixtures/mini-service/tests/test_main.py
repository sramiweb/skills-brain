from app.main import handle_request


def test_strict_validation_rejects_missing_amount():
    result = handle_request({"customer_id": "c-1"})
    assert result["accepted"] is False
    assert result["reason"] == "missing: amount"
    assert result["mode"] == "strict"
