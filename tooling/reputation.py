#!/usr/bin/env python3
"""Aggregate verified runtime outcomes into scoped Skill reputation signals.

Reputation is advisory ranking evidence only. Global reports include only outcomes
without tenant_hash. Tenant-scoped reports include one explicit pseudonymous tenant
and are intended to remain runtime-local.
"""

from __future__ import annotations

import argparse
import json
import math
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parent.parent
OUTCOME_SCHEMA = ROOT / "schemas" / "outcome.schema.json"
REPORT_SCHEMA = ROOT / "schemas" / "reputation-report.schema.json"


def load_json(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return data


def parse_time(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def iso(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def wilson_lower_bound(successes: int, total: int, z: float = 1.96) -> float:
    if total <= 0:
        return 0.0
    p = successes / total
    denominator = 1 + (z * z / total)
    centre = p + (z * z / (2 * total))
    margin = z * math.sqrt((p * (1 - p) / total) + (z * z / (4 * total * total)))
    return max(0.0, (centre - margin) / denominator)


def freshness_factor(last_observed: datetime | None, as_of: datetime) -> float:
    if last_observed is None:
        return 0.75
    age_days = max(0, (as_of - last_observed).days)
    if age_days <= 90:
        return 1.0
    if age_days <= 180:
        return 0.90
    if age_days <= 365:
        return 0.75
    return 0.50


def iter_outcomes(path: Path):
    schema = load_json(OUTCOME_SCHEMA)
    paths = [path] if path.is_file() else sorted(path.rglob("*.json"))
    for item in paths:
        document = load_json(item)
        jsonschema.validate(document, schema)
        yield item, document


def scope_matches(outcome: dict, scope_type: str, tenant_hash: str | None) -> bool:
    scope = outcome.get("scope") or {}
    observed_tenant = scope.get("tenant_hash")
    if scope_type == "global":
        # Canonical/global reputation is deliberately generic-only.
        return not observed_tenant
    return bool(tenant_hash) and observed_tenant == tenant_hash


def aggregate(
    outcomes_path: Path,
    *,
    scope_type: str = "global",
    tenant_hash: str | None = None,
    minimum_samples: int = 5,
    minimum_verification_score: float = 0.70,
    as_of: datetime | None = None,
) -> dict:
    if scope_type not in {"global", "tenant"}:
        raise ValueError("scope_type must be global or tenant")
    if scope_type == "tenant" and not tenant_hash:
        raise ValueError("tenant scope requires tenant_hash")
    if minimum_samples < 1:
        raise ValueError("minimum_samples must be >= 1")
    if not 0 <= minimum_verification_score <= 1:
        raise ValueError("minimum_verification_score must be between 0 and 1")

    as_of = (as_of or datetime.now(timezone.utc)).astimezone(timezone.utc)
    grouped: dict[tuple[str, str], list[dict]] = defaultdict(list)

    for _, outcome in iter_outcomes(outcomes_path):
        subject = outcome["subject"]
        if subject["type"] != "skill":
            continue
        if not outcome.get("verified", False):
            continue
        verification_score = outcome.get("verification_score")
        if verification_score is None or float(verification_score) < minimum_verification_score:
            continue
        if not scope_matches(outcome, scope_type, tenant_hash):
            continue
        grouped[(str(subject["id"]), str(subject["version"]))].append(outcome)

    # A report must never collapse multiple versions into one reputation entry.
    by_id: dict[str, list[tuple[str, list[dict]]]] = defaultdict(list)
    for (skill_id, version), records in grouped.items():
        by_id[skill_id].append((version, records))

    subjects = {}
    for skill_id, versions in sorted(by_id.items()):
        # If multiple versions are present, choose the version with the most recent
        # timestamp, then sample count, then lexical version. Resolver still verifies
        # exact version equality before using the signal.
        def version_key(item):
            version, records = item
            times = [parse_time(record["occurred_at"]) for record in records if record.get("occurred_at")]
            latest = max(times) if times else datetime.min.replace(tzinfo=timezone.utc)
            return latest, len(records), version

        version, records = max(versions, key=version_key)
        total = len(records)
        successes = sum(1 for record in records if record.get("success") is True)
        success_rate = successes / total
        verification_avg = sum(float(record["verification_score"]) for record in records) / total
        override_rate = sum(1 for record in records if record.get("human_override") is True) / total
        failure_counts = [int(record.get("tool_failures", 0)) for record in records]
        tool_failure_rate = sum(1 for value in failure_counts if value > 0) / total
        average_tool_failures = sum(failure_counts) / total

        durations = [int(record["duration_ms"]) for record in records if "duration_ms" in record]
        costs = [float(record["cost"]) for record in records if "cost" in record]
        observed_times = [parse_time(record["occurred_at"]) for record in records if record.get("occurred_at")]
        last_observed = max(observed_times) if observed_times else None
        freshness = freshness_factor(last_observed, as_of)
        lower = wilson_lower_bound(successes, total)

        eligible = total >= minimum_samples
        base_score = (
            lower * 0.60
            + verification_avg * 0.20
            + (1.0 - override_rate) * 0.10
            + (1.0 - tool_failure_rate) * 0.10
        )
        reputation_score = round(max(0.0, min(1.0, base_score * freshness)), 4) if eligible else None

        subjects[skill_id] = {
            "version": version,
            "samples": total,
            "eligible_for_ranking": eligible,
            "verified_success_rate": round(success_rate, 4),
            "wilson_lower_bound": round(lower, 4),
            "average_verification_score": round(verification_avg, 4),
            "human_override_rate": round(override_rate, 4),
            "tool_failure_rate": round(tool_failure_rate, 4),
            "average_tool_failures": round(average_tool_failures, 4),
            "average_duration_ms": round(sum(durations) / len(durations), 2) if durations else None,
            "average_cost": round(sum(costs) / len(costs), 6) if costs else None,
            "last_observed_at": iso(last_observed) if last_observed else None,
            "freshness_factor": freshness,
            "reputation_score": reputation_score,
        }

    scope = {"type": scope_type}
    if scope_type == "tenant":
        scope["tenant_hash"] = tenant_hash

    report = {
        "schema_version": "1.0",
        "generated_at": iso(datetime.now(timezone.utc)),
        "as_of": iso(as_of),
        "scope": scope,
        "policy": {
            "minimum_samples": minimum_samples,
            "minimum_verification_score": minimum_verification_score,
        },
        "subjects": subjects,
    }
    jsonschema.validate(report, load_json(REPORT_SCHEMA))
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description="Aggregate verified Skill outcomes into reputation signals")
    parser.add_argument("outcomes", type=Path, help="Outcome JSON file or directory")
    parser.add_argument("--scope", choices=["global", "tenant"], default="global")
    parser.add_argument("--tenant-hash")
    parser.add_argument("--minimum-samples", type=int, default=5)
    parser.add_argument("--minimum-verification-score", type=float, default=0.70)
    parser.add_argument("--as-of", help="ISO-8601 timestamp for deterministic freshness calculation")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    as_of = parse_time(args.as_of) if args.as_of else None
    payload = aggregate(
        args.outcomes,
        scope_type=args.scope,
        tenant_hash=args.tenant_hash,
        minimum_samples=args.minimum_samples,
        minimum_verification_score=args.minimum_verification_score,
        as_of=as_of,
    )
    text = json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
