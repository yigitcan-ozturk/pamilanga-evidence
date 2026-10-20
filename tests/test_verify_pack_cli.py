import json
import subprocess
import sys

from pamilanga_evidence.trace.integrity import event_hash
from pamilanga_evidence.trace.recorder import TraceRecorder


def test_independent_pack_verification(tmp_path):
    sealed = TraceRecorder(tmp_path / "evidence.jsonl").record([
        {"event_id": "one", "payload": {"data": 1}},
        {"event_id": "two", "payload": {"data": 2}},
    ])
    (tmp_path / "manifest.json").write_text(json.dumps({
        "stream": "evidence.jsonl", "event_count": 2,
        "root_hash": event_hash(sealed[-1]),
    }))
    cmd = [sys.executable, "-m", "pamilanga_evidence.verify_pack", str(tmp_path)]
    good = subprocess.run(cmd, capture_output=True, text=True)
    assert good.returncode == 0, good.stderr
    assert json.loads(good.stdout)["status"] == "PASS"

    (tmp_path / "evidence.jsonl").write_text(
        (tmp_path / "evidence.jsonl").read_text().splitlines()[0] + "\n"
    )
    bad = subprocess.run(cmd, capture_output=True, text=True)
    assert bad.returncode == 1
    assert json.loads(bad.stdout)["reason"] == "EVENT_COUNT_MISMATCH"
