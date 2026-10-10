"""End-to-end deterministic Evidence Object generation from the F01 scenario."""
import json
from pathlib import Path

from pamilanga_evidence.prove import build_evidence_object
from pamilanga_evidence.replay import first_divergence
from pamilanga_evidence.trace.recorder import TraceRecorder
from pamilanga_evidence.trace.verifier import verify_stream

ROOT = Path(__file__).resolve().parents[1]


def comparison_view(e: dict) -> dict:
    return {
        "event_id": e["event_id"],
        "event_type": e["event_type"],
        "time": e["time"],
        "payload": {"data": {"freshness_ms": e["quality"]["freshness_ms"], "value": e["payload"]["data"]}},
    }


def generate(output: Path) -> dict:
    n01 = json.loads((ROOT / "scenarios/N01.json").read_text(encoding="utf-8"))
    f01 = json.loads((ROOT / "scenarios/F01.json").read_text(encoding="utf-8"))
    output.mkdir(parents=True, exist_ok=True)
    stream = output / "evidence.jsonl"
    stream.unlink(missing_ok=True)
    sealed = TraceRecorder(stream).record(f01["events"])
    verification = verify_stream(stream)
    divergence = first_divergence(
        [comparison_view(e) for e in n01["events"]],
        [comparison_view(e) for e in f01["events"]],
    )
    obj = build_evidence_object(f01["run_id"], sealed, verification, divergence)
    (output / "evidence_object.json").write_text(
        json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    return obj


if __name__ == "__main__":
    generate(ROOT / "runs/RUN-F01")
