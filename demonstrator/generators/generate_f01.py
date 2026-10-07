import json
from pathlib import Path

from pamilanga_evidence.replay import first_divergence
from pamilanga_evidence.trace.integrity import event_hash
from pamilanga_evidence.trace.recorder import TraceRecorder
from pamilanga_evidence.trace.verifier import verify_stream

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SCENARIOS = ROOT / "scenarios"
RUN_DIR = ROOT / "runs" / "RUN-F01"


def comparison_view(event: dict) -> dict:
    return {
        "event_id": event["event_id"],
        "event_type": event["event_type"],
        "time": event["time"],
        "payload": {
            "data": {
                "freshness_ms": event["quality"]["freshness_ms"],
                "value": event["payload"]["data"],
            }
        },
    }


def main() -> None:
    nominal = json.loads((SCENARIOS / "N01.json").read_text(encoding="utf-8"))
    faulted = json.loads((SCENARIOS / "F01.json").read_text(encoding="utf-8"))
    RUN_DIR.mkdir(parents=True, exist_ok=True)
    stream = RUN_DIR / "evidence.jsonl"
    stream.unlink(missing_ok=True)

    sealed = TraceRecorder(stream).record(faulted["events"])
    verification = verify_stream(stream)
    root_hash = event_hash(sealed[-1]) if sealed else None
    manifest = {
        "schema_version": "0.1.0",
        "run_id": faulted["run_id"],
        "scenario_id": faulted["scenario_id"],
        "event_count": len(sealed),
        "root_hash": root_hash,
        "stream": "evidence.jsonl",
    }
    divergence = first_divergence(
        [comparison_view(e) for e in nominal["events"]],
        [comparison_view(e) for e in faulted["events"]],
    )
    (RUN_DIR / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    (RUN_DIR / "verification.json").write_text(json.dumps(verification, indent=2) + "\n", encoding="utf-8")
    (RUN_DIR / "first_divergence.json").write_text(json.dumps(divergence, indent=2) + "\n", encoding="utf-8")

    if verification["status"] != "PASS" or verification["root_hash"] != root_hash:
        raise SystemExit("RUN-F01 integrity verification failed")
    if divergence.get("status") != "FOUND" or divergence.get("observed_event_id") != "evt_000002":
        raise SystemExit("RUN-F01 divergence verification failed")


if __name__ == "__main__":
    main()
