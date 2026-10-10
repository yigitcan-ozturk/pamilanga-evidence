import json
from pathlib import Path

from demonstrator.generators.generate_f01_evidence_object import generate
from pamilanga_evidence.trace.canonical import canonical_bytes
from pamilanga_evidence.trace.integrity import sha256_hex


def test_f01_prove_end_to_end(tmp_path):
    obj = generate(tmp_path / "one")
    again = generate(tmp_path / "two")
    assert obj == again
    assert obj["evidence"]["event_count"] == 5
    assert obj["first_divergence"]["observed_event_id"] == "evt_000002"
    assert obj["evidence_sufficiency"]["status"] == "PARTIAL"
    assert obj["integrity"]["object_hash"].startswith("sha256:")
    unsigned = {k: v for k, v in obj.items() if k != "integrity"}
    assert obj["integrity"]["object_hash"] == sha256_hex(canonical_bytes(unsigned))
    assert json.loads((tmp_path / "one/evidence_object.json").read_text()) == obj
