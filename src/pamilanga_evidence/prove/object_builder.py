"""Portable evidence summary; claims remain bounded by observed inputs."""
from pamilanga_evidence.trace.canonical import canonical_bytes
from pamilanga_evidence.trace.integrity import sha256_hex


def build_evidence_object(run_id: str, events: list[dict], verification: dict, divergence: dict) -> dict:
    if not events or verification.get("status") != "PASS":
        raise ValueError("Verified non-empty evidence stream required")
    if verification.get("events_verified") != len(events):
        raise ValueError("Event count mismatch")
    if divergence.get("status") not in ("FOUND", "NONE"):
        raise ValueError("Unsupported divergence status")
    body = {
        "schema_version": "0.1.0",
        "evidence_object_id": f"eo-{run_id}",
        "run": {"run_id": run_id, "started_at": events[0]["time"]["event_time_ns"], "ended_at": events[-1]["time"]["event_time_ns"], "system_id": "physical-ai-demo"},
        "evidence": {"event_count": len(events), "event_ids": [e["event_id"] for e in events], "root_hash": verification["root_hash"]},
        "temporal_integrity": {"status": "NOT_ASSESSED", "clock_domains": sorted({e["time"]["clock_domain"] for e in events}), "detected_anomalies": []},
        "reconstruction": {"status": "COMPARISON_ONLY", "deterministic": False},
        "first_divergence": divergence,
        "causal_hypotheses": [],
        "counterfactual_replays": [],
        "evidence_sufficiency": {"status": "PARTIAL", "missing_evidence": ["independent sensor validation", "causal validation"], "limitations": ["Synthetic scenario", "No root-cause determination", "No independent timestamp attestation"]},
    }
    body["integrity"] = {"generated_at": None, "generator_version": "0.1.0", "object_hash": sha256_hex(canonical_bytes(body))}
    return body
