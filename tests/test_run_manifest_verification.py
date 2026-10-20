import json

from pamilanga_evidence.trace.integrity import event_hash
from pamilanga_evidence.trace.recorder import TraceRecorder
from pamilanga_evidence.trace.run_verifier import verify_run


def event(i):
    return {
        "event_id": f"e{i}",
        "payload": {"format": "application/json", "data": {"value": i}},
    }


def test_manifest_verified_run_passes(tmp_path):
    stream = tmp_path / "events.jsonl"
    sealed = TraceRecorder(stream).record([event(1), event(2), event(3)])
    manifest = tmp_path / "manifest.json"
    manifest.write_text(json.dumps({"event_count": 3, "root_hash": event_hash(sealed[-1])}))
    assert verify_run(stream, manifest)["status"] == "PASS"


def test_last_event_truncation_detected(tmp_path):
    stream = tmp_path / "events.jsonl"
    sealed = TraceRecorder(stream).record([event(1), event(2), event(3)])
    manifest = tmp_path / "manifest.json"
    manifest.write_text(json.dumps({"event_count": 3, "root_hash": event_hash(sealed[-1])}))
    stream.write_text("\n".join(stream.read_text().splitlines()[:-1]) + "\n")
    result = verify_run(stream, manifest)
    assert result["status"] == "FAIL"
    assert result["reason"] == "EVENT_COUNT_MISMATCH"


def test_rewritten_chain_detected_by_root_hash(tmp_path):
    stream = tmp_path / "events.jsonl"
    sealed = TraceRecorder(stream).record([event(1), event(2)])
    manifest = tmp_path / "manifest.json"
    manifest.write_text(json.dumps({"event_count": 2, "root_hash": event_hash(sealed[-1])}))
    stream.unlink()
    TraceRecorder(stream).record([event(1), event(99)])
    result = verify_run(stream, manifest)
    assert result["status"] == "FAIL"
    assert result["reason"] == "ROOT_HASH_MISMATCH"
