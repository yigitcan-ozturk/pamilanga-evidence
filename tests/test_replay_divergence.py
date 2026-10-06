from copy import deepcopy

from pamilanga_evidence.replay import first_divergence


def event(event_id, event_type, value, time_ns):
    return {"event_id": event_id, "event_type": event_type, "time": {"event_time_ns": time_ns}, "payload": {"format": "application/json", "data": {"value": value}}}


def test_identical_runs_have_no_divergence():
    baseline = [event("e1", "observation", 1, 10), event("e2", "fusion", 2, 20)]
    assert first_divergence(baseline, deepcopy(baseline)) == {"status": "NONE"}


def test_returns_earliest_payload_divergence():
    baseline = [event("e1", "observation", 1, 10), event("e2", "fusion", 2, 20), event("e3", "decision", 3, 30)]
    observed = deepcopy(baseline)
    observed[1]["payload"]["data"]["value"] = 99
    observed[2]["payload"]["data"]["value"] = 100
    result = first_divergence(baseline, observed)
    assert result["status"] == "FOUND"
    assert result["index"] == 1
    assert result["observed_event_id"] == "e2"
    assert result["stage"] == "fusion"
    assert result["time_ns"] == 20


def test_missing_event_is_visible():
    baseline = [event("e1", "observation", 1, 10), event("e2", "fusion", 2, 20)]
    result = first_divergence(baseline, baseline[:1])
    assert result["status"] == "FOUND"
    assert result["index"] == 1
    assert result["stage"] == "missing_event"
    assert result["observed"] is None
