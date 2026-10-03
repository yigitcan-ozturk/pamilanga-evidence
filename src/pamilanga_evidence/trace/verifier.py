import json
from pathlib import Path

from .integrity import event_hash, payload_hash


def verify_stream(path: str | Path) -> dict:
    previous_hash = None
    count = 0

    with Path(path).open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            try:
                event = json.loads(line)
            except json.JSONDecodeError as exc:
                return {"status": "FAIL", "reason": "INVALID_JSON", "line": line_number, "detail": str(exc)}

            count += 1
            event_id = event.get("event_id")
            integrity = event.get("integrity", {})

            if integrity.get("payload_hash") != payload_hash(event.get("payload")):
                return {"status": "FAIL", "reason": "PAYLOAD_HASH_MISMATCH", "event_id": event_id, "line": line_number}

            if integrity.get("previous_event_hash") != previous_hash:
                return {"status": "FAIL", "reason": "CHAIN_MISMATCH", "event_id": event_id, "line": line_number}

            previous_hash = event_hash(event)

    return {"status": "PASS", "events_verified": count, "root_hash": previous_hash}
