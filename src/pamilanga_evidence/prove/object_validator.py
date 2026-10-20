"""Validate Evidence Object v0.1 structural contract and content hash."""
from pathlib import Path
import json

from pamilanga_evidence.trace.canonical import canonical_bytes
from pamilanga_evidence.trace.integrity import sha256_hex

SCHEMA_PATH = Path(__file__).resolve().parents[3] / "schemas/evidence-object-v0.1.schema.json"


def validate_evidence_object(obj: dict) -> dict:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    if not isinstance(obj, dict):
        return {"status": "FAIL", "reason": "OBJECT_NOT_DICT"}
    for field in schema["required"]:
        if field not in obj:
            return {"status": "FAIL", "reason": "MISSING_FIELD", "field": field}
    if obj.get("schema_version") != "0.1.0":
        return {"status": "FAIL", "reason": "SCHEMA_VERSION_MISMATCH"}
    for field, definition in schema["properties"].items():
        if field not in obj:
            continue
        kind = definition.get("type")
        allowed = kind if isinstance(kind, list) else [kind]
        if kind is not None and not any(
            (t == "object" and isinstance(obj[field], dict))
            or (t == "array" and isinstance(obj[field], list))
            or (t == "string" and isinstance(obj[field], str))
            or (t == "null" and obj[field] is None)
            for t in allowed
        ):
            return {"status": "FAIL", "reason": "INVALID_FIELD_TYPE", "field": field}
    integrity = obj.get("integrity", {})
    if not isinstance(integrity, dict) or not isinstance(integrity.get("object_hash"), str):
        return {"status": "FAIL", "reason": "MISSING_OBJECT_HASH"}
    body = {key: value for key, value in obj.items() if key != "integrity"}
    if integrity["object_hash"] != sha256_hex(canonical_bytes(body)):
        return {"status": "FAIL", "reason": "OBJECT_HASH_MISMATCH"}
    return {"status": "PASS"}
