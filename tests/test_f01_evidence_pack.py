import json
from pathlib import Path

from pamilanga_evidence.replay import first_divergence
from pamilanga_evidence.trace.integrity import event_hash
from pamilanga_evidence.trace.recorder import TraceRecorder
from pamilanga_evidence.trace.verifier import verify_stream

ROOT = Path(__file__).resolve().parents[1]


def view(e):
    return {"event_id": e["event_id"], "event_type": e["event_type"], "time": e["time"], "payload": {"data": {"freshness_ms": e["quality"]["freshness_ms"], "value": e["payload"]["data"]}}}


def test_f01_evidence_pack_is_reproducible(tmp_path):
    n01 = json.loads((ROOT / "demonstrator/scenarios/N01.json").read_text(encoding="utf-8"))["events"]
    f01 = json.loads((ROOT / "demonstrator/scenarios/F01.json").read_text(encoding="utf-8"))["events"]
    stream = tmp_path / "evidence.jsonl"
    sealed = TraceRecorder(stream).record(f01)
    verification = verify_stream(stream)
    divergence = first_divergence([view(e) for e in n01], [view(e) for e in f01])

    assert verification["status"] == "PASS"
    assert verification["root_hash"] == event_hash(sealed[-1])
    assert divergence["status"] == "FOUND"
    assert divergence["observed_event_id"] == "evt_000002"
    assert divergence["stage"] == "observation"
