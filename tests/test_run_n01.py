import json
from pathlib import Path

from pamilanga_evidence.trace.integrity import event_hash
from pamilanga_evidence.trace.recorder import TraceRecorder
from pamilanga_evidence.trace.verifier import verify_stream

ROOT = Path(__file__).resolve().parents[1]


def test_run_n01_nominal_artifact(tmp_path):
    spec = json.loads((ROOT / "demonstrator/scenarios/N01.json").read_text(encoding="utf-8"))
    stream = tmp_path / "evidence.jsonl"
    sealed = TraceRecorder(stream).record(spec["events"])
    result = verify_stream(stream)

    assert len(sealed) == 5
    assert result["status"] == "PASS"
    assert result["events_verified"] == 5
    assert result["root_hash"] == event_hash(sealed[-1])
    assert sealed[0]["time"]["event_time_ns"] != sealed[0]["time"]["capture_time_ns"]
