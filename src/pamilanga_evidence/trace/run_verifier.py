"""Verify a TRACE stream against an independently retained run manifest."""
import json
from pathlib import Path

from .verifier import verify_stream


def verify_run(stream_path: str | Path, manifest_path: str | Path) -> dict:
    manifest = json.loads(Path(manifest_path).read_text(encoding="utf-8"))
    result = verify_stream(stream_path)
    if result["status"] != "PASS":
        return result
    if result["events_verified"] != manifest.get("event_count"):
        return {
            "status": "FAIL",
            "reason": "EVENT_COUNT_MISMATCH",
            "expected": manifest.get("event_count"),
            "observed": result["events_verified"],
        }
    if result["root_hash"] != manifest.get("root_hash"):
        return {
            "status": "FAIL",
            "reason": "ROOT_HASH_MISMATCH",
            "expected": manifest.get("root_hash"),
            "observed": result["root_hash"],
        }
    return result
