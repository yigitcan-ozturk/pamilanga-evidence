import json
from pathlib import Path

from pamilanga_evidence.trace.integrity import event_hash
from pamilanga_evidence.trace.recorder import TraceRecorder
from pamilanga_evidence.trace.verifier import verify_stream

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SCENARIO = ROOT / "scenarios" / "N01.json"
RUN_DIR = ROOT / "runs" / "RUN-N01"


def main() -> None:
    spec = json.loads(SCENARIO.read_text(encoding="utf-8"))
    RUN_DIR.mkdir(parents=True, exist_ok=True)
    stream = RUN_DIR / "evidence.jsonl"
    stream.unlink(missing_ok=True)

    sealed = TraceRecorder(stream).record(spec["events"])
    verification = verify_stream(stream)
    manifest = {
        "schema_version": "0.1.0",
        "run_id": spec["run_id"],
        "scenario_id": spec["scenario_id"],
        "event_count": len(sealed),
        "root_hash": event_hash(sealed[-1]) if sealed else None,
        "stream": "evidence.jsonl",
    }
    (RUN_DIR / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    (RUN_DIR / "verification.json").write_text(json.dumps(verification, indent=2) + "\n", encoding="utf-8")
    if verification["status"] != "PASS" or verification["root_hash"] != manifest["root_hash"]:
        raise SystemExit("RUN-N01 verification failed")


if __name__ == "__main__":
    main()
