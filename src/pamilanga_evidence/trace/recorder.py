import json
from pathlib import Path
from typing import Iterable

from .integrity import event_hash, seal_event


class TraceRecorder:
    """Append-only TRACE recorder for Evidence Event streams."""

    def __init__(self, output: str | Path):
        self.output = Path(output)
        self.output.parent.mkdir(parents=True, exist_ok=True)
        self._previous_hash: str | None = None

    def append(self, event: dict) -> dict:
        sealed = seal_event(event, self._previous_hash)
        with self.output.open("a", encoding="utf-8", newline="\n") as handle:
            handle.write(json.dumps(sealed, sort_keys=True, separators=(",", ":"), ensure_ascii=False))
            handle.write("\n")
        self._previous_hash = event_hash(sealed)
        return sealed

    def record(self, events: Iterable[dict]) -> list[dict]:
        return [self.append(event) for event in events]
