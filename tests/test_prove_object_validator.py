from copy import deepcopy

from pamilanga_evidence.prove import build_evidence_object
from pamilanga_evidence.prove.object_validator import validate_evidence_object


def sample():
    return build_evidence_object(
        "RUN-F01",
        [{"event_id": "e1", "time": {"event_time_ns": 10, "clock_domain": "rig"}}],
        {"status": "PASS", "events_verified": 1, "root_hash": "sha256:example"},
        {"status": "FOUND", "observed_event_id": "e1"},
    )


def test_object_passes_contract_and_hash():
    assert validate_evidence_object(sample())["status"] == "PASS"


def test_tampered_object_rejected():
    obj = deepcopy(sample())
    obj["evidence"]["event_count"] = 99
    assert validate_evidence_object(obj)["reason"] == "OBJECT_HASH_MISMATCH"


def test_missing_field_rejected():
    obj = sample()
    del obj["evidence_sufficiency"]
    assert validate_evidence_object(obj)["reason"] == "MISSING_FIELD"
