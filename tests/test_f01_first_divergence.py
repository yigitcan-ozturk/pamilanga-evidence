import json
from pathlib import Path

from pamilanga_evidence.replay import first_divergence

ROOT = Path(__file__).resolve().parents[1]


def test_f01_stale_lidar_first_divergence():
    nominal = json.loads((ROOT / "demonstrator/scenarios/N01.json").read_text(encoding="utf-8"))["events"]
    faulted = json.loads((ROOT / "demonstrator/scenarios/F01.json").read_text(encoding="utf-8"))["events"]

    # Compare evidence-bearing fields, not run identity/provenance labels.
    baseline = [{"event_id": e["event_id"], "event_type": e["event_type"], "time": e["time"], "payload": {"data": {"freshness_ms": e["quality"]["freshness_ms"], "value": e["payload"]["data"]}}} for e in nominal]
    observed = [{"event_id": e["event_id"], "event_type": e["event_type"], "time": e["time"], "payload": {"data": {"freshness_ms": e["quality"]["freshness_ms"], "value": e["payload"]["data"]}}} for e in faulted]

    result = first_divergence(baseline, observed)
    assert result["status"] == "FOUND"
    assert result["index"] == 1
    assert result["observed_event_id"] == "evt_000002"
    assert result["stage"] == "observation"
    assert result["time_ns"] == 1010000000
