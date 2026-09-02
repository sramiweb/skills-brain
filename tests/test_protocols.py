import json
from pathlib import Path

import jsonschema
import yaml

ROOT = Path(__file__).resolve().parents[1]


def test_canonical_debate_protocols_validate():
    schema = json.loads((ROOT / "schemas" / "protocol.schema.json").read_text(encoding="utf-8"))
    jsonschema.Draft202012Validator.check_schema(schema)
    protocol_paths = sorted((ROOT / "protocols" / "debate").glob("*/protocol.yaml"))
    assert protocol_paths, "Expected at least one canonical debate protocol"
    ids = set()
    for path in protocol_paths:
        payload = yaml.safe_load(path.read_text(encoding="utf-8"))
        jsonschema.validate(instance=payload, schema=schema)
        assert payload["id"] not in ids, f"Duplicate protocol id: {payload['id']}"
        ids.add(payload["id"])
        assert payload["rules"]["preserve_dissent"] is True
        assert payload["rules"]["majority_vote_allowed"] is False
        assert payload["rules"]["proposer_may_judge"] is False
        assert payload["rules"]["security_veto_overrides"] is True


def test_first_round_is_blind_for_all_canonical_debates():
    for path in sorted((ROOT / "protocols" / "debate").glob("*/protocol.yaml")):
        payload = yaml.safe_load(path.read_text(encoding="utf-8"))
        assert payload["rounds"][0]["id"] == "independent-analysis"
        assert payload["rounds"][0]["blind"] is True
