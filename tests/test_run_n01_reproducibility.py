import json
from pathlib import Path

from pamilanga_evidence.trace.integrity import event_hash
from pamilanga_evidence.trace.recorder import TraceRecorder
from pamilanga_evidence.trace.verifier import verify_stream

ROOT = Path(__file__).resolve().parents[1]
SCENARIO = ROOT / "demonstrator/scenarios/N01.json"
RUN_DIR = ROOT / "demonstrator/runs/RUN-N01"


def test_checked_in_run_n01_is_reproducible(tmp_path):
    spec = json.loads(SCENARIO.read_text(encoding="utf-8"))
    generated = tmp_path / "evidence.jsonl"
    sealed = TraceRecorder(generated).record(spec["events"])
    result = verify_stream(generated)

    manifest = json.loads((RUN_DIR / "manifest.json").read_text(encoding="utf-8"))
    verification = json.loads((RUN_DIR / "verification.json").read_text(encoding="utf-8"))

    root_hash = event_hash(sealed[-1])
    assert result["status"] == "PASS"
    assert len(sealed) == manifest["event_count"] == verification["events_verified"]
    assert root_hash == result["root_hash"]
    assert root_hash == manifest["root_hash"]
    assert root_hash == verification["root_hash"]
