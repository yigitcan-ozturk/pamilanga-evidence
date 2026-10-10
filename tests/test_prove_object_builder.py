import pytest
from pamilanga_evidence.prove import build_evidence_object


def test_evidence_object_deterministic_and_bounded():
    events = [{"event_id": "e1", "time": {"event_time_ns": 10, "clock_domain": "rig"}}]
    verification = {"status": "PASS", "events_verified": 1, "root_hash": "sha256:example"}
    divergence = {"status": "FOUND", "observed_event_id": "e1"}
    a = build_evidence_object("RUN-F01", events, verification, divergence)
    b = build_evidence_object("RUN-F01", events, verification, divergence)
    assert a == b
    assert a["evidence_sufficiency"]["status"] == "PARTIAL"
    assert a["reconstruction"]["deterministic"] is False
    assert a["integrity"]["object_hash"].startswith("sha256:")


def test_unverified_input_rejected():
    with pytest.raises(ValueError):
        build_evidence_object("RUN-F01", [], {"status": "FAIL"}, {"status": "NONE"})
