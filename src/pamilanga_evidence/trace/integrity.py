import hashlib
from copy import deepcopy
from typing import Any

from .canonical import canonical_bytes

GENESIS = None


def sha256_hex(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def payload_hash(payload: Any) -> str:
    return sha256_hex(canonical_bytes(payload))


def event_hash(event: dict) -> str:
    """Hash the complete persisted event deterministically."""
    return sha256_hex(canonical_bytes(event))


def seal_event(event: dict, previous_event_hash: str | None) -> dict:
    sealed = deepcopy(event)
    sealed.setdefault("integrity", {})
    sealed["integrity"]["payload_hash"] = payload_hash(sealed["payload"])
    sealed["integrity"]["previous_event_hash"] = previous_event_hash
    return sealed
