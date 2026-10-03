import json

from pamilanga_evidence.trace.recorder import TraceRecorder
from pamilanga_evidence.trace.verifier import verify_stream


def event(i: int) -> dict:
    return {
        "schema_version": "0.1.0",
        "event_id": f"evt_{i:06d}",
        "run_id": "RUN-N01",
        "source": {"source_id": "rig", "source_type": "simulator", "producer": "physical-ai-demo"},
        "time": {"event_time_ns": i, "capture_time_ns": i + 1, "clock_domain": "demo", "sequence": i},
        "event_type": "observation" if i == 1 else "system",
        "payload": {"format": "application/json", "data": {"value": i}},
        "integrity": {"payload_hash": "", "previous_event_hash": None},
        "quality": {"confidence": 1.0, "freshness_ms": 1.0, "valid": True},
        "provenance": {"origin": "rig", "transform_chain": []},
        "relationships": {"parent_event_ids": []},
    }


def test_valid_chain_passes(tmp_path):
    path = tmp_path / "evidence.jsonl"
    TraceRecorder(path).record(event(i) for i in range(1, 6))
    result = verify_stream(path)
    assert result["status"] == "PASS"
    assert result["events_verified"] == 5


def test_payload_tamper_fails(tmp_path):
    path = tmp_path / "evidence.jsonl"
    TraceRecorder(path).record(event(i) for i in range(1, 6))
    lines = path.read_text(encoding="utf-8").splitlines()
    changed = json.loads(lines[2])
    changed["payload"]["data"]["value"] = 999
    lines[2] = json.dumps(changed, sort_keys=True, separators=(",", ":"))
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    result = verify_stream(path)
    assert result["status"] == "FAIL"
    assert result["reason"] == "PAYLOAD_HASH_MISMATCH"
    assert result["event_id"] == "evt_000003"


def test_deletion_breaks_chain(tmp_path):
    path = tmp_path / "evidence.jsonl"
    TraceRecorder(path).record(event(i) for i in range(1, 6))
    lines = path.read_text(encoding="utf-8").splitlines()
    del lines[2]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    result = verify_stream(path)
    assert result["status"] == "FAIL"
    assert result["reason"] == "CHAIN_MISMATCH"
